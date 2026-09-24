extends SceneTree

const DB=preload("res://scripts/catalog.gd")
const RULES=preload("res://scripts/rules.gd")
const PROTOCOL="allstars-0.61.0-service-1"
var catalog=DB.new()
var game=RULES.new(catalog)
var listener=TCPServer.new()
var peers:Array=[]
var room:Dictionary={}
var directory=""
var secret=""
var deadline=0.0
var last_status=0.0
var last_roster=0.0
var used:Dictionary={}
var manager=0
var started=0.0
var sequences:Dictionary={}

func now():return Time.get_ticks_msec()/1000.0

func _initialize():
	var port=15001
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--room="):directory=arg.trim_prefix("--room=")
		if arg.begins_with("--port="):port=int(arg.trim_prefix("--port="))
	secret=OS.get_environment("TAVERN_TICKET_KEY")
	if directory.is_empty() or secret.is_empty():quit(2);return
	read_roster()
	if room.is_empty() or listener.listen(port,"127.0.0.1")!=OK:quit(3);return
	Engine.max_fps=20
	started=now()
	write_status()
	print("SERVICE READY ",port)

func read_roster():
	var parsed=JSON.parse_string(FileAccess.get_file_as_string(directory+"/room.json"))
	if not parsed is Dictionary:return
	room=parsed
	if manager==0:manager=int(room.owner) if room.mode=="friend" else -999
	if game.phase!="lobby":return
	var allowed=[]
	for person in room.members:allowed.append(int(person.id))
	for p in game.players.duplicate():
		if int(p.id)>0 and not int(p.id) in allowed:
			game.players.erase(p)
			for peer in peers:
				if int(peer.id)==int(p.id):peer.id=0;peer.ws.close()
	if room.mode=="friend" and not manager in allowed:manager=int(room.owner)
	if game.players.is_empty():game.ai_difficulty=3;game.trinkets_enabled=true;game.anomaly_mode="random"
	for person in room.members:
		var id=int(person.id)
		if game.player(id).is_empty():
			# Human reservations take precedence over bots added in the lobby.
			if game.players.size()>=8:
				for p in game.players:
					if int(p.id)<0:game.players.erase(p);break
			game.add_player(id,str(person.name),false)

func send(peer:Dictionary,value:Dictionary):
	if peer.ws.get_ready_state()==WebSocketPeer.STATE_OPEN:
		peer.ws.send_text(JSON.stringify(value))

func reject(peer:Dictionary,message:String):
	send(peer,{"type":"error","message":message})
	peer.ws.close(1008,"rejected")

func authenticate(peer:Dictionary,packet:Dictionary):
	var text=str(packet.get("ticket",""));var pieces=text.rsplit("|",true,1)
	if pieces.size()!=2:reject(peer,"入场票据无效");return
	var context=HMACContext.new();context.start(HashingContext.HASH_SHA256,secret.to_utf8_buffer());context.update(pieces[0].to_utf8_buffer())
	if context.finish().hex_encode()!=pieces[1]:reject(peer,"入场票据无效");return
	var claims=JSON.parse_string(pieces[0])
	if not claims is Dictionary:reject(peer,"入场票据无效");return
	if claims.get("room","")!=room.id or claims.get("protocol","")!=PROTOCOL or float(claims.get("exp",0))<Time.get_unix_time_from_system() or used.has(claims.get("nonce","")):reject(peer,"票据失效，请重连");return
	var id=int(claims.get("account",0));read_roster()
	if game.player(id).is_empty():reject(peer,"不属于该房间");return
	used[claims.nonce]=true
	for previous in peers:
		if int(previous.id)==id:previous.id=0;previous.ws.close(1000,"replaced")
	peer.id=id;peer.last=now()
	game.player(id).bot=false
	send(peer,{"type":"content","cards":catalog.cards,"heroes":catalog.heroes,"spells":catalog.spells,"trinkets":catalog.trinkets,"prizes":catalog.prizes,"wheel":catalog.wheel})
	broadcast()

func add_bot():
	var id=-1
	while not game.player(id).is_empty():id-=1
	game.add_player(id,"霸主AI %d"%-id,true)
	var p=game.player(id)
	if not p.is_empty():p.hero=p.hero_offers[game.rng.randi_range(0,p.hero_offers.size()-1)]

func begin():
	if game.phase!="lobby" or game.players.size()<2:return
	for p in game.players:
		if int(p.id)>0:p.bot=false
	game.start()
	for p in game.players:
		if int(p.id)>0 and not connected(int(p.id)):p.bot=true
	deadline=now()+game.round_duration();write_status();broadcast()

func connected(id:int)->bool:
	for p in peers:
		if int(p.id)==id and p.ws.get_ready_state()==WebSocketPeer.STATE_OPEN:return true
	return false

func action(peer:Dictionary,packet:Dictionary):
	var id=int(peer.id);var serial=int(packet.get("serial",0));var previous=int(peer.get("serial",0))
	if serial<=previous:return
	peer.serial=serial
	var act=str(packet.get("action",""));var index=int(packet.get("index",-1));var target=int(packet.get("target",-1))
	if act.begins_with("room_"):
		if room.mode!="friend" or id!=manager or game.phase!="lobby":return
		match act:
			"room_add":add_bot()
			"room_remove":
				var p=game.player(index)
				if index<0 and not p.is_empty():game.players.erase(p)
			"room_start":begin()
			"room_trinkets":game.trinkets_enabled=not game.trinkets_enabled
			"room_difficulty":game.ai_difficulty=1+game.ai_difficulty%3
			"room_anomaly":
				if index>=0 and index<RULES.ANOMALY.OPTIONS.size():game.anomaly_mode=RULES.ANOMALY.OPTIONS[index]
		broadcast();return
	var guard=packet.get("guard",{})
	if not guard is Dictionary:return
	for field in ["serial","index","aim"]:
		if guard.has(field):guard[field]=int(guard[field])
	var error=game.act_guarded(id,act,index,target,guard)
	if not error.is_empty():send(peer,{"type":"notice","message":error})
	else:broadcast()

func broadcast():
	for peer in peers:
		if int(peer.id)<=0 or game.player(int(peer.id)).is_empty():continue
		var v=game.view(int(peer.id))
		v["remaining"]=maxf(0,deadline-now()-(game.TOMORROW.penalty(game,game.player(int(peer.id))) if game.phase=="recruit" else 0))
		v["manager_id"]=manager
		send(peer,{"type":"state","state":v})

func write_status():
	var results=[]
	for p in game.players:results.append({"id":p.id,"rank":p.get("rank",0),"bot":p.bot})
	var f=FileAccess.open(directory+"/status.tmp",FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify({"phase":game.phase,"round":game.round_no,"players":results,"at":Time.get_unix_time_from_system()}));f.close()
		DirAccess.rename_absolute(directory+"/status.tmp",directory+"/status.json")

func _process(_delta):
	if room.is_empty():return false
	if listener.is_connection_available():
		var stream=listener.take_connection()
		if peers.size()<32:
			var ws=WebSocketPeer.new();ws.inbound_buffer_size=262144;ws.outbound_buffer_size=16777216;ws.max_queued_packets=64
			ws.accept_stream(stream);peers.append({"ws":ws,"id":0,"at":now(),"last":now(),"window":now(),"count":0,"serial":0})
	var dirty=false
	for peer in peers.duplicate():
		peer.ws.poll()
		if peer.ws.get_ready_state()==WebSocketPeer.STATE_CLOSED:
			var id=int(peer.id);peers.erase(peer)
			if id>0 and not connected(id):
				var p=game.player(id)
				if not p.is_empty():p.bot=true
				if manager==id:
					for other in peers:
						if int(other.id)>0:manager=int(other.id);break
				dirty=true
			continue
		if (int(peer.id)==0 and now()-peer.at>10) or now()-peer.last>40:peer.ws.close();continue
		while peer.ws.get_available_packet_count()>0:
			var data=peer.ws.get_packet()
			if data.size()>16384:peer.ws.close(1009);break
			if now()-peer.window>=1:peer.window=now();peer.count=0
			peer.count+=1
			if peer.count>30:peer.ws.close(1008);break
			var packet=JSON.parse_string(data.get_string_from_utf8())
			if not packet is Dictionary:continue
			peer.last=now()
			if int(peer.id)==0:authenticate(peer,packet)
			elif packet.get("type","")=="action":action(peer,packet)
	if now()-last_roster>1:
		last_roster=now();read_roster()
		if room.mode=="ranked" and game.phase=="lobby" and now()-started>=25:
			while game.players.size()<8:add_bot()
			begin()
	if game.phase=="recruit":
		var ready=true
		for p in game.players:
			if game.TOMORROW.expire(game,p,deadline-now()):dirty=true
			if p.hp>0 and not p.ready and not p.bot:ready=false
		if now()>=deadline or ready:
			for p in game.players:
				if p.hp<=0:continue
				game.TRINKETS.auto_choose(game,p);game.auto_discover(p)
				if p.bot:game.bot_turn(p)
			game.begin_settling();deadline=now()+game.settling_seconds;dirty=true
	elif game.phase=="settling" and now()>=deadline:
		game.battle();var longest=5.0
		for r in game.replays.values():
			var duration=2.0
			for event in r.events:
				if event.has("tomorrow"):duration+=2.6 if event.tomorrow.kind=="wheel" else 1.5
				elif event.get("effects",[]).any(func(e):return e.kind=="attack_prepare"):duration+=.24
				elif not event.get("attacker","").is_empty():duration+=.95
				elif event.get("effects",[]).any(func(e):return e.kind in ["macaw","on_attack"]):duration+=1.25
				else:duration+=.85
			longest=maxf(longest,duration)
		deadline=now()+longest;dirty=true
	elif game.phase=="combat" and now()>=deadline:
		game.finish_combat();deadline=now()+game.round_duration();dirty=true
	if dirty:broadcast()
	if now()-last_status>1:last_status=now();write_status()
	return false

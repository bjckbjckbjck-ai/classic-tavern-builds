extends SceneTree

const DB=preload("res://scripts/catalog.gd")
const RULES=preload("res://scripts/rules.gd")
const PROTOCOL="allstars-0.61.0-service-2"
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
var draft_active=false
var confirmed:Dictionary={}
var combat_views:Dictionary={}
var combat_until:Dictionary={}
var combat_round=0
var spectator_views:Dictionary={}
var spectator_until:Dictionary={}
var public_template:Dictionary={}
var roster_dirty=false
var pending_start=false

func now():return Time.get_ticks_msec()/1000.0

func _initialize():
	var port=15001
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--room="):directory=arg.trim_prefix("--room=")
		if arg.begins_with("--port="):port=int(arg.trim_prefix("--port="))
	secret=OS.get_environment("TAVERN_TICKET_KEY")
	if directory.is_empty() or secret.is_empty():quit(2);return
	read_roster()
	var template_game=RULES.new(catalog);template_game.add_player(-10000,"观战",false)
	public_template=template_game.players[0].duplicate(true);public_template.hero_offers=[]
	if room.is_empty() or listener.listen(port,"127.0.0.1")!=OK:quit(3);return
	Engine.max_fps=20
	started=now()
	write_status()
	print("SERVICE READY ",port)

func read_roster():
	if directory.is_empty():return
	var parsed=JSON.parse_string(FileAccess.get_file_as_string(directory+"/room.json"))
	if not parsed is Dictionary:return
	parsed["departed"]=parsed.get("departed",[]).map(func(id):return int(id))
	if parsed!=room:roster_dirty=true
	room=parsed
	var departed=room.get("departed",[])
	for peer in peers:
		if not peer.get("spectator",false) and int(peer.id) in departed:
			peer.id=0;peer.ws.close(1000,"departed")
	if manager==0:manager=int(room.owner) if room.mode=="friend" else -999
	if game.phase!="lobby" or draft_active:return
	var allowed=[]
	for person in room.members:
		if not int(person.id) in departed:allowed.append(int(person.id))
	for p in game.players.duplicate():
		if int(p.id)>0 and not int(p.id) in allowed:
			game.players.erase(p)
			for peer in peers:
				if int(peer.id)==int(p.id):peer.id=0;peer.ws.close()
	if room.mode=="friend" and not manager in allowed:manager=int(room.owner)
	if game.players.is_empty():game.ai_difficulty=3;game.trinkets_enabled=true;game.anomaly_mode="random"
	for person in room.members:
		var id=int(person.id)
		if not id in allowed:continue
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
	var watching=claims.get("role","")=="spectator"
	if watching:
		if peers.filter(func(p):return p.get("spectator",false) and int(p.id)>0).size()>=8:reject(peer,"观战席已满（8人）");return
	else:
		if game.player(id).is_empty() or id in room.get("departed",[]):reject(peer,"不属于该房间或已彻底退出");return
	used[claims.nonce]=true
	for previous in peers:
		if int(previous.id)==id:previous.id=0;previous.ws.close(1000,"replaced")
	peer.id=id;peer.last=now();peer["spectator"]=watching;peer["watch_id"]=0;peer["skip_round"]=-1
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
	game.start()
	deadline=now()+game.round_duration();write_status();broadcast()

func start_draft():
	if game.phase!="lobby" or draft_active or game.players.size()<2:return
	if not directory.is_empty():
		if DirAccess.make_dir_absolute(directory+"/admission.lock")!=OK:pending_start=true;return
		read_roster()
		if game.players.size()<2:
			DirAccess.remove_absolute(directory+"/admission.lock");pending_start=false;return
	pending_start=false
	draft_active=true;confirmed.clear();deadline=now()+30
	write_status()
	if not directory.is_empty():DirAccess.remove_absolute(directory+"/admission.lock")
	broadcast()

func complete_draft():
	draft_active=false
	begin()

func replay_seconds(replay:Dictionary)->float:
	var duration=2.0
	for event in replay.get("events",[]):
		if event.has("tomorrow"):duration+=2.6 if event.tomorrow.kind=="wheel" else 1.5
		elif event.get("effects",[]).any(func(e):return e.kind=="attack_prepare"):duration+=.24
		elif not event.get("attacker","").is_empty():duration+=.95
		elif event.get("effects",[]).any(func(e):return e.kind in ["macaw","on_attack"]):duration+=1.25
		else:duration+=.85
	return maxf(duration,5.0)

func prepare_combat():
	game.battle();combat_round=game.round_no
	combat_views.clear();combat_until.clear()
	spectator_views.clear();spectator_until.clear()
	var longest=0.0
	for p in game.players:
		var view=game.view(int(p.id))
		var duration=replay_seconds(view.get("replay",{}))
		spectator_views[int(p.id)]=public_view(view,int(p.id));spectator_until[int(p.id)]=now()+duration
		if int(p.id)>0:
			combat_views[int(p.id)]=view
			combat_until[int(p.id)]=now()+duration
		longest=maxf(longest,duration)
	# Resolve and initialize once. Each viewer retains its own private replay.
	game.finish_combat()
	deadline=now()+longest+game.round_duration()

func finish_replay(id:int,round_id:int):
	if round_id!=combat_round or not combat_views.has(id):return
	combat_views.erase(id);combat_until.erase(id)

func snapshot(id:int)->Dictionary:
	var v=combat_views[id].duplicate(true) if combat_views.has(id) else game.view(id)
	for player in v.players:player["bot"]=automated(game.player(int(player.id)))
	v["remaining"]=maxf(0,float(combat_until[id])-now()) if combat_views.has(id) else maxf(0,deadline-now()-(game.TOMORROW.penalty(game,game.player(id)) if game.phase=="recruit" else 0))
	v["manager_id"]=manager
	if draft_active:
		v["phase"]="hero_select"
		v["hero_confirmed"]=confirmed.has(id)
		v["confirmed_count"]=confirmed.size()
	return v

func automated(p:Dictionary)->bool:
	# Keep human identity intact: takeover must not grant boss-only economy perks.
	return p.bot or not connected(int(p.id))

func connected(id:int)->bool:
	for p in peers:
		if not p.get("spectator",false) and int(p.id)==id and p.ws.get_ready_state()==WebSocketPeer.STATE_OPEN:return true
	return false

func public_view(view:Dictionary,watch:int)->Dictionary:
	var v=view.duplicate(true);var safe=public_template.duplicate(true)
	for key in ["id","name","hero","hp","armor","tier","rank","last","ready","board","trinkets"]:
		if v.me.has(key):safe[key]=v.me[key]
	safe["power_cost"]=0;safe["hero_offers"]=[]
	v.me=safe;v["spectating"]=true;v["viewer_dead"]=true;v["viewer_id"]=0;v["watch_id"]=watch;v["manager_id"]=-999
	for player in v.players:player["bot"]=automated(game.player(int(player.id)))
	strip_private(v.get("replay",{}))
	return v

func strip_private(value):
	if value is Dictionary:
		for key in ["hand","hands","own_hand","hand_states","hand_state","shop","spell_shop","spell_extras","discover","discover_queue","trinket_offers","hero_offers","pending_hand","summoned_hand"]:value.erase(key)
		for child in value.values():strip_private(child)
	elif value is Array:
		for child in value:strip_private(child)

func spectator_snapshot(peer:Dictionary)->Dictionary:
	var watch=int(peer.get("watch_id",0))
	if game.player(watch).is_empty():
		if game.players.is_empty():return {}
		watch=int(game.players[0].id);peer.watch_id=watch
	var replay=spectator_views.has(watch) and now()<float(spectator_until.get(watch,0)) and int(peer.get("skip_round",-1))!=combat_round
	var v=spectator_views[watch].duplicate(true) if replay else public_view(game.view(watch),watch)
	v["remaining"]=maxf(0,float(spectator_until[watch])-now()) if replay else maxf(0,deadline-now())
	if draft_active:v.phase="hero_select"
	return v

func action(peer:Dictionary,packet:Dictionary):
	read_roster()
	if int(peer.id)<=0:return
	var id=int(peer.id);var serial=int(packet.get("serial",0));var previous=int(peer.get("serial",0))
	if serial<=previous:return
	peer.serial=serial
	var act=str(packet.get("action",""));var index=int(packet.get("index",-1));var target=int(packet.get("target",-1))
	if peer.get("spectator",false):
		if act=="spectate" and not game.player(index).is_empty():peer.watch_id=index;peer.skip_round=-1
		elif act=="replay_done" and index==combat_round:peer.skip_round=combat_round
		else:send(peer,{"type":"notice","message":"观战只能查看公开场面，不能操作对局"})
		send(peer,{"type":"state","state":spectator_snapshot(peer)});return
	if act.begins_with("room_"):
		if room.mode!="friend" or id!=manager or game.phase!="lobby" or draft_active:return
		match act:
			"room_add":add_bot()
			"room_remove":
				var p=game.player(index)
				if index<0 and not p.is_empty():game.players.erase(p)
			"room_start":start_draft()
			"room_trinkets":game.trinkets_enabled=not game.trinkets_enabled
			"room_difficulty":game.ai_difficulty=1+game.ai_difficulty%3
			"room_anomaly":
				if index>=0 and index<RULES.ANOMALY.OPTIONS.size():game.anomaly_mode=RULES.ANOMALY.OPTIONS[index]
		broadcast();return
	if act=="replay_done":
		finish_replay(id,index);broadcast();return
	if combat_views.has(id):return
	if game.phase=="lobby" and (not draft_active or act!="hero" or confirmed.has(id)):return
	var guard=packet.get("guard",{})
	if not guard is Dictionary:return
	for field in ["serial","index","aim"]:
		if guard.has(field):guard[field]=int(guard[field])
	var error=game.act_guarded(id,act,index,target,guard)
	if not error.is_empty():send(peer,{"type":"notice","message":error})
	else:
		if draft_active and act=="hero":confirmed[id]=true
		broadcast()

func broadcast():
	for peer in peers:
		if int(peer.id)>0 and peer.get("spectator",false):
			send(peer,{"type":"state","state":spectator_snapshot(peer)});continue
		if int(peer.id)<=0 or game.player(int(peer.id)).is_empty():continue
		send(peer,{"type":"state","state":snapshot(int(peer.id))})

func write_status():
	var results=[]
	for p in game.players:results.append({"id":p.id,"rank":p.get("rank",0),"bot":p.bot})
	var f=FileAccess.open(directory+"/status.tmp",FileAccess.WRITE)
	if f:
		var phase="hero_select" if draft_active else ("combat" if game.phase=="finished" and not combat_views.is_empty() else game.phase)
		f.store_string(JSON.stringify({"phase":phase,"round":game.round_no,"players":results,"at":Time.get_unix_time_from_system()}));f.close()
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
			if id>0 and not peer.get("spectator",false) and not connected(id):
				if manager==id:
					for other in peers:
						if int(other.id)>0 and not other.get("spectator",false):manager=int(other.id);break
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
		last_roster=now();var previous_room=room.duplicate(true);read_roster()
		if room!=previous_room:dirty=true
		for peer in peers:
			if peer.get("spectator",false) and int(peer.id)>0:send(peer,{"type":"state","state":spectator_snapshot(peer)})
		if room.mode=="ranked" and game.phase=="lobby" and not draft_active:
			while game.players.size()<8:add_bot()
			start_draft()
	if draft_active:
		var all_chosen=true
		for p in game.players:
			if not p.bot and not int(p.id) in room.get("departed",[]) and not confirmed.has(int(p.id)):all_chosen=false
		if all_chosen or now()>=deadline:complete_draft();dirty=true
	elif pending_start and game.phase=="lobby":start_draft()
	for id in combat_views.keys():
		if not connected(int(id)) or now()>=float(combat_until[id]):finish_replay(int(id),combat_round);dirty=true
	if game.phase=="recruit":
		var ready=true
		for p in game.players:
			if game.TOMORROW.expire(game,p,deadline-now()):dirty=true
			if connected(int(p.id)) and (combat_views.has(int(p.id)) or (p.hp>0 and not p.ready)):ready=false
		if now()>=deadline or ready:
			for p in game.players:
				if p.hp<=0:continue
				game.TRINKETS.auto_choose(game,p);game.auto_discover(p)
				if automated(p):game.bot_turn(p)
			game.begin_settling();deadline=now()+game.settling_seconds;dirty=true
	elif game.phase=="settling" and now()>=deadline:
		prepare_combat();dirty=true
	if roster_dirty:dirty=true;roster_dirty=false
	if dirty:broadcast()
	if now()-last_status>1:last_status=now();write_status()
	return false

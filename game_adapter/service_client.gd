extends Node
const PROTOCOL="allstars-0.61.0-service-2"
var app
var base="https://bjckwrn.xyz:21111"
var token=""
var account=""
var password=""
var room_code=""
var desired="friend"
var page=""
var message=""
var active=false
var ws:WebSocketPeer
var ticket=""
var authed=false
var serial=0
var last_ping=0.0
var next_retry=0.0
var last_poll=0.0
var busy=false
var model:Dictionary={}
var replay_exit_round=-1

func normalize(value):
	if value is float and value==floor(value):return int(value)
	if value is Array:
		for i in range(value.size()):value[i]=normalize(value[i])
	elif value is Dictionary:
		for key in value:value[key]=normalize(value[key])
	return value

func api(path:String,body:Dictionary={},method:int=HTTPClient.METHOD_POST)->Dictionary:
	var req=HTTPRequest.new();add_child(req);req.timeout=12
	var headers=PackedStringArray(["Content-Type: application/json"])
	if not token.is_empty():headers.append("Authorization: Bearer "+token)
	var err=req.request(base+path,headers,method,"" if method==HTTPClient.METHOD_GET else JSON.stringify(body))
	if err!=OK:req.queue_free();return {"error":"网络请求失败"}
	var result=await req.request_completed;req.queue_free()
	var data=JSON.parse_string(result[3].get_string_from_utf8())
	if not data is Dictionary:return {"error":"服务器暂不可用"}
	if result[1]>=400:return {"error":str(data.get("detail","请求失败"))}
	return data

func open(mode:String):
	desired=mode
	if token.is_empty():login_page()
	else:await refresh();home()

func frame(title:String):
	app.clear();app.panel(Rect2(225,125,990,660))
	app.label(title,Rect2(270,150,900,64),34,"ffe4a6",true)
	app.label(message,Rect2(275,645,890,84),18,"ffcf9f",true)
	app.button("返回主界面",Rect2(520,740,400,50),func():
		if page=="queue":await api("/api/queue",{"protocol":PROTOCOL,"cancel":true})
		if active:app.leave_room()
		else:page="";app.menu())

func login_page():
	page="login";frame("云端酒馆 · 登录 / 注册")
	app.label("账号（3—24位英文、数字、下划线）",Rect2(335,245,760,40),21)
	app.input_field(account,"账号",Rect2(335,290,760,55),func(v):account=v)
	app.label("密码（10—128位，仅当前会话保存）",Rect2(335,365,760,40),21)
	var edit=app.input_field(password,"密码",Rect2(335,410,760,55),func(v):password=v);edit.secret=true
	app.button("登录",Rect2(335,510,350,65),do_login,false,true)
	app.button("注册账号",Rect2(745,510,350,65),do_register)
	app.button("使用恢复码重置密码",Rect2(460,590,520,45),recover_page)

func do_login():
	if busy:return
	busy=true
	var data=await api("/api/login",{"name":account,"password":password});busy=false;password=""
	if data.has("error"):message=data.error;login_page();return
	token=data.token;account=data.name;message="";await refresh();home()

func do_register():
	if busy:return
	busy=true
	var data=await api("/api/register",{"name":account,"password":password});busy=false
	if data.has("error"):message=data.error;login_page();return
	page="recovery";frame("注册成功 · 保存恢复码")
	app.label("请保存以下恢复码，忘记密码时使用。",Rect2(295,265,850,60),24,"ffe4a6",true)
	var code=app.input_field(data.recovery_code,"恢复码",Rect2(295,355,850,70),func(_v):pass);code.editable=false
	app.button("复制恢复码",Rect2(465,465,510,60),func():DisplayServer.clipboard_set(data.recovery_code))
	app.button("已保存，前往登录",Rect2(465,550,510,60),func():message="";login_page())

func recover_page():
	page="recover";frame("通过恢复码重置密码")
	app.label("账号 / 恢复码 / 新密码",Rect2(335,245,760,45),22)
	var recovery={"value":""}
	app.input_field(account,"账号",Rect2(335,310,760,55),func(v):account=v)
	app.input_field("","",Rect2(335,385,760,55),func(v):recovery.value=v)
	var edit=app.input_field("","",Rect2(335,460,760,55),func(v):password=v);edit.secret=true
	app.button("重置并获取新恢复码",Rect2(395,555,650,65),func():
		var data=await api("/api/recover",{"name":account,"password":password,"recovery_code":recovery.value})
		password=""
		if data.has("error"):message=data.error;recover_page();return
		DisplayServer.clipboard_set(data.recovery_code);message="重置成功，新恢复码已复制，请妥善保存。";login_page())

func refresh():
	var data=await api("/api/me",{},HTTPClient.METHOD_GET)
	if data.has("error"):message=data.error;return
	model=data

func home():
	page="home";frame("好友房间" if desired=="friend" else "在线积分匹配")
	app.label("%s  ·  积分 %d"%[account,int(model.get("rating",1000))],Rect2(295,225,850,48),25,"ffe4a6",true)
	if model.get("room")!=null:
		app.label("已有房间："+str(model.room.code),Rect2(320,320,800,60),27,"ffe4a6",true)
		app.button("进入 / 断线重连",Rect2(465,425,510,75),connect_room,false,true)
		app.button("离开尚未开局的房间",Rect2(465,535,510,50),func():
			var data=await api("/api/leave")
			message=data.get("error","");await refresh();home())
	elif model.get("queue")!=null:queue_page()
	elif desired=="friend":
		app.button("创建好友房间",Rect2(465,310,510,70),func():await friend_room(""),false,true)
		app.input_field(room_code,"房间码",Rect2(365,435,710,60),func(v):room_code=v)
		app.button("填写房间码后加入",Rect2(465,535,510,70),func():await friend_room(room_code))
	else:
		app.label("按名次计分 · 等待60秒后可选择最高难度AI",Rect2(270,310,900,55),22,"ffe4a6",true)
		app.label("真人局全积分；多人AI混合局半积分；单人AI局不计分",Rect2(250,380,940,65),20,"d5c29b",true)
		app.button("开始匹配",Rect2(465,495,510,80),func():
			var data=await api("/api/queue",{"protocol":PROTOCOL})
			message=data.get("error","");await refresh();queue_page(),false,true)
	app.button("退出账号",Rect2(965,160,190,45),func():await api("/api/logout");token="";model={};login_page())

func friend_room(code:String):
	if busy:return
	busy=true
	var data=await api("/api/friends",{"code":code});busy=false
	if data.has("error"):message=data.error;home();return
	await connect_room()

func queue_page():
	if model.get("room")!=null:await connect_room();return
	if model.get("queue")==null:home();return
	page="queue";frame("正在匹配 · %d秒"%int(model.queue.seconds))
	app.label("正在寻找匹配：%d 人 · 已同意AI：%d 人"%[int(model.queue.get("players",1)),int(model.queue.get("consenting",0))],Rect2(270,245,900,60),23,"ffe4a6",true)
	if int(model.queue.seconds)>=60:
		app.label("所有排队玩家同意后，一起加入最高难度AI",Rect2(270,335,900,60),24,"ffe4a6",true)
		app.button("接受AI" if not model.queue.ai_consent else "已同意，等待其他玩家/桌位",Rect2(315,425,380,65),func():await api("/api/queue",{"protocol":PROTOCOL,"consent":true});await refresh();queue_page())
		app.button("继续等真人",Rect2(745,425,380,65),func():await api("/api/queue",{"protocol":PROTOCOL,"consent":false});await refresh();queue_page())
	app.button("取消匹配",Rect2(465,545,510,65),func():await api("/api/queue",{"protocol":PROTOCOL,"cancel":true});await refresh();home())

func connect_room():
	if busy:return
	busy=true
	var data=await api("/api/ticket",{"protocol":PROTOCOL});busy=false
	if data.has("error"):message=data.error;active=false;await refresh();home();return
	if ws:ws.close()
	ws=WebSocketPeer.new();ws.inbound_buffer_size=16777216;ws.outbound_buffer_size=262144
	ticket=data.ticket;room_code=data.code;authed=false;serial=0;active=true;page="play"
	app.multiplayer.multiplayer_peer=OfflineMultiplayerPeer.new()
	app.online=true;app.state={};app.replay_round=-1
	replay_exit_round=-1
	ws.connect_to_url(base.replace("https://","wss://").replace("http://","ws://")+"/play/"+str(int(data.slot)))
	message="正在连接，断线期间由AI托管";frame("房间 "+room_code)
	next_retry=Time.get_ticks_msec()/1000.0+8

func stop():
	active=false;page="";ticket=""
	if ws:ws.close();ws=null

func intent(action:String,index:int,target:int,guard:Dictionary):
	if not ws or ws.get_ready_state()!=WebSocketPeer.STATE_OPEN:return
	serial+=1
	ws.send_text(JSON.stringify({"type":"action","serial":serial,"action":action,"index":index,"target":target,"guard":guard}))

func finish_replay():
	if app.state.get("phase","")!="combat" or replay_exit_round==int(app.state.round):return
	if not ws or ws.get_ready_state()!=WebSocketPeer.STATE_OPEN:return
	replay_exit_round=int(app.state.round)
	intent("replay_done",replay_exit_round,-1,{})

func hero_draft():
	app.draft_offers=app.state.me.hero_offers.duplicate()
	if not app.selected_hero in app.draft_offers:app.selected_hero=int(app.state.me.hero)
	preload("res://scripts/hero_draft_ui.gd").show_draft(app)

func confirm_hero():
	if app.state.get("phase","")=="hero_select" and not app.state.get("hero_confirmed",false):app.request("hero",app.selected_hero)

func _process(_delta):
	var now=Time.get_ticks_msec()/1000.0
	if page=="queue" and not busy and now-last_poll>2:
		last_poll=now;busy=true;await refresh();busy=false
		if page=="queue":queue_page()
	if not active or not ws:return
	ws.poll()
	if ws.get_ready_state()==WebSocketPeer.STATE_OPEN:
		if not authed:ws.send_text(JSON.stringify({"ticket":ticket}));ticket="";authed=true
		if now-last_ping>10:ws.send_text('{"type":"ping"}');last_ping=now
		while ws.get_available_packet_count()>0:
			var packet=normalize(JSON.parse_string(ws.get_packet().get_string_from_utf8()))
			if not packet is Dictionary:continue
			match packet.get("type",""):
				"content":app.content(packet.cards,packet.heroes,packet.spells,packet.trinkets,packet.prizes,packet.wheel)
				"state":
					var before={}
					for key in packet.state.get("combat_before",{}):before[int(key)]=packet.state.combat_before[key]
					packet.state.combat_before=before
					app.receive_state(packet.state)
				"notice":app.notify(packet.message)
				"error":message=packet.message
	elif ws.get_ready_state()==WebSocketPeer.STATE_CLOSED and now>=next_retry and not busy:
		if ws.get_close_reason()=="replaced":
			stop();message="账号已由另一个连接接管";token="";app.online=false;login_page();return
		if app.state.get("phase","")=="finished":stop();return
		next_retry=now+5;message="连接中断，正在恢复原席位（AI托管中）";await connect_room()

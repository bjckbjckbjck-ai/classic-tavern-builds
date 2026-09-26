extends "res://scripts/service_server.gd"
var sent=[]
func write_status():pass
func broadcast():pass
func send(_peer:Dictionary,value:Dictionary):sent.append(value)
func _process(_delta):return false
class Socket extends RefCounted:
	var closed=false
	func get_ready_state():return WebSocketPeer.STATE_CLOSED if closed else WebSocketPeer.STATE_OPEN
	func close(_code=1000,_reason=""):closed=true
func _initialize():
	room={"mode":"friend","owner":11,"members":[],"departed":[]};manager=11
	game.add_player(11,"one",false);game.add_player(22,"two",false)
	public_template=game.player(11).duplicate(true);public_template.hero_offers=[]
	begin()
	var human=game.player(11)
	game.act_guarded(11,"buy",0,-1,game.action_guard(human,"buy",0,-1))
	assert(not human.hand.is_empty())
	var observer={"id":99,"serial":0,"spectator":true,"watch_id":11,"skip_round":-1,"ws":Socket.new()}
	peers.append(observer)
	var s=spectator_snapshot(observer)
	var recruitment=s.duplicate(true)
	assert(s.spectating and s.viewer_dead and s.me.hand.is_empty() and s.me.shop.is_empty())
	assert(s.me.hero_offers.is_empty() and s.me.trinket_offers.is_empty())
	assert(s.me.coins==0 and s.me.id==11 and s.manager_id==-999)
	game.act_guarded(11,"play",0,-1,game.action_guard(human,"play",0,-1))
	recruitment=spectator_snapshot(observer)
	assert(not recruitment.me.board.is_empty())
	var before=human.duplicate(true)
	action(observer,{"serial":1,"action":"ready"})
	assert(human==before and sent[0].type=="notice")
	action(observer,{"serial":2,"action":"spectate","index":22})
	assert(observer.watch_id==22)
	observer.id=11;assert(not connected(11));observer.id=99
	game.begin_settling();prepare_combat()
	s=spectator_snapshot(observer)
	var file=FileAccess.open("res://.runtime/spectator-fixtures.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"recruit":recruitment,"combat":s}));file.close()
	assert(s.phase=="combat" and not s.replay.has("hand_states"))
	for event in s.replay.get("events",[]):assert(not event.has("own_hand") and not event.has("hands") and not event.has("hand_state"))
	action(observer,{"serial":3,"action":"replay_done","index":combat_round})
	assert(spectator_snapshot(observer).phase=="recruit" and combat_views.has(22))
	print("PASS spectator read-only, private zones redacted, no player connection/seat, independent replay")
	quit()

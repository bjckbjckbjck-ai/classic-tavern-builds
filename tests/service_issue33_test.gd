extends "res://scripts/service_server.gd"
func write_status():pass
func broadcast():pass
func send(_peer:Dictionary,_value:Dictionary):pass
func connected(_id:int)->bool:return true
func _process(_delta):return false
func _initialize():
	room={"mode":"friend"};manager=11
	game.add_player(11,"one",false);game.add_player(22,"two",false)
	var peer={"id":11,"serial":0}
	var p=game.player(11);var chosen=int(p.hero_offers[1])
	action(peer,{"serial":1,"action":"hero","index":chosen,"guard":game.action_guard(p,"hero",chosen,-1)})
	assert(p.hero!=chosen)
	action(peer,{"serial":2,"action":"room_start"})
	assert(draft_active and snapshot(11).phase=="hero_select" and game.round_no==0)
	action(peer,{"serial":3,"action":"hero","index":chosen,"guard":game.action_guard(p,"hero",chosen,-1)})
	assert(p.hero==chosen and confirmed.has(11) and game.round_no==0)
	complete_draft()
	assert(game.round_no==1 and game.phase=="recruit")
	game.begin_settling();prepare_combat()
	assert(game.phase=="recruit" and game.round_no==2)
	assert(snapshot(11).phase=="combat" and snapshot(22).phase=="combat")
	var coins=p.coins;var serial=p.action_serial
	action(peer,{"serial":4,"action":"buy","index":0,"guard":game.action_guard(p,"buy",0,-1)})
	assert(p.coins==coins and p.action_serial==serial)
	finish_replay(11,combat_round-1)
	assert(snapshot(11).phase=="combat")
	action(peer,{"serial":5,"action":"replay_done","index":combat_round})
	assert(snapshot(11).phase=="recruit" and snapshot(22).phase=="combat")
	var other=snapshot(22)
	action(peer,{"serial":6,"action":"buy","index":0,"guard":game.action_guard(p,"buy",0,-1)})
	assert(p.coins<coins and not p.hand.is_empty())
	var after=snapshot(22);after.erase("remaining");other.erase("remaining")
	assert(after==other)
	coins=p.coins
	finish_replay(11,combat_round);finish_replay(22,combat_round)
	assert(p.coins==coins and game.round_no==2 and snapshot(22).phase=="recruit")
	game.player(22).hp=0
	game.begin_settling();prepare_combat()
	assert(game.phase=="finished" and snapshot(11).phase=="combat")
	finish_replay(11,combat_round)
	assert(snapshot(11).phase=="finished" and p.rank==1)
	print("PASS issue33 draft gate, per-seat recruit/actions, immutable replay, duplicate/stale completion, final standings")
	quit()

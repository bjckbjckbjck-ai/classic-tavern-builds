extends SceneTree
var app
func _initialize():call_deferred("run")
func wait_phase(phase:String,round_id:int=0):
	var until=Time.get_ticks_msec()+60000
	while Time.get_ticks_msec()<until:
		if app.state.get("phase","")==phase and int(app.state.get("round",0))>=round_id:return true
		await create_timer(.05).timeout
	printerr("FAIL waiting ",phase," ",app.state.get("phase",""));quit(1);return false
func run():
	app=load("res://scenes/main.tscn").instantiate();root.add_child(app);await process_frame
	app.feedback.muted=true
	var cloud=app.cloud;cloud.base=OS.get_environment("TAVERN_TEST_BASE")
	var credentials={"name":"qa_%08x"%randi(),"password":"ui-test-only-%d-%d"%[randi(),randi()]}
	var result=await cloud.api("/api/register",credentials)
	assert(not result.has("error"))
	result=await cloud.api("/api/login",credentials);cloud.token=result.token;cloud.account=result.name
	result=await cloud.api("/api/friends",{})
	assert(not result.has("error"))
	await cloud.connect_room()
	# Local API has no reverse proxy; use its matching Godot slot directly.
	cloud.ws.close();cloud.ws=WebSocketPeer.new();cloud.ws.inbound_buffer_size=16777216
	cloud.ws.connect_to_url("ws://127.0.0.1:%d"%(15000+int(result.slot)))
	if not await wait_phase("lobby"):return
	for child in app.ui.get_children():assert(not child.has_meta("lobby_hero"))
	app.room_command("add");await create_timer(.4).timeout
	app.room_command("start")
	if not await wait_phase("hero_select"):return
	var draft=app.ui.get_node("HeroDraft");assert(draft.cards.size()==4)
	await process_frame
	root.get_texture().get_image().save_png("res://build/issue33-hero-draft.png")
	draft.confirm_button.pressed.emit()
	if not await wait_phase("recruit",1):return
	app.request("ready")
	if not await wait_phase("combat",1):return
	app.skip_battle()
	if not await wait_phase("recruit",2):return
	app.request("buy",0);await create_timer(.5).timeout
	assert(not app.state.me.hand.is_empty())
	root.get_texture().get_image().save_png("res://build/issue33-after-skip.png")
	app.request("ready")
	if not await wait_phase("combat",2):return
	# Let the actual rendering/settlement callback send replay_done this time.
	if not await wait_phase("recruit",3):return
	assert(cloud.replay_exit_round==2)
	print("PASS native UI: hidden pre-start draft, four hero cards, confirm, skip and buy, automatic replay completion")
	cloud.stop();app.queue_free();await process_frame;quit()

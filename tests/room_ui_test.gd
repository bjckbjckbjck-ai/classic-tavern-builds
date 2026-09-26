extends "res://tests/ui_test.gd"
func shot(name:String):
	await create_timer(.2).timeout
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://.runtime/"+name+".png")
func run_test():
	app=load("res://scenes/main.tscn").instantiate();root.add_child(app);current_scene=app
	await process_frame
	app.cloud.room_list=[]
	for i in range(4):
		app.cloud.room_list.append({"id":str(i),"slot":i+1,"code":"ABCD1234","mode_label":"好友房" if i%2==0 else "积分赛","human_count":i+2,"phase":"lobby" if i==0 else "recruit","mine":false,"joinable":i==0,"spectatable":true})
	app.cloud.page="rooms";app.cloud.last_poll=Time.get_ticks_msec()/1000.0
	app.cloud.draw_rooms();await shot("server-room-list")
	check(app.ui.get_children().filter(func(n):return n is Button and n.text=="观战").size()==4,"four rooms have spectator buttons")
	check(app.ui.get_children().filter(func(n):return n is Button and n.text=="加入" and not n.disabled).size()==1,"only waiting friend room joinable")
	app.cloud.draw_leave({"id":"test","mode":"ranked","code":"ABCD1234"});await shot("permanent-leave-confirm")
	check(app.menu_page=="cloud_leave","leave dialog guards render")
	var fixtures=JSON.parse_string(FileAccess.get_file_as_string("res://.runtime/spectator-fixtures.json"))
	app.menu_page="";app.cloud.active=true;app.cloud.spectator=true;app.cloud.page="play";app.online=true
	for phase in ["recruit","combat"]:
		var value=app.cloud.normalize(fixtures[phase]);var before={}
		for key in value.combat_before:before[int(key)]=value.combat_before[key]
		value.combat_before=before;app.receive_state(value);await shot("public-spectator-"+phase)
		check(app.state.spectating and app.state.me.hand.is_empty() and app.state.me.shop.is_empty(),"public "+phase+" renders without private zones")
	print("ROOM_UI failures=",failures);quit(1 if failures else 0)

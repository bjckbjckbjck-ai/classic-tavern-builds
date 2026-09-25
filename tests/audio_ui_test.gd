extends "res://tests/ui_test.gd"
func run_test():
	var capture=AudioEffectCapture.new();capture.buffer_length=2;AudioServer.add_bus_effect(0,capture)
	app=load("res://scenes/main.tscn").instantiate();root.add_child(app);current_scene=app
	await create_timer(1).timeout
	check(app.ui.has_node("ClientUpdateButton"),"update entry exists")
	var frames=capture.get_buffer(capture.get_frames_available());var energy=0.0
	for frame in frames:energy+=frame.length_squared()
	check(energy>0.01,"recruit music emits real PCM")
	app.music.set_combat(true);capture.clear_buffer();await create_timer(1).timeout
	frames=capture.get_buffer(capture.get_frames_available());energy=0
	for frame in frames:energy+=frame.length_squared()
	check(energy>0.01,"combat music emits real PCM")
	app.LIBRARY.updates(app);await create_timer(.2).timeout
	check(app.menu_page=="updates","update page opens")
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://.runtime/audio-updates-ui.png")
	app.SETTINGS.audio_sources(app);await create_timer(.2).timeout
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://.runtime/audio-sources-ui.png")
	check(app.ui.get_children().any(func(n):return n is RichTextLabel and "原创" in n.text),"original sound attribution visible")
	AudioServer.remove_bus_effect(0,0)
	print("AUDIO_UI failures=",failures);quit(1 if failures else 0)

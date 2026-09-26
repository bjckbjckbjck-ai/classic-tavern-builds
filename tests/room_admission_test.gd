extends "res://scripts/service_server.gd"
func broadcast():pass
func _process(_delta):return false
func _initialize():
	directory=ProjectSettings.globalize_path("res://.runtime/admission-"+str(Time.get_ticks_usec()))
	DirAccess.make_dir_recursive_absolute(directory)
	room={"id":"admission-test","mode":"friend","owner":11,"members":[{"id":11,"name":"one"},{"id":22,"name":"two"},{"id":33,"name":"joining"}],"departed":[]}
	var file=FileAccess.open(directory+"/room.json",FileAccess.WRITE);file.store_string(JSON.stringify(room));file.close()
	game.add_player(11,"one",false);game.add_player(22,"two",false)
	DirAccess.make_dir_absolute(directory+"/admission.lock")
	start_draft();assert(not draft_active and pending_start)
	DirAccess.remove_absolute(directory+"/admission.lock")
	start_draft();assert(draft_active and not game.player(33).is_empty())
	assert(JSON.parse_string(FileAccess.get_file_as_string(directory+"/status.json")).phase=="hero_select")
	assert(not DirAccess.dir_exists_absolute(directory+"/admission.lock"))
	print("PASS joining roster admitted before host draft; shared boundary lock released")
	quit()

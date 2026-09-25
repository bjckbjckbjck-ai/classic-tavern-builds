extends SceneTree
var failures=0
func check(ok:bool,label:String):
	if not ok:failures+=1;push_error(label)
class Recorder extends "res://scripts/feedback.gd":
	var calls=[]
	func cue(kind:String):calls.append(kind)
func _initialize():call_deferred("run")
func run():
	var music=load("res://scripts/music.gd").new();root.add_child(music)
	for group in music.TRACKS:
		for name in group:
			var stream=load("res://assets/audio/music/"+name+".mp3")
			check(stream is AudioStreamMP3 and stream.get_length()>40,"decode "+name)
	await create_timer(.8).timeout
	check(music.players[0].playing and music.gains[0]==1,"recruit playback")
	var track=music.last_track[0];music.set_combat(false)
	check(track==music.last_track[0],"snapshot does not restart track")
	music.set_combat(true);await create_timer(.8).timeout
	check(music.players[0].stream_paused and music.players[1].playing and music.gains[1]==1,"combat crossfade")
	music.set_combat(false);await create_timer(.8).timeout
	check(music.last_track[0]==track and not music.players[0].stream_paused,"recruit resumes")
	for i in range(12):
		var old=music.last_track[0];music.next_track(0);check(old!=music.last_track[0],"no consecutive repeat")
	var fx=Recorder.new();root.add_child(fx)
	for seconds in [21,20,20,19,19,5,5,4,0]:fx.update_timer("recruit",1,seconds,true)
	check(fx.calls==["countdown_start","countdown_tick","countdown_urgent","countdown_urgent"],"timer dedupe and urgency")
	fx.update_timer("recruit",1,3,false);check(fx.calls.size()==4,"ready seat silent")
	fx.update_timer("combat",1,2,true);check(fx.calls.size()==4,"combat silent")
	for name in fx.KINDS:check(fx.streams[name] is AudioStreamWAV,"SFX imported "+name)
	var u=load("res://scripts/service_updater.gd").new()
	var manifest={"channel":"service","build":u.BUILD+1,"version":"test5","platforms":{"windows":{"file":"ClassicTavern-Service-5.exe","bytes":2000000,"sha256":"a".repeat(64)}}}
	check(u.parse_manifest(manifest) and u.download_url.ends_with("-5.exe"),"new service build")
	manifest.platforms.windows.file="../ClassicTavern-Service-5.exe";check(not u.parse_manifest(manifest),"reject traversal")
	manifest.platforms.windows.file="https://evil/ClassicTavern-Service-5.exe";check(not u.parse_manifest(manifest),"reject remote origin")
	manifest.platforms.windows.file="ClassicTavern-Service-5.exe";manifest.platforms.windows.sha256="no";check(not u.parse_manifest(manifest),"reject bad digest")
	manifest.channel="standalone";check(not u.parse_manifest(manifest),"channel isolation")
	manifest.channel="service";manifest.build=u.BUILD;check(u.parse_manifest(manifest) and u.download_url.is_empty(),"same build no update")
	u.free();music.queue_free();fx.queue_free()
	await process_frame
	print("AUDIO_UPDATE_TEST failures=",failures);quit(1 if failures else 0)

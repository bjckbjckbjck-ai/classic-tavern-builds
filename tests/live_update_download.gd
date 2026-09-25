extends SceneTree
func _initialize():call_deferred("run")
func run():
 var u=load("res://scripts/service_updater.gd").new();root.add_child(u)
 while u.busy:await create_timer(.1).timeout
 var req=HTTPRequest.new();root.add_child(req);req.request(u.BASE+"latest.json")
 var response=await req.request_completed
 var manifest=JSON.parse_string(response[3].get_string_from_utf8());manifest.build=u.BUILD+1
 assert(u.parse_manifest(manifest));u.staged="user://qa-service4-download.part"
 u.downloading=true;u.busy=true;u.http.download_file=u.staged;u.http.timeout=1800;u.http.body_size_limit=u.expected_size
 assert(u.http.request(u.download_url)==OK)
 while u.busy:await create_timer(1).timeout
 if not u.ready_to_install():push_error(u.message);quit(1);return
 print("PUBLIC_DOWNLOAD_VERIFIED bytes=",u.expected_size," sha256=",u.expected_hash)
 u.expected_hash="a".repeat(64);u.downloading=true;u.received(HTTPRequest.RESULT_SUCCESS,200,PackedStringArray(),PackedByteArray())
 assert(not FileAccess.file_exists(u.staged));assert("校验失败" in u.message)
 print("CORRUPT_PACKAGE_REJECTED_AND_REMOVED")
 u.queue_free();req.queue_free();await process_frame;quit()

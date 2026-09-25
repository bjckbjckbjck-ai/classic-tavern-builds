extends Node
signal completed
const VERSION="0.61.0-service5"
const BUILD=5
const BASE="https://bjckwrn.xyz:21111/downloads/"
const REPO="https://bjckwrn.xyz:21111"
var busy=false
var message="从云服检查客户端更新。"
var download_url=""
var latest=""
var expected_hash=""
var expected_size=0
var http:HTTPRequest
var downloading=false
var staged="user://client-update.exe.part"
var elapsed=0.0

func _ready():
	http=HTTPRequest.new();http.timeout=20;http.body_size_limit=65536;http.max_redirects=0;add_child(http)
	http.request_completed.connect(received)
	check()

func check():
	if busy:return
	busy=true;download_url="";message="正在检查云服最新版本……";completed.emit()
	http.download_file="";http.timeout=20;http.body_size_limit=65536
	if http.request(BASE+"latest.json?t="+str(Time.get_unix_time_from_system()))!=OK:fail("无法连接更新服务器，可以继续游戏。")

func parse_manifest(data)->bool:
	download_url=""
	if not data is Dictionary or data.get("channel","")!="service":return false
	if typeof(data.get("build")) not in [TYPE_INT,TYPE_FLOAT]:return false
	latest=str(data.get("version",""))
	if int(data.build)<=BUILD:message="当前已是最新云服版："+VERSION;return true
	var platform="android" if OS.get_name()=="Android" else "windows"
	if not data.get("platforms",{}) is Dictionary:return false
	var entry=data.get("platforms",{}).get(platform,{})
	if not entry is Dictionary:return false
	var filename=str(entry.get("file",""))
	var suffix=".apk" if platform=="android" else ".exe"
	if filename.get_file()!=filename or not filename.begins_with("ClassicTavern-Service-") or not filename.ends_with(suffix):return false
	var hash=str(entry.get("sha256","")).to_lower()
	if hash.length()!=64 or not hash.is_valid_hex_number(false):return false
	if typeof(entry.get("bytes")) not in [TYPE_INT,TYPE_FLOAT]:return false
	var size=int(entry.get("bytes",0))
	if size<1000000 or size>1073741824:return false
	download_url=BASE+filename;expected_hash=hash;expected_size=size
	message="发现新版 "+latest+"（%.1f MB）。"%(size/1048576.0)
	message+="点击后由浏览器下载 APK，再由系统确认安装。" if platform=="android" else "一键下载、校验、退出并更新；旧程序保留为 .previous。"
	return true

func install():
	if busy or download_url.is_empty():return
	if OS.get_name()=="Android":
		if OS.shell_open(download_url)!=OK:fail("无法打开浏览器，请使用手动下载。")
		return
	if OS.get_name()!="Windows" or OS.has_feature("editor"):fail("请使用导出的 Windows 客户端，或手动下载。 ");return
	busy=true;downloading=true;http.download_file=staged;http.timeout=1800;http.body_size_limit=expected_size
	message="正在下载更新，游戏仍可继续。";completed.emit()
	if http.request(download_url)!=OK:fail("下载无法开始，请重试。")

func _process(delta):
	if not downloading:return
	elapsed+=delta
	if elapsed<.5:return
	elapsed=0
	message="正在下载：%.1f / %.1f MB"%[http.get_downloaded_bytes()/1048576.0,expected_size/1048576.0];completed.emit()

func fail(text:String):
	busy=false;downloading=false;message=text;completed.emit()

func received(result:int,status:int,_headers:PackedStringArray,body:PackedByteArray):
	if result!=HTTPRequest.RESULT_SUCCESS or status!=200:
		fail("更新请求失败，现有客户端不受影响；可以重试或手动下载。");return
	if not downloading:
		busy=false
		if not parse_manifest(JSON.parse_string(body.get_string_from_utf8())):message="更新清单无效，已拒绝更新。"
		completed.emit();return
	downloading=false
	var file=FileAccess.open(staged,FileAccess.READ)
	if file==null:fail("下载文件不可读，请重试。");return
	var size=file.get_length();file.close()
	if size!=expected_size or FileAccess.get_sha256(staged)!=expected_hash:
		DirAccess.remove_absolute(ProjectSettings.globalize_path(staged));fail("更新包校验失败，已丢弃；旧程序保持不变。");return
	busy=false;message="下载并校验完成。点击“安装并重启”，请先结束当前对局。";completed.emit()
	# Never close a game entered while the background download was running.
	var app=get_parent()
	if app.get("state") is Dictionary and app.state.is_empty() and (not app.get("cloud") or not app.cloud.active):restart_install()

func ready_to_install()->bool:
	return not busy and expected_hash!="" and FileAccess.file_exists(staged) and message.begins_with("下载并校验完成")

func restart_install():
	if not ready_to_install():return
	var config={"target":OS.get_executable_path(),"source":ProjectSettings.globalize_path(staged),"sha256":expected_hash,"pid":OS.get_process_id()}
	var config_path=ProjectSettings.globalize_path("user://update-job.json")
	var script_path=ProjectSettings.globalize_path("user://install-update.ps1")
	var file=FileAccess.open(config_path,FileAccess.WRITE)
	if file==null:fail("无法保存更新任务，请手动下载。");return
	file.store_string(JSON.stringify(config));file.close()
	file=FileAccess.open(script_path,FileAccess.WRITE)
	if file==null:fail("无法写入更新程序，请手动下载。");return
	file.store_string(INSTALL_SCRIPT);file.close()
	var pid=OS.create_process("powershell.exe",PackedStringArray(["-NoProfile","-NonInteractive","-ExecutionPolicy","Bypass","-WindowStyle","Hidden","-File",script_path,"-Config",config_path]))
	if pid<=0:fail("更新程序启动失败，请手动下载。");return
	get_tree().quit()

const INSTALL_SCRIPT="""param([Parameter(Mandatory=$true)][string]$Config)
$ErrorActionPreference='Stop'
$job=Get-Content -LiteralPath $Config -Raw | ConvertFrom-Json
$target=[IO.Path]::GetFullPath($job.target)
$source=[IO.Path]::GetFullPath($job.source)
$backup=$target+'.previous'
$temp=$target+'.incoming'
$log=Join-Path ([IO.Path]::GetDirectoryName($Config)) 'update-result.txt'
function Get-Sha256([string]$Path) {
  $stream=[IO.File]::OpenRead($Path)
  $hasher=[Security.Cryptography.SHA256]::Create()
  try { return [BitConverter]::ToString($hasher.ComputeHash($stream)).Replace('-','').ToLowerInvariant() }
  finally { $hasher.Dispose(); $stream.Dispose() }
}
try {
  Wait-Process -Id $job.pid -Timeout 60 -ErrorAction SilentlyContinue
  if (Get-Process -Id $job.pid -ErrorAction SilentlyContinue) { throw 'Game did not exit' }
  if ((Get-Sha256 $source) -ne $job.sha256) { throw 'Invalid download hash' }
  Copy-Item -LiteralPath $source -Destination $temp -Force
  if ((Get-Sha256 $temp) -ne $job.sha256) { throw 'Invalid staged hash' }
  [IO.File]::Replace($temp,$target,$backup,$true)
  Start-Process -FilePath $target -WorkingDirectory ([IO.Path]::GetDirectoryName($target))
  'Update installed; previous executable: '+$backup | Set-Content -LiteralPath $log
} catch {
  $_.Exception.Message | Set-Content -LiteralPath $log
  Add-Type -AssemblyName PresentationFramework
  [System.Windows.MessageBox]::Show('Update failed. Your previous executable is preserved. See '+$log,'Classic Tavern') | Out-Null
}
"""

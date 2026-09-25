# 云服客户端 0.61.0-service5

2026-09-26 发布，Android versionCode 5，保持原 org.classictavern.service 包名和现有签名。
后端仍为 0.2.0-preview，协议不变，账号和房间不受客户端发行影响。

## 音乐与音效

所有者提供的六首音乐已接入：招募播放水手之家、血帆、深水；战斗播放 Human BGM 2、Orc BGM 4、Orc Victory。原文件虽然名为 FLAC，实际是 MP3；保持字节内容并纠正扩展名，不重新压缩。阶段分别随机轮播，避免连续重复，0.65 秒淡入淡出，切回阶段继续原曲。

本次未取得可核实的原版倒计时、结束回合等 UI 音频文件。新增七个原创程序拟音：倒计时开启、每秒提醒、紧急提醒、按钮扣合、回合开启、战斗开始、按钮点击。游戏声音设置内可查看来源及原创声明；提供的音乐不声明为本项目原创。完整来源记录在游戏 assets/audio/README.md 和 music/manifest.json。

## 客户端更新

- 启动时检查固定 HTTPS 地址 `/downloads/latest.json`，只接受 service 通道和更高 build。检查失败可继续游戏。
- 首页“客户端更新”显示检查结果和下载进度。独立版仍保留自己的原更新通道。
- Windows：下载到用户数据目录，检查文件大小和 SHA-256，校验后退出、原子替换并启动新版。旧程序留为 `<程序名>.previous`，结果记录在用户数据目录 update-result.txt。安装目录不可写时显示失败提示并保留旧文件，可手动下载。
- 下载期间进入对局则不会自动退出，待回到菜单点击“安装并重启”。下载不会更改账号、偏好和存档。
- Android：一键打开该版本的 APK 下载，由系统浏览器保存，用户确认覆盖安装。当前未实现应用内 APK 校验或绕过系统确认的静默安装。
- 安装包使用带构建号的不可变文件名，先发布两端文件并校验，再原子切换清单；旧的固定下载链接仍然有效。
- 老客户端没有此云服更新器，因此首次需要手动安装 service5。后续从应用内更新。

## 验证

- Godot 测试覆盖六首音乐资源解码、阶段切换/恢复、不连续重复、48 个音效导入、倒计时去重与停止条件、清单通道/版本/来源路径/散列校验。
- Windows 原生界面测试：招募、战斗均通过 AudioEffectCapture 检测到非零 PCM 音频；更新入口、更新页、原创声明页通过，截图已保存。
- Windows 辅助安装器使用独立测试程序实际完成替换、旧文件保留、新程序启动。不在真实账号客户端上故意执行降级或破坏性替换。
- EXE release、APK debug 导出通过；APK ZIP 完整性、包名/versionCode 和六首内置音乐核对通过。
- 服务器发布上传文件 SHA-256 与本地一致；HTTPS 清单、两端下载入口、后端健康检查正常。
- 未做实体 Android 听感与系统覆盖安装验收；本轮不涉及容量压测。

## 后续发布

1. 更新游戏源码并同步服务适配；递增 service_updater.gd 的 BUILD/VERSION 与 Android versionCode/versionName。
2. 导出 Windows Desktop 和 Android 到游戏 build/ClassicTavern-Service.exe、.apk，跑相关测试。
3. 执行 `python deploy/publish_clients.py --game-dir <游戏工作树> --build <递增整数> --version <版本> --key <本地SSH密钥路径>`。密钥不要提交。
4. 更新 release-manifest.json 中客户端提交与构建散列。若只改客户端，不需要重启后端。

发布脚本拒绝用不同内容覆盖已经发布的构建号。不要先发布清单再上传文件，也不要把独立版包写入 service 通道。

最终 Windows 安装辅助器已改为直接使用系统 SHA-256 API，避免依赖 PowerShell 模块自动加载。含空格目录的真实替换/保留旧文件/启动测试通过（pytest 1 passed）。发布过程中的构建 4 已完成 Godot 实际 HTTPS 全量下载校验，并通过故意错配摘要后的拒绝/删除测试；构建 5 只修复辅助安装器环境兼容性，网络下载逻辑未改变。

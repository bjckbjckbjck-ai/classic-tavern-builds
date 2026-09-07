# v0.9.0 验证（2026-09-07）

- 14 个回归套件，306 项断言通过：五种关键词 71 项、联机/UI 新增 10 项，既有 225 项全部通过。
- 真实两个 Windows EXE 进程：连接、购买、上阵、准备、战斗回放、公开快照隐私与退出后 BOT 托管通过。日志 `.runtime/v9-network-host.log` / `client.log`。
- Windows EXE 作为房主进程，Android 13 模拟器运行最终 APK，通过 10.0.2.2:14281 连接。实际触摸操作填地址、加入、添加七个 BOT、调整霸主难度、开局、购买、上阵、结束回合。成功收到战斗和第二回合状态（58 生命、4/4 铸币），截图 v9-android-lobby / recruit / combat / next-round。
- 关闭 Windows 房主后，Android 返回主菜单并提示房主断开。测试房主已关闭，没有留下游戏服务器。
- Android APK 覆盖原安装成功，包名 org.classictavern.game、versionCode 9；APK ZIP 完整、资源与公告正确，未打包测试和旧浏览器参考目录；v2/v3 签名验证通过，证书与 v0.8.0 相同。
- 原生 Windows 渲染检查菜单、联机页、房间、五色层数与金色扎普详情。两行短徽标保留随从原画空间。
- 未实测：两台实体设备同一 Wi-Fi、安卓机型差异与公网高延迟；不把模拟器互通视为实体手机验收。没有公网中继部署、断线重接管、主机迁移。部分 headless UI 退出仍有 ObjectDB 存活警告；Android 启动有缓存 shader 重编译提示，无此次 GDScript 错误或 AndroidRuntime 崩溃。

- ClassicTavern-v0.9.0.exe: 150620800 bytes; SHA256 `08f76aeba4c7c38d5ef07353be59b997454c42e8b660e95c24b4322201b59a2c`
- ClassicTavern-v0.9.0.apk: 130104623 bytes; SHA256 `3456579afc04f93e82a4b70409ec8714a3213ab471cd13094054b52920204c9b`

---

## v0.8.0 发布验证（2026-09-07）

- 发布后在最终 APK 内手动检查更新，成功返回“当前已是最新版本：v0.8.0”；验证结束后已关闭模拟器中的游戏进程。
- 包：`build/ClassicTavern-v0.8.0.apk`，125,095,083 字节（约 119.3 MiB）。
- SHA256：`e81fc7481ab17296c0638fe4253189955a4c5cf070fd5d43cfa4312c7e6f6193`。
- 公开地址：https://github.com/bjckbjckbjck-ai/classic-tavern-builds/releases/download/v0.8.0/ClassicTavern-v0.8.0.apk 。发布后匿名完整下载，SHA256 与本机构建一致。
- Android versionCode 8 / versionName 0.8.0；工程、更新检查与页脚统一版本来源。沿用原签名，v2/v3 验证通过；Android 13 模拟器覆盖安装成功。
- ZIP 完整性检查通过；包内 six-tribes.json、archetypes.json 与最新公告存在，33 张新牌及衍生物数据已核对；新原画导入并截图检查。references、tests、.runtime 不在 APK 中。
- 225 项检查通过：rules 32、migration 12、stacking 25、offline UI 7、feel 6、AI content 32、difficulty UI 5、allstars 20、UX v7 12、six tribes 48、UX v8 14、pool integrity 12。最终排版与页脚修改后，额外重跑 UX v8 和 feel 共 20 项，通过。
- 测试包含正常/金色、铜须多次发现、烈毒叠加、复生、磁力与三连继承、卡池归还、六族触发及多种子完整对局。12 个种子在每回合招募与战斗后检查共享卡池数量守恒。
- 30 局相同英雄与普通经济的困难/休闲 AI 对照：困难第一 25 次、平均名次 3.6；休闲第一 5 次、平均名次 5.4。只衡量本地难度区别，不作为种族平衡或真人胜率结论。
- Windows 原生渲染：菜单、六族规则、龙/海盗图鉴、混合六族棋盘、毒鳍详情、乔治指向与战斗截图。输入回归含非法松手、满场磁力、首位插入、尾部换位、死亡禁跳和结算展示快照。
- Android 13：初次候选包验证六族规则滚动、龙/海盗图鉴与公告。最终包重新覆盖安装，页脚 v0.8.0；进入乔治单机八人局，真实触摸指令拖动购买红色雏龙、上阵、结束回合、进入第二回合、英雄技能拖动加圣盾（1），铸币从 4 减为 2。
- 日志未见 GDScript 错误或 Android 崩溃。模拟器启动有缓存着色器重新编译警告；部分无头 UI 测试退出时有 ObjectDB 未释放警告，不等同于实体设备长期内存验证。
- 尚未验证：用户实体手机的触摸与性能、长时极端连锁内存、真实多设备联机。本轮不增加暂停或续局，不运行游戏服务器。

# v0.7.0 verification

Godot 4.6.1, Android code 7. 151 assertions passed: original rules 32, v0.5 migration 12, stacking 25, offline UI 7, drag/long press 6, AI/content 32, difficulty UI 5, allstars/updater 20, new UX 12. Existing full eight-bot simulations remain included. Final gallery input changes reran UX and feel tests successfully.

Allstars tests cover normal/golden frog inheritance without re-doubling on recipients, additive Titus repeats, living Wolf excluding itself, Mama flat buff followed by 2x/3x Slamma multiplication, no recruitment Slamma multiplier, Macaw post-attack trigger, leap budget limit, four new hero powers, numeric version validation, same-repository APK URL checks, draft rejection and announcement version.

UI tests cover news/update entry, offline error handling, second hero page, targeted release over empty/wrong/valid targets, filtered golden gallery, living skip and dead skip rejection. Native screenshots inspected arrow alignment and unobscured target after correcting scaled coordinates. Real physical phone targeting is not yet verified.

Android 13 emulator final APK: overlay install succeeded, manual update request completed, in-game news opened, hero and card galleries drag-scrolled after fixing child input propagation. Purchase/play and living combat skip entered round 2 on the prior candidate with identical combat logic. No SCRIPT ERROR or runtime ERROR in final captured Godot log. Known shader-cache warning recompiles on launch; known ObjectDB warning appears in headless UI cleanup during active animation.

APK 116584458 bytes; SHA256 37d60fb6e0b74c587fff820be2dc1603507a778b038af6d061d2776e57d9a468. Signatures verified, ZIP integrity passed, allstars.json and releases.json included, references excluded. GitHub upload API returned 201, matching size. Published v0.7.0 with APK and checksum.

This is a cross-era curated pool, 38 purchasable minions plus 9 tokens and 8 heroes. It is not every historical minion/hero. New hero powers are selected historical configurations rather than old browser custom-power reskins. Physical-phone performance, human balance and installation of a future newer APK through the update button remain unverified.

# v0.6.0 verification

2026-09-07, Godot 4.6.1. Rules 32/32; migration 12/12; stacking 25/25; offline UI 7/7; drag/long press 6/6; AI/content 32/32; difficulty UI 5/5. Total 119 assertions. AI/content covers 40 full eight-bot simulations (4 difficulty levels, 2 rule modes, 5 seeds), with coin bounds, armor, board/hand limits and unique winner checks.

Equal-resource benchmark: 30 seeds, four easy versus four hard bots, classic mode, rotating assignments. Easy: 0 wins, average rank 6.22. Hard: 30 wins, average rank 2.78. This is a bot-only bounded benchmark, not a human difficulty or win-rate guarantee. Log: .runtime/v6-ai_benchmark.log.

Android 13 emulator: final APK installed over v0.5, difficulty menu selected boss, seven bots started with visible 10 armor while human had none; dragging purchase/play and combat worked. Damaged bots lost armor before health. Captured Godot log contains no SCRIPT ERROR, ERROR or exception. Screenshots: android-v060-difficulty.png, android-v060-boss.png, android-v060-combat.png. Physical phone performance and human balance remain unverified. Headless UI tests retain the known ObjectDB cleanup warning at exit during animation.

APK v2/v3 signatures verified. org.classictavern.game code 6. Size 115226305 bytes. SHA256 d7c2a51288b997a049e0d9104519cc4a8f5f5a6249ea79bf1cee0f1a4fdbb7f6. ZIP integrity passed; synergy pack included; references excluded. Five new art source URLs/hashes recorded in ASSET_SOURCES.json. Browser source not modified.

# v0.5.0 verification

2026-09-07, Godot 4.6.1. Rules 32/32; migration effects 12/12; stacking 25/25; offline UI 7/7; drag/long press 6/6. Total 82 assertions, including 10 classic and 10 stacking full eight-bot games.

Android 13 emulator: final APK successfully installed over previous version, selected Yogg, entered offline eight-player match, dragged shop purchase and hand play, and entered combat. Hero description wrapping and portrait edge crop inspected on Android. Screenshots: android-v050-heroes.png, android-v050-play.png, android-v050-combat.png. No SCRIPT ERROR or runtime ERROR in captured godot log; shader cache warning caused recompilation. Physical phone, audio listening and long-session device performance remain unverified. Offline UI test still reports the known ObjectDB warning when exiting during animations.

APK v2/v3 signatures verified. Package org.classictavern.game, version code 5. Size 114811192 bytes. SHA256 80381854bf8c6fae5774879c56009ed8028020a166366e577c2c4c4d02c5b6d6.

Migrated six original cards from browser v0.6.0 selection. Original 32 base entries remain unchanged. Six new art source URLs and hashes recorded in ASSET_SOURCES.json. Migration includes golden effects; it is not an exact launch-era content set.

# v0.4.0 verification

2026-09-07, Godot 4.6.1.

- Classic rules 32/32; stacking rules 25/25 (includes 10 complete eight-bot simulations); offline UI 5/5; drag/long press 6/6.
- Android 13 emulator: final APK installed over prior version, entered offline practice, dragged purchase/play, selected minion, applied shield and opened detail with count and copied shield art. See screenshots/android-v040-shield.png.
- Offline practice explicitly uses OfflineMultiplayerPeer. No server opened for this delivery.
- Browser material copy: 335 files, 72074052 bytes; all copied file hashes match manifest; reference files in APK: zero. Only selected shield/venom images used at runtime.
- APK signature v2/v3 valid. Size 114326539 bytes. SHA256 bfc759be118c221eeec2e26495bbc42526bea40ddf3ac268c8aeb021cd3d4942.
- Public GitHub Release v0.4.0 published with APK, checksum and Upgrade-Plan-v1.md. Full anonymous APK download through local HTTP proxy completed; SHA256 matches local build.
- Physical Android device not tested. Offline UI test exits during active short animations and may emit ObjectDB leak warning; no new script errors observed in Android flow.
- Original permanent poison remains distinct from venom. Reborn/windfury stacking and tavern spells not implemented in this release.

## v0.3.0 historical verification

Date: 2026-09-07. Godot 4.6.1 native Android/Windows.

- Rules 32/32, base UI 11/11, input-level drag/long-press 6/6 passed. Logs in .runtime/*-v030.log.
- Android 13 emulator: final APK installed over v0.2.0; entered seven-bot practice; touch drag purchased and played a minion; long press opened card details; tap closed details; end-turn initiated combat.
- Final runtime no new script errors during these actions. Initial cached-shader warning falls back to recompilation. Host GPU emulator mode used; physical ARM phone not tested. Synthesized audio cues are implemented but listening quality was not tested.
- APK v2/v3 signature verification passed. Package org.classictavern.game, versionCode 3. ARMv7/ARM64/x86_64.
- Native staged presentation screenshot screenshots/table.png; actual Android screenshots android-v030-detail.png and android-v030-battle.png.
- SHA256: 5af6b7536d8d0596340289d909436c3d44e68e87a2dfc819a5f092b1e1ba5701.
- Published standalone APK and checksum to https://github.com/bjckbjckbjck-ai/classic-tavern-builds/releases/tag/v0.3.0. No game-server exposure required.
- Anonymous public download completed through the local HTTP proxy; downloaded APK SHA256 matches the local build exactly, 112433628 bytes.

## v0.2.0 historical verification

Date: 2026-09-07. Godot 4.6.1, native GDScript.

- Rules 32/32 passed; UI 11/11 passed after deferred button callbacks. Headless UI tests now skip framebuffer capture and exit normally.
- WebSocket dedicated server through local HTTP upgrade gateway: client joins, manages room, adds bot, purchases, plays and receives combat replay.
- Android 13 x86_64 emulator: APK installed, landscape menu/lobby visible, joined the PC dedicated server through 10.0.2.2, added bot, started match, bought and played Righteous Protector and received round 2 combat. Screenshots: android-menu.png, android-lobby.png, android-table.png, android-battle.png.
- APK supports ARMv7, ARM64 and x86_64; INTERNET permission; debug signing. ARM physical device not tested.
- Final APK reinstalled; Android Back key keeps the app alive, and saved gateway URL rejoins the room successfully (android-final.png). APK SHA256: dd0de2397df17cfb31c1f8709db4343a114b5e16c27a115d28c4b968fbc3190e.
- Simulator software SwiftShader failed to compile Godot canvas shaders. Host GPU mode with OpenGL compatibility rendered correctly; fresh cold-start first launch exited during emulator boot, relaunch succeeded. Physical phone compatibility remains unverified.
- Public deployment NOT completed: Cloudflare tunnel launch rejected by automatic approval, no specific reason returned. No public WSS or cellular connection test performed. Remote one-click button intentionally disabled without a configured URL.

## Previous v0.1.0 baseline (historical)
Date: 2026-09-07
Engine: Godot 4.6.1.stable.official.14d19694e
Renderer: OpenGL compatibility, NVIDIA RTX 5060 Laptop GPU

- Rules: 32/32 PASS (tests/rules-results.log).
- Includes 10 seeded complete eight-bot matches and 32 original-card name/stat comparisons against build 35747.
- Native mouse UI: 11/11 PASS (tests/ui-results.log).
- Exported EXE: host/client ENet room, buy/play/ready, round 1, matching 6-event replay PASS.
- Private snapshots: other players have no hand/shop data PASS.
- Client disconnect: server switches disconnected player to bot PASS.
- Exported external mods: extra card + fifth hero loaded PASS.
- Exported native renderer boot: PASS, no stderr.
- Original artwork: 32 minions/tokens and 4 heroes present, SHA256 in ASSET_SOURCES.json.
- Screenshots: menu.png, lobby.png, table.png, ui-tested-battle.png.
- Final demonstration: screenshots/result/3/video.mp4, 450 source PNGs, 30 FPS, 15 seconds. Staged boards and frozen clock for capture; not a naturally timed match.

Not tested: two physical PCs, actual router/AP isolation, Windows firewall prompt workflow, reconnect (not implemented), full historical card pool, exact advanced deathrattle ordering versus official client.


Public release v0.5.0 published. Full anonymous download from the public APK URL verified against local SHA256: exact match. APK archive integrity passed; legacy-expansion.json present; reference files packaged: zero.



Public v0.6.0 release published. Complete anonymous download SHA256 equals the built APK. Initial gh large-asset upload stalled twice; authenticated GitHub upload API with curl HTTP/1.1 succeeded (201, 115226305 bytes). Authentication was piped in memory, not stored in files or logs.


Full anonymous download from the public v0.7.0 APK URL completed. SHA256 exactly matches the final local package.

# v0.14.0 验证（2026-09-08）

- 26 个套件、481 项断言通过，日志 `.runtime/v14-*_test.log`。初次全回归的龙图鉴数量断言仍是旧值，修改为当前 14 后通过；未跳过测试。结算文案调整后重跑 UI、公告和体验检查。
- 新英雄完成标准/霸主各两个随机种子的八 BOT 完整对局；检查币上限、手牌/战场上限、护甲和唯一冠军。不是大样本胜率平衡结果。
- 新规则：免费刷新来源与过期、帕奇斯费用/满手/空池退款、阿莱克丝塔萨双发现、吞食、消费成长、每层破盾成长、金色琥珀不同目标叠盾、七点伤害分为五护甲与两生命。
- 原生 Windows 截图：`screenshots/v14-heroes.png`、`v14-armor-recruit.png`、`v14-armor-impact.png`、`v14-armor-depleted.png`。检查英雄文案不溢出、护甲数字可读；修正结算数字压住头像的问题。
- 最终 EXE 双独立进程完成建房、加入、购买、使用、法术同步、战斗、私有快照及客户端离线 BOT 接管。日志 `.runtime/v14-network-host.log` / `client.log`。
- Android 13 模拟器从旧版覆盖安装成功。包名 org.classictavern.game，versionCode 14，versionName 0.14.0。实际选择帕奇斯、进入单机、进入第二回合、4 币获取甲板杂兵，UI 显示 0/4 铸币与本轮已用；查看游戏内 v0.14 公告；在线检查返回最新版本 v0.14.0。截图 `screenshots/v14-android-*.png`。
- APK 签名验证通过，沿用原 Android Debug 证书：5d15dbad38e4504fa3b1e7ad1aab3c91d0e65bc57f29e8d775866893a659b2cc。属于体验安装包。
- 32 WAV 资源均载入并有有效时长，PCM 峰值无满幅削波，静音/限频测试通过；真实手机扬声器听感未测。
- APK ZIP 完整性、100 在池随从/14 衍生物/15 英雄所用扩充包、原图、32 音效、公告和资源排除检查通过；原始用户照片附件不入包。
- GitHub 公开 APK/EXE 均已完整匿名下载，SHA256 与本地产物一致。
- 未覆盖：实体安卓手机、两台实体设备同 Wi-Fi 对战、长期真人平衡及极端连锁帧率。部分历史 headless 测试退出时仍有 ObjectDB/resource 清理警告，未出现 SCRIPT ERROR。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| ClassicTavern-v0.14.0.exe | 167430192 | 373aa1d100b579abbd500e2adda0214a692bd472d965cb3d2fe373c649d879ea |
| ClassicTavern-v0.14.0.apk | 146734725 | c26021460e33cc49908283917277b312fc0284e76a0e78f111ffa62eb542050c |

---

# v0.13.0 验证（2026-09-08）

- 23 个套件、446 项断言通过（`.runtime/v13-*_test.log`）。初次全回归在公告同步前启动，公告版本检查失败；同步后重跑通过，未跳过断言。最后文案精简后重跑英雄、体验和公告检查。
- 国王老汉：5 币费用、满手/不足币不推进随机数、每轮一次、1～6 精确星级、可高于当前酒馆、共享副本扣除、空池退款、奖励三连均通过。新英雄进入标准/霸主、两个种子的完整八人 AI 对局。
- UI 验证商店对子计数排除金色、手牌与场上合计、资源摘要、技能可用、骰子结果记录只写一次、记录滚动容器。原生截图 v13-recruit-hints、v13-dice-result、v13-history、v13-king-draft。
- Android 13 模拟器实际跨回合使用国王老汉：第三回合 5 币掷出 5，获得五星提克迪奥斯，金币变为 0/5、技能标记 1/1；进入操作记录查看结果。截图 v13-android-king-roll、v13-android-history。此规则体验在最后仅精简技能文案之前；最终包重新覆盖安装，并检查最终选人页与更新功能。
- 安卓实际排版发现长技能文案超出选人卡框，已精简，最终截图 v13-android-final-draft 中说明完整位于卡框内。
- 最终 Windows EXE 两个独立进程完成连接、购买/施放、战斗同步、私有快照和断线机器人托管。日志 v13-network-host / client；有既有退出资源存活警告，未见 GDScript 错误。
- 最终 APK ZIP 完整，含自创英雄画作、12 英雄、20 法术、最新公告；不含上传原照片、测试和参考目录。v2/v3 签名通过，沿用旧签名。版本号 0.13.0 / versionCode 13。
- 正式发布后匿名完整重下载 APK/EXE，大小和 SHA256 一致。最终 APK 实际检查更新返回 v0.13.0 已为最新。
- 未验证实体安卓机型性能与长期平衡，也不把模拟器和同机双进程视为两台实体设备 Wi-Fi 验收。没有常驻公网服务器。本版操作记录属于本机最近操作摘要，不是完整战斗回放档案。

- ClassicTavern-v0.13.0.exe: 164217912 bytes; SHA256 `8d02d759466e7559c07c3f932468a31728f1d8d8a253e7b92e30de59ab370774`
- ClassicTavern-v0.13.0.apk: 143576103 bytes; SHA256 `2ef1fea95deadb0fd033d1fc3a9148b75aacec977cde8e3bd32005ecb64d8fde`

---

# v0.12.0 验证（2026-09-08）

- 21 组回归检查、428 项断言通过。20 组主回归 424 项，新增三英雄全局模拟 4 项。日志 `.runtime/v12-*-test.log`（实际套件名使用下划线，如 v12-playstyles_v12_test.log）。
- 覆盖手牌成长、低音提琴战斗副本与单次限制、合唱回放不泄露手牌、提克迪奥斯与回溯、娜拉分族增益、生火专家法术等级、7 张法术、第三次购买免费、蛇眼冷却、荷利戴与自负结算。
- 新英雄在标准和霸主难度、两个种子下各完成八人 BOT 全局，检查铸币、手牌、战场与唯一冠军边界。既有 AI 回归含多难度完整模拟；这不等同于长期平衡数据。
- 原生 Windows 实际渲染检查 `screenshots/v12-minion-grey.png`、`v12-hero-grey.png`：致命伤灰化、0 血、灰色英雄头像和淘汰名次；测试另外检查灰色离场残影及清理。`v12-playstyles.png` 检查新核心原画与免费法术价格。
- 最终 Windows EXE 双进程加入、购买/施放法术、上阵、战斗、私有快照与断线 BOT 托管通过。日志 `.runtime/v12-network-host.log` / `v12-network-client.log`。
- Android 13 模拟器覆盖安装最终 APK 成功，实际触摸第三页新英雄选择、蛇眼开局与技能。投出 1 点后，3 币先扣 1 再加 1，仍为 3/3，旁边显示冷却 1 回合并禁用技能。截图 `v12-android-menu.png`、`v12-android-snake-roll.png`。
- Android versionCode 12、versionName 0.12.0；arm64-v8a / armeabi-v7a / x86_64。v2/v3 签名检查通过，证书与旧版一致；ZIP 完整，包内有 20 张法术、最新公告、卡池和 24 音效映射，不含 tests/references/.runtime。
- GitHub 正式发布后，匿名完整下载 APK 和 EXE，大小与 SHA256 均匹配。Android 内实际点击检查更新，显示“当前已是最新版本：v0.12.0”。
- 尚未实测实体安卓手机、两台实体设备 Wi-Fi、不同机型性能与长期胜率。既有 headless 退出资源警告不等同于游戏中故障；本次 Android 日志未发现 GDScript 错误或 AndroidRuntime 致命崩溃。没有常驻公网服务器。

- ClassicTavern-v0.12.0.exe: 162316720 bytes; SHA256 `303df27def8aa4224787fab59061a67ad0229948855de6bde77f1fd5be9f3a89`
- ClassicTavern-v0.12.0.apk: 141675022 bytes; SHA256 `036b0e377dbdd9a3457bb34cc3b442c8590453c9658870b0e75a91c50ee4777d`

---

# v0.11.0 验证（2026-09-08）

- 18 个回归套件共 383 项断言通过。新增 25 项规则与事件检查、8 项 UI/音频资源检查；旧计数断言更新为包含五张退池兼容定义，实际商店仍为 83 种。
- 覆盖小瞎眼相邻战吼、达卡莱倍数、回溯致命招募伤害/护甲/战斗不回溯、特塞斯共享池/满手/进度、凯尔萨斯第三次购买与法术不计数、跳蛙实际源目标及烈毒撞盾分流。
- 检查 24 个 AudioStreamWAV 正常加载、静音阻止音源创建、同类音效限频。声音为本地合成设计；尚未经实体手机扬声器主观试听验收，不把资源加载与事件检查视为音质结论。
- Windows 原生渲染截图：v11-counters、v11-frog-trail、v11-hero-impact、v11-settled。英雄结算先显示战前生命，动画结束后显示实际生命；打开图鉴不会阻止结算完成，重绘不重播同一视觉事件。
- 两个最终 Windows EXE 进程通过加入、购买随从/法术、施放、上阵、战斗、私人快照与断线 BOT 接管检查。日志 `.runtime/v11-network-host.log`、`v11-network-client.log`。
- Android 13 模拟器覆盖安装最终 APK 成功，实际触摸选择凯尔萨斯单机开局、购买上阵、进入战斗并跨三回合购买随从。计数显示 1/3、2/3；第三个粗俗的矮劣魔从 2/4 变为 4/6，计数归零。截图 v11-android-counter1、counter2、third-purchase。
- Android versionCode 11 / versionName 0.11.0，v2/v3 签名验证通过并沿用原证书。ZIP 完整，24 音效导入映射、新卡数据和最新公告在包内，tests/references/.runtime 未打包。导出 EXE 内嵌资源。
- 发布后匿名完整重下载 APK 与 EXE，大小和 SHA256 与最终本地包一致；Android 实际检查更新显示 v0.11.0 已是最新。测试游戏进程已关闭，没有留下游戏服务器。
- 尚未验证：实体手机触控/扬声器/性能、两个实体设备跨 Wi-Fi、极端连锁长期内存与种族长期胜率。本轮保留部分 headless 退出时 ObjectDB/资源存活警告；Android 冷启动有 shader 缓存重编译，未见本次 GDScript 错误或 AndroidRuntime 致命崩溃。

- ClassicTavern-v0.11.0.exe: 157611696 bytes; SHA256 `2b2e7ceea10e12baae3e3500195acfbe30acbfb65184ad51e98a585e3f8a4fce`
- ClassicTavern-v0.11.0.apk: 137013917 bytes; SHA256 `ae30f8c90671ebf8e334c722e008e3899d31987a14d1acfc49240fe8e686b8c9`

---

# v0.10.0 验证（2026-09-07）

- 16 个回归套件共 350 项断言通过，包含新增法术与核心随从 36 项、法术交互 8 项；最终显示与同步调整后重跑这 44 项通过。
- 两个最终 Windows EXE 进程完成联机，验证购买随从、上阵、购买法术、施放、战斗同步、私人状态隔离及退出后 BOT 接管。日志 `.runtime/v10-network-host.log` / `v10-network-client.log`。
- 最终 APK 覆盖安装成功；Android 13 模拟器连接最终 Windows EXE 房主，实际触摸加入房间、添加三个 BOT、开局、购买附魔链索、拖动施放获得雄斑虎、上阵并进入战斗。截图 `screenshots/v10-android-spell-buy.png`、`v10-android-spell-cast.png`、`v10-android-combat.png`。
- Windows 原生截图检查五色关键词、金色透明圣盾膜、法术独立商店位置与 13 张法术图鉴。输入回归覆盖目标法术拖给商店随从、无效松手保留手牌、己方满场仍可施法。
- APK ZIP 完整，含 13 张法术、6 张新增核心、公告和原画；未打包 tests、references、.runtime。v2/v3 签名验证通过并沿用原证书，versionCode 10。
- 发布后匿名完整下载 APK 与 EXE，大小及 SHA256 均与最终本地包一致。Android 实际点击检查更新，返回“当前已是最新版本：v0.10.0”。
- 测试房主与模拟器中的游戏已关闭。本轮未实测实体手机、两台实体设备 Wi-Fi 和公网延迟；模拟器互通不等同于实体机验收。350 项检查也不代表长期种族平衡已验证。部分 headless UI 退出仍有 ObjectDB 警告，Android 有缓存 shader 重编译提示；本次 Android 日志未发现 GDScript 错误或 AndroidRuntime 致命崩溃。

- ClassicTavern-v0.10.0.exe: 154994736 bytes; SHA256 `6a445ed5f768ec4452a012625041b02fd7b0995dfc13b1ec99f8b6a604bb800f`
- ClassicTavern-v0.10.0.apk: 134450659 bytes; SHA256 `b4246add9044268dd17a89d33232a5610f094f25dbe73847dd4727f142da98cb`

---

# v0.9.0 验证（2026-09-07）

- 14 个回归套件，306 项断言通过：五种关键词 71 项、联机/UI 新增 10 项，既有 225 项全部通过。
- 真实两个 Windows EXE 进程：连接、购买、上阵、准备、战斗回放、公开快照隐私与退出后 BOT 托管通过。日志 `.runtime/v9-network-host.log` / `client.log`。
- Windows EXE 作为房主进程，Android 13 模拟器运行最终 APK，通过 10.0.2.2:14281 连接。实际触摸操作填地址、加入、添加七个 BOT、调整霸主难度、开局、购买、上阵、结束回合。成功收到战斗和第二回合状态（58 生命、4/4 铸币），截图 v9-android-lobby / recruit / combat / next-round。
- 关闭 Windows 房主后，Android 返回主菜单并提示房主断开。测试房主已关闭，没有留下游戏服务器。
- Android APK 覆盖原安装成功，包名 org.classictavern.game、versionCode 9；APK ZIP 完整、资源与公告正确，未打包测试和旧浏览器参考目录；v2/v3 签名验证通过，证书与 v0.8.0 相同。
- 公开发布后，以无登录下载方式重新下载 EXE / APK，两者 SHA256 均与本地最终包一致；Android 实际点击检查更新返回 v0.9.0 已为最新。
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

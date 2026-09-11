# v0.32.0 验证记录

发布核验：GitHub latest=v0.32.0、非草稿，四个附件大小及SHA256匹配本地；APK/EXE/素材包链接均返回HTTP200。

6套专项检查65条通过，包括空间弧线起终点、离桌高度、减弱晃动、受击恢复、视觉不改状态、生命周期及2D回退；同时回归上一版立体交互、渲染健康、设置和攻击手感。原生Windows截图检查招募、拖动、满场、鹦鹉触发空间轨迹和设置框体。未重跑全部历史测试，也不做平衡模拟。

最终APK已覆盖安装到Android13/API33模拟器，检查主菜单、设置、战斗和3D像素验证，采集日志未见SCRIPT ERROR。最终EXE双进程联机烟测通过。APK签名沿用原证书，1071条目CRC通过。未验证实体手机、长时发热和声音听测。


证据目录：`validation/v0.32.0`。

---

# v0.31.0 验证记录（2026-09-11）

- 发布核验：GitHub latest=v0.31.0、非草稿；四个附件大小和服务端SHA256均匹配本地，APK/EXE/录像公开链接均返回HTTP200。最终APK的减弱晃动设置切换后离开再进入仍正确显示。

- 7套专项回归共76条断言通过；最终界面微调后重跑体验设置与立体交互专项。原生Windows立体交互14条通过，包含实际鼠标拖放、无效位置恢复和圣盾最后一层清理。
- 最终APK在Android13/API33、2280×1080横屏模拟器覆盖安装。检查插牌、换位、冻结、战斗、设置；渲染日志通过Android像素检查，最终采集日志未见脚本异常。检查操作录像与截图，随从正常显示。
- 最终EXE双进程联机通过注册、购买上阵、施法同步、回放、私有快照和断线BOT接管；真实图形客户端与2D房主互通。
- APK共1065条目CRC检查通过，签名校验通过，证书SHA256沿用5d15dbad38e4504fa3b1e7ad1aab3c91d0e65bc57f29e8d775866893a659b2cc。
- 未进行实体手机、长时温度/续航、声音听测或平衡模拟；专项通过不等于穷举全部历史卡牌组合。

证据目录：`validation/v0.31.0`。包大小与哈希见 [本版说明](v0.31.0-立体交互升级.md)。

---

# v0.30.1 验证记录（2026-09-11）

- 发布已完成：GitHub latest=v0.30.1，非草稿；三个附件大小及SHA256与本地一致，APK/EXE下载链接均返回HTTP200。模拟器点击检查更新返回“当前已是最新版本：v0.30.1”。

- 交付APK安装到Android13/API33 x86_64模拟器，versionCode31/versionName0.30.1；2280×1080横屏，GLES3.1/NVIDIA硬件图形转译。`v301-android.log`记录`PRESENTATION VERIFIED Android msaa=0`及后台恢复后重新通过。未见SCRIPT ERROR或运行异常，启动有一次旧shader缓存重新编译警告。
- 同一旧v0.30.0 APK在硬件模式也能显示；未完全复现用户实体机空白。SwiftShader软件模式有引擎uniform上限报错，已明确记录，不以硬件模式通过覆盖此限制。
- 实际APK截图和触控覆盖招募/买牌/手牌/出牌/长按详情/战斗灰化/后台恢复、随从与英雄与法术与暗月图鉴、滚动、流派、设置、公告、更新页、房间/BOT、大小饰品选择与返回战场。
- APK连接电脑本机测试房主，实际战吼赋毒、香蕉施法、购买staff_lesser与tip_jar两件饰品，主机最终阵容bronze/toxfin/tidecaller、手牌micro，与画面一致；这是本机模拟器路径，未验证双实体设备或公网。
- 9套专项功能/UI回归89条断言通过，原生Windows3D专项22条通过，原生渲染健康专项9条通过（故意关闭相机可见层制造实际空白，自动回退后仍可出牌）。未重跑全部历史套件或平衡模拟。
- 最终EXE通过两个独立进程的联机注册、买牌上阵、施法同步、战斗、私有快照隔离和断线BOT接管；客户端有真实OpenGL与像素检查通过记录。
- APK 1062条目CRC完整，无上传原图/Git/运行目录；v2/v3签名通过，证书与v0.30.0相同。大小/SHA256见本版说明和`v301-artifacts.json`。
- 界面清单与截图范围见 [本版说明](v0.30.1-安卓显示修复.md)。未做实体手机、温度/续航或声音听测，也未穷举所有卡牌/英雄/结算分支。

---

# v0.30.0 验证记录（2026-09-11）

- GitHub v0.30.0已从3d分支发布并设为latest；仓库默认分支确认为3d。APK、EXE和说明附件的大小与服务端SHA256均匹配本地，APK/EXE完整下载链接返回HTTP200。未做整包匿名回下载。
- 本地源码建立main基线247c385并切至3d；发行仓库3d已创建并通过GitHub接口确认为默认分支。两套Git历史独立，公开仓库仍只存发行资料。
- 59套功能/UI回归最终日志全部通过，共1125条断言。完整运行后重跑两处旧测试假设和3D专项：免费刷新测试固定普通英雄，避免随机诺兹多姆额外刷新；旧死亡残影测试明确使用2D兼容，3D有独立覆盖。见`validation/v0.30.0/v30-final-summary.log`。
- 新3D专项22条通过；同时在原生Windows窗口运行22条检查，通过真实鼠标拖动上阵、无效撤回、战吼预览/取消、UID对象复用、纹理缓存、投影坐标、抬起与落回、1血复生、退场释放及2D切换。修复透明拖放背景压暗3D卡牌及前景视图未共享实际World3D的问题。
- Windows Compatibility原生截图覆盖招募、七随从、十手牌、七商店位、拖起前景与鹦鹉进击。使用预置英雄、铸币、随从及高身材敌人的测试局面，截图不是正常开局或AI加成。
- 短时桌面静态负载采样：1280×800，24个卡牌对象，122帧，墙钟帧间隔中位数16.665ms、P95 16.681ms，约316次绘制调用。环境为RTX5060 Laptop/OpenGL。只采样约2秒，不等于安卓性能、长连锁或长时间温度结论。
- 专用双进程实测2D/headless房主与原生3D客户端：客户端真实3D对象显示，出售从10到11币、加里维克斯下轮支付一次并清零，双方蓄势时间和战斗数据一致。沿用v29经济夹具，日志中的V29前缀是测试名称，不是运行包版本。
- 最终EXE原生成品作为3D客户端，配合独立2D/headless房主通过注册、买牌/上阵、施法同步、战斗回放、隐藏信息隔离和断线BOT接管。日志包含OpenGL启动及3D=true；仅同机两个进程，未验证双实体设备或公网。
- APK导出完成：org.classictavern.game，versionCode30/versionName0.30.0，最低API24；v2/v3签名通过，原Debug证书SHA256 `5d15dbad38e4504fa3b1e7ad1aab3c91d0e65bc57f29e8d775866893a659b2cc`。1062条目CRC完整，包含3D场景/脚本，未打入Git、运行目录或上传原照。
- 本轮没有安卓模拟器或实体手机运行验证，不能将签名/ZIP检查视作触控、音效、发热和兼容性通过。提供2D兼容选项以便用户对照体验。
- 未进行平衡胜率模拟。保留既有三场AI功能场景；未改规则数值。部分既有headless退出仍有ObjectDB/资源清理警告，未出现SCRIPT ERROR，不声称已修复历史退出清理问题。
- 未更改系统网络、代理、防火墙、电源；没有关机、重启、断网操作或常驻服务。仅按用户要求更改仓库默认分支，测试游戏进程在结束后退出。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| ClassicTavern-v0.30.0.apk | 194598035 | `be6c567a1ae981be45c6e489bd5835c835835cc6440095226d08382b20d9faec` |
| ClassicTavern-v0.30.0.exe | 215861784 | `4bb5f37f20c764a27e37ad19982393c33e8cc787eb3f9cb68ff82f30743cf337` |

---

# v0.29.0 验证记录（2026-09-11）

- GitHub v0.29.0已公开并设为latest；APK、EXE和说明附件的大小及服务端SHA256全部匹配本地，APK/EXE完整下载链接均返回HTTP200。未进行整包匿名回下载。
- 依据issue #9/#10正文实施，发布前复查仍分别更新于2026-09-10 19:16:07 / 19:14:02 UTC，无新增评论。
- 58套功能/UI回归的最终日志全部通过，共1103条通过断言；完整运行后修正旧版预期，并重跑相关套件，汇总见`validation/v0.29.0/v29-final-summary.log`。新规则30条、UI11条，覆盖收益超额、永久额度、英雄返币、馅饼冻结重置、免费法术失败/重叠、复仇鱼人和进击顺序。
- Windows原生渲染检查按钮高光、冻结蓝态、英雄待领币、蜡烛次数、鹦鹉抬起与地面阴影、目标闪光及新鱼人详情。修复阶段横幅遮挡首个效果；最终截图见`validation/v0.29.0/`。截图含预置高身材/生命/铸币等测试局面，不代表正常起手或新增隐藏加成。
- 专用双进程真实RPC通过：客户端10币出售到11币，加里维克斯bank=1；双方蓄势帧时长0.24秒一致，下一轮补满10再发1，共11币，bank清零。测试为检查支付而由房主提前推进下一轮，不代表完整动画均已实看。
- 最终Windows EXE两个独立进程通过注册、买牌/上阵、施法、战斗、隐藏信息隔离、断线BOT接管，见`v29-exe-network.log`。这是同一台电脑两个进程的本地WebSocket验证，未测试两台实体设备或公网链路。
- 最终APK包名org.classictavern.game，versionCode29/versionName0.29.0，最低API24；v2/v3签名验证通过。沿用原Debug证书SHA256 `5d15dbad38e4504fa3b1e7ad1aab3c91d0e65bc57f29e8d775866893a659b2cc`。1054条目ZIP CRC通过，包含v29卡包，未打入.runtime和上传原照。
- 本轮未启动安卓模拟器，未验证ARM实体手机、触摸、扬声器或两台实体设备联机；APK签名和归档完整性不等于设备运行验证。
- 未进行平衡胜率模拟。既有AI功能测试仅保留标准/困难/霸主三个固定种子场景，检查回合终止及资源合法性，移除已取消的休闲与非叠层矩阵及过时的铸币上限断言。不能据此给出强度结论。
- 导出与游戏回归顺序运行，协议测试只启动必要的两个游戏进程；未修改系统网络、代理、防火墙、电源，未执行关机/重启，也未部署常驻服务。部分既有headless测试退出仍有ObjectDB清理警告，未出现SCRIPT ERROR，不声称解决历史退出警告。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| ClassicTavern-v0.29.0.apk | 194580884 | `eedee9627e4bf8de654b87b52a6d48b6277f7fe1b6af9dba705e2d45c9afe43a` |
| ClassicTavern-v0.29.0.exe | 215841688 | `9506465becb524ba189ab23a84610a8e813df382bae8fa48f1cfdb4ba80b9b4b` |

---

# v0.28.0 验证记录（2026-09-10）

- 按issue #8正文实施；发布前复查更新时间仍为2026-09-10 06:33:15 UTC，无新评论。
- 56套功能/UI回归最终日志全部通过，共1067条通过断言；见`validation/v0.28.0/v28-final-summary.log`及逐套日志。本次新增规则37条、UI9条。旧测试同步新增卡数、五选一和休闲映射标准的要求。修复无战場直接伤害访问空数组的初始化边界。
- 实际Windows渲染截图检查五列饰品、三档难度、卡牌详情和复仇x/N图标；发现并修复旧阶段提示残留遮住饰品的情况。最终截图见`validation/v0.28.0/`。
- 新机制真实双进程RPC通过：客户端购买第五选项，扣费正确，私有候选不发送给旁观对手；战斗后房主/客户端的四个原始随从攻击总和同为34（基础20），受伤永久成长正确同步。高血量、多盾对手为确定性测试夹具，并非正常牌池改动。
- 最终Windows EXE双进程注册、买牌/上阵、法术、战斗回放、隐藏信息隔离、断线BOT接管通过。只验证同机两个独立进程的本地WebSocket链路，未测试两台实体设备Wi-Fi或公网。
- 最终APK导出成功；包名org.classictavern.game，versionCode28/versionName0.28.0，最低API24。v2/v3签名验证通过，沿用原Debug证书SHA256 `5d15dbad38e4504fa3b1e7ad1aab3c91d0e65bc57f29e8d775866893a659b2cc`；ZIP全部1037条目CRC正常，未打入上传附件原照或.runtime目录。不能把签名/ZIP检查等同于设备运行验证。
- 本轮未启动安卓模拟器，未验证ARM实体手机、实际触摸音效或双实体设备联机；请以手机覆盖安装体验为准。先前v0.27的模拟器记录仅是历史记录，不代表本版已实测安卓。
- 没有进行新平衡胜率模拟；保留既有AI功能回归（固定种子检查经济/卡槽/对局终止），不据此下强度结论。全部构建和回归顺序运行，除协议验证必要的两个游戏进程外不额外并行游戏测试；未改系统网络、代理、防火墙、电源设置，未关机/重启，未部署常驻服务。
- 部分既有headless/网络测试退出有ObjectDB资源清理警告；未出现SCRIPT ERROR，不声称已解决这些历史退出警告。

- GitHub v0.28.0已公开并设为latest；三个附件大小与GitHub服务端SHA256全部匹配本地，APK/EXE下载链接均返回HTTP200。未做整包匿名回下载。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| ClassicTavern-v0.28.0.apk | 192912018 | `390634cd1d380db9db4dc6daadbd845a2e94d5901189620bd9eee0226dd5a70c` |
| ClassicTavern-v0.28.0.exe | 214171576 | `74939a3016c4a20fcec136c1589b1bbc5c6d34c6cd2dc10640927f6042772b21` |

---

# v0.27.0 验证记录（2026-09-10）

- 对照issue #6/#7正文与评论（本轮无评论），完成两项清单；发布前复查更新时间没有变化。
- 完整54套功能/UI回归1021条断言通过，失败0，见 `validation/v0.27.0/v27-all-final.log`。新增规则23条、UI8条。后续仅修正提示条覆盖、饰品画作回退和多字符进度徽章，相关3套UI再验证25条通过，见 `v27-ui-final.log`。未进行平衡胜率模拟，既有AI功能回归保留。
- 专用真实双进程RPC通过：客户端预览后确认战吼，房主与客户端站位index=1一致，烈毒目标正确；随后高级杂耍师复生/死亡及大饰品复仇产生的恶魔点数双方均为5，余数均为2。首版测试夹具被新赋予的烈毒提前杀死唯一敌人，修正夹具为多层圣盾后才用于完整死亡链验证，没有更改烈毒规则。
- 最终导出Windows EXE双进程注册、买牌、上阵、施法同步、战斗、隐私隔离、断线BOT接管通过，见 `v27-exe-network.log`。并非两台实体设备验证。
- 最终Android APK覆盖安装成功（Android13/API33 x86_64模拟器，27/0.27.0），真实触摸拖毒鳍到战場、点空处撤回、重新上场选裁脍、再上高级杂耍师并结束回合。房主记录毒鳍在index0、裁脍烈毒1，4秒结算后战斗，双饰品链最终恶魔点数8。测试夹具有意使用高身材/多盾敌人、预置手牌、饰品、金币和长招募计时；APK没有测试补丁。最终截图确认图标与0/5、0/3及战斗进度可读。
- 原始Android实操暴露了饰品画作目录不匹配及圆形角标裁切x/N，修复后重新导出、安装、实操验证。最终Android日志无SCRIPT ERROR或FATAL EXCEPTION。未验证ARM实体手机、扬声器或两台真实设备Wi-Fi。
- APK签名有效并沿用原Debug证书；ZIP1012条目完整，没有上传附件原图。测试房主与模拟器已关闭。部分既有headless用例退出仍有ObjectDB/资源清理警告，不声称已解决这些历史警告。

- GitHub v0.27.0已公开并设为latest，三个附件大小和服务端SHA256均匹配本地；APK/EXE完整下载链接HTTP200。未进行整包匿名回下载。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| ClassicTavern-v0.27.0.apk | 190677102 | `364a21d81ad5cd1c8b39cd44a08fd00cabf5cf1d6051cf6175aec2c3ed1abbb2` |
| ClassicTavern-v0.27.0.exe | 211934880 | `2ace5ec2780b3330afe3746469e45d38b81f914e42b25b1ef90fc5e6eafdf1e5` |

---

# v0.26.0 验证记录（2026-09-10）

- 最终52套功能/UI回归全部通过：990条断言，失败0。新增回合阶段与卡牌规则32条、界面8条；日志 `validation/v0.26.0/v26-all-final.log`。未进行平衡胜率模拟。
- 专用双客户端实测结算等待分别4.159秒与4.168秒，回合末效果只执行一次，之后发送战斗回放。最终Windows EXE双进程注册、上阵、施法同步、隐私隔离、断线BOT接管通过。
- Android13/API33 x86_64模拟器覆盖安装最终APK成功，版本26/0.26.0。通过真实触摸拖动魔血黏浆上阵、结束回合，实际显示结算03秒与禁用按钮，然后进入战斗。准备好的确定性对局用于复现：房主记录等待4.193秒、濒死鹦鹉进击1次、酒馆累计+6攻击/+2生命。测试布阵有意设置高生命和长招募时间；最终APK未修改。未验证ARM实体手机或两台实体设备Wi-Fi。
- 桌面回合末反馈截图确认同目标成长合并，来源轨迹保留。Android日志无SCRIPT ERROR/FATAL EXCEPTION。既有headless退出仍可能有ObjectDB/资源清理警告，不代表这些历史警告已修复。
- APK签名验证有效，与旧版Debug证书一致；ZIP共1005条目完整，未包含上传附件原图。测试模拟器和临时Android房主已关闭。

- GitHub v0.26.0已公开并设为latest，三个附件大小及服务端SHA256均匹配本地；APK/EXE下载链接HTTP200。没有进行整包匿名回下载。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| ClassicTavern-v0.26.0.apk | 190197191 | `716c873a20a622e8d570ee45f4e89412766d1c08244132b743b6539cafd95741` |
| ClassicTavern-v0.26.0.exe | 211448344 | `d2241a04150eedb5167fe09faa5147efb7376eeead0c0a71d2130f783182d359` |

---

# v0.25.0 验证记录（2026-09-10）

- `scripts/verify.py` 最终50套功能/UI回归通过，950条断言，失败0。日志 `.runtime/v25-all-final.log`；新增规则与UI分别在 `experience_v25_test` / `experience_ui_v25_test`。旧视觉用例更新为允许跳蛙存活载体，旧图鉴用例改为核对当前完整法术列表。
- Windows实际导出EXE双独立进程注册、买卖/上阵、购买施法、同步战斗、隐私隔离及断线BOT接管通过，`.runtime/v25-exe-network.log`。非两台实体设备验证。
- Android 13/API33 x86_64模拟器覆盖安装最终APK成功，版本25/0.25.0，沿用原包名与Debug签名。实际开启饰品、选择国王老汉、拖动购买甲板杂兵（3→0币）、拖动上阵、打开已装备饰品/状态页；截图 `screenshots/v25-android-*.png`。未验证ARM实体机触摸、扬声器或两台真实设备Wi-Fi。
- 桌面渲染截图验证新原画、附加跳蛙详情、效果摘要及12条转盘历史。Android日志无SCRIPT ERROR/FATAL EXCEPTION，导出和截图无脚本错误。部分既有headless用例退出仍有ObjectDB/资源清理警告，不代表已修复这些历史警告。
- APK签名有效，与旧版证书一致；ZIP998条目完整，无上传附件原图。未进行平衡胜率模拟，保留既有AI功能回归。
- GitHub v0.25.0已公开并设为latest，三个附件的大小/服务端SHA256均匹配本地；APK/EXE完整下载链接HTTP200。没有进行整包匿名回下载。测试模拟器及临时进程已关闭。
- 本轮确认并修复的是“活着的跳蛙载体被错误排除接收目标”；纯附加亡语本来就可被其他鹦鹉触发，新增针对性回归确认。未声称复现所有用户观察到的漏触发局面。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| ClassicTavern-v0.25.0.apk | 189455108 | `f9f6913417c8b4ee66a34d7fc48aad96e4c0379dcc40213d351bd14ff8757202` |
| ClassicTavern-v0.25.0.exe | 210704856 | `dc21302b4b5f9c8c61e45d350d3326d740bd1ad25c65fc1b15bd0d11845a7ff2` |

---

# v0.24.0 验证（2026-09-10）

- 按issue #5五项逐一实现；最终完整回归48组、916项断言通过，`.runtime/v24-all-final.log`。新增规则26项、界面16项；全部最新套件日志无SCRIPT ERROR/失败断言。包含既有40局有限BOT功能对局，未进行胜率/平衡分析。
- 实际输入事件验证9张手牌上方购买、酒馆随从/法术上方出售、满手拒绝、过期拖动UID拒绝、重复快照保留卡牌节点。首个测试夹具错误使用9张相同合唱鱼人，购买触发三连导致手牌不为10；改用9种不同牌后，实际拖动断言通过。
- 金色购买、上阵、首次回手点金、已领奖再次回手、偷取金色、金色磁力及B-Box、六星奖励上限、满手拒绝均通过；三连实体副本归属不变。
- 轮盘新增有序step验证，自动停留1秒、返回后展示、手动历史不自动关闭、重复同步不重复奖励。可扩展单奖项100%圆盘在实际渲染中暴露退化多边形问题，已改为整圆绘制，最终桌面捕获无该错误。
- 内部战斗可记录双方手牌，发送前按席位消除对方手牌；只发送自己按变化索引的手牌状态与敌方数量。旧Choral测试同步调整到验证真正发送的私密投影，不再禁止规则端内部存储。低音提琴召唤标记、观察席位投影及未改变原始回放验证通过。
- 专用双独立进程 `tests/issue_network_v24.gd` 实际RPC验证：10→7币购买金色，上阵获得5星三连奖励；敌方未上场手牌的哨兵UID没有出现在客户端回放中，自己手牌与对手公开饰品同步。
- 导出Windows EXE双进程：注册、买/上阵/准备、购买施放法术、战斗、隐私及断线BOT接管通过；`.runtime/v24-exe-network.log`。部分headless退出有既有ObjectDB/资源清理警告，无脚本运行错误；未宣称这些退出清理警告已修复。
- Android最终APK覆盖安装成功：org.classictavern.game，versionCode=24/versionName=0.24.0。Android 13/API33 x86_64模拟器使用host GPU，经10.0.2.2:14333连接Windows验证房主。实际触屏完成9手牌卡面买金色（20→17币）、卡面出售（17→18币）、上阵发奖、轮盘停留自动返回、奖品施放及双方战斗HUD/饰品详情。`.runtime/v24-android-host.log`、`screenshots/v24-android-*.png`。
- 安卓夹具为可复现而设固定手牌/金色商店、较高铸币与生命、300秒计时，并将测试转盘确定为命运之手和压袋零钱；正式包保留六种概率及原计时，完整效果由规则测试覆盖。实际APK客户端代码未修改。不是ARM实体机或双实体设备网络验证。
- Android本次日志无SCRIPT ERROR/FATAL EXCEPTION；Windows/Android导出与最终导入无ERROR。APK ZIP 980条目完整，无原始附件；签名有效，沿用Android Debug证书SHA256 `5d15dbad38e4504fa3b1e7ad1aab3c91d0e65bc57f29e8d775866893a659b2cc`。
- 固定场景30次headless界面构建：旧版中位7.791ms/P95 8.142ms；最终版本中位2.505ms/P95 2.982ms。仅为UI重建开销，不是GPU耗时或跨设备FPS保证。最终测试仍在同机模拟器开启时执行，负载会影响绝对值。原始日志 `.runtime/v24-perf-before.log` / `v24-perf-final.log`。
- 临时房主和安卓模拟器已关闭。未验证实体ARM触摸/扬声器、两台实体设备跨Wi-Fi、复杂亡语链极端性能；没有常驻公网服务。
- GitHub v0.24.0已公开并设为latest；APK/EXE/指南三附件大小与SHA256 digest逐项匹配本地，两个安装包下载链接HTTP 200。未做整包匿名回下载复核。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| ClassicTavern-v0.24.0.apk | 187179805 | 20802d2988d52ad75aad685e28e61fe5c68c2c4c3bed249a3d513cfc4f34ec94 |
| ClassicTavern-v0.24.0.exe | 208428936 | a37caa648bbee1686350882b18c12636d3104a91392adaf05a7f74900534df63 |

---

# v0.23.0 验证（2026-09-10）

- 46组功能套件的最终日志合计874项断言通过，无SCRIPT ERROR或失败断言。完整扫测873项通过，随后修正诺米恶魔加成应在战吼后触发，增加1项时序断言，重跑暗月规则、暗月UI、饰品规则和旧界面四组共122项通过。包含既有有限BOT功能对局，未进行胜率/平衡模拟。
- 本版新增暗月规则63项、界面10项断言，覆盖六项转盘、概率和数据校验、奖品分级、满手、金色与副本归属、发现队列隔离、磁力、商店永久成长、资源随从、阵容推荐、目标和重复操作。
- 源码双独立进程通过饰品权威扣费、奖品同步、客人不能修改模式、拒绝重复购买及伪造转盘结果、回合开始仅转一次、私密记录。日志 `.runtime/v23-network-host.log` / `v23-network-client.log`。
- 最终Windows EXE双进程通过注册、购买、上阵、准备、法术购买/施放、战斗同步、私密快照和断线BOT接管。日志 `.runtime/v23-exe-network-summary.log`。部分headless退出仍有ObjectDB/资源清理警告，无脚本运行错误；没有据此宣称清理警告已解决。
- 最终APK在Android 13/API33 x86_64模拟器（host GPU）安装启动，实际点击连接Windows验证房主、购买尤格饰品、观看轮盘、返回战场、使用压袋零钱、查看暗月图鉴。房主确认5币扣费（8→3），获得两张奖品，施放一张后手牌为另一张奖品及两张可用酒馆币。截图 `screenshots/v23-android-*.png`，主机日志 `.runtime/v23-android-host.log`。
- 安卓联机用10.0.2.2:14333同机测试路径；为确定验证结果，专用房主在完整图鉴同步后把本局转盘限制为命运之手、奖品限制为压袋零钱，时间延长至300秒。正式包保留六项19/19/19/19/19/5概率；全部效果另由规则测试覆盖。此验证不等于实体设备跨Wi-Fi联机或随机命中所有转盘效果。
- Android本次日志无SCRIPT ERROR/FATAL EXCEPTION。尚未验证ARM实体手机触摸、实体扬声器、双实体设备联机或长期对局性能。临时验证房主与模拟器已关闭，没有常驻公网服务。
- Windows/Android导出无ERROR。APK ZIP全部976条目完整，未包含原始附件；签名有效，沿用Android Debug证书SHA256 `5d15dbad38e4504fa3b1e7ad1aab3c91d0e65bc57f29e8d775866893a659b2cc`，versionCode=23/versionName=0.23.0。61条素材下载记录完成，来源与哈希留存。
- 桌面检查阵容推荐、转盘结果、装备图标与图鉴，修正技能/饰品图标与铸币区域重叠；APK实拍确认暗月紫色边框和等级标签。
- GitHub上传的APK、EXE及指南附件大小与SHA256 digest匹配本地；未做整包匿名回下载复核。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| ClassicTavern-v0.23.0.apk | 187163103 | 639fc4fb5b80daae38897c7da0d17656fb7a4f6d3f69a2b48655fa32fac587c8 |
| ClassicTavern-v0.23.0.exe | 208412872 | 562b22cfe275651b665fba3758e71b30b788ccbb6f3e7256f1fe49bdeee92178 |

---

# v0.22.0 验证（2026-09-10）

- 完整规则/UI回归：44组、793项断言通过；仅功能验证，没有运行平衡模拟。测试入口 `python scripts/verify.py`，本轮日志 `.runtime/v22-*.log`。
- 新增41项规则断言和10项界面断言：模式开关与锁定、四个唯一候选、种族倾向、私密快照、价格与重复购买校验、跳过与超时、磁力非递归复制、次数/产币/成长三连保留、永久商店与手牌收益、保留增益不恢复消耗、饰品召唤/复仇/赠牌等。
- 原卡素材与饰品图片：31条新增/更新素材记录下载成功，记录URL与SHA256。桌面捕获主菜单、大小饰品、已装备栏和图鉴；图片尺寸与英雄栏遮挡问题已修复。
- 两个独立Godot进程：`tests/trinkets_network_v22.gd` 验证客人不能切换模式、候选不泄露、6/9回合购买与扣费同步。
- 导出的Windows EXE：两个独立进程完成注册、购买/上阵/准备、法术购买施放、战斗同步、断线机器人托管。退出测试进程时有一条ObjectDB资源清理警告，无SCRIPT ERROR；此项不等于真人远端验证。
- 导出的APK：安装成功，包名org.classictavern.game，versionCode=22，versionName=0.22.0；安卓API33 x86_64模拟器采用host GPU实际启动，单机打开饰品模式并进入七机器人对局。
- APK模拟器通过10.0.2.2连接Windows上的Godot验证房主，触屏购买小/大饰品，主机确认扣费及两件饰品；民谣歌手肖像赠牌出现在安卓手中。截图保存在screenshots/v22-android-*.png，主机日志.runtime/v22-android-host.log。
- 验证房间为方便截图将时间固定180秒；生产时钟另以规则断言核验6回合100秒、9回合115秒、后期120秒，安卓单机首回合实际显示60秒。
- 首次使用模拟器SwiftShader软件GPU时遇到Godot GLES统一变量上限错误；改用host GPU后启动、UI和操作正常，后续Android日志无SCRIPT ERROR/FATAL EXCEPTION。尚未验证此软件GPU配置、ARM实体手机或两台实体设备跨Wi-Fi联机。
- 没有运行常驻公网服务、没有新增暂停。临时验证房主与模拟器在检查后关闭。

安装包SHA256：

- `ClassicTavern-v0.22.0.apk`：`199171c9502034f7db12890652f6244493857549f8101ff6ed8d9600a8fbc02b`（171718680 bytes）
- `ClassicTavern-v0.22.0.exe`：`59bd1c18dce1f6e29e586ce958a24d096f5d5cd3d0e302237383b9f64548b8bf`（192974688 bytes）

---

# v0.21.0 验证（2026-09-09）

- 42个功能套件、743项断言通过。首次回归的旧数量/层数/翻页断言已按issue改动更新，失败套件重新运行通过；按最新每套日志汇总至 `.runtime/v21-final-result.txt`。未运行平衡模拟。
- 本版新增规则26项、UI10项、战斗审计14项：购买计数、金色与铜须发现、满手、七格法术陈列、相邻与同时死亡、战斗收益跨阶段、临时属性隔离、盾毒与连续复生、受伤召唤时序。
- 原生触摸模拟测试实际拖动第四张展开法术购买；截图 `screenshots/v21-spell-row-large-stats.png`、`v21-counter-pulse.png`、`v21-exact-stats.png`、`v21-rylak-detail.png` 检查五张法术、十亿级攻血与大量圣盾、计数浮字、卡牌详情。
- 最终Windows EXE两独立进程通过建房、加入、购买、法术同步、战斗、私有快照和断线BOT接管：`.runtime/v21-network-summary.log`。没有部署公网服务器。
- Android 13模拟器覆盖安装成功，versionCode 21 / versionName 0.21.0；实际触摸进入英雄选择、开局、右侧法术拖入手牌、音乐停用设置及检查更新，更新页确认当前最新v0.21.0。截图 `screenshots/v21-android-*.png`，日志 `.runtime/v21-android.log` 无SCRIPT ERROR/FATAL EXCEPTION。
- Godot导入、Windows与Android导出无ERROR。APK ZIP完整校验通过，含新增8张原图、3随从、26法术与v0.21公告，不含原始附件，也不含上一版两首通用音乐的导入音频。41类音效加载通过。
- APK签名有效，沿用Android Debug证书 SHA256 `5d15dbad38e4504fa3b1e7ad1aab3c91d0e65bc57f29e8d775866893a659b2cc`。
- GitHub发布附件大小与SHA256 digest逐项匹配本地；未做整包匿名回下载复核。
- 未验证：实体安卓触摸与扬声器、两台实体设备跨平台LAN、真人平衡、极端亡语链性能。用户未指明的旧卡漏触发仍需具体阵容和复现步骤。初次安卓启动有缓存着色器重编译提示；部分headless退出仍有历史资源清理警告。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| ClassicTavern-v0.21.0.apk | 163563575 | 356e62ea8e738be77124a865b8f6f8173f8d9eeb5580b821ed7db76d8bbbe9af |
| ClassicTavern-v0.21.0.exe | 184834944 | 7d91c761bfef9541f16c064cff9a64900b1241b3f2e4dfa5e226d104c11b5c94 |

---

# v0.20.0 验证（2026-09-09）

- 39 个功能套件、688 项断言通过，汇总 `.runtime/v20-final-result.txt`。按用户要求未运行平衡模拟。
- 新增规则测试16项、UI测试8项，覆盖随机四选一、备选隐私、三位新英雄、固定配对、幽灵对手、阵亡观战权限、目标淘汰切换和独立音乐设置。
- 实际主程序双进程观战检查通过：死亡客户端切换视角、目标死亡自动切换，房主拒绝死亡玩家购买。日志 `.runtime/v20-spectator-summary.log`。
- 最终 EXE 双独立进程通过建房、加入、购买、法术同步、战斗、私有快照及断线BOT接管，日志 `.runtime/v20-network-summary.log`。没有部署公网服务器。
- 原生截图检查英雄选择、卡牌光影、下一对手、观战与音乐设置。Android 13 模拟器覆盖安装成功，实际触摸选择塔隆并进入招募，截图 `screenshots/v20-android-recruit.png`。安装版本 versionCode 20 / versionName 0.20.0。
- Godot 导入、Windows和Android导出无 ERROR；APK ZIP校验及签名验证通过，沿用旧版证书。包内两首MP3对应的导入音频资源完整；41类音效资源检查通过。
- 安卓实际点击检查更新，返回当前已是最新 v0.20.0，截图 `screenshots/v20-android-update.png`；本轮Android日志无 SCRIPT ERROR / FATAL EXCEPTION。
- 使用原版炉石公开原声 Pull up a Chair 与 Tabletop Battles，非战棋专属配乐。音乐独立音量与场景切换通过功能检查。
- GitHub发布附件大小和SHA256与本地一致，未完成整包匿名回下载复核。
- 未验证：实体安卓触控与扬声器、两台实体设备LAN、真人平衡、复杂亡语极端性能。部分headless退出保留历史资源清理警告。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| ClassicTavern-v0.20.0.apk | 173822787 | 0512b113d3bb479a5039ccdeb289e37985a9252a40eb41655f1982137f4550eb |
| ClassicTavern-v0.20.0.exe | 196081608 | b8dcd8b71661832a50046208dc5d86950677ce0677bc7b56f2451cf8acc21101 |

---

# v0.19.0 验证（2026-09-08）

- 37 个功能套件、664 项断言通过；按用户要求未运行平衡模拟。日志为 `.runtime/v19-套件名.log`，最终汇总 `.runtime/v19-final-result.txt`。
- 新规则测试21项、新UI测试4项：三连合成不立即发现；打出/磁力给法术；零费奖励、固定星级、非酒馆法术计数、满手、重复战吼不重复奖励；诈骗犯普通/金色/多张/跨回合/三连；两原创与铜须/达卡莱；鹦鹉目标及轨迹。
- 原生可视截图检查：金色无盾与金色有盾的区别、骷髅图标、奖励法术详情、6张原创美术重绘以及2张新原创画作。截图 `screenshots/v19-gold-shield-reward.png`、`v19-triple-reward.png`、`v19-original-art.png`。金色标识已移动到星级栏，避免遮挡经济进度。
- 38类音效资源加载与有效时长通过。音效为本地合成；实体手机扬声器听感尚未验证。
- 最终 EXE 双独立进程通过建房、加入、购买、法术同步、战斗、私有快照及断线BOT接管：`.runtime/v19-network-summary.log`。新奖励拖动和发现用原生UI测试验证；没有声称双实体设备已测。
- Android 13 模拟器覆盖安装成功，打开主菜单、图鉴与更新页；本轮日志无 SCRIPT ERROR/FATAL EXCEPTION。APK沿用原包名和签名证书，versionCode 19 / versionName 0.19.0。
- Godot 导入和两个导出无 ERROR；APK ZIP 完整校验通过，含新增3张卡、原创图集及v0.19公告，附件照片不入包。
- GitHub发布附件返回的大小和SHA256与本地一致。未做整包匿名回下载复核。
- 未验证：实体安卓触控/扬声器、两台实体设备LAN、真人平衡及复杂亡语极端性能。部分headless场景退出仍有历史资源清理警告。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| ClassicTavern-v0.19.0.apk | 160734195 | 0c78b11e43556661eca06d5a5e22e2bb3eee01866aef6893a36c94acc9bc823b |
| ClassicTavern-v0.19.0.exe | 181999824 | 440c629d1d73f9e86b80b17dd8362d8489b668615716e8d29cbdac05aa6ff37e |

---

# v0.18.0 验证（2026-09-08）

- 按用户要求不进行平衡模拟。未运行批量完整对局、胜率统计或旧新平衡对照；v0.17 报告不适用于本版。
- 35 个功能套件共 639 项断言通过，日志 `.runtime/v18-*-test.log`（实际每套件文件名为 v18-套件名.log）。本版新增经济规则 54 项、经济 UI 9 项。旧测试的卡池数量、铜须/达卡莱触发次数及死神基础攻击预期按 issue 更新。
- 覆盖多法术展示、按索引购买、冻结保留、无效操作不扣费；产币/磁力/三连；伤害刷新次数/免费优先/回溯；蓝壳售价；侦查员成长、出售发现和金色；队伍上限隔离；姆诺兹多复制、共享库存与磁力材料归还。
- 原生界面截图检查法术翻页、刷新次数、产币标签、铸币上限、侦查员详情和退役图鉴：`screenshots/v18-*.png`。
- 最终 Windows EXE 两个独立进程通过建房加入、购买、法术同步、战斗、私有快照和断线 BOT 接管，日志 `.runtime/v18-network-summary.log`。没有部署公网服务器。
- Android 13 模拟器覆盖安装成功，versionName 0.18.0 / versionCode 18。实际触摸打开图鉴、切换分类和检查更新；主菜单显示当前已是最新 v0.18.0。该轮日志无 SCRIPT ERROR 或 FATAL EXCEPTION。
- APK 签名通过，沿用 Android Debug 证书 SHA256 `5d15dbad38e4504fa3b1e7ad1aab3c91d0e65bc57f29e8d775866893a659b2cc`。APK ZIP 校验通过，含新增经济卡 JSON，原始照片附件不入包。Godot 导入与两个导出日志无 ERROR。
- 发布地址：https://github.com/bjckbjckbjck-ai/classic-tavern-builds/releases/tag/v0.18.0 。GitHub 返回的两个附件大小和 SHA256 digest 与本地产物一致，应用更新接口可识别。匿名链接已开始返回文件内容，但当前网络较慢，未完成整包匿名回下载复核。
- 未验证：实体安卓触摸与扬声器、两台实体设备跨平台 LAN、真人运营平衡。本版没有新增双打界面，仅预留显式队伍字段；普通对抗不会给对手增加上限。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| ClassicTavern-v0.18.0.exe | 178903416 | cc68fc4725fa0256407fa398ba5d8b4d677193d6aba72ebdd38e92fdb80d1d8c |
| ClassicTavern-v0.18.0.apk | 157639711 | 5917e89addce544662a00fd8527aabe4e33bdd001eeb21d4be71e5d6ff063b00 |

---

# v0.17.0 验证（2026-09-08）

- 34 个回归套件、588 项断言通过，汇总 `.runtime/v17-final-tests.log`。新套件分别覆盖亡灵规则 33 项、AI 买卖规划 10 项和亡灵 UI 8 项；旧套件继续通过。最终黏冻卡牌说明文字明确招募增益会保留。
- 亡灵测试包含玩家全局增益隔离、商店/手牌/发现同步、三连不重复光环、多次复生逐层消耗与 1 血、骑士真正死亡计数、永久收益回写、重复亡语、已有复生继续叠层、招募宰割原子校验、无出售收益、生成骑士不增池、满场阻止复生时回收实体副本、金色屠夫满手边界，以及巫妖王到期和塔隆等待空位。
- 200 局固定种子、四档各 50 局正常结束；每轮经济/容量/护甲与共享实体副本检查无异常，平均 17.09 回合。1600 席位共施放 133 次宰割。详见 [对局验证](v0.17.0对局验证.md) 和 [原始数据](validation/v0.17.0-bot-games.json)。不代表长期平衡或完整旧新 AI 胜率提升。
- 原生截图检查亡灵图鉴、详情、宰割结果、全局计数、复生青色环及英雄标记。调整了全局计数与战场标题的遮挡，以及英雄标记与复仇进度重叠。截图 `screenshots/v17-undead-*.png`、`v17-butchering.png`。
- 最终 Windows EXE 双独立进程通过建房、加入、购买/使用、法术同步、战斗、私有快照及断线 BOT 接管，日志 `.runtime/v17-network-*.log`。没有部署公网游戏服务器。
- Android 13 模拟器成功覆盖 v0.16，版本 0.17.0 / code 17。实际触摸选择巫妖王、购买海盗无赖、拖动上牌、拖动英雄技能，目标出现“下场复生 +1”和本回合已用；随后进入战斗。实际切换图鉴亡灵筛选，所有新卡图正常载入。截图 `screenshots/v17-android-*.png`，该轮日志无 SCRIPT ERROR/FATAL EXCEPTION；首次启动有缓存着色器重新编译警告。
- Android 主菜单手动检查更新返回最新 v0.17.0。APK 签名验证通过，沿用证书 SHA256：5d15dbad38e4504fa3b1e7ad1aab3c91d0e65bc57f29e8d775866893a659b2cc，仍为 Android Debug 签名体验包。
- APK ZIP 与资源检查通过：146 个定义（124 在池、17 衍生物、5 退役）、17 英雄、21 法术、32 音效、新亡灵画作和公告齐全；原始照片附件、测试、运行日志不入包。
- 最终 APK / EXE 公开链接均已完整匿名下载，大小与 SHA256 匹配本地产物。
- 未验证：实体安卓触摸/扬声器、两台实体设备跨平台 LAN、长期真人平衡及极端连锁实机帧率。宰割招募动画目前为结果与来源反馈，尚非逐帧死亡/复生队列；附魔说明仅近期记录，尚未覆盖所有来源。部分历史 headless / 网络测试有退出资源清理警告。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| ClassicTavern-v0.17.0.exe | 176954064 | 65e3c7fe8fe0c349dd05c3fe531b655ca55b065f6fddbb360d4bc309f0faaafc |
| ClassicTavern-v0.17.0.apk | 155696302 | 5a9f251b17d19f9a0532ac322d55034bb638e297998865bf2382154fb445f864 |

---

# v0.16.0 验证（2026-09-08）

- 31 个套件、536 项断言通过，日志 `.runtime/v16-*_test.log`。最终手牌提示和复制状态排版修改后，重跑相关 UI 与公告体验测试通过。
- 新规则测试覆盖真实出售来源位置、手牌目标、私有事件隔离、序号与有界记录，以及裁脍/保育员/低音提琴/合唱留牌、低生命释放、发现奖励、满币保留酒馆币、免费刷新、空池和满手边界。
- UI 测试验证重复快照不重复播放、重绘不销毁轨迹、不拦截拖拽、动画清理、音量滑杆、诊断样本及零音量不启动新声源。原生截图为 `screenshots/v16-sale-trace.png`、`v16-hand-trace.png`、`v16-settings.png`；把来源文字从卡牌数值处移到空隙。
- 200 局固定种子、四档难度各 50 局全部正常结束；每轮铸币/手牌/战场/护甲检查无越界。平均 17.39 回合，详见《v0.16.0 对局验证》及原始 JSON。这是新版本运行验证，不是旧新 AI 胜率对照。
- 最终 Windows EXE 双独立进程通过建房、加入、购买/使用、法术同步、战斗、私有快照与断线 BOT 接管。日志 `.runtime/v16-network-host.log` / `client.log`。
- Android 13 模拟器成功覆盖 v0.15，版本 0.16.0 / code 16；滑杆调到 50%，强制关闭后重新启动仍为 50%。最终安装包检查复制状态完整可见，系统剪贴板预览出现诊断文本；进入单机对局后直接复制诊断成功。测试后恢复 100% 音量。截图 `screenshots/v16-android-*.png`，该轮日志无 SCRIPT ERROR/FATAL EXCEPTION。
- 主菜单在线检查更新返回最新 v0.16.0。APK 签名验证通过，沿用证书 SHA256：5d15dbad38e4504fa3b1e7ad1aab3c91d0e65bc57f29e8d775866893a659b2cc，仍为 Android Debug 签名体验包。
- APK ZIP、126 个定义、106 在池、15 衍生物、15 英雄、20 法术、32 音效、六张原创 PNG 与公告资源完整；原始照片附件、测试及运行日志不入包。
- 最终 APK 和 EXE 公开地址均完整匿名下载，大小及 SHA256 与本地产物相同。
- 未验证：实体安卓触摸与扬声器、两台实体设备跨平台 LAN、长期真人平衡与极端连锁实机帧率；部分历史 headless 套件仍有退出资源清理警告。诊断展示最近最多 600 帧的间隔，包含逻辑/渲染等待与可能的菜单帧，不是 GPU 耗时或完整局平均。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| ClassicTavern-v0.16.0.exe | 170814248 | 8ac4835f39d7c654d38bf39b210e564b0c2fe772c08c77d94242216903843c9d |
| ClassicTavern-v0.16.0.apk | 150062829 | ec76c5d91b0920f9b06d68ab310ccf822f039ed008986ca326e77705904f6d77 |

---

# v0.15.0 验证（2026-09-08）

- 28 个套件、505 项断言通过，日志 `.runtime/v15-*_test.log`。最后的原创画作取景与金色按钮样式调整后重跑原创 UI 和公告体验测试。
- 新测试覆盖六张原创来源、施法计数、跨回合重置、观星者金色与达卡莱、满手产币、手牌鱼人增益、晶簇金色/空目标/跨回合/非出售不触发、分赃手最左目标、鸽子实际伤害与圣盾阻挡。固定种子含原创单位的八 BOT 对局完整结束。
- UI 测试验证产币条件标签、原创来源文字、金色基础卡属性、预览不修改真实场面，以及旧 PNG 原画实际载入。
- Windows 原生截图检查：`screenshots/v15-originals-recruit.png`、`v15-originals-detail.png`、`v15-gold-preview.png`、`v15-dragon-gallery.png`。调整原创画作使用完整画幅，避免过度裁掉高贵鸽子的头冠；金色预览按钮使用统一酒馆金棕样式。
- 最终 EXE 双进程测试通过：建房、加入、购买/使用、法术同步、战斗、私有快照和断线 BOT 接管。日志 `.runtime/v15-network-host.log` / `client.log`。
- Android 13 模拟器成功覆盖 v0.14，versionCode 15、versionName 0.15.0；实际触摸图鉴种族筛选、滚动至原创龙、打开晶簇详情并切换金色基础卡。在线更新返回当前最新 v0.15.0。截图 `screenshots/v15-android-*.png`，该轮 Android 日志未发现 SCRIPT ERROR/FATAL EXCEPTION。
- APK 沿用原签名，apksigner 验证通过，证书 SHA256 为 5d15dbad38e4504fa3b1e7ad1aab3c91d0e65bc57f29e8d775866893a659b2cc。依旧是 Android Debug 签名体验包。
- 包检查：ZIP 完整、126 个定义、106 在池、15 衍生物、15 英雄、20 法术、32 音效、六张原创 PNG 与公告资源齐全；不含 tests/.runtime/原始照片附件。首次包统计脚本漏算四张未显式写 pool 的中立卡，已按 Catalog 默认 12 副本修正统计和文档，游戏规则无需修改。
- APK 和 EXE 公开链接均完整匿名下载，SHA256 与本地最终产物一致。
- 未验证：实体安卓触摸/扬声器、两台实体设备跨平台 LAN、大样本胜率平衡和极端连锁实机帧率。部分历史 headless 测试仍有退出资源清理警告；没有 SCRIPT ERROR。AI 本轮增加新效果价值及流派识别，完整手牌规划仍在下一步建议中。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| ClassicTavern-v0.15.0.exe | 170801136 | 9850e180fd149477e984dfe7593d84326d8dd651fc1aba6c38eb28c88acc6116 |
| ClassicTavern-v0.15.0.apk | 150049881 | c6040b047afaaecce909f64322e2878d9a56baf64baeea77cc2e49d94aa1fd44 |

---

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

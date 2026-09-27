# v0.61.1 / service8：对局阅读、快捷买卖与拖拽跟手

2026-09-27。对应新 issue [#34](https://github.com/bjckbjckbjck-ai/classic-tavern-builds/issues/34)、[#35](https://github.com/bjckbjckbjck-ai/classic-tavern-builds/issues/35)、[#36](https://github.com/bjckbjckbjck-ai/classic-tavern-builds/issues/36)。旧 #18 全面 UI 审计与 #31 登场动画仍单独维护。

游戏源码：[classic-tavern-game/main，1d36dad](https://github.com/bjckbjckbjck-ai/classic-tavern-game/commit/1d36dadcf6990b304f041cb234748f0a6a101601)（私有，需要仓库权限）。后端继续在 service-platform 维护；生成的适配快照及源码锁已同步。公开发行仓的 main/3d 不代表完整游戏源码。

## #34 对局简要说明，图鉴保留完整规则

- 对局卡面和悬停详情省略诗心龙“含嘲讽及叠层”“含跳蛙”等举例括注，保留实际作用对象、亡语、关键词、数值及限制。
- 对局详情突出当前属性、关键词层数和附加亡语；完整说明仍可通过“图鉴完整说明”按钮查看，再切回简要说明。图鉴默认完整显示，金色切换保持说明模式。
- 响尾蛇等具有关键限制的卡牌原有效果文字保持不变；没有批量重写规则或删掉数值。
- 仅展示层变化，不改卡牌数据、服务端规则或战斗计算。

原生 Windows 游戏截图：[对局简要说明](../validation/client8/issue34-concise.png)、[点击按钮后的完整说明](../validation/client8/issue34-full.png)。

## #35 右键买卖与手牌出售

- 设置 → 操作 → 右键快捷买卖，默认关闭并保存选择；启用后电脑端右键商店卡购买，右键自己的场上/手牌随从出售。
- 手牌随从也可以选中后点“出售随从”，或拖向鲍勃/出售区域；手机继续使用触摸入口。
- 直接出售不先上场，不触发战吼，也不领取金色随从的上场三连奖励。金币、卡池归还及出售触发沿用正常出售规则。
- 法术不能出售；准备后、非招募阶段、奖励待选择、观战等状态保持操作限制。动作携带卡牌 UID 与操作序号，过期操作不会误卖另一张卡。

## #36 跟手问题与定量验证

原实现给手持卡牌的位置也加了逐帧指数插值，因此鼠标已经移动时，牌的位置仍在缓慢追赶。现在手持期间直接使用本帧目标位置；空闲排列、落地平滑以及倾斜惯性继续保留。共用 3D 卡牌演员覆盖商店、手牌和战场拖拽。

调研参考：

- [Godot 官方论坛：拖拽卡牌的 clamp 与 lerp](https://forum.godotengine.org/t/combining-clamp-and-lerp-for-draggable-object/98141)。开发者使用插值制造拖动延迟；这一机制与本项目的位置滞后相符。
- [Godot 官方论坛：快速拖动时物体落后鼠标](https://forum.godotengine.org/t/how-can-we-avoid-the-problem-that-the-position-of-the-dragged-object-lags-behind-the-mouse-position-when-dragging-quickly/84022)。软件渲染物体与硬件光标仍可能存在不同显示时序，不能据此承诺端到端零延迟。
- [Godot 4.6 Input 文档](https://docs.godotengine.org/en/4.6/classes/class_input.html#class-input-property-use-accumulated-input)。关闭输入合并有响应性与 CPU 成本取舍；本次没有改这个全局设置，先消除已定位的位置插值延迟。

使用真实 main.tscn 招募场景，Windows / Godot 4.6.1，8 席、7 个场上随从、10 张手牌、1440×900 逻辑画布。通过 Godot 输入事件按 600 逻辑像素/秒往返移动，预热 30 帧，采集 120 帧。对照为 fd2fd0b 的原位置插值，修复版本为 1d36dad。度量渲染后卡牌投影位置与同帧指针目标位置的距离，扣除双方共有的举牌偏移。

| 帧率设置 | 平均额外偏移：修复前 → 后 | P95 额外偏移：前 → 后 | 平均帧时间：前 → 后 |
| --- | --- | --- | --- |
| 30 | 13.76 → 0.00 px | 14.78 → 0.00 px | 33.32 → 33.32 ms |
| 60 | 17.47 → 0.00 px | 18.73 → 0.00 px | 16.66 → 16.66 ms |
| 120 上限，实际约 61 | 17.50 → 0.00 px | 18.54 → 0.00 px | 16.39 → 16.39 ms |

这里的 0 是消除了本游戏位置平滑引入的额外偏移，不是鼠标到显示器的硬件延迟为 0。120 上限受到本机呈现节奏限制，不能当成原生 120 FPS 测试。平均帧时间基本不变，也不声称提升了 FPS。本次是原生场景中的受控输入回放，没有高帧率相机或实体手机触摸延迟测量。

原始数据：[30 前](../validation/client8/drag-before-30.json) / [后](../validation/client8/drag-after-30.json)，[60 前](../validation/client8/drag-before-60.json) / [后](../validation/client8/drag-after-60.json)，[120 上限前](../validation/client8/drag-before-120.json) / [后](../validation/client8/drag-after-120.json)。复现脚本位于游戏仓 tests/drag_latency_benchmark.gd；设置 BENCH_FPS=30/60/120、BENCH_TAG=before/after，以带窗口模式执行 `godot --path . --script tests/drag_latency_benchmark.gd`。对照需在单独 worktree 使用原 card_actor.gd 和同一测试脚本，不覆盖正在开发的目录。

## 验证与发行

- 卡牌正常/金色说明、手牌出售和动作防护：1428 项检查通过。
- Windows 原生 2D/3D 界面：20 项检查通过，包括设置、真实右键购买/出售、满场手牌出售、出售按钮和完整说明按钮。
- 两个 profile、观战、开局限制、逐人回酒馆回归通过；两个真实 Godot 进程的局域网法术与观战流程通过。
- 后端、Windows 更新器和固定源码测试：18 项通过。公网 HTTPS/WSS 三客户端验证直接手牌出售、房间列表、公开观战/隐藏私有区域/只读/切换视角、永久退出/新建房间、旧票据撤销和最后真人离开释放桌位全部通过。
- 测试中的初始英雄可能自带法术，公网测试按购买随从 UID 定位，避免误把第一张起始手牌当作新购买随从。测试账号已按精确名单清理，原有 4 个账号保留。
- 上线前确认无活动桌或排队，排空、加密备份、保存旧源码后更新，再恢复分配。最终将旧部署的 CRLF 源文件按固定 Git 提交统一为 LF，语义校验一致；完整 79 个专服文件的逐字节哈希核对见 [源码验证](../validation/client8/server-source-check.json)。
- Windows 服务版/独立版 release 导出及 headless 启动通过；APK 归档与包名/版本检查通过。短时强制退出仍有已有的 ObjectDB/资源退出警告；后端仍有 Starlette 弃用提示。没有实体 Android 验收，没有重跑 32 人容量或复杂亡语压力测试。
- Android 沿用既有调试签名：服务版 org.classictavern.service / code 8，独立版 org.classictavern.game / code 66。Windows 为 release 导出。

服务版为 0.61.1-service8，后端为 0.3.1-preview，协议仍兼容 allstars-0.61.0-service-2。服务版在游戏内检查更新；[Windows](https://bjckwrn.xyz:21111/downloads/ClassicTavern-Service-8.exe) / [Android](https://bjckwrn.xyz:21111/downloads/ClassicTavern-Service-8.apk)。Windows 可下载校验后替换重启，Android 仍需系统确认安装。

独立版为 [v0.61.1](https://github.com/bjckbjckbjck-ai/classic-tavern-builds/releases/tag/v0.61.1)，使用原独立更新通道；LAN 双方建议同时升级才能使用新手牌出售动作。发行包 SHA-256 见 [校验清单](../validation/client8/SHA256SUMS.txt)，线上记录见 config/release-manifest.json。

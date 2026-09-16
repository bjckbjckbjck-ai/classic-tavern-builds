# #25 设计阶段核查

日期：2026-09-16。被检查版本：v0.49.0，源代码基线 `b452e66`。本目录是设计证据，不是 v0.50.0 发布验证。

## 实际运行

Windows，Godot 4.6.1，Compatibility / OpenGL 3.3，NVIDIA GeForce RTX 5060 Laptop GPU。使用项目真实 `main.tscn`，以练习房间设置固定手牌／场面，调用实际客户端输入展开手牌；通过 `root.get_texture().get_image()` 取得原生渲染截图。测试结束正常退出。

在含完整源码的本地工程根目录运行：

```powershell
& 'D:/godot/Godot_v4.6.1-stable_win64.exe/Godot_v4.6.1-stable_win64_console.exe' --path . --script validation/issue25-design/audit.gd
```

脚本原始输出在 `.runtime/issue25-runtime-catalog.json`，截图在 `screenshots/issue25-*.png`。本次封存见本目录的 `runtime-catalog.json`、`run.txt` 和 `screenshots/`。初始化英雄／法术可能因练习房间随机数而不同，卡池统计和检查路径不受影响。公开仓库只发布文档和证据，运行脚本需要完整本地源码。

- 实际 Catalog：193 条定义、141 张在池随从、37 张法术，`errors=[]`。
- 静态按扩展加载顺序合并的清单与引擎实际加载的在池 ID 集合一致。
- 输入检查：手机布局首次点击仅展开微扇形，手牌仍为 10 张。
- 程序退出码 0，未记录脚本错误。

## 截图

|状态|本次原生截图|
|---|---|
|桌面底部中央 10 张微扇形|[桌面](screenshots/issue25-desktop-fan.png)|
|手机布局右下收纳|[收纳](screenshots/issue25-mobile-folded.png)|
|手机布局展开 10 张|[10 张](screenshots/issue25-mobile-fan.png)|
|手机布局展开 4 张，与参考图张数相近|[4 张](screenshots/issue25-mobile-four-fan.png)|
|亡灵收藏第一页，共 16 张|[收藏](screenshots/issue25-undead-collection.png)|

原版参照是用户上传的 `1-Photo-1.jpg`（电脑）、`2-Photo-2.jpg`（手机发现）、`3-Photo-3.jpg`（手机展开），位于当前会话 `6c984d0c-7f57-4137-9227-0640768c5919` 附件目录。这里只发布我方截图，没有额外复制用户附件。差距和改法见[设计第 7 节](../../v0.50.0-七族卡池设计.md)。

## 检查范围

本轮确认的是当前数据、原生可见布局及一次真实输入。手机布局通过 `mobile_override` 切换，**没有重跑 Android APK、没有实体手机验证、没有帧率或声音实听测量**。这些截图不能证明候选新卡已经存在或新效果正确。固定场面含高星卡，属于视觉核查布置，不代表第一回合的正常商店发牌。

当前游戏代码／数据未修改；没有生成新的 APK／EXE，没有进行平衡模拟。#25 保持开放供设计调整；#18 继续跟踪实际视觉和操作差距。

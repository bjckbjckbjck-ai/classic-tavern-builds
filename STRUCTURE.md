# Architecture · v0.30.0

- `scripts/catalog.gd`：JSON卡池与mods加载校验。
- `scripts/rules.gd`：房主权威经济、卡槽、共享池、回合与操作。
- `scripts/combat.gd`：按种子在副本上模拟，生成私有过滤后的回放事件。
- `scripts/main.gd`：WebSocket会话、私人快照、统一计时、现有2D输入和界面组织。
- `scenes/tavern_3d.tscn` / `scripts/presentation3d/tavern_stage.gd`：3D表现适配器，固定镜头、桌面、UID对象映射、前景拖拽视图和暂停渲染管理。
- `scripts/presentation3d/card_actor.gd`：长期存在的Node3D，卡面纹理缓存、实体边框、盾/复生、退场；不调用Rules.act。
- `scripts/card.gd`：保留2D命中/拖放接口，也用于卡面纹理绘制。`presentation_proxy`禁止重复画卡；`render_3d_face`避免重复套2D圣盾膜。
- `scripts/attack_motion.gd`：共用时间常量和现阶段Control运动轨迹；3D适配器跟随轨迹并加入离桌高度/倾斜。后续迁出独立时间线。
- `scripts/presentation_fx.gd`：现有2D法术轨迹、英雄结算和声音；3D启用时不再生成重复2D死亡残影。

联机使用WebSocket/TCP，默认4271。房主只接受意图并校验发送者，向每位客户端发送过滤的私人视图。3D/2D选择只影响本机渲染，不影响同版本之间的规则同步；专用房主不启用3D。

源码Git位于项目根目录，main为v0.29基线、3d为当前工作分支。公开发行仓库在`.runtime/publish-v24`，仅上传文档、验证与成品；其默认分支也为3d。两者历史独立，源码未自动上传公开仓库。上传原照、构建缓存、签名文件和本地运行目录不纳入源码Git。

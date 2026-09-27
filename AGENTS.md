# 服务框架维护约定

- 本仓长期分支是 service-platform。账号、分段匹配、积分、数据库、房间调度、备份和部署在此维护；临时分支使用 codex/ 前缀。
- 完整游戏在私有 classic-tavern-game/main，本地 D:/ai/codex/新联机炉石战棋。卡牌规则、客户端音效/UI、Godot 云端适配在游戏仓维护；不直接合并两个仓库的独立历史。
- game_adapter/*.gd 是生成快照，不直接编辑。用 deploy/game_source.py 锁定游戏提交并更新；deploy/bundle.py 从该提交打包。
- game-source.json 是候选构建源码锁，release-manifest.json 是实际上线记录，不得混用。
- 固定四张共享桌，每桌八人；好友房和积分匹配、断线托管和重连、每日备份继续保留。
- 先读 docs/GAME_UPDATES.md；上线前排空、备份并验证，不中断真实玩家对局。

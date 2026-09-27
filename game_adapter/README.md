# 自动生成的 Godot 适配快照

2026-09-27 起，唯一可编辑源码位于私有 classic-tavern-game/main 的 scripts/service_client.gd、service_server.gd、service_updater.gd。

本目录三个 .gd 文件是固定提交的生成快照，供审阅与后端独立验证使用。不要直接修改副本；运行 python deploy/game_source.py --game-dir <游戏路径> --ref <commit> --update 更新，省略 --update 则检查一致性。版本及 SHA-256 见 config/game-source.json。

游戏规则只有一份；服务器包从固定 Git 提交读 rules.gd 及依赖，不读未提交修改。线上实际版本仍以 config/release-manifest.json 为准。

legacy/integration-service7.patch 仅保存旧分支资料；新 main 已包含适配，不再套用补丁。维护流程见 ../docs/GAME_UPDATES.md。

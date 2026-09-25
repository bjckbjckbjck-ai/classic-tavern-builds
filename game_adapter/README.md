# Godot适配与版本来源

本目录只保留服务专用适配代码，不复制游戏规则。完整规则来自config/release-manifest.json记录的游戏源码基线。

- service_client.gd：账号页面、双模式、API、JSON WSS、重连与快照适配。
- service_server.gd：无画面权威桌进程，复用原catalog/rules及其依赖。
- integration.patch：现有main/foyer/hero_draft_ui/export配置改动。应用前在独立分支运行`git apply --check`，检查通过再应用，并把上述两个脚本放进scripts目录。
- 完整本地实现提交在service-integration分支；commit记录在release-manifest。该游戏源码历史没有推送到公开发行分支。

更新游戏时在游戏侧合并新规则，再更新此适配目录和补丁；不要直接把服务仓的独立历史合并进游戏。重新做协议、重连、32客户端和备份回归，构建对应客户端后再维护排空发布。

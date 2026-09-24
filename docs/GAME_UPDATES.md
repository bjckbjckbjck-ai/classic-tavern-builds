# 独立分支与游戏更新

- GitHub仓库使用 bjckbjckbjck-ai/classic-tavern-builds，新建独立历史 service-platform 分支存服务化后端、部署、协议和验证。3d/main保持原用途；不把独立历史分支直接合并覆盖游戏分支。
- 本地服务工作区与游戏工作区分离。公开3d当前不是完整可构建游戏源码，不宣称拉取它即可构建专服。
- 游戏适配将在游戏源码侧使用 service-integration 分支，记录对应上游游戏提交。共享规则只维护一份，服务差异集中在启动入口、网络适配和账号/匹配UI。
- 不将整个游戏工作区直接推送：签名、.runtime、密钥、私人素材及未跟踪文件先排除；当前推送仅服务化文档和配置。

每次游戏更新：核对新版源码提交和内容哈希 → 合入service-integration → 检查ID/状态/RPC/最高难度AI变化 → 构建Linux专服和Windows/Android客户端 → 更新兼容清单（game_version/source_commit/service_version/protocol_version/content_hash/schema_version/rating_policy_version/产物SHA-256） → 好友/积分/重连/备份回归与4桌验收 → 维护排空 → 发布。

随游戏更新指以上可追溯适配流程，不自动未经测试拉latest替换线上。当前尚未实现CI、定时同步或自动构建。

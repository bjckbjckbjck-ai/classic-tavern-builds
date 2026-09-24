# Classic Tavern 服务化仓库

状态：规划与仓库初始化完成；业务服务、客户端改造、部署脚本尚未实现，不能部署上线。

目标：固定4张云服桌，好友房间和在线积分匹配共享，每桌8席、合计32席。两模式均支持托管重连，账号数据存云服，每日加密备份到指定本地电脑。大厅/队列上限另设，32席不代表已压测容量。

游戏基线：v0.61.0，源码提交 `75fc987`，Godot 4.6.1。2026-09-24 通过 GitHub API 确认公开 latest 为 v0.61.0。本地游戏源码位于 `D:/ai/codex/新联机炉石战棋`；原仓库无 remote，公开 `bjckbjckbjck-ai/classic-tavern-builds` 是发行仓，不能当作完整游戏源码拉取。

- [实施计划与验收](docs/IMPLEMENTATION_PLAN.md)
- [服务器交接与部署约定](docs/DEPLOYMENT.md)
- [最新产品规则（优先）](docs/PRODUCT_RULES.md)
- [游戏更新与独立分支](docs/GAME_UPDATES.md)
- [机器可读规划配置](config/product-policy.json)（尚无业务服务加载）

本仓库存放大厅后端、数据库迁移、进程管理、部署脚本及服务测试。游戏规则和客户端继续以游戏源码仓为唯一来源；构建 Linux 服务端产物后按提交和 SHA-256 引入，避免复制出两套规则。后续添加 apps/api、apps/supervisor、db/migrations、deploy、tests/load 目录。

独立本地工作区对应GitHub的service-platform独立历史分支；不更改3d/main。只发布服务化文档与配置，不包含用户数据、密钥和备份。

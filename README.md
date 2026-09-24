# Classic Tavern 服务化仓库

状态：规划与仓库初始化完成；业务服务、客户端改造、部署脚本尚未实现，不能部署上线。

目标：在一台云服务器上承载最多 8 场、每场 8 席位的对局，提供注册登录、匹配、原位重连、战绩及可重复部署。64 是对局席位上限，不代表已测得的服务器容量；大厅连接与排队上限单独配置。

游戏基线：v0.61.0，源码提交 `75fc987`，Godot 4.6.1。2026-09-24 通过 GitHub API 确认公开 latest 为 v0.61.0。本地游戏源码位于 `D:/ai/codex/新联机炉石战棋`；原仓库无 remote，公开 `bjckbjckbjck-ai/classic-tavern-builds` 是发行仓，不能当作完整游戏源码拉取。

- [实施计划与验收](docs/IMPLEMENTATION_PLAN.md)
- [服务器交接与部署约定](docs/DEPLOYMENT.md)

本仓库存放大厅后端、数据库迁移、进程管理、部署脚本及服务测试。游戏规则和客户端继续以游戏源码仓为唯一来源；构建 Linux 服务端产物后按提交和 SHA-256 引入，避免复制出两套规则。后续添加 apps/api、apps/supervisor、db/migrations、deploy、tests/load 目录。

独立本地 Git 仓库，尚未创建 GitHub 远程仓库、上传源码或存入任何凭据。

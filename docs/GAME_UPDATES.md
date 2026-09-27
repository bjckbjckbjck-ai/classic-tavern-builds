# 两个仓库、按模块维护

2026-09-27 用户批准统一游戏分支后，本页替代旧的长期 service-integration 分叉流程。

| 维护对象 | 唯一源 | 工作区 |
| --- | --- | --- |
| 卡牌、英雄、AI、版本、规则 | 私有 classic-tavern-game / main | D:/ai/codex/新联机炉石战棋 |
| 客户端框架：音效、UI、云端客户端、Godot 桌进程 | 同一游戏 main，按 scripts/ 和 assets/audio/ 模块分工 | 同上 |
| 后端框架：账号、分段匹配、积分、备份、部署 | classic-tavern-builds / service-platform | D:/ai/codex/classic-tavern-service |

临时任务分支用 codex/content-*、codex/client-*、codex/cloud-client-*、codex/service-*，完成后合回所属仓库主线。音效随客户端构建，不会仅修改后端就出现在已安装客户端。分段匹配主要属于后端；新增协议字段或交互时需同步游戏云端适配。

## 源码锁与发布锁

- config/game-source.json：下一次构建的固定游戏提交、专服内容 SHA-256、适配快照 SHA-256。
- config/release-manifest.json：实际上线版本。整理分支不修改它，也不代表发布了新客户端。
- game_adapter/*.gd：从源码锁生成的快照，用于审阅和独立后端测试，禁止直接修改。游戏中的 scripts/service_*.gd 才是唯一源。
- game_adapter/legacy/integration-service7.patch：旧 service7 构建历史，不再应用到统一 main。

```powershell
python deploy/game_source.py --game-dir 'D:/ai/codex/新联机炉石战棋' --ref <已验证commit> --update
python deploy/game_source.py --game-dir 'D:/ai/codex/新联机炉石战棋'
python deploy/bundle.py 'D:/ai/codex/新联机炉石战棋' '<Godot Linux executable>'
```

从零恢复：克隆本仓 service-platform；通过有权限的 GitHub 账号克隆私有游戏仓；在构建目录检出 game-source.json 的完整 commit；安装 Godot 4.6.1 及依赖；运行源码锁检查、测试和构建。公开发行仓 main/3d 不是完整源码。

D:/ai/codex/classic-tavern-service-game 现在只是固定提交的构建 worktree。原有未提交导入配置保留；切换版本前检查工作目录，不覆盖人工改动。旧 3d / service-integration 已合并并以 archive/pre-unify-20260927-* 标签归档，私有远端保留完整 Git 历史。

## 发布顺序

模块修改 → 各自主线提交 → 更新候选源码锁 → 协议兼容和对应功能测试 → 构建客户端与专服 → 验证包名、通道、版本及哈希 → 隔离环境与公网回归 → 排空和备份 → 发布 → 更新实际发布清单。

服务器包从固定 Git 提交读取游戏文件，不混入工作目录未提交修改。后端框架独立发布不意味着游戏规则也自动更新；不得自动拉 main 覆盖运行中的游戏。尚未配置自动构建或自动部署 CI。

## 分支整理时的验收（历史，2026-09-27）

- 游戏 main：fd2fd0b；私有远端已保存完整历史及 3 个归档标签。
- 两种 profile 入口共 15 项通过；原生 Windows 局域网菜单、开局、购买、上场、冻结、战斗通过。修正旧 UI 测试中过期坐标。
- 两进程真实回环联机、法术动作、观战切换通过；观战隐私、开局锁、逐人回酒馆回归通过；配对检查 129114 项通过。
- 后端、更新器和固定 Git 源码测试共 18 项通过。已有短时 headless 退出资源警告和 Starlette 弃用提示未扩大处理。
- 本次没有新客户端发行、线上重启或实体 Android 验收；线上仍为 service7 / 0.3.0-preview。

后续 issue #34–36 已按上述双仓流程发布 v0.61.1 / service8，源码锁和实际上线锁均为 1d36dad；见 [更新验证](ISSUES34-36.md)。

最新：用户批准后已部署 v0.62.0 / service9，游戏提交3a1bfd0、后端0.3.2-preview。部署采用暂存验证、排空备份、健康检查与回滚保留，公网双模式重连和备份恢复通过，详见 [service9发布记录](SERVICE9-v062.md)。

2026-09-28：已部署 v0.63.1 / service10，固定提交756a202；详见 [service10发布记录](SERVICE10-v0631.md)。

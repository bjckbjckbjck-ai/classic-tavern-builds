# Classic Tavern 服务化仓库

状态：服务化预览版0.3.1已实现并部署到 https://bjckwrn.xyz:21111 。游戏规则基于v0.61.1。上线验证范围与限制见[部署报告](docs/DEPLOYED.md)，不把短时测试当作长期稳定性保证。

**当前发布记录（2026-09-27）：** 21111 TLS入口为`https://bjckwrn.xyz:21111`，客户端service8、Android版本code=8。新增对局简要说明、可选右键买卖、直接出售手牌随从和拖拽位置跟随修复，见 [#34–36 验证报告](docs/ISSUES34-36.md)。该端口已通过外部HTTPS/WSS登录、好友开局及断线托管重连测试；本次新增公网手牌出售回归。原80/443域名入口曾遭腾讯云webblock拦截，保留历史记录；非80端口不免除ICP备案义务，也不能保证不会被后续拦截，见[腾讯云说明](https://cloud.tencent.com/document/api/243/19630)。

目标：固定4张云服桌，好友房间和在线积分匹配共享，每桌8席、合计32席。两模式均支持托管重连，账号数据存云服，每日加密备份到指定本地电脑。大厅/队列上限另设，32席不代表已压测容量。

游戏基线：v0.61.1。完整源码已统一到私有 [classic-tavern-game/main](https://github.com/bjckbjckbjck-ai/classic-tavern-game)，本地 `D:/ai/codex/新联机炉石战棋`。本仓独立维护后端框架；候选游戏提交见 config/game-source.json，实际上线提交见 config/release-manifest.json。

- [实施计划与验收](docs/IMPLEMENTATION_PLAN.md)
- [服务器交接与部署约定](docs/DEPLOYMENT.md)
- [最新产品规则（优先）](docs/PRODUCT_RULES.md)
- [游戏更新与独立分支](docs/GAME_UPDATES.md)
- [产品配置](config/product-policy.json)（描述当前策略；运行时常量与修改需要一起验证）

本仓库包含Python/FastAPI账号与调度服务、SQLite WAL数据库、部署/灾备工具、服务测试及Godot适配代码。固定单机4桌阶段采用SQLite事务和一致性备份，替代初始Node/PostgreSQL方案；线上HTTPS/WSS入口使用Nginx+Certbot。Godot仍是唯一权威规则实现，没有在后端重写卡牌逻辑。

本地服务工作区对应 GitHub 的 service-platform 分支。游戏内容、客户端公共框架（含音效）和 Godot 云端适配在统一游戏 main 按模块维护；game_adapter 是生成快照，禁止手改。参阅 [游戏与服务更新](docs/GAME_UPDATES.md)。

## Issue #33 更新（2026-09-26）

- 每人看完或跳过自己的回放即可进入下一轮酒馆并操作；其他玩家仍可继续观看，下一轮战斗仍统一结算。
- 好友房主开始后进入单机同款四选一英雄界面，全体真人确认即开始，30秒超时保留默认选择；开始选英雄后不再允许新玩家加入。
- 匹配页每2秒刷新排队人数与AI同意人数。未满8人时，当前队列所有人均等待满60秒并同意才一起开AI局；已满8人直接开真人局。
- 协议升级为`allstars-0.61.0-service-2`，必须重新下载客户端。详情见[验证记录](docs/ISSUE33.md)。

## 使用

从域名首页下载专用Windows/Android客户端，在好友房间或在线匹配入口注册账号并登录。账号为3—24位英文/数字/下划线，密码至少10位。注册恢复码请另存。好友房间分享房间码；在线匹配等待60秒后可选择最高难度AI。APK使用独立包名org.classictavern.service，可与原离线版共存。

积分暂定：第1—8名 +70/+45/+25/+10/-10/-25/-45/-70，初始1000、最低0。多人AI混合局系数0.5，向零取整；只有1名真人时不计分。好友房不计分。断线托管仍按本人名次结算，异常中止不计分。

## 验证与运维

`python -m pytest tests/test_service.py -q` 运行隔离数据库测试。`tests/live_*.py`为指定预览环境的主动联机测试，会创建/占用测试房间，不作为日常监测任务运行。

服务器：`sudo python3 /opt/classic-tavern/deploy/ops.py status` 查看桌位；`drain`暂停新分配，`resume`恢复，`backup`执行一次加密备份。更新前先drain并等现有对局结束；install.sh在仍有活动对局时拒绝覆盖。

云端每天04:00 Asia/Shanghai生成加密备份；当前Windows接收任务ClassicTavern-BackupReceiver每小时及登录时拉取，电脑离线后补传。私钥只在本地secrets目录，必须由用户额外离线保存。备份恢复的是账号/积分/战绩，不恢复崩溃前的半场比赛。

## 云服客户端 service5

已接入六首分阶段音乐、七个原创回合提示音和云服更新入口。Windows 一键下载校验/替换重启，Android 浏览器下载后系统确认安装。首次需手动安装本版，后续应用内更新。实现、验证及发布步骤见 [客户端音乐与更新说明](docs/CLIENT5-AUDIO-UPDATES.md)。

## service6 房间列表与观战

服务器房间列表显示积分赛/好友房、阶段和真人数量，支持加入、重连及公开观战；离开时可选择暂离或彻底退出，退出后可新建房间。规则、积分及验证见 [房间与观战说明](docs/ROOMS-SPECTATORS.md)。

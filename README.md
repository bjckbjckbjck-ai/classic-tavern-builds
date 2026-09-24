# Classic Tavern 服务化仓库

状态：服务化预览版0.1.0已实现并部署到 https://bjckwrn.xyz 。游戏规则基于v0.61.0。上线验证范围与限制见[部署报告](docs/DEPLOYED.md)，不把短时测试当作长期稳定性保证。

**最终公网阻塞（2026-09-25 03:02 CST）：** 此前域名公网验证通过，但收尾复测时HTTP被跳转至腾讯云`dnspod.qcloud.com/static/webblock.html?d=bjckwrn.xyz`，HTTPS握手被重置。服务器内HTTPS与服务均正常，公网域名目前不能交付使用。需要域名持有人核实ICP备案及腾讯云接入备案，或处理云厂商误拦截。下面的域名下载/登录步骤应在解除拦截后使用。

目标：固定4张云服桌，好友房间和在线积分匹配共享，每桌8席、合计32席。两模式均支持托管重连，账号数据存云服，每日加密备份到指定本地电脑。大厅/队列上限另设，32席不代表已压测容量。

游戏基线：v0.61.0，源码提交 `75fc987`，Godot 4.6.1。2026-09-24 通过 GitHub API 确认公开 latest 为 v0.61.0。本地游戏源码位于 `D:/ai/codex/新联机炉石战棋`；原仓库无 remote，公开 `bjckbjckbjck-ai/classic-tavern-builds` 是发行仓，不能当作完整游戏源码拉取。

- [实施计划与验收](docs/IMPLEMENTATION_PLAN.md)
- [服务器交接与部署约定](docs/DEPLOYMENT.md)
- [最新产品规则（优先）](docs/PRODUCT_RULES.md)
- [游戏更新与独立分支](docs/GAME_UPDATES.md)
- [产品配置](config/product-policy.json)（描述当前策略；运行时常量与修改需要一起验证）

本仓库包含Python/FastAPI账号与调度服务、SQLite WAL数据库、部署/灾备工具、服务测试及Godot适配代码。固定单机4桌阶段采用SQLite事务和一致性备份，替代初始Node/PostgreSQL方案；线上HTTPS/WSS入口使用Nginx+Certbot。Godot仍是唯一权威规则实现，没有在后端重写卡牌逻辑。

独立本地工作区对应GitHub的service-platform独立历史分支；不更改3d/main。服务化游戏适配在本地service-integration分支开发；本仓game_adapter保留适配文件/补丁与基线说明。不上传用户数据、密钥、数据库或备份。

## 使用

从域名首页下载专用Windows/Android客户端，在好友房间或在线匹配入口注册账号并登录。账号为3—24位英文/数字/下划线，密码至少10位。注册恢复码请另存。好友房间分享房间码；在线匹配等待60秒后可选择最高难度AI。APK使用独立包名org.classictavern.service，可与原离线版共存。

积分暂定：第1—8名 +70/+45/+25/+10/-10/-25/-45/-70，初始1000、最低0。多人AI混合局系数0.5，向零取整；只有1名真人时不计分。好友房不计分。断线托管仍按本人名次结算，异常中止不计分。

## 验证与运维

`python -m pytest tests/test_service.py -q` 运行隔离数据库测试。`tests/live_*.py`为指定预览环境的主动联机测试，会创建/占用测试房间，不作为日常监测任务运行。

服务器：`sudo python3 /opt/classic-tavern/deploy/ops.py status` 查看桌位；`drain`暂停新分配，`resume`恢复，`backup`执行一次加密备份。更新前先drain并等现有对局结束；install.sh在仍有活动对局时拒绝覆盖。

云端每天04:00 Asia/Shanghai生成加密备份；当前Windows接收任务ClassicTavern-BackupReceiver每小时及登录时拉取，电脑离线后补传。私钥只在本地secrets目录，必须由用户额外离线保存。备份恢复的是账号/积分/战绩，不恢复崩溃前的半场比赛。

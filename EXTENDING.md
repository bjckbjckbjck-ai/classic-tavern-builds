# v0.23 暗月与饰品扩展

转盘和暗月奖品已拆分为独立JSON。数据字段、概率校验、处理器与联机边界参见 [扩展方法](v0.23.0-暗月转盘与资源轮换.md#后续如何扩展)。沿用本项目Godot 4.6.1导出，双方安装相同版本。下文的外置mods仍用于随从和英雄；新暗月脚本需要重新导出，不支持热下载脚本。

---

# v0.11.0 新扩展字段

最终内置覆盖为 data/spotlight-expansion.json，随后仍加载外部 mods。retired:true / pool:0 表示移出当前图鉴和可抽池，旧 id 保留兼容测试。修改旧牌时应同时设置 retired:false 和正数 pool。

被动新增 rewind、end_multiplier、end_battlecry、spend_pirate。spend_pirate 的 spent 为随从持有的 0..7 进度，金色三连继承最高进度。回合末多个附魔师取最大倍数。回放 events.effects 包含 kind/source/target/from/to；from/to 为 [side,index,board_size]，客户端只读、最多每帧 32 条，不可用于反向修改规则。

声音源生成器 scripts/generate_audio.py；音效受静音、同类 95ms 限频及最多八路音源限制。

## v0.10.0 法术扩展

新增 data/spells.json 与 scripts/tavern_spells.gd。法术独立 catalog.spells，经房主同步；对象 kind=spell、token=true，不放入随从共享池。effect 支持 gold、investment、target、set、shop、board、menagerie、steal、recruit、discover。target 为 any（战场或酒馆）、board 或省略（不指定目标）；cost 为购买费用，cast 不再次扣费。新增类别应补充施放验证、AI 与联机测试。桌面 mods 仍只扩展随从/英雄；法术扩展需修改数据重新打包。

新随从触发支持 hand_added、consume_shop、start_adjacent；召唤被动可设 combat_only。所有获取手牌的规则路径应通过 Rules.add_hand，以便佩姬等触发一致。

## v0.9.0 扩展字段

charges 支持 shield / reborn / windfury / venom / cleave，非负整数；显式 0 覆盖 keywords。gold_charges 用同样五键单独配置金色基础，例如扎普 {"windfury":3}。其他字段不自动推断金色层数。
Windows 扩展放 EXE 同级 mods/*.json，房主将验证后的内容发送给客户端；Android 通过打包 data 扩展。移除联机后重新加载本机目录，防止房主扩展残留。修改结算代码需升级 NETWORK_VERSION，避免规则不一致。

## v0.8.0 六族叠层扩展

只支持叠层游戏规则。种族白名单为野兽、鱼人、龙、机械、恶魔、海盗、中立。永久 `poison` 关键词不再允许：使用 `venom`，在 `charges` 写初始层数；目标战吼使用 `keyword: "venom", charges: 1, gold_charges: 2`。`shield` / `reborn` 同样用非负整数层数；印刷关键词金色不默认翻倍。

新牌包示例 `data/six-tribes.json`：`magnetic: true` 允许磁力，`sell_value` 支持特殊出售；`adaptation` 用于游戏详情说明版本差异。附加亡语保留材料的 `gold` 状态。招募触发集中在 `scripts/recruit_effects.gd`；战斗触发在 `scripts/combat.gd`；AI 新机制应同时更新估值和操作。

新增战吼类型 `discount`、`missing_health`、`discover_tribe`；新增被动类型见 `catalog.gd` 白名单。测试入口 `scripts/verify.py`，发版构建同时检查工程、Android 与更新检查版本，公告仅从 `更新记录.md` 生成。

以下为历史扩展说明；旧经典模式和永久剧毒相关例子不再适用于当前版本。

# 自定义扩展

v0.4 新增层数字段：在完整卡牌定义中使用 `"charges":{"shield":2,"venom":1}`。只接受非负整数，支持 shield / venom；未显式指定时，原有 shield 关键词表示 1 层。显式 0 层不会回退到 1 层。永久 poison 与消耗型 venom 不同。战斗用拷贝消耗层数，三连保留金色基础层数一次和所有额外层数。安卓仍需将扩展与素材打进 APK，尚无手机文件导入界面。

开发环境把 JSON 放进项目 `mods/`；导出后放进 EXE 同目录的 `mods/`。按文件名顺序加载，相同 id 覆盖，不同 id 新增。重启房主游戏后开房生效。房主把卡牌和英雄数据发给客户端，客户端使用房主的数据。素材仍需要随客户端打包。

## 卡牌示例

以下示例覆盖已有原卡，不会自动加载。默认发行版不含原创卡。

```json
{
  "cards": [{
    "id": "cat",
    "name": "雄斑虎",
    "tier": 1,
    "attack": 1,
    "health": 1,
    "tribe": "野兽",
    "art": 0,
    "source": "CFM_315",
    "pool": 18,
    "keywords": [],
    "text": "战吼：召唤一个 1/1 的小猫。",
    "battlecry": {"type":"summon","id":"kitten","count":1},
    "deathrattle": {}
  }]
}
```

- `tier` 1–6，`attack` 非负，`health` 正数；`pool` 是共享卡池普通份数。衍生物使用 `token:true,pool:0`。
- `art` 是内置 12 格插画图集的 0–11 索引；`source` 对应 `assets/original/<source>.png`，需重新导入和导出。
- 关键词：`taunt` 嘲讽、`shield` 圣盾、`poison` 剧毒、`cleave` 顺劈、`windfury` 风怒。
- 战吼：`summon`，`self_damage`，`target`（指定种族、attack/health/keyword），`buff_all`，`buff_tribe`。
- 亡语：`summon`（count 或 count_attack），`damage`（随机敌人、amount），`buff`（attack/health，可选 tribe 或 random）。
- 光环：`aura:{"tribe":"恶魔","attack":1}`，作用于战斗中其他同种族随从。
- 金色基础身材翻倍，定量增益翻倍；召唤升级为金色衍生物，召唤数量不翻倍。随机伤害亡语执行两次。
- 尚未支持的效果需在 `catalog.gd` 注册，并分别在 `rules.gd` / `combat.gd` 实现，不要只改描述文本。

## 英雄

JSON 顶层可有 `heroes` 数组，每项包含 `id,name,text,art,cost,power,hp`。`power` 当前支持 `passive,pyramad,jaraxxus,yogg`。相同 id 覆盖原英雄；新增技能行为需扩展 `rules.gd` 的 power 分支。未来原创英雄可沿用此结构。

## 模块边界

- 招募、经济、三连、AI：`scripts/rules.gd`。
- 战斗、伤害、亡语、回放事件：`scripts/combat.gd`。
- 本地 UI、房间、网络：`scripts/main.gd`。
- 卡牌展示及拖动：`scripts/card.gd`。

规则改动后执行 `tests/rules_test.gd`，网络改动后运行双进程测试，并在两个设备上复测。不要让客户端自行结算战斗。

## v0.5.0 原卡包机制

`data/legacy-expansion.json` 在基础卡包之后、外部 mods 之前加载。ID 必须避开现有衍生物（例如 `hyena` 已属于草原狮的衍生物，食腐土狼使用 `scavenging_hyena`）。

新增 `passive` 对象支持 `type: start_turn / menagerie / friendly_death / battlecry_multiplier`；前三者使用 attack/health 数值，friendly_death 还需 tribe。普通/金色成长系数为 1/2；铜须倍数为 2/3，多个铜须取最高值。menagerie 忽略中立，每种族随机一个目标。新增 `deathrattle: {"type":"shield","count":1}`，金色目标数翻倍，目标不重复。圣盾是否叠层由本局 stacking 规则决定。新增原画支持 source 对应的 jpg，优先使用 webp。

## v0.6.0 召唤与难度

`data/synergy-expansion.json` 添加 passive.type `summon_buff`（tribe/attack/health）和 `summon_shield`（tribe）。共享处理器 `summon_effects.gd` 在实际新单位进入战场时调用；不在战斗开始复制阵容时调用，也不让单位触发自己的召唤监听。金色 summon_buff 加倍；金色钴制的效果仍为获得一层。

玩家状态包含 armor、coin_cap 和 income；护甲伤害统一通过 hurt_hero。AI 难度为规则配置 ai_difficulty，详见 AI设计.md。

## v0.7.0 全明星与公告

allstars.json 在其他内置包之后加载；当前 wolf 使用 goldrinn ID 覆盖为六星精选版本，不复制成两张同名池牌。
passive.type 新增 macaw、deathrattle_multiplier、summon_multiply；deathrattle.type 新增 leap。
战斗继承亡语记录在 unit.leaps 中，键为增益强度（普通 1、金色 2），值为层数。接收者是否金色不会再次放大已继承的亡语。Titus 额外触发次数相加；多个 Slamma 在平面召唤增益后按板序乘算（普通 2、金色 3）。仅战斗阶段使用乘算。
每场 20000 次跳蛙传递预算，触顶平局；召唤乘算数值钳制到 1000000000。此限制是手机计算保护，不是原版规则。

发布时先写 更新记录.md，更新 update_checker.gd 的 VERSION 和 export_presets.cfg，再运行 scripts/sync_release_notes.py。构建脚本会检查三个版本一致后再导出。游戏内公告只读 data/releases.json，不需要联网。
更新 API 只请求指定 GitHub 仓库的 latest 稳定版，验证规范版本号和相同仓库的精确 APK URL。下载按钮调用系统浏览器，不后台安装；失败时给出可重试提示。


## v0.12 扩展接口

最终内置覆盖层为 `data/playstyles-expansion.json`，外部 mods 随后加载。新增 passive：hand_murloc、hand_stats、damage_demons、spell_menagerie、end_spells；deathrattle：summon_hand、lowest_damage。酒馆法术增加 free_refresh、roar、battlecry、shield、confidence、shop_aura、armor。

`Combat.fight` 第四参数为双方私有手牌。v0.24内部事件可保存双侧手牌，但发送前必须经过 `RULES.private_replay`：删除 `hands/summoned_hand`，只保留观看席位的 `hand_states` 与对手数量。UI用 `RULES.replay_hand` 读取索引，严禁直接发送原始replays。招募快照不发送上一场回放。`roars` 是永久附魔层数，磁力和三连相加；`SPELLS.buy_price` 为购买价格唯一入口，base_cost 保留原费用。


## v0.13 国王老汉

英雄 power=king_laohan，cost=5。使用 `draw_card(roll,true)` 从精确星级共享池抽取。`dice_serial` 递增标识成功处理的掷骰事件，`last_roll` 为结果；客户端不生成规则随机数。本地操作记录不通过玩家公开快照分享。AI 有至少三名随从时考虑技能。


## v0.14 扩展

最终内置覆盖包为 `data/armor-expansion.json`，之后加载外部 mods。新增 passive：end_tribe、start_dragon_shield、shield_loss、play_consume、spend_attack；战吼 consume 以及 target 的 per_pirate_buy/per_gold_spent。英雄 power：nozdormu、alexstrasza、patches。实际费用统一调用 Rules.power_cost。spent 三连取最高值。


## v0.15 原创迁移

最终内置覆盖包 `data/originals-expansion.json`，外部 mods 在其后。custom/origin/legacy_id 标记原创来源；画作支持 PNG。新增 passive：spell_self、end_spell_coin、end_hand_tribe、sell_tribe、sell_tribe_scaling。spells_cast_turn 每轮清零，crystal_sales 仅玩家真实出售时递增。详情切换通过 Catalog.unit 创建新基础卡，不改动原对象。


## v0.16 招募事件

RecruitTrace.emit/buff 记录来源、目标、位置、增益及单调序号。事件只随所属玩家 me 发送，每人环形缓存 32 条；严禁加入公开 players 或共享 combat events。RecruitFeedback 与棋盘分层，单批最多八组、最多三批，去重使用 recruit_serial。generated_coins 与 triples 是验证用累计计数，不参与奖励。


## v0.17 亡灵与永久收益

`undead.gd` 管理玩家级全局攻击/骑士计数与每单位已应用值；不可把光环当作普通附魔三次相加。`undead_combat.gd` 记录显式永久收益、复生来源关联、宰割奖励和待召回复制；通过弱引用连接 combat，避免保留整份回放。

招募消灭进入同一个死亡结算器。`pool_copies` 表示持有的真实共享副本数：生成单位为 0；复生继承，三连求和，出售按实际归属回收。新增生成/复制效果必须测满场、普通/金色、再三连与出售后的共享池守恒。英雄标记只在战斗结束到期，不在普通宰割结算时清掉其他目标标记。

来源日志不是完整属性账本，不能据此重新构造单位。对手公开列表不要加入手牌信息。`ai_trade_enabled` 只供固定场景对照，正常游戏默认开启；并非新的用户难度设置。

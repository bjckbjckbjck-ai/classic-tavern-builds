extends "res://scripts/service_server.gd"

func write_status():pass
func broadcast():pass
func _process(_delta):return false

func _initialize():
	game.add_player(123,"Disconnected human",false)
	game.add_player(-1,"Permanent AI",true)
	game.ai_difficulty=3
	begin()
	var human=game.player(123)
	assert(automated(human) and not human.bot)
	assert(human.coin_cap==10)
	assert(human.armor==int(catalog.heroes[int(human.hero)].get("armor",0)))
	assert(game.player(-1).coin_cap==12)
	game.bot_turn(human)
	assert(not human.bot and human.ready)
	assert(not human.board.is_empty())
	assert(preload("res://scripts/boss_plan.gd").guaranteed(game,human,"lesser").is_empty())
	print("PASS: disconnected human takes an AI turn without permanent AI privileges")
	quit()

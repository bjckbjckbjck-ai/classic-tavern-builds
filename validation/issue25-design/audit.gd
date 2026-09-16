extends "res://tests/purchase_v38_test.gd"
func shot(name:String):
	if is_instance_valid(app.timer_label):app.timer_label.text="76 秒"
	await super.shot(name)
func run_test():
	app=load("res://scenes/main.tscn").instantiate();root.add_child(app);current_scene=app;await process_frame
	app.visual_3d=true;app.visual_quality=2;app.practice_room();app.set_process(false);app.deadline=app.now()+600
	var p=app.game.player(1);p.coins=10;p.board=[];p.hand=[];p.discover=[];p.trinket_offers=[]
	var active=[];var counts={};var tiers={}
	for c in app.catalog.cards.values():
		if c.get("retired",false) or c.get("token",false) or c.pool<=0:continue
		active.append(c);counts[c.tribe]=int(counts.get(c.tribe,0))+1
		if not tiers.has(c.tribe):tiers[c.tribe]=[0,0,0,0,0,0]
		tiers[c.tribe][int(c.tier)-1]+=1
	var f=FileAccess.open("res://.runtime/issue25-runtime-catalog.json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"active":active,"counts":counts,"tiers":tiers,"total":app.catalog.cards.size(),"spells":app.catalog.spells.size(),"errors":app.catalog.errors},"  "));f.close()
	for id in ["macaw","bronze","reaper","brann","mama","hoggarr","frog"]:p.board.append(app.catalog.unit(id))
	for id in ["pupbot","cat","bronze","reaper","frog","brann","mama","hoggarr","tad","choral"]:p.hand.append(app.catalog.unit(id))
	p.shop=[app.catalog.unit("greater_soul_juggler"),app.catalog.unit("reaper"),app.catalog.unit("mama"),app.catalog.unit("hoggarr"),app.catalog.unit("brann")]
	root.size=Vector2i(1280,720);app.layout.mobile_override=0;app.broadcast();await create_timer(.8).timeout
	await shot("issue25-desktop-fan")
	app.layout.mobile_override=1;app.table();await create_timer(.6).timeout
	await shot("issue25-mobile-folded")
	await click(app.layout.compact_hand_region().get_center());await create_timer(.6).timeout
	check(p.hand.size()==10 and app.layout.hand_open,"first tap opens shallow fan without playing a card")
	await shot("issue25-mobile-fan")
	p.hand=p.hand.slice(6);app.broadcast();await create_timer(.6).timeout
	await shot("issue25-mobile-four-fan")
	app.gallery=true;app.gallery_kind="cards";app.gallery_tribe="亡灵";app.gallery_pool="在池";app.gallery_query="";app.gallery_page=0;app.show_gallery();await create_timer(.6).timeout
	await shot("issue25-undead-collection")
	print("AUDIT ACTIVE=",active.size()," COUNTS=",counts," ERRORS=",app.catalog.errors)
	app.free();await process_frame;quit(1 if failures else 0)

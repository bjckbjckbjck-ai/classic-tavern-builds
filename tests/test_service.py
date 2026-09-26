import importlib.util,time,json,sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def service(tmp_path,monkeypatch):
    monkeypatch.setenv('TAVERN_DATA',str(tmp_path))
    monkeypatch.setenv('TAVERN_TICKET_KEY','test-only-secret')
    monkeypatch.delenv('GODOT_BIN',raising=False)
    spec=importlib.util.spec_from_file_location('isolated_service',Path(__file__).parents[1]/'app.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.init()
    return m,TestClient(m.app)

def account(m,name):
    with m.db() as c:
        cur=c.execute('INSERT INTO accounts(name,password,recovery) VALUES(?,?,?)',(name,'unused','unused'))
        uid=cur.lastrowid
        c.execute('INSERT INTO sessions VALUES(?,?,?)',(m.sha(name),uid,time.time()+600))
    return uid,{'Authorization':'Bearer '+name}

def test_four_shared_tables(service):
    m,c=service
    for n in range(4):
        uid,h=account(m,f'person{n}')
        assert c.post('/api/friends',headers=h,json={}).status_code==200
    uid,h=account(m,'fifth')
    assert c.post('/api/friends',headers=h,json={}).status_code==409

def test_consent_is_explicit_after_60_seconds(service):
    m,c=service;uid,h=account(m,'waiting')
    assert c.post('/api/queue',headers=h,json={'protocol':m.VERSION}).status_code==200
    assert c.post('/api/queue',headers=h,json={'protocol':m.VERSION,'consent':True}).status_code==400
    with m.db() as db: db.execute('UPDATE queue SET joined=?',(time.time()-61,))
    m.tick()
    assert c.get('/api/me',headers=h).json()['room'] is None
    assert c.post('/api/queue',headers=h,json={'protocol':m.VERSION,'consent':True}).status_code==200
    m.tick()
    assert c.get('/api/me',headers=h).json()['room']['mode']=='ranked'

def test_partial_queue_waits_for_everyone_and_starts_together(service):
    m,c=service;people=[account(m,'cohort'+str(i)) for i in range(3)]
    for uid,h in people:c.post('/api/queue',headers=h,json={'protocol':m.VERSION})
    with m.db() as db:db.execute('UPDATE queue SET joined=?',(time.time()-61,))
    for uid,h in people[:2]:c.post('/api/queue',headers=h,json={'protocol':m.VERSION,'consent':True})
    m.tick()
    for uid,h in people:
        me=c.get('/api/me',headers=h).json()
        assert me['room'] is None and me['queue']['players']==3 and me['queue']['consenting']==2
    c.post('/api/queue',headers=people[2][1],json={'protocol':m.VERSION,'consent':True})
    m.tick()
    rooms=[c.get('/api/me',headers=h).json()['room']['id'] for uid,h in people]
    assert len(set(rooms))==1

def test_cancel_and_late_join_update_cohort(service):
    m,c=service;uid,h=account(m,'early');other,oh=account(m,'late')
    c.post('/api/queue',headers=h,json={'protocol':m.VERSION})
    with m.db() as db:db.execute('UPDATE queue SET joined=?',(time.time()-61,))
    c.post('/api/queue',headers=h,json={'protocol':m.VERSION,'consent':True})
    c.post('/api/queue',headers=oh,json={'protocol':m.VERSION})
    m.tick();assert c.get('/api/me',headers=h).json()['room'] is None
    c.post('/api/queue',headers=oh,json={'protocol':m.VERSION,'cancel':True})
    assert c.get('/api/me',headers=h).json()['queue']['players']==1
    m.tick();assert c.get('/api/me',headers=h).json()['room'] is not None

def test_full_human_queue_needs_no_ai_consent(service):
    m,c=service;people=[account(m,'full'+str(i)) for i in range(8)]
    for uid,h in people:c.post('/api/queue',headers=h,json={'protocol':m.VERSION})
    m.tick()
    assert len({c.get('/api/me',headers=h).json()['room']['id'] for uid,h in people})==1

def test_ranked_result_idempotent(service):
    m,c=service;ids=[account(m,f'rank{i}')[0] for i in range(8)]
    with m.LOCK,m.db() as db:
        r=m.allocate(db,'ranked',ids)
        result={'players':[{'id':uid,'rank':i+1} for i,uid in enumerate(ids)]}
        m.finalize(db,r,result);m.finalize(db,r,result)
        assert db.execute('SELECT count(*) FROM results').fetchone()[0]==8
        assert db.execute('SELECT rating FROM accounts WHERE id=?',(ids[0],)).fetchone()[0]==1070
        assert db.execute('SELECT rating FROM accounts WHERE id=?',(ids[-1],)).fetchone()[0]==930

def test_friend_results_no_rating(service):
    m,c=service;ids=[account(m,'friend'+str(i))[0] for i in range(2)]
    with m.db() as db:
        r=m.allocate(db,'friend',ids)
        m.finalize(db,r,{'players':[{'id':uid,'rank':i+1} for i,uid in enumerate(ids)]})
        assert [r[0] for r in db.execute('SELECT rating FROM accounts')]==[1000,1000]

def test_auth_recovery_and_logout(service):
    m,c=service
    r=c.post('/api/register',json={'name':'tester','password':'long-enough-password'})
    recovery=r.json()['recovery_code']
    assert c.post('/api/login',json={'name':'tester','password':'bad'}).status_code==401
    token=c.post('/api/login',json={'name':'tester','password':'long-enough-password'}).json()['token']
    h={'Authorization':'Bearer '+token}
    assert c.get('/api/me',headers=h).status_code==200
    assert c.post('/api/recover',json={'name':'tester','password':'replacement-password','recovery_code':recovery}).status_code==200
    assert c.get('/api/me',headers=h).status_code==401
    assert c.post('/api/recover',json={'name':'tester','password':'replacement-password','recovery_code':recovery}).status_code==401

def test_ticket_membership_and_cancel(service):
    m,c=service;uid,h=account(m,'alice');other,oh=account(m,'bob')
    r=c.post('/api/friends',headers=h,json={}).json()
    assert c.post('/api/ticket',headers=oh,json={'protocol':m.VERSION}).status_code==404
    t=c.post('/api/ticket',headers=h,json={'protocol':m.VERSION}).json()
    assert json.loads(t['ticket'].rsplit('|',1)[0])['account']==uid
    assert c.post('/api/queue',headers=h,json={'protocol':m.VERSION}).status_code==409
    assert c.post('/api/leave',headers=h).status_code==200
    assert c.get('/api/me',headers=h).json()['room'] is None

def test_ticket_waits_for_bound_game_listener(service,monkeypatch):
    m,c=service;uid,h=account(m,'booting')
    room=c.post('/api/friends',headers=h,json={}).json()
    monkeypatch.setenv('GODOT_BIN','configured-after-test-allocation')
    assert c.post('/api/ticket',headers=h,json={'protocol':m.VERSION}).status_code==503
    class Child:
        def poll(self):return None
    m.PROCESSES[room['id']]=Child()
    delays=[]
    def ready_after_delay(seconds):
        delays.append(seconds)
        m.atomic_json(m.ROOT/room['id']/'status.json',{'phase':'lobby'})
    monkeypatch.setattr(m.time,'sleep',ready_after_delay)
    assert c.post('/api/ticket',headers=h,json={'protocol':m.VERSION}).status_code==200
    assert delays==[.1]

def test_list_modes_join_rules_and_spectator_ticket(service):
    m,c=service;owner,oh=account(m,'owner');watcher,wh=account(m,'watcher')
    friend=c.post('/api/friends',headers=oh,json={}).json()
    ids=[account(m,'ranked'+str(i))[0] for i in range(2)]
    with m.db() as db:ranked=m.allocate(db,'ranked',ids)
    assert c.get('/api/rooms').status_code==401
    listing=c.get('/api/rooms',headers=wh).json()['rooms']
    assert [r['mode_label'] for r in listing]==['好友房','积分赛']
    assert listing[0]['joinable'] and not listing[1]['joinable']
    response=c.post('/api/spectate',headers=wh,json={'room':friend['id'],'protocol':m.VERSION})
    claims=json.loads(response.json()['ticket'].rsplit('|',1)[0])
    assert claims['role']=='spectator' and claims['account']==watcher
    assert c.get('/api/me',headers=wh).json()['room'] is None
    with m.db() as db:assert db.execute('SELECT count(*) FROM members WHERE account=?',(watcher,)).fetchone()[0]==0
    assert c.post('/api/spectate',headers=oh,json={'room':ranked['id'],'protocol':m.VERSION}).status_code==409
    m.atomic_json(m.ROOT/friend['id']/'status.json',{'phase':'hero_select'})
    assert not c.get('/api/rooms',headers=wh).json()['rooms'][0]['joinable']
    assert c.post('/api/friends',headers=wh,json={'code':friend['code']}).status_code==409

def test_permanent_leave_frees_binding_transfers_owner_and_preserves_participant(service):
    m,c=service;owner,oh=account(m,'owner');other,h=account(m,'other')
    room=c.post('/api/friends',headers=oh,json={}).json()
    c.post('/api/friends',headers=h,json={'code':room['code']})
    with m.db() as db:db.execute("UPDATE rooms SET phase='recruit' WHERE id=?",(room['id'],))
    assert c.post('/api/leave',headers=oh).status_code==409
    assert c.post('/api/leave',headers=oh,json={'room':room['id'],'permanent':True}).status_code==200
    assert c.get('/api/me',headers=oh).json()['room'] is None
    with m.db() as db:
        assert db.execute('SELECT owner FROM rooms WHERE id=?',(room['id'],)).fetchone()[0]==other
        assert db.execute('SELECT count(*) FROM members WHERE room=?',(room['id'],)).fetchone()[0]==2
    roster=json.loads((m.ROOT/room['id']/'room.json').read_text())
    assert roster['departed']==[owner]
    new=c.post('/api/friends',headers=oh,json={}).json()
    assert new['id']!=room['id']
    assert c.post('/api/leave',headers=oh,json={'room':room['id'],'permanent':True}).status_code==409
    assert c.get('/api/me',headers=oh).json()['room']['id']==new['id']
    assert c.post('/api/leave',headers=h,json={'room':room['id'],'permanent':True}).status_code==200
    assert room['id'] not in [r['id'] for r in c.get('/api/rooms',headers=h).json()['rooms']]

def test_ranked_forfeit_cannot_escape_loss_or_double_settle(service):
    m,c=service;people=[account(m,'forfeit'+str(i)) for i in range(8)];ids=[a for a,h in people]
    with m.db() as db:r=m.allocate(db,'ranked',ids)
    h=people[0][1]
    assert c.post('/api/leave',headers=h,json={'room':r['id'],'permanent':True}).status_code==200
    assert c.get('/api/me',headers=h).json()['rating']==930
    assert c.post('/api/leave',headers=h,json={'room':r['id'],'permanent':True}).status_code==200
    with m.db() as db:
        m.finalize(db,r,{'players':[{'id':uid,'rank':i+1} for i,uid in enumerate(ids)]})
        assert db.execute('SELECT rating FROM accounts WHERE id=?',(ids[0],)).fetchone()[0]==930
        assert db.execute('SELECT count(*) FROM results').fetchone()[0]==8

def test_lobby_departure_not_required_in_final_standings(service):
    m,c=service;owner,oh=account(m,'host');other,h=account(m,'left');third,th=account(m,'third')
    r=c.post('/api/friends',headers=oh,json={}).json()
    c.post('/api/friends',headers=h,json={'code':r['code']});c.post('/api/leave',headers=h)
    assert c.post('/api/friends',headers=h,json={'code':r['code']}).status_code==409
    assert c.post('/api/friends',headers=th,json={'code':r['code']}).status_code==200
    with m.db() as db:
        m.finalize(db,r,{'players':[{'id':owner,'rank':1},{'id':third,'rank':2}]})
        assert db.execute('SELECT count(*) FROM results').fetchone()[0]==2

def test_finished_or_eliminated_leave_keeps_earned_rank(service):
    m,c=service;people=[account(m,'done'+str(i)) for i in range(2)]
    with m.db() as db:r=m.allocate(db,'ranked',[p[0] for p in people])
    m.atomic_json(m.ROOT/r['id']/'status.json',{'phase':'recruit','players':[{'id':people[0][0],'rank':3}]})
    c.post('/api/leave',headers=people[0][1],json={'room':r['id'],'permanent':True})
    assert c.get('/api/me',headers=people[0][1]).json()['results'][0]['rank']==3
    m.atomic_json(m.ROOT/r['id']/'status.json',{'phase':'finished','players':[{'id':people[0][0],'rank':3},{'id':people[1][0],'rank':1}]})
    c.post('/api/leave',headers=people[1][1],json={'room':r['id'],'permanent':True})
    assert c.get('/api/me',headers=people[1][1]).json()['results'][0]['rank']==1

def test_join_rechecks_start_under_shared_admission_lock(service):
    from concurrent.futures import ThreadPoolExecutor
    m,c=service;owner,oh=account(m,'racehost');other,h=account(m,'racejoin')
    room=c.post('/api/friends',headers=oh,json={}).json()
    lock=m.ROOT/room['id']/'admission.lock';lock.mkdir()
    with ThreadPoolExecutor(max_workers=1) as pool:
        pending=pool.submit(c.post,'/api/friends',headers=h,json={'code':room['code']})
        time.sleep(.1);assert not pending.done()
        m.atomic_json(m.ROOT/room['id']/'status.json',{'phase':'hero_select'})
        lock.rmdir()
        assert pending.result(timeout=5).status_code==409
    assert c.get('/api/me',headers=h).json()['room'] is None

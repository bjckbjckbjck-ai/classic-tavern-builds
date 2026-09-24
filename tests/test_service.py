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

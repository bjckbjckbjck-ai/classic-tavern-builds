"""Three real clients: room discovery, public spectating, permanent exit/recreate."""
import asyncio,json,os,secrets
from pathlib import Path
import httpx,websockets

BASE=os.environ.get('TAVERN_TEST_BASE','https://bjckwrn.xyz:21111')
PROTO='allstars-0.61.0-service-2'
async def run():
    sockets=[];users=[]
    async with httpx.AsyncClient(base_url=BASE,timeout=20,trust_env=False) as api:
        async def call(i,path,data=None):
            headers={'Authorization':'Bearer '+users[i]['token']} if i is not None else {}
            r=await (api.get(path,headers=headers) if data is None else api.post(path,headers=headers,json=data))
            r.raise_for_status();return r.json()
        async def open_ticket(ticket):
            url=os.environ.get('TAVERN_TEST_WS',BASE.replace('https','wss').replace('http:','ws:')+'/play/{slot}').format(slot=ticket['slot'])
            ws=await websockets.connect(url,max_size=16*1024*1024,proxy=None,close_timeout=1)
            sockets.append(ws);await ws.send(json.dumps({'ticket':ticket['ticket']}));return ws
        async def state(ws,predicate=lambda s:True):
            async def receive():
                while True:
                    p=json.loads(await ws.recv())
                    if p.get('type')=='state' and predicate(p['state']):return p['state']
            return await asyncio.wait_for(receive(),20)
        serial={}
        async def act(ws,action,index=-1,s=None):
            serial[ws]=serial.get(ws,0)+1
            guard={} if not s else dict(serial=s['me'].get('action_serial',0),action=action,index=index,aim=-1,source=s['me']['shop'][index]['uid'] if action=='buy' else '',target='')
            await ws.send(json.dumps(dict(type='action',serial=serial[ws],action=action,index=index,target=-1,guard=guard)))
        saved=Path(__file__).resolve().parents[1]/'secrets/rooms-qa-users.json'
        reuse=json.loads(saved.read_text()) if os.environ.get('TAVERN_QA_REUSE')=='1' else []
        for i in range(3):
            user=reuse[i] if reuse else {'name':'qa_'+secrets.token_hex(4),'password':secrets.token_urlsafe(20)}
            if not reuse:
                r=await api.post('/api/register',json=user);r.raise_for_status()
            r=await api.post('/api/login',json=user);r.raise_for_status();user.update(r.json());users.append(user)
        (Path(__file__).resolve().parents[1]/'secrets/rooms-qa-users.json').write_text(json.dumps(users),encoding='utf-8')
        try:
            room=await call(0,'/api/friends',{})
            await call(1,'/api/friends',{'code':room['code']})
            listing=(await call(2,'/api/rooms'))['rooms'];entry=next(r for r in listing if r['id']==room['id'])
            assert entry['mode_label']=='好友房' and entry['human_count']==2 and entry['joinable']
            players=[await open_ticket(await call(i,'/api/ticket',{'protocol':PROTO})) for i in range(2)]
            s0=await state(players[0],lambda s:len(s['players'])==2);s1=await state(players[1])
            observer=await open_ticket(await call(2,'/api/spectate',{'protocol':PROTO,'room':room['id']}))
            view=await state(observer);assert view['spectating'] and view['me']['hero_offers']==[]
            await act(players[0],'room_start')
            for ws in players:
                s=await state(ws,lambda s:s['phase']=='hero_select');await act(ws,'hero',int(s['me']['hero_offers'][0]),s)
            s0=await state(players[0],lambda s:s['phase']=='recruit')
            s1=await state(players[1],lambda s:s['phase']=='recruit')
            await act(players[0],'buy',0,s0)
            s0=await state(players[0],lambda s:bool(s['me']['hand']))
            view=await state(observer,lambda s:s['phase']=='recruit')
            assert view['me']['hand']==[] and view['me']['shop']==[] and view['me']['discover']==[]
            await act(observer,'ready');view=await state(observer,lambda s:s['phase']=='recruit')
            assert not next(p for p in view['players'] if p['id']==s0['me']['id'])['ready']
            await act(observer,'spectate',s1['me']['id'])
            view=await state(observer,lambda s:s['watch_id']==s1['me']['id']);assert view['spectating']
            unused=await call(0,'/api/ticket',{'protocol':PROTO})
            await call(0,'/api/leave',{'room':room['id'],'permanent':True})
            assert (await call(0,'/api/me'))['room'] is None
            new=await call(0,'/api/friends',{});assert new['id']!=room['id']
            await state(players[1],lambda s:any(p['id']==s0['me']['id'] and p['bot'] for p in s['players']))
            rejected=await open_ticket(unused)
            packet=json.loads(await asyncio.wait_for(rejected.recv(),5));assert packet['type']=='error'
            assert (await call(2,'/api/me'))['room'] is None
            await call(1,'/api/leave',{'room':room['id'],'permanent':True})
            assert room['id'] not in [r['id'] for r in (await call(2,'/api/rooms'))['rooms']]
            await call(0,'/api/leave',{'room':new['id'],'permanent':True})
            print(json.dumps(dict(room_listing=True,public_spectator=True,private_zones_hidden=True,read_only=True,switch_view=True,permanent_exit=True,recreate=True,revoked_unused_ticket=True,last_player_releases_table=True)))
        finally:
            for ws in sockets:await ws.close()
            for i in range(len(users)):
                try:
                    me=await call(i,'/api/me')
                    if me['room']:await call(i,'/api/leave',{'room':me['room']['id'],'permanent':True})
                except Exception:pass

asyncio.run(run())

"""Real HTTPS/WSS test; generated credentials stay under ignored secrets/."""
import asyncio,json,secrets,time,os
from pathlib import Path
import httpx,websockets
BASE=os.environ.get('TAVERN_TEST_BASE','https://bjckwrn.xyz:21111')
PROTO='allstars-0.61.0-service-2'
root=Path(__file__).resolve().parents[1]
async def run():
    users=[]
    async with httpx.AsyncClient(base_url=BASE,timeout=25,trust_env=False) as api:
        for n in range(2):
            user={'name':'qa_'+secrets.token_hex(4),'password':secrets.token_urlsafe(20)}
            r=await api.post('/api/register',json=user);r.raise_for_status();user.update(r.json())
            r=await api.post('/api/login',json=user);r.raise_for_status();user.update(r.json())
            users.append(user)
        (root/'secrets/live-users.json').write_text(json.dumps(users),encoding='utf-8')
        def headers(i):return {'Authorization':'Bearer '+users[i]['token']}
        r=await api.post('/api/friends',headers=headers(0),json={});r.raise_for_status();room=r.json()
        await asyncio.sleep(2)
        r=await api.post('/api/friends',headers=headers(1),json={'code':room['code']});r.raise_for_status()
        sockets=[]
        async def connect(i):
            r=await api.post('/api/ticket',headers=headers(i),json={'protocol':PROTO});r.raise_for_status();t=r.json()
            ws=await websockets.connect(os.environ.get('TAVERN_TEST_WS',BASE.replace('https','wss')+'/play/{slot}').format(slot=t['slot']),max_size=16*1024*1024,proxy=None,close_timeout=2)
            await ws.send(json.dumps({'ticket':t['ticket']}))
            return ws
        async def state(ws,predicate=lambda s:True):
            async def receive():
                while True:
                    msg=json.loads(await ws.recv())
                    if msg.get('type') in ['error','notice']:raise AssertionError(msg['message'])
                    if msg.get('type')=='state' and predicate(msg['state']):return msg['state']
            return await asyncio.wait_for(receive(),35)
        serials={}
        async def act(ws,action,index=-1,target=-1,s=None):
            serials[ws]=serials.get(ws,0)+1
            guard={}
            if s:
                source=s['me']['shop'][index]['uid'] if action=='buy' else ''
                guard=dict(serial=s['me'].get('action_serial',0),action=action,index=index,aim=target,source=source,target='')
            await ws.send(json.dumps(dict(type='action',serial=serials[ws],action=action,index=index,target=target,guard=guard)))
        try:
            for i in range(2):sockets.append(await connect(i))
            s0=await state(sockets[0],lambda s:len(s['players'])==2)
            s1=await state(sockets[1]);uid=s1['me']['id']
            assert s0['me']['id']!=uid
            assert all('hand' not in p and 'shop' not in p for p in s0['players'])
            assert s0['phase']=='lobby'
            await act(sockets[0],'room_start')
            s0=await state(sockets[0],lambda s:s['phase']=='hero_select')
            s1=await state(sockets[1],lambda s:s['phase']=='hero_select')
            for i,s in enumerate([s0,s1]):await act(sockets[i],'hero',int(s['me']['hero_offers'][0]),s=s)
            s0=await state(sockets[0],lambda s:s['phase']=='recruit')
            s1=await state(sockets[1],lambda s:s['phase']=='recruit')
            await act(sockets[0],'ready',s=s0);await act(sockets[1],'ready',s=s1)
            s0=await state(sockets[0],lambda s:s['phase']=='combat')
            s1=await state(sockets[1],lambda s:s['phase']=='combat')
            await act(sockets[0],'replay_done',s0['round'])
            s0=await state(sockets[0],lambda s:s['phase']=='recruit')
            assert s0['round']==2
            still=await state(sockets[1]);assert still['phase']=='combat' and still['round']==1
            coins=s0['me']['coins']
            await act(sockets[0],'buy',0,s=s0)
            s0=await state(sockets[0],lambda s:s['phase']=='recruit' and len(s['me']['hand'])>0)
            assert s0['me']['coins']<coins
            await act(sockets[1],'replay_done',s1['round'])
            s1=await state(sockets[1],lambda s:s['phase']=='recruit')
            await sockets[1].close();await asyncio.sleep(1)
            s0=await state(sockets[0],lambda s:any(p['id']==uid and p['bot'] for p in s['players']))
            await act(sockets[0],'ready',s=s0)
            await state(sockets[0],lambda s:s['phase'] in ['combat','finished'])
            sockets[1]=await connect(1)
            s1=await state(sockets[1],lambda s:s['phase'] in ['recruit','combat','finished'])
            assert s1['me']['id']==uid and not s1['me']['bot']
            assert s1['me']['coin_cap']==10
            print(json.dumps({'https_login':True,'start_then_hero_draft':True,'private_snapshots':True,'independent_recruit_purchase':True,'reconnect_same_seat':True,'takeover_without_boss_perks':True,'room_id':room['id']},ensure_ascii=False))
        finally:
            for ws in sockets:await ws.close()
asyncio.run(run())

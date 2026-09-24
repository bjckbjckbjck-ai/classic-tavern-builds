"""Real HTTPS/WSS test; generated credentials stay under ignored secrets/."""
import asyncio,json,secrets,time
from pathlib import Path
import httpx,websockets
BASE='https://bjckwrn.xyz'
PROTO='allstars-0.61.0-service-1'
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
            ws=await websockets.connect(BASE.replace('https','wss')+'/play/'+str(t['slot']),max_size=16*1024*1024,proxy=None,close_timeout=2)
            await ws.send(json.dumps({'ticket':t['ticket']}))
            return ws
        async def state(ws,predicate=lambda s:True):
            async def receive():
                while True:
                    msg=json.loads(await ws.recv())
                    if msg.get('type') in ['error','notice']:raise AssertionError(msg['message'])
                    if msg.get('type')=='state' and predicate(msg['state']):return msg['state']
            return await asyncio.wait_for(receive(),35)
        async def act(ws,serial,action,index=-1,target=-1,guard=None):
            await ws.send(json.dumps(dict(type='action',serial=serial,action=action,index=index,target=target,guard=guard or {})))
        def ready_guard(s):return dict(serial=s['me'].get('action_serial',0),action='ready',index=-1,aim=-1,source='',target='')
        try:
            for i in range(2):sockets.append(await connect(i))
            s0=await state(sockets[0],lambda s:len(s['players'])==2)
            s1=await state(sockets[1]);uid=s1['me']['id']
            assert s0['me']['id']!=uid
            assert all('hand' not in p and 'shop' not in p for p in s0['players'])
            await act(sockets[0],1,'room_start')
            s0=await state(sockets[0],lambda s:s['phase']=='recruit')
            s1=await state(sockets[1],lambda s:s['phase']=='recruit')
            await sockets[1].close();await asyncio.sleep(1)
            s0=await state(sockets[0],lambda s:any(p['id']==uid and p['bot'] for p in s['players']))
            await act(sockets[0],2,'ready',guard=ready_guard(s0))
            await state(sockets[0],lambda s:s['phase'] in ['combat','finished'])
            sockets[1]=await connect(1)
            s1=await state(sockets[1],lambda s:s['phase'] in ['combat','finished'])
            assert s1['me']['id']==uid and not s1['me']['bot']
            assert s1['me']['coin_cap']==10 and s1['me']['board']
            print(json.dumps({'https_login':True,'friend_join':True,'private_snapshots':True,'reconnect_same_seat':True,'takeover_without_boss_perks':True,'combat_phase':s1['phase'],'room_id':room['id']},ensure_ascii=False))
        finally:
            for ws in sockets:await ws.close()
asyncio.run(run())

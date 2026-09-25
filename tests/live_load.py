import asyncio,json,time
from pathlib import Path
import httpx,websockets
root=Path(__file__).resolve().parents[1]
PROTO='allstars-0.61.0-service-1';BASE='https://bjckwrn.xyz:21111'
users=json.loads((root/'secrets/load-users.json').read_text())
async def run():
    roomids=set();slots=set();messages=0;wire_bytes=0;phases=set();clients=0
    async with httpx.AsyncClient(base_url=BASE,timeout=25,trust_env=False) as api:
        for u in users:
            h={'Authorization':'Bearer '+u['token']}
            current=await api.get('/api/me',headers=h);current.raise_for_status()
            if current.json()['room'] is None and current.json()['queue'] is None:
                r=await api.post('/api/queue',headers=h,json={'protocol':PROTO});r.raise_for_status()
        await asyncio.sleep(3)
        assigned=[]
        for u in users:
            h={'Authorization':'Bearer '+u['token']}
            r=await api.get('/api/me',headers=h);r.raise_for_status();data=r.json()
            if data['room']:
                roomids.add(data['room']['id']);slots.add(data['room']['slot'])
                t=await api.post('/api/ticket',headers=h,json={'protocol':PROTO});t.raise_for_status();assigned.append((u,t.json()))
        assert len(assigned)==32 and len(roomids)==4 and slots=={1,2,3,4},(len(assigned),len(roomids))
        async def client(u,t):
            nonlocal messages,wire_bytes,clients
            async with websockets.connect(BASE.replace('https','wss')+'/play/'+str(t['slot']),max_size=16*1024*1024,close_timeout=2,proxy=None) as ws:
                await ws.send(json.dumps({'ticket':t['ticket']}));clients+=1
                async def heartbeat():
                    while True:await asyncio.sleep(8);await ws.send('{"type":"ping"}')
                beat=asyncio.create_task(heartbeat());end=time.monotonic()+120;ready=set();serial=0
                try:
                    while time.monotonic()<end:
                        try:raw=await asyncio.wait_for(ws.recv(),12)
                        except TimeoutError:continue
                        messages+=1;wire_bytes+=len(raw.encode() if isinstance(raw,str) else raw)
                        msg=json.loads(raw)
                        if msg.get('type')=='error':raise AssertionError(msg)
                        if msg.get('type')!='state':continue
                        s=msg['state'];phases.add(s['phase']);assert s['me']['id']==u['id']
                        assert all('hand' not in p and 'shop' not in p for p in s['players'])
                        if s['phase']=='recruit' and s['round'] not in ready:
                            ready.add(s['round']);serial+=1
                            guard=dict(serial=s['me'].get('action_serial',0),action='ready',index=-1,aim=-1,source='',target='')
                            await ws.send(json.dumps(dict(type='action',serial=serial,action='ready',index=-1,target=-1,guard=guard)))
                finally:beat.cancel()
        await asyncio.gather(*(client(u,t) for u,t in assigned))
        result=dict(clients=clients,tables=len(roomids),extra_player_waited=True,duration_seconds=120,messages=messages,application_bytes=wire_bytes,phases=sorted(phases))
        (root/'runtime/live-load.json').write_text(json.dumps(result,indent=2))
        print(json.dumps(result))
asyncio.run(run())

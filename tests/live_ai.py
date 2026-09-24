import asyncio,json,time
from pathlib import Path
import httpx,websockets
root=Path(__file__).resolve().parents[1];u=json.loads((root/'secrets/load-users.json').read_text())[-1]
BASE='https://bjckwrn.xyz';PROTO='allstars-0.61.0-service-1';h={'Authorization':'Bearer '+u['token']}
async def run():
    async with httpx.AsyncClient(base_url=BASE,headers=h,timeout=20,trust_env=False) as c:
        r=await c.post('/api/queue',json={'protocol':PROTO});r.raise_for_status()
        r=await c.post('/api/queue',json={'protocol':PROTO,'consent':True});assert r.status_code==400
        await asyncio.sleep(61)
        r=await c.get('/api/me');r.raise_for_status();assert r.json()['room'] is None and not r.json()['queue']['ai_consent']
        r=await c.post('/api/queue',json={'protocol':PROTO,'consent':True});r.raise_for_status()
        await asyncio.sleep(2)
        r=await c.post('/api/ticket',json={'protocol':PROTO});r.raise_for_status();t=r.json()
        async with websockets.connect(BASE.replace('https','wss')+'/play/'+str(t['slot']),max_size=16*1024*1024,close_timeout=2,proxy=None) as ws:
            await ws.send(json.dumps({'ticket':t['ticket']}))
            async with asyncio.timeout(40):
                while True:
                    msg=json.loads(await ws.recv())
                    if msg.get('type')=='state' and msg['state']['phase']=='recruit':
                        s=msg['state'];assert s['ai_difficulty']==3 and len(s['players'])==8
                        assert sum(p['bot'] for p in s['players'])==7
                        print(json.dumps({'waited_60_seconds':True,'no_automatic_consent':True,'early_consent_rejected':True,'highest_ai':True,'humans':1,'bots':7,'phase':s['phase']}));break
asyncio.run(run())

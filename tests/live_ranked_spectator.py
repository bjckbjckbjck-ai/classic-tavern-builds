"""Ranked spectator check using the preceding live_rooms QA accounts."""
import asyncio,json,os
from pathlib import Path
import httpx,websockets

async def run():
    users=json.loads((Path(__file__).resolve().parents[1]/'secrets/rooms-qa-users.json').read_text())
    async with httpx.AsyncClient(base_url=os.environ.get('TAVERN_TEST_BASE','http://127.0.0.1:18082'),timeout=20,trust_env=False) as api:
        async def post(i,path,data):
            r=await api.post(path,headers={'Authorization':'Bearer '+users[i]['token']},json=data);r.raise_for_status();return r.json()
        for i in range(2):await post(i,'/api/queue',{'protocol':'allstars-0.61.0-service-2'})
        print('Waiting real 61 seconds for explicit AI consent',flush=True)
        await asyncio.sleep(61)
        for i in range(2):await post(i,'/api/queue',{'protocol':'allstars-0.61.0-service-2','consent':True})
        await asyncio.sleep(2)
        r=await api.get('/api/me',headers={'Authorization':'Bearer '+users[0]['token']});r.raise_for_status();room=r.json()['room']
        assert room['mode']=='ranked'
        t=await post(2,'/api/spectate',{'protocol':'allstars-0.61.0-service-2','room':room['id']})
        async with websockets.connect(os.environ.get('TAVERN_TEST_WS','ws://127.0.0.1:1500{slot}').format(slot=t['slot']),max_size=16*1024*1024,proxy=None) as ws:
            await ws.send(json.dumps({'ticket':t['ticket']}))
            while True:
                packet=json.loads(await asyncio.wait_for(ws.recv(),10))
                if packet.get('type')=='state':break
            s=packet['state'];assert s['spectating'] and s['me']['hero_offers']==[] and len(s['players'])==8
            assert s['me']['hand']==[] and s['me']['shop']==[]
        for i in range(2):await post(i,'/api/leave',{'room':room['id'],'permanent':True})
        r=await api.get('/api/me',headers={'Authorization':'Bearer '+users[0]['token']})
        assert r.json()['rating']==965 and r.json()['room'] is None
        print('PASS ranked 2-human/6-AI public spectator, no seat, each forfeit settles once at -35')

asyncio.run(run())

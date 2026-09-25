"""Two queued humans must both consent, then share one AI-filled match."""
import asyncio,json,secrets,os
import httpx,websockets
BASE=os.environ.get('TAVERN_TEST_BASE','https://bjckwrn.xyz:21111');PROTO='allstars-0.61.0-service-2'
async def run():
    async with httpx.AsyncClient(base_url=BASE,timeout=20,trust_env=False) as c:
        headers=[]
        for _ in range(2):
            credentials={'name':'qa_'+secrets.token_hex(4),'password':secrets.token_urlsafe(20)}
            r=await c.post('/api/register',json=credentials);r.raise_for_status()
            r=await c.post('/api/login',json=credentials);r.raise_for_status()
            h={'Authorization':'Bearer '+r.json()['token']};headers.append(h)
            r=await c.post('/api/queue',headers=h,json={'protocol':PROTO});r.raise_for_status()
            r=await c.post('/api/queue',headers=h,json={'protocol':PROTO,'consent':True});assert r.status_code==400
        await asyncio.sleep(61)
        r=await c.post('/api/queue',headers=headers[0],json={'protocol':PROTO,'consent':True});r.raise_for_status()
        await asyncio.sleep(2)
        for h in headers:
            r=await c.get('/api/me',headers=h);r.raise_for_status();m=r.json()
            assert m['room'] is None and m['queue']['players']==2 and m['queue']['consenting']==1
        r=await c.post('/api/queue',headers=headers[1],json={'protocol':PROTO,'consent':True});r.raise_for_status()
        async def assigned():
            while True:
                rooms=[]
                for h in headers:
                    r=await c.get('/api/me',headers=h);r.raise_for_status();rooms.append(r.json()['room'])
                if all(rooms):
                    assert rooms[0]['id']==rooms[1]['id'];return
                await asyncio.sleep(.5)
        # Finished processes retain their port briefly; allocation is asynchronous.
        await asyncio.wait_for(assigned(),35)
        tickets=[];sockets=[]
        try:
            for h in headers:
                r=await c.post('/api/ticket',headers=h,json={'protocol':PROTO});r.raise_for_status();t=r.json();tickets.append(t)
                ws=await websockets.connect(os.environ.get('TAVERN_TEST_WS',BASE.replace('https','wss')+'/play/{slot}').format(slot=t['slot']),max_size=16*1024*1024,close_timeout=2,proxy=None)
                await ws.send(json.dumps({'ticket':t['ticket']}));sockets.append(ws)
            assert tickets[0]['room']==tickets[1]['room']
            async def recruiting(ws):
                confirmed=False
                while True:
                    msg=json.loads(await ws.recv())
                    if msg.get('type')!='state':continue
                    s=msg['state']
                    if s['phase']=='hero_select' and not confirmed:
                        chosen=int(s['me']['hero_offers'][0]);confirmed=True
                        guard=dict(serial=s['me'].get('action_serial',0),action='hero',index=chosen,aim=-1,source='',target='')
                        await ws.send(json.dumps(dict(type='action',serial=1,action='hero',index=chosen,target=-1,guard=guard)))
                    if s['phase']=='recruit':
                        assert s['ai_difficulty']==3 and len(s['players'])==8
                        assert sum(p['bot'] for p in s['players'])==6
                        return
            await asyncio.wait_for(asyncio.gather(*(recruiting(ws) for ws in sockets)),40)
            print(json.dumps({'waited_60_seconds':True,'queue_count':2,'one_consent_does_not_split':True,'same_room':True,'highest_ai':True,'humans':2,'bots':6}))
        finally:
            for ws in sockets:await ws.close()
asyncio.run(run())

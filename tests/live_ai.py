"""Two queued humans must both consent, then share one AI-filled match."""
import asyncio,json,secrets,os
from pathlib import Path
import httpx,websockets
BASE=os.environ.get('TAVERN_TEST_BASE','https://bjckwrn.xyz:21111');PROTO='allstars-0.63.1-service-4'
async def run():
    async with httpx.AsyncClient(base_url=BASE,timeout=20,trust_env=False) as c:
        headers=[];users=[]
        root=Path(__file__).resolve().parents[1]
        reuse=json.loads((root/'secrets/rooms-qa-users.json').read_text())[:2] if os.environ.get('TAVERN_QA_REUSE')=='1' else []
        for index in range(2):
            credentials=reuse[index] if reuse else {'name':'qa_'+secrets.token_hex(4),'password':secrets.token_urlsafe(20)}
            if not reuse:
                r=await c.post('/api/register',json=credentials);r.raise_for_status()
            r=await c.post('/api/login',json=credentials);r.raise_for_status()
            credentials.update(r.json());users.append(credentials)
            (root/'secrets/ai-qa-users.json').write_text(json.dumps(users),encoding='utf-8')
            h={'Authorization':'Bearer '+credentials['token']};headers.append(h)
            r=await c.post('/api/queue',headers=h,json={'protocol':'allstars-0.61.0-service-2'});assert r.status_code==409
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
                confirmed=False;serial=0
                while True:
                    msg=json.loads(await ws.recv())
                    if msg.get('type')!='state':continue
                    s=msg['state']
                    if s['phase']=='hero_select' and not confirmed:
                        chosen=int(s['me']['hero_offers'][0]);confirmed=True
                        guard=dict(serial=s['me'].get('action_serial',0),action='hero',index=chosen,aim=-1,source='',target='')
                        serial+=1
                        await ws.send(json.dumps(dict(type='action',serial=serial,action='hero',index=chosen,target=-1,guard=guard)))
                    if s['phase']=='recruit':
                        if s['me'].get('discover'):
                            serial+=1
                            guard=dict(serial=s['me'].get('action_serial',0),action='discover',index=0,aim=-1,source=s['me']['discover'][0]['uid'],target='')
                            await ws.send(json.dumps(dict(type='action',serial=serial,action='discover',index=0,target=-1,guard=guard)))
                            continue
                        assert s['ai_difficulty']==3 and len(s['players'])==8
                        assert sum(p['bot'] for p in s['players'])==6
                        assert not s['buddies_enabled'] and not s['quests_enabled'] and not s['me'].get('buddy_id')
                        return s
            states=await asyncio.wait_for(asyncio.gather(*(recruiting(ws) for ws in sockets)),40)
            identity=states[1]['me']['id'];buddy=states[1]['me'].get('buddy_id')
            await sockets[1].close();await asyncio.sleep(1)
            async def takeover():
                while True:
                    packet=json.loads(await sockets[0].recv())
                    if packet.get('type')=='state' and any(p['id']==identity and p['bot'] for p in packet['state']['players']):return
            await asyncio.wait_for(takeover(),10)
            r=await c.post('/api/ticket',headers=headers[1],json={'protocol':PROTO});r.raise_for_status();t=r.json()
            sockets[1]=await websockets.connect(os.environ.get('TAVERN_TEST_WS',BASE.replace('https','wss')+'/play/{slot}').format(slot=t['slot']),max_size=16*1024*1024,close_timeout=2,proxy=None)
            await sockets[1].send(json.dumps({'ticket':t['ticket']}))
            recovered=await asyncio.wait_for(recruiting(sockets[1]),20)
            assert recovered['me']['id']==identity and recovered['me'].get('buddy_id')==buddy and not recovered['me']['bot']
            print(json.dumps({'waited_60_seconds':True,'queue_count':2,'one_consent_does_not_split':True,'same_room':True,'highest_ai':True,'humans':2,'bots':6,'old_protocol_rejected':True,'ranked_reconnect_same_seat_optional_modes_off':True}))
        finally:
            for ws in sockets:await ws.close()
            for h in headers:
                await c.post('/api/leave',headers=h,json={'permanent':True})
                await c.post('/api/queue',headers=h,json={'protocol':PROTO,'cancel':True})
asyncio.run(run())

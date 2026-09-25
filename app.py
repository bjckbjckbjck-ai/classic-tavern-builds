"""Single-host, four-table service. Run exactly one uvicorn worker."""
import asyncio, base64, hashlib, hmac, json, os, re, secrets, sqlite3, subprocess, threading, time
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

ROOT = Path(os.environ.get('TAVERN_DATA', 'runtime')).resolve()
ROOT.mkdir(parents=True, exist_ok=True)
DB = ROOT / 'accounts.sqlite3'
VERSION = 'allstars-0.61.0-service-2'
KEY = os.environ.get('TAVERN_TICKET_KEY', '')
LOCK = threading.RLock()
PH = PasswordHasher(time_cost=2, memory_cost=19456, parallelism=1)
PROCESSES = {}
LIMITS = {}

def db():
    c = sqlite3.connect(DB, timeout=10)
    c.row_factory = sqlite3.Row
    c.execute('PRAGMA foreign_keys=ON')
    return c

def init():
    with db() as c:
        c.execute('PRAGMA journal_mode=WAL')
        c.executescript('''
        CREATE TABLE IF NOT EXISTS accounts(id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, password TEXT NOT NULL, recovery TEXT NOT NULL, rating INTEGER NOT NULL DEFAULT 1000);
        CREATE TABLE IF NOT EXISTS sessions(hash TEXT PRIMARY KEY, account INTEGER NOT NULL REFERENCES accounts(id), expires REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS rooms(id TEXT PRIMARY KEY, slot INTEGER NOT NULL, code TEXT UNIQUE, mode TEXT NOT NULL, owner INTEGER NOT NULL, phase TEXT NOT NULL, created REAL NOT NULL, updated REAL NOT NULL, config TEXT NOT NULL, result TEXT);
        CREATE UNIQUE INDEX IF NOT EXISTS active_slot ON rooms(slot) WHERE phase NOT IN ('finished','aborted');
        CREATE TABLE IF NOT EXISTS members(room TEXT NOT NULL REFERENCES rooms(id), account INTEGER NOT NULL REFERENCES accounts(id), PRIMARY KEY(room, account));
        CREATE TABLE IF NOT EXISTS queue(account INTEGER PRIMARY KEY REFERENCES accounts(id), joined REAL NOT NULL, consent INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS results(room TEXT NOT NULL, account INTEGER NOT NULL, rank INTEGER NOT NULL, delta INTEGER NOT NULL, rating INTEGER NOT NULL, PRIMARY KEY(room,account));
        ''')

def sha(value): return hashlib.sha256(value.encode()).hexdigest()
def fail(message, status=400): raise HTTPException(status, message)
def rate(request, category, maximum):
    key = (request.client.host, category)
    now = time.time()
    with LOCK:
        if len(LIMITS)>5000:
            for k in list(LIMITS):
                if now-LIMITS[k][0]>60: LIMITS.pop(k)
        at, n = LIMITS.get(key, (now, 0))
        if now-at>=60: at,n=now,0
        LIMITS[key]=(at,n+1)
    if n>=maximum: fail('请求过于频繁，请稍后再试',429)

def auth(request):
    token=request.headers.get('authorization','').removeprefix('Bearer ')
    with db() as c:
        row=c.execute('SELECT a.* FROM sessions s JOIN accounts a ON a.id=s.account WHERE s.hash=? AND s.expires>?',(sha(token),time.time())).fetchone()
    if not row: fail('登录已失效，请重新登录',401)
    return dict(row)

def active(c, account):
    return c.execute("SELECT r.* FROM rooms r JOIN members m ON m.room=r.id WHERE m.account=? AND r.phase NOT IN ('finished','aborted')",(account,)).fetchone()

def public_room(r):
    return {k:r[k] for k in ['id','slot','code','mode','phase']}

def atomic_json(path, value):
    tmp=path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8')
    tmp.replace(path)

def roster(c,r):
    directory=ROOT/r['id']; directory.mkdir(exist_ok=True)
    members=[dict(x) for x in c.execute('SELECT a.id,a.name FROM accounts a JOIN members m ON m.account=a.id WHERE m.room=? ORDER BY a.id',(r['id'],))]
    atomic_json(directory/'room.json',dict(id=r['id'],slot=r['slot'],mode=r['mode'],owner=r['owner'],members=members,created=r['created'],**json.loads(r['config'])))

def launch(c, r):
    roster(c,r)
    executable=os.environ.get('GODOT_BIN')
    if not executable: return # Tests only; production readiness rejects missing executable.
    directory=ROOT/r['id']
    with (directory/'server.log').open('ab') as log:
        PROCESSES[r['id']]=subprocess.Popen([executable,'--headless','--path',os.environ['GAME_PATH'],'--script','scripts/service_server.gd','--','--room='+str(directory),'--port='+str(15000+r['slot'])],stdout=log,stderr=subprocess.STDOUT,env=os.environ.copy())

def wait_ready(r):
    if not os.environ.get('GODOT_BIN'): return # Isolated API tests have no child server.
    until=time.monotonic()+5
    while time.monotonic()<until:
        p=PROCESSES.get(r['id'])
        if p is None or p.poll() is not None: fail('对局进程不可用，请重新连接',503)
        # Godot writes this atomically only after binding its WebSocket listener.
        if (ROOT/r['id']/'status.json').exists(): return
        time.sleep(.1)
    fail('对局正在启动，请稍后重连',503)

def allocate(c,mode,accounts):
    if (ROOT/'maintenance').exists(): fail('正在维护，暂不创建新房间',503)
    used={r[0] for r in c.execute("SELECT slot FROM rooms WHERE phase NOT IN ('finished','aborted')")}
    for rid,p in PROCESSES.items():
        if p.poll() is None:
            row=c.execute('SELECT slot FROM rooms WHERE id=?',(rid,)).fetchone()
            if row: used.add(row[0])
    slot=next((i for i in range(1,5) if i not in used),None)
    if slot is None: fail('4桌已满，请等待桌位',409)
    rid=secrets.token_hex(12); code=secrets.token_hex(4).upper(); now=time.time()
    c.execute('INSERT INTO rooms VALUES(?,?,?,?,?,?,?,?,?,NULL)',(rid,slot,code,mode,accounts[0],'lobby',now,now,json.dumps({'ai_difficulty':3,'trinkets':True,'anomaly':'random'})))
    c.executemany('INSERT INTO members VALUES(?,?)',[(rid,a) for a in accounts])
    c.executemany('DELETE FROM queue WHERE account=?',[(a,) for a in accounts])
    r=c.execute('SELECT * FROM rooms WHERE id=?',(rid,)).fetchone()
    launch(c,r)
    return r

def finalize(c,r,result):
    if c.execute('SELECT phase FROM rooms WHERE id=?',(r['id'],)).fetchone()[0] in ('finished','aborted'): return
    people=[row[0] for row in c.execute('SELECT account FROM members WHERE room=?',(r['id'],))]
    ranks={int(p['id']):int(p['rank']) for p in result.get('players',[]) if int(p.get('id',0)) in people}
    if set(ranks)!=set(people) or any(x<1 or x>8 for x in ranks.values()): raise ValueError('Incomplete final standings')
    base=[70,45,25,10,-10,-25,-45,-70]
    factor=1 if len(people)==8 else (0.5 if len(people)>1 else 0)
    if r['mode']=='friend': factor=0
    for a,rank in ranks.items():
        old=c.execute('SELECT rating FROM accounts WHERE id=?',(a,)).fetchone()[0]
        delta=int(base[rank-1]*factor); new=max(0,old+delta)
        c.execute('INSERT INTO results VALUES(?,?,?,?,?)',(r['id'],a,rank,new-old,new))
        c.execute('UPDATE accounts SET rating=? WHERE id=?',(new,a))
    c.execute("UPDATE rooms SET phase='finished',updated=?,result=? WHERE id=?",(time.time(),json.dumps(result),r['id']))

def tick():
    with LOCK, db() as c:
        now=time.time()
        for r in c.execute("SELECT * FROM rooms WHERE phase NOT IN ('finished','aborted')").fetchall():
            p=PROCESSES.get(r['id']); statusfile=ROOT/r['id']/'status.json'
            if p and p.poll() is not None:
                # Final status is read before deciding that an exit was abnormal.
                pass
            if statusfile.exists():
                try:
                    status=json.loads(statusfile.read_text(encoding='utf-8'))
                    if status.get('phase')=='finished': finalize(c,r,status); continue
                    if status.get('phase') in ['lobby','hero_select','recruit','settling','combat']:
                        c.execute('UPDATE rooms SET phase=? WHERE id=?',(status['phase'],r['id']))
                except (ValueError,OSError): pass
            if (p and p.poll() is not None) or (r['phase']=='lobby' and now-r['created']>600):
                if p and p.poll() is None: p.terminate()
                c.execute("UPDATE rooms SET phase='aborted',updated=? WHERE id=?",(now,r['id']))
        for r in c.execute("SELECT * FROM rooms WHERE phase IN ('finished','aborted')").fetchall():
            p=PROCESSES.get(r['id'])
            if p and now-r['updated']>20:
                if p.poll() is None: p.terminate()
                PROCESSES.pop(r['id'],None)
        # Never reuse a port until the preceding finished process has exited.
        if any(p.poll() is None and c.execute('SELECT phase FROM rooms WHERE id=?',(rid,)).fetchone()[0] in ('finished','aborted') for rid,p in PROCESSES.items()): return
        for _ in range(0 if (ROOT/'maintenance').exists() else 4):
            rows=c.execute('SELECT * FROM queue ORDER BY joined').fetchall()
            eligible=[x for x in rows if x['consent'] and now-x['joined']>=60]
            # A partial lobby is one cohort: do not split early consenters into solo AI games.
            selected=rows[:8] if len(rows)>=8 else (rows if rows and len(eligible)==len(rows) else [])
            if not selected: break
            if c.execute("SELECT count(*) FROM rooms WHERE phase NOT IN ('finished','aborted')").fetchone()[0]>=4: break
            allocate(c,'ranked',[x['account'] for x in selected])
        c.execute('DELETE FROM sessions WHERE expires<?',(now,))

@asynccontextmanager
async def lifespan(app):
    init()
    if not KEY or not os.environ.get('GODOT_BIN'): raise RuntimeError('Production secrets / Godot executable missing')
    with db() as c:
        c.execute("UPDATE rooms SET phase='aborted',updated=? WHERE phase NOT IN ('finished','aborted')",(time.time(),))
        c.execute('DELETE FROM queue')
    async def loop():
        while True:
            try: await asyncio.to_thread(tick)
            except Exception as e: print('supervisor_error',type(e).__name__,flush=True)
            await asyncio.sleep(1)
    task=asyncio.create_task(loop())
    yield
    task.cancel()
    for p in PROCESSES.values():
        if p.poll() is None: p.terminate()

app=FastAPI(lifespan=lifespan,docs_url=None,redoc_url=None,openapi_url=None)

@app.middleware('http')
async def limits(request,call_next):
    if int(request.headers.get('content-length','0') or 0)>16384: return HTMLResponse('Request too large',413)
    response=await call_next(request)
    response.headers['Cache-Control']='no-store'
    response.headers['X-Content-Type-Options']='nosniff'
    return response

@app.get('/api/health')
def health(): return {'status':'ok','protocol':VERSION,'tables':4,'game':'0.61.0','service':'0.2.0-preview'}

@app.post('/api/register')
def register(request:Request, body:dict):
    rate(request,'register',5)
    name=str(body.get('name','')).strip().lower(); password=str(body.get('password',''))
    if not re.fullmatch(r'[a-z0-9_]{3,24}',name): fail('账号限3—24位英文字母、数字或下划线')
    if not 10<=len(password)<=128: fail('密码长度10—128位')
    recovery=secrets.token_urlsafe(24)
    hashed=PH.hash(password)
    try:
        with LOCK,db() as c: c.execute('INSERT INTO accounts(name,password,recovery) VALUES(?,?,?)',(name,hashed,sha(recovery)))
    except sqlite3.IntegrityError: fail('该账号不可用',409)
    return {'ok':True,'recovery_code':recovery}

@app.post('/api/login')
def login(request:Request,body:dict):
    rate(request,'login',15)
    with db() as c: a=c.execute('SELECT * FROM accounts WHERE name=?',(str(body.get('name','')).strip().lower(),)).fetchone()
    try:
        if not a or not PH.verify(a['password'],str(body.get('password',''))): fail('账号或密码错误',401)
    except VerificationError: fail('账号或密码错误',401)
    token=secrets.token_urlsafe(32)
    with LOCK,db() as c:
        c.execute('DELETE FROM sessions WHERE account=?',(a['id'],))
        c.execute('INSERT INTO sessions VALUES(?,?,?)',(sha(token),a['id'],time.time()+86400))
    return {'token':token,'name':a['name'],'rating':a['rating']}

@app.post('/api/recover')
def recover(request:Request,body:dict):
    rate(request,'recover',5)
    password=str(body.get('password',''))
    if not 10<=len(password)<=128: fail('密码长度10—128位')
    hashed=PH.hash(password); recovery=secrets.token_urlsafe(24)
    with LOCK,db() as c:
        a=c.execute('SELECT id FROM accounts WHERE name=? AND recovery=?',(str(body.get('name','')).lower(),sha(str(body.get('recovery_code',''))))).fetchone()
        if not a: fail('恢复信息不正确',401)
        c.execute('UPDATE accounts SET password=?,recovery=? WHERE id=?',(hashed,sha(recovery),a['id']))
        c.execute('DELETE FROM sessions WHERE account=?',(a['id'],))
    return {'ok':True,'recovery_code':recovery}

@app.post('/api/logout')
def logout(request:Request):
    auth(request)
    with LOCK,db() as c: c.execute('DELETE FROM sessions WHERE hash=?',(sha(request.headers['authorization'].removeprefix('Bearer ')),))
    return {'ok':True}

@app.get('/api/me')
def me(request:Request):
    a=auth(request)
    with LOCK,db() as c:
        r=active(c,a['id']); q=c.execute('SELECT * FROM queue WHERE account=?',(a['id'],)).fetchone()
        results=[dict(x) for x in c.execute('SELECT * FROM results WHERE account=? ORDER BY rowid DESC LIMIT 10',(a['id'],))]
        waiting=c.execute('SELECT count(*),coalesce(sum(consent),0) FROM queue').fetchone()
    return {'name':a['name'],'rating':a['rating'],'room':public_room(r) if r else None,'queue':{'seconds':int(time.time()-q['joined']),'ai_consent':bool(q['consent']),'players':waiting[0],'consenting':waiting[1]} if q else None,'results':results}

@app.post('/api/friends')
def friends(request:Request,body:dict):
    rate(request,'rooms',20); a=auth(request)
    with LOCK,db() as c:
        if active(c,a['id']): fail('请先恢复或结束当前对局',409)
        if c.execute('SELECT 1 FROM queue WHERE account=?',(a['id'],)).fetchone(): fail('请先取消匹配',409)
        code=str(body.get('code','')).strip().upper()
        if not code: r=allocate(c,'friend',[a['id']])
        else:
            r=c.execute("SELECT * FROM rooms WHERE code=? AND mode='friend' AND phase='lobby'",(code,)).fetchone()
            if not r: fail('房间不存在或已经开局',404)
            if c.execute('SELECT count(*) FROM members WHERE room=?',(r['id'],)).fetchone()[0]>=8: fail('房间已满',409)
            # Refuse late joins after the game process has already started.
            statuspath=ROOT/r['id']/'status.json'
            if statuspath.exists() and json.loads(statuspath.read_text())['phase']!='lobby': fail('房间已经开局',409)
            c.execute('INSERT INTO members VALUES(?,?)',(r['id'],a['id']))
            roster(c,r)
    return public_room(r)

@app.post('/api/queue')
def queue(request:Request,body:dict):
    rate(request,'queue',40); a=auth(request)
    if body.get('protocol')!=VERSION: fail('客户端版本不一致，请更新',409)
    if (ROOT/'maintenance').exists() and not body.get('cancel'): fail('维护期间暂停匹配',503)
    with LOCK,db() as c:
        if active(c,a['id']): fail('已有进行中的对局',409)
        if body.get('cancel'):
            c.execute('DELETE FROM queue WHERE account=?',(a['id'],)); return {'ok':True}
        q=c.execute('SELECT * FROM queue WHERE account=?',(a['id'],)).fetchone()
        if not q: c.execute('INSERT INTO queue VALUES(?,?,0)',(a['id'],time.time()))
        elif 'consent' in body:
            if time.time()-q['joined']<60: fail('等待满60秒后才能选择AI')
            c.execute('UPDATE queue SET consent=? WHERE account=?',(int(body['consent'] is True),a['id']))
    return {'ok':True}

@app.post('/api/ticket')
def ticket(request:Request,body:dict):
    rate(request,'ticket',60); a=auth(request)
    if body.get('protocol')!=VERSION: fail('客户端版本不一致',409)
    with LOCK,db() as c: r=active(c,a['id'])
    if not r: fail('没有进行中的房间',404)
    wait_ready(r)
    payload=json.dumps({'room':r['id'],'account':a['id'],'exp':int(time.time()+45),'nonce':secrets.token_hex(16),'protocol':VERSION},separators=(',',':'))
    signature=hmac.new(KEY.encode(),payload.encode(),hashlib.sha256).hexdigest()
    return {'ticket':payload+'|'+signature,'slot':r['slot'],'room':r['id'],'code':r['code']}

@app.post('/api/leave')
def leave(request:Request):
    a=auth(request)
    with LOCK,db() as c:
        r=active(c,a['id'])
        if not r: return {'ok':True}
        if r['phase']!='lobby' or r['mode']!='friend': fail('已开局不能释放席位，离线期间托管至终局',409)
        statuspath=ROOT/r['id']/'status.json'
        if statuspath.exists() and json.loads(statuspath.read_text())['phase']!='lobby': fail('已经开局',409)
        c.execute('DELETE FROM members WHERE room=? AND account=?',(r['id'],a['id']))
        other=c.execute('SELECT account FROM members WHERE room=? ORDER BY account',(r['id'],)).fetchone()
        if not other:
            c.execute("UPDATE rooms SET phase='aborted',updated=? WHERE id=?",(time.time(),r['id']))
            p=PROCESSES.get(r['id'])
            if p and p.poll() is None: p.terminate()
        else:
            if r['owner']==a['id']: c.execute('UPDATE rooms SET owner=? WHERE id=?',(other[0],r['id']))
            roster(c,c.execute('SELECT * FROM rooms WHERE id=?',(r['id'],)).fetchone())
    return {'ok':True}

@app.get('/',response_class=HTMLResponse)
def index():
    return '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>经典酒馆</title><style>body{background:#211a16;color:#f7deb1;font:20px system-ui;max-width:760px;margin:60px auto;padding:24px}a{color:#ffc969}</style><h1>经典酒馆 · 云端酒馆</h1><p>固定4桌 · 好友房间 · 在线匹配 · 断线托管</p><p>服务化预览版，需要专用客户端。</p><p><a href="/downloads/ClassicTavern-Service.exe">Windows 客户端</a></p><p><a href="/downloads/ClassicTavern-Service.apk">Android 客户端</a></p><p>账号在游戏内注册；请保存注册时的恢复码。</p>'

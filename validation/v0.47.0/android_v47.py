import subprocess,time,sys
from pathlib import Path
adb='C:/Users/16073/AppData/Local/Android/Sdk/platform-tools/adb.exe'
def run(*args):return subprocess.run([adb,'-s','emulator-5554',*map(str,args)],check=True,capture_output=True)
def point(x,y):return str(round(x*1.2)),str(round(y*1.2))
def tap(x,y):run('shell','input','tap',*point(x,y));time.sleep(.7)
def swipe(a,b,duration=650):run('shell','input','swipe',*point(*a),*point(*b),str(duration));time.sleep(1)
def shot(name):Path('screenshots/v47-android-'+name+'.png').write_bytes(run('exec-out','screencap','-p').stdout)
def mode(value):Path('.runtime/v47-device-command.txt').write_text(value,encoding='utf-8');time.sleep(1)
if __name__=='__main__':
    if sys.argv[1]=='shot':shot(sys.argv[2])
    elif sys.argv[1]=='tap':tap(float(sys.argv[2]),float(sys.argv[3]));shot(sys.argv[4])
    elif sys.argv[1]=='swipe':swipe((float(sys.argv[2]),float(sys.argv[3])),(float(sys.argv[4]),float(sys.argv[5])),int(sys.argv[7]) if len(sys.argv)>7 else 650);shot(sys.argv[6])
    elif sys.argv[1]=='mode':mode(sys.argv[2]);shot(sys.argv[2])

from android_v47 import run,shot
from pathlib import Path
from PIL import Image
from io import BytesIO
import time,sys,json
size=Image.open(BytesIO(run('exec-out','screencap','-p').stdout)).size
scale=size[1]/900;offset=(size[0]/scale-1440)/2
def tap(x,y,center=True):
    run('shell','input','tap',round((x+(offset if center else 0))*scale),round(y*scale));time.sleep(.6)
def swipe(a,b,duration=600,center=True):
    run('shell','input','swipe',round((a[0]+(offset if center else 0))*scale),round(a[1]*scale),round((b[0]+(offset if center else 0))*scale),round(b[1]*scale),duration);time.sleep(.8)
if __name__=='__main__':
    action=sys.argv[1]
    if action=='shot':shot(sys.argv[2]);print(size,scale,offset)
    elif action=='tap':tap(float(sys.argv[2]),float(sys.argv[3]),'absolute' not in sys.argv);shot(sys.argv[4])
    elif action=='text':run('shell','input','text',sys.argv[2]);time.sleep(.4);run('shell','input','keyevent',4);time.sleep(.4);shot(sys.argv[3])

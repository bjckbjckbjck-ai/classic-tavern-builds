from qa_v47 import *
import subprocess
from android_v47 import adb
record=subprocess.Popen([adb,'-s','emulator-5554','shell','screenrecord','--time-limit','55','/sdcard/v47-book.mp4'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
Path('.runtime/v47-record-pid.txt').write_text(str(record.pid))
tap(924,510);shot('cards')
tap(872,809);shot('cards-next')
tap(1230,232);run('shell','input','text','1/1');time.sleep(.5);run('shell','input','keyevent',4);time.sleep(.4);shot('search')
tap(1230,616);tap(420,83);shot('heroes')
tap(290,324);shot('hero-detail');tap(715,542)
tap(610,83);shot('spells');tap(240,331);shot('spell-detail');tap(1300,737)
tap(809,83);shot('trinkets');tap(1230,111);shot('trinkets-return')
tap(1225,805);shot('book-return-menu')
print('BOOK ACTIONS COMPLETE',flush=True)

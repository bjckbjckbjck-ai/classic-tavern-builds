from qa_v47 import *
tap(1620,50,False);time.sleep(1.5);shot('book-before-one-return')
run('shell','input','tap',round((1225+offset)*scale),round(805*scale))
start=time.monotonic()
marks=[]
for target in [.3,1.5,3.0]:
    time.sleep(max(0,target-(time.monotonic()-start)))
    shot('return-'+str(target).replace('.','_')+'s')
    marks.append({'seconds_after_single_return':round(time.monotonic()-start,3),'target':target})
Path('.runtime/v47-return-timing.json').write_text(json.dumps(marks,indent=2))
print(marks,flush=True)

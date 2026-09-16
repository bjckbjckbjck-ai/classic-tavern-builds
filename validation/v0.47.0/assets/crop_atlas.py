"""Crop the approved four-cell atlas without stretching objects or changing their art."""
from pathlib import Path
import json, shutil
from itertools import groupby
from PIL import Image
root=Path(__file__).resolve().parents[2]
folder=root/'references/v47'; target=root/'assets/generated/v47'; target.mkdir(parents=True,exist_ok=True)
source=folder/'ui-atlas.png'
if not source.exists():
    shutil.copy2(Path('C:/Users/16073/.codex/generated_images/01a0823b-21f6-7d60-88a6-8136ceb32f4a/exec-15f50988-4e4b-49e6-adbc-c72038bb248f.png'),source)
im=Image.open(source).convert('RGBA'); w,h=im.size; result=[]
for index,name in enumerate(['foyer_board','collection_book','wood_button','seat_frame']):
    x=index%2*w//2; y=index//2*h//2; cell=im.crop((x,y,x+w//2,y+h//2)); a=cell.getchannel('A'); px=a.load()
    # Ignore isolated generation specks in transparent gutters; leave edge antialiasing intact.
    rows=[j for j in range(cell.height) if sum(px[i,j]>32 for i in range(cell.width))>8]
    cols=[i for i in range(cell.width) if sum(px[i,j]>32 for j in range(cell.height))>8]
    def main_run(values):
        return max(([v for _,v in group] for _,group in groupby(enumerate(values),lambda pair:pair[1]-pair[0])),key=len)
    rows=main_run(rows); cols=main_run(cols)
    box=(max(0,min(cols)-3),max(0,min(rows)-3),min(cell.width,max(cols)+4),min(cell.height,max(rows)+4))
    out=cell.crop(box)
    if name=='wood_button':out=out.resize((304,83),Image.Resampling.LANCZOS)
    out.save(target/(name+'.webp'),'WEBP',quality=94,method=6)
    result.append({'id':name,'grid_cell':[x,y,w//2,h//2],'crop_in_cell':box,'size':out.size})
(folder/'atlas-map.json').write_text(json.dumps({'source_size':im.size,'assets':result},indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))

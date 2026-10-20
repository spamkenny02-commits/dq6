from pathlib import Path
import json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;O=R/'dq6-fr/v0.48'
rv=json.loads((O/'revue-lot-v048.json').read_text());sel={x['id']:x for x in json.loads((O/'insertion-candidates.json').read_text())}
rows=[]
for x in rv:
 for page in range(1,(len(sel[x['id']]['lines'])+2)//3+1):
  f=O/f'screenshots/v048-{x["id"]}-page{page}.png'
  if not f.exists():break
  rows.append((x['id'],page,f))
for no in range((len(rows)+23)//24):
 im=Image.new('RGB',(1488,768),'#eee');d=ImageDraw.Draw(im)
 for k,(mid,page,f) in enumerate(rows[no*24:no*24+24]):
  pic=Image.open(f);pic.load();pic=pic.crop((0,432,744,648)).resize((372,108));x=k%4*372;y=k//4*128;im.paste(pic,(x,y+20));d.text((x+8,y+3),f'{mid} / {page}',fill='black')
 im.save(R/f'qa48-{no}.jpg',quality=92)
print(len(rows),'captured pages,', (len(rows)+23)//24,'contact sheets')

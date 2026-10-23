"""Build private review sheets from the capture hashes listed in a QA report."""
from pathlib import Path
import argparse,json,hashlib
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--report',required=True,type=Path);p.add_argument('--batch',type=int,default=16);a=p.parse_args();rows=json.loads(a.report.read_text())['results']
for n in range((len(rows)+a.batch-1)//a.batch):
 group=rows[n*a.batch:n*a.batch+a.batch];out=Image.new('RGB',(1536,230*((len(group)+1)//2)),'#ddd');d=ImageDraw.Draw(out)
 for k,r in enumerate(group):
  page=r['pages'][-1];f=a.out/page['capture'];assert hashlib.sha256(f.read_bytes()).hexdigest()==page['sha256'];out.paste(Image.open(f).crop((0,432,768,648)),(k%2*768,k//2*230+14));d.text((k%2*768,k//2*230),str(r['id']),fill='black')
 out.save(a.out/f'{a.report.stem}-sheet-{n:02}.png')

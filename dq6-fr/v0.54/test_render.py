"""Diagnostic camp rendering for every reviewed v0.54 addition."""
from pathlib import Path
import argparse,json,subprocess,sys,math,hashlib,shutil
ap=argparse.ArgumentParser();ap.add_argument('--camp-state',required=True,type=Path);ap.add_argument('--ids',default='');ap.add_argument('--report',default='qa-render-fixtures.json');a=ap.parse_args();O=Path(__file__).resolve().parent;P=O.parent;E=P/'emulator-tests';sys.path.insert(0,str(O));from native_helpers import encode
review=json.loads((O/'revue-lot-v054.json').read_text());ids=[x['id'] for x in review];ids=list(map(int,a.ids.split(','))) if a.ids else ids;subprocess.run([sys.executable,str(O/'render_fixtures.py'),'v0.54',','.join(map(str,ids))],check=True)
rows={x['id']:x for x in json.loads((O/'insertion-candidates.json').read_text())};out=[];S=O/'screenshots';S.mkdir(exist_ok=True)
for mid in ids:
 sid=0x8f9 if mid in [6417,6562,6565] else 0x9a7 if mid in [6351,6378,6528,6538,6543,6651] else 2352
 count=math.ceil(len(rows[mid]['lines'])/3)
 for page in range(1,count+1):
  tag=f'v054-{mid}-page{page}';cmd=[sys.executable,str(E/'run_core.py'),'--rom',str(E/f'fixture-v054-{mid}.sfc'),'--session',f'v054-fixture-{mid}','--tag',tag]
  if page==1:
   seq=[{'button':'a','frames':4,'press':1},{'frames':330},{'button':'down','frames':8,'press':1},{'frames':10},{'frames':240}]
   cmd+=['--load-state',str(a.camp_state),'--set-wram',json.dumps({'0x5a24':[3,0],'0x5a2e':[57,48,0],'0x3b2f':[2,0],'0x3b2d':[3,0],'0x5a2a':[1,0],'0x5a2c':[2,0],'0x5a28':list(sid.to_bytes(2,'little')),'0x3b6d':list(encode('MAXIME')+b'\xac')}),'--sequence',json.dumps(seq)]
  else:cmd+=['--sequence',json.dumps([{'button':'a','frames':1,'press':1},{'frames':240}])]
  r=subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=45);f=E/(tag+'.png');m=json.loads(r.stdout.splitlines()[0])['message_id'];initial=None
  if page==1 and m==101:
   assert count==1,(mid,page,m);saved=S/('initial-'+f.name);shutil.copy2(f,saved);initial=dict(message_id=m,output=r.stdout,screenshot='screenshots/'+saved.name,reason='Short text completed before final A selected host choice; rejected capture.')
   seq=json.loads(cmd[-1]);seq=[x for x in seq if x.get('button')!='down'];cmd[-1]=json.dumps(seq);r=subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=45);m=json.loads(r.stdout.splitlines()[0])['message_id']
  assert m==100,(mid,page,m);shutil.copy2(f,S/f.name);out.append(dict(id=mid,page=page,screenshot='screenshots/'+f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),output=r.stdout,initial_capture=initial))
 (O/'render-partial-private.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
 (O/'render-progress-private.json').write_text(json.dumps(dict(id=mid,captures=len(out))))
(O/a.report).write_text(json.dumps(dict(result_sha256=hashlib.sha256((O/'result.sfc').read_bytes()).hexdigest(),rows=out,diagnostic_RAM=dict(C0_name_ID=3,C1_name_ID=2,D8_buffer='MAXIME',BB_decimal=12345,B5_item_ID=1,B3_name_ID=3,B2_vocation=0x8f9,B2_name_ID=0x9a7,other_B2=2352),limits='Camp message100 redirections. No natural scenes, real transactions, naming writes or save effects tested.'),ensure_ascii=False,indent=2));print('Rendered',len(out),'pages for',len(ids),'texts')

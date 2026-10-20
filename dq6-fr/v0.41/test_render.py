"""Render every v0.41 addition from private camp fixtures, not natural scenes."""
from pathlib import Path
import argparse,json,subprocess,sys,math,hashlib,shutil
ap=argparse.ArgumentParser();ap.add_argument('--camp-state',required=True,type=Path);ap.add_argument('--ids',default='');ap.add_argument('--report',default='qa-render-fixtures.json');ap.add_argument('--tag-suffix',default='');ap.add_argument('--stress',action='store_true');a=ap.parse_args()
O=Path(__file__).resolve().parent;P=O.parent;E=P/'emulator-tests'
review=json.loads((O/'revue-lot-v041.json').read_text());ids=[r['id'] for r in review]
if a.ids:ids=list(map(int,a.ids.split(',')))
subprocess.run([sys.executable,str(P/'render_fixtures.py'),'v0.41',','.join(map(str,ids))],check=True)
if a.stress:raise ValueError('No stress pool mutation in this batch')
rows={r['id']:r for r in json.loads((O/'insertion-candidates.json').read_text())};report=[]
S=O/'screenshots';S.mkdir(exist_ok=True)
for mid in ids:
 sid=0x870 if mid in [780,785,797] else 0 if mid in [6631,1793] else 0x8f9 if mid==6415 else 558 if mid in [5899,5892,5870,5890] else 2352
 count=math.ceil(len(rows[mid]['lines'])/3)
 for page in range(1,count+1):
  tag=f'v041{a.tag_suffix}-{mid}-page{page}';cmd=[sys.executable,str(E/'run_core.py'),'--rom',str(E/f'fixture-v041-{mid}.sfc'),'--session',f'v041{a.tag_suffix}-fixture-{mid}','--tag',tag]
  if page==1:
   cmd+=['--load-state',str(a.camp_state),'--set-wram',json.dumps({'0x5a2e':[0x39,0x30,0],'0x3b2f':[2,0],'0x3b2d':[2,0],'0x5a2a':[1,0],'0x5a28':list(sid.to_bytes(2,'little'))}),'--sequence',json.dumps([{'button':'a','frames':4,'press':4},{'frames':330},{'button':'down','frames':8,'press':8},{'frames':10},{'button':'a','frames':1,'press':1},{'frames':240}])]
  else:cmd+=['--sequence',json.dumps([{'button':'a','frames':1,'press':1},{'frames':240}])]
  result=subprocess.run(cmd,check=True,capture_output=True,text=True);s=E/(tag+'.png');shutil.copy2(s,S/s.name)
  report.append(dict(id=mid,page=page,screenshot='screenshots/'+s.name,sha256=hashlib.sha256(s.read_bytes()).hexdigest(),output=result.stdout.strip()))
(O/a.report).write_text(json.dumps(dict(result_sha256=hashlib.sha256((O/'result.sfc').read_bytes()).hexdigest(),fixture_message_redirect=100,diagnostic_item_name_swap=a.stress,diagnostic_RAM={'B5_item_ID':1,'B2_values_by_ID':{'armor':2160,'vocation':2297,'monster':558,'rank':0,'other':2352},'C0_C1_name_ID':2,'5A2E_5A2F_5A30_bytes':[57,48,0],'BB_expected_decimal':12345,'3B2F':2},rows=report,limits='Diagnostic camp redirections, not natural scenes or monetary actions; injected display values do not test calculations or save state.'),ensure_ascii=False,indent=2))
print('Rendered',len(report),'captures for all',len(ids),'new texts')

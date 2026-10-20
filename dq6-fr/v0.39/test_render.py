"""Render every v0.39 addition from private camp fixtures, not natural scenes."""
from pathlib import Path
import argparse,json,subprocess,sys,math,hashlib,shutil
ap=argparse.ArgumentParser();ap.add_argument('--camp-state',required=True,type=Path);ap.add_argument('--ids',default='');ap.add_argument('--report',default='qa-render-fixtures.json');ap.add_argument('--tag-suffix',default='');a=ap.parse_args()
O=Path(__file__).resolve().parent;P=O.parent;E=P/'emulator-tests'
review=json.loads((O/'revue-lot-v039.json').read_text());ids=[1236]+[r['id'] for r in review if r['id']!=1236]
if a.ids:ids=list(map(int,a.ids.split(',')))
subprocess.run([sys.executable,str(P/'render_fixtures.py'),'v0.39',','.join(map(str,ids))],check=True)
rows={r['id']:r for r in json.loads((O/'insertion-candidates.json').read_text())};report=[]
S=O/'screenshots';S.mkdir(exist_ok=True)
for mid in ids:
 count=math.ceil(len(rows[mid]['lines'])/3)
 for page in range(1,count+1):
  tag=f'v039{a.tag_suffix}-{mid}-page{page}';cmd=[sys.executable,str(E/'run_core.py'),'--rom',str(E/f'fixture-v039-{mid}.sfc'),'--session',f'v039{a.tag_suffix}-fixture-{mid}','--tag',tag]
  if page==1:
   cmd+=['--load-state',str(a.camp_state),'--set-wram',json.dumps({'0x5a2e':[0x39,0x30,0],'0x3b2f':[2]}),'--sequence',json.dumps([{'button':'a','frames':4,'press':4},{'frames':330},{'button':'down','frames':8,'press':8},{'frames':10},{'button':'a','frames':1,'press':1},{'frames':240}])]
  else:cmd+=['--sequence',json.dumps([{'button':'a','frames':1,'press':1},{'frames':240}])]
  result=subprocess.run(cmd,check=True,capture_output=True,text=True);s=E/(tag+'.png');shutil.copy2(s,S/s.name)
  report.append(dict(id=mid,page=page,screenshot='screenshots/'+s.name,sha256=hashlib.sha256(s.read_bytes()).hexdigest(),output=result.stdout.strip()))
(O/a.report).write_text(json.dumps(dict(result_sha256=hashlib.sha256((O/'result.sfc').read_bytes()).hexdigest(),fixture_message_redirect=100,diagnostic_RAM={'5A2E_5A2F_5A30_bytes':[57,48,0],'BB_expected_decimal':12345,'3B2F':2},rows=report,limits='Diagnostic camp redirections, not natural scenes or monetary actions; injected display values do not test calculations or save state.'),ensure_ascii=False,indent=2))
print('Rendered',len(report),'captures for all',len(ids),'new texts')

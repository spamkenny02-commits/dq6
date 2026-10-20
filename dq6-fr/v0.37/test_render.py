"""Snes9x camp redirections, not a natural playthrough. Private images only."""
from pathlib import Path
import argparse,json,subprocess,sys,math,hashlib,shutil
ap=argparse.ArgumentParser();ap.add_argument('--camp-state',required=True,type=Path);a=ap.parse_args()
O=Path(__file__).resolve().parent;P=O.parent;E=P/'emulator-tests'
ids=[20,337,2296,2315,3784,3887,5009,5177,5279,6589,6220,5686]
subprocess.run([sys.executable,str(P/'render_fixtures.py'),'v0.37',','.join(map(str,ids))],check=True)
rows={r['id']:r for r in json.loads((O/'insertion-candidates.json').read_text())};report=[]
S=O/'screenshots';S.mkdir(exist_ok=True)
for mid in ids:
 count=math.ceil(len(rows[mid]['lines'])/3)+(2 if mid==6220 else 0)
 for page in range(1,count+1):
  tag=f'v037-{mid}-page{page}';cmd=[sys.executable,str(E/'run_core.py'),'--rom',str(E/f'fixture-v037-{mid}.sfc'),'--session',f'v037-fixture-{mid}','--tag',tag]
  if page==1:
   cmd+=['--load-state',str(a.camp_state),'--sequence',json.dumps([{'button':'a','frames':4,'press':4},{'frames':330},{'button':'down','frames':8,'press':8},{'frames':10},{'button':'a','frames':4,'press':4},{'frames':240}])]
  else:cmd+=['--sequence',json.dumps([{'button':'a','frames':4,'press':4},{'frames':240}])]
  result=subprocess.run(cmd,check=True,capture_output=True,text=True)
  screenshot=E/(tag+'.png');shutil.copy2(screenshot,S/screenshot.name)
  report.append(dict(id=mid,page=page,screenshot='screenshots/'+screenshot.name,sha256=hashlib.sha256(screenshot.read_bytes()).hexdigest(),output=result.stdout.strip()))
(O/'qa-render-fixtures.json').write_text(json.dumps(dict(result_sha256=hashlib.sha256((O/'result.sfc').read_bytes()).hexdigest(),fixture_message_redirect=100,rows=report,limits='Diagnostic camp redirections; 12 sampled messages, not all 51; no natural scene progression.'),ensure_ascii=False,indent=2))
print('Rendered',len(report),'captures from',len(ids),'reviewed messages')

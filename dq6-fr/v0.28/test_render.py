"""Targeted renderer fixtures; requires a local compatible camp state and Snes9x core.
Never distributes diagnostic ROMs or emulator states.
"""
from pathlib import Path
import argparse,json,subprocess,sys,math,hashlib,shutil
ap=argparse.ArgumentParser();ap.add_argument('--camp-state',required=True,type=Path);a=ap.parse_args()
O=Path(__file__).resolve().parent;P=O.parent;E=P/'emulator-tests'
ids=[1181,5471,6804,5615,1259,6447,5735,5742,4113,4932,1848]
subprocess.run([sys.executable,str(P/'render_fixtures.py'),'v0.28',','.join(map(str,ids))],check=True)
rows={r['id']:r for r in json.loads((O/'insertion-candidates.json').read_text())};report=[]
S=O/'screenshots';S.mkdir(exist_ok=True)
for mid in ids:
 count=math.ceil(len(rows[mid]['lines'])/3)
 for page in range(1,count+1):
  tag=f'v028-{mid}-page{page}';cmd=[sys.executable,str(E/'run_core.py'),'--rom',str(E/f'fixture-v028-{mid}.sfc'),'--session',f'v028-fixture-{mid}','--tag',tag]
  if page==1:
   cmd+=['--load-state',str(a.camp_state),'--sequence',json.dumps([{'button':'a','frames':4,'press':4},{'frames':330},{'button':'down','frames':8,'press':8},{'frames':10},{'button':'a','frames':4,'press':4},{'frames':240}])]
  else:cmd+=['--sequence',json.dumps([{'button':'a','frames':4,'press':4},{'frames':240}])]
  result=subprocess.run(cmd,check=True,capture_output=True,text=True)
  screenshot=E/(tag+'.png');shutil.copy2(screenshot,S/screenshot.name)
  report.append(dict(id=mid,page=page,screenshot='screenshots/'+screenshot.name,sha256=hashlib.sha256(screenshot.read_bytes()).hexdigest(),output=result.stdout.strip()))
(O/'qa-render-fixtures.json').write_text(json.dumps(dict(result_sha256=hashlib.sha256((O/'result.sfc').read_bytes()).hexdigest(),fixture_message_redirect=100,rows=report,limits='Diagnostic redirections from local camp state; no natural scene progression or full playthrough.'),ensure_ascii=False,indent=2))
print('Rendered',len(report),'pages from',len(ids),'reviewed messages')

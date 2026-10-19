"""Local diagnostic of all eight inserted places through native B2 formatting.
No ROM/state is distributed. Diagnostic redirection is not a natural travel menu.
"""
from pathlib import Path
import json,subprocess,sys,hashlib,argparse
ap=argparse.ArgumentParser();ap.add_argument('--camp-state',required=True,type=Path);a=ap.parse_args()
O=Path(__file__).resolve().parent;P=O.parent;E=P/'emulator-tests';D=P/'v0.33-place-fixtures';D.mkdir(exist_ok=True)
for n in ['result.sfc','placements.json']:
 if not(D/n).exists():(D/n).symlink_to(O/n)
charset={v:int(k,16) for k,v in json.loads((O/'charset.json').read_text()).items()};text='Destination ';tokens=[charset[c] for c in text]+[0xb2,charset['.'],0xac]
review=json.loads((O/'revue-lieux-v033.json').read_text());(D/'insertion-candidates.json').write_text(json.dumps([dict(id=x['sid'],tokens=tokens) for x in review]))
subprocess.run([sys.executable,str(P/'render_fixtures.py'),D.name,','.join(str(x['sid']) for x in review)],check=True)
rows=[]
for x in review:
 sid=x['sid'];tag=f'v033-place-{sid}';cmd=[sys.executable,str(E/'run_core.py'),'--rom',str(E/f'fixture-v033-place-fixtures-{sid}.sfc'),'--session',tag,'--tag',tag,'--load-state',str(a.camp_state),'--set-wram',json.dumps({'0x5a28':[sid&255,sid>>8]}),'--sequence',json.dumps([{'button':'a','frames':4,'press':4},{'frames':330},{'button':'down','frames':8,'press':8},{'frames':10},{'button':'a','frames':4,'press':4},{'frames':240}])]
 subprocess.run(cmd,check=True,capture_output=True,text=True);rows.append(dict(sid=sid,expected=x['french'],screenshot=tag+'.png',sha256=hashlib.sha256((E/(tag+'.png')).read_bytes()).hexdigest()))
(O/'qa-place-fixtures.json').write_text(json.dumps(dict(result_sha256=hashlib.sha256((O/'result.sfc').read_bytes()).hexdigest(),rows=rows,diagnostic_only=True,natural_travel_menu_tested=False),ensure_ascii=False,indent=2));print('Rendered eight native place entries')

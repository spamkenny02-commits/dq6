"""Sequential Snes9x diagnostics. Local ROM/camp/state/images remain outside Git.
Called explicitly only; rebuilding a release does not claim these tests reran.
"""
from common import *
import argparse,subprocess
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--runner',type=Path,required=True);p.add_argument('--camp',type=Path,required=True);a=p.parse_args()
args=['--out',str(a.out.resolve()),'--runner',str(a.runner.resolve()),'--camp',str(a.camp.resolve())]
def run(n,extra):subprocess.run([sys.executable,str(O/n)]+args+extra,check=True)
for i in range(2):run('emulator_consumers.py',['--jp',str(a.jp.resolve()),'--sids',json.dumps(SIDS[i*25:(i+1)*25]),'--report-suffix',f'-{i}'])
run('emulator_names_probe.py',[]);run('emulator_names_probe.py',['--mutate-pointer']);run('emulator_render_names.py',['--jp',str(a.jp.resolve())])
parts=[read(O/f'qa-name-consumers-{i}.json') for i in range(2)];assert set(parts[0]['checked_SIDs']).isdisjoint(parts[1]['checked_SIDs']);assert sorted(parts[0]['checked_SIDs']+parts[1]['checked_SIDs'])==SIDS
q=dict(release='v0.75',ROM_sha256=parts[0]['ROM_sha256'],all50_changed_encodings_checked=True,checked_SIDs=SIDS,rows=parts[0]['rows']+parts[1]['rows'],field_consumer=parts[0]['field_consumer'],B2_consumer=parts[0]['B2_consumer'],natural_validation=False,limits=parts[1]['limits']);(O/'qa-name-consumers.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
layout=a.out/'bus-layout.json';subprocess.run([sys.executable,str(O/'bus_layout.py'),'--rom',str(a.out/'result.sfc'),'--out',str(layout)],check=True)
seq=[dict(frames=360),dict(button='a',frames=1,press=1),dict(frames=120),dict(button='a',frames=1,press=1),dict(frames=120)]
subprocess.run([sys.executable,str(a.runner.resolve()),'--rom',str((a.out/'result.sfc').resolve()),'--check-layout',str(layout.resolve()),'--reset','--session','v075-cold','--tag','v075-cold','--sequence',json.dumps(seq)],check=True)

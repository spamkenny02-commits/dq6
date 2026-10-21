"""Sequential Snes9x bus, boot and explicit diagnostic variable probes.
Run only after test_render.py completes. Private ROMs/states are never artifacts.
The forced C4 branch tests display/layout, not the real party-count computation.
"""
from pathlib import Path
import subprocess,sys,json,hashlib,struct,shutil
import names,native_helpers
O=Path(__file__).resolve().parent;P=O.parent;E=P/'emulator-tests'
sha=lambda b:hashlib.sha256(b).hexdigest()
rom=(O/'result.sfc').read_bytes();rows={x['id']:x for x in json.loads((O/'insertion-candidates.json').read_text())}
layout=json.loads((O/'placements.json').read_text())+[x for x in json.loads((P/'v0.55/layout-engine-check.json').read_text()) if not isinstance(x['group'],int)]
for copy in [0,0x400000]:
 for label,a,n in [('C7',0x692ee,16),('E0',0x6929b,22),('DC',0x69492,11),('DC_helper',0x6957e,20),('E1',0x695b1,15),('AE',0x6906b,32),('AE_common',0x6903d,46),('D5',0x6949d,4)]:layout.append(dict(group='native-'+label+'-'+str(copy),file_offset=copy+a,cpu_address=(0xc00000+a if copy==0 else copy+a),size=n))
(O/'layout-engine-check.json').write_text(json.dumps(layout,indent=2))
def run(args):
 r=subprocess.run([sys.executable,str(E/'run_core.py')]+args,capture_output=True,text=True,check=True,timeout=90)
 return r.stdout
boot=run(['--rom',str(O/'result.sfc'),'--session','v056-boot','--reset','--check-layout',str(O/'layout-engine-check.json'),'--tag','v056-boot','--sequence',json.dumps([{'frames':1260},{'button':'start','frames':4,'press':4},{'frames':120},{'button':'a','frames':4,'press':4},{'frames':120}])])
bus=json.loads((E/'bus-verification.json').read_text());bus.update(result_sha256=sha(rom),layout_sha256=sha((O/'layout-engine-check.json').read_bytes()));(O/'qa-script-name-engine-bus.json').write_text(json.dumps(bus,indent=2))
S=O/'screenshots';S.mkdir(exist_ok=True);shutil.copy2(E/'v056-boot.png',S/'v056-boot.png')

(O/"qa-runtime.json").write_text(json.dumps(dict(result_sha256=sha(rom),boot_output=boot,boot_screenshot="screenshots/v056-boot.png",boot_screenshot_sha256=sha((S/"v056-boot.png").read_bytes()),probes=[],limits="Cold boot and ROM bus only. Compositions covered separately; no natural scenes validated."),indent=2))

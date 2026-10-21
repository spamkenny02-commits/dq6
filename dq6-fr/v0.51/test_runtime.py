"""Current ROM bus + cold boot, followed sequentially by inherited variable diagnostics."""
from pathlib import Path
import json,hashlib,subprocess,sys,shutil
O=Path(__file__).resolve().parent;P=O.parent;E=P/'emulator-tests';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
layout=json.loads((O/'placements.json').read_text())+[x for x in json.loads((P/'v0.50/layout-engine-check.json').read_text()) if not isinstance(x['group'],int)]
(O/'layout-engine-check.json').write_text(json.dumps(layout,indent=2))
cmd=[sys.executable,str(E/'run_core.py'),'--rom',str(O/'result.sfc'),'--session','v051-boot','--reset','--check-layout',str(O/'layout-engine-check.json'),'--tag','v051-boot','--sequence',json.dumps([{'frames':1260},{'button':'start','frames':4,'press':4},{'frames':120},{'button':'a','frames':4,'press':4},{'frames':120}])]
r=subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=120)
bus=json.loads((E/'bus-verification.json').read_text());bus.update(result_sha256=sha(O/'result.sfc'),layout_sha256=sha(O/'layout-engine-check.json'));(O/'qa-script-name-engine-bus.json').write_text(json.dumps(bus,indent=2));shutil.copy2(E/'v051-boot.png',O/'screenshots/v051-boot.png')
subprocess.run([sys.executable,str(O/'test_render.py'),'--camp-state',str(P.parent.parent/'work-v026/dq6-fr/emulator-tests/v026-camp.state'),'--ids','784,6939,752','--report','qa-regression-variables.json'],check=True)
report=dict(result_sha256=sha(O/'result.sfc'),boot_output=r.stdout,boot_screenshot='screenshots/v051-boot.png',boot_sha256=sha(O/'screenshots/v051-boot.png'),inherited_variable_diagnostic_ids=[784,6939,752],limits='All new vocation texts lack dynamic names and numbers. Inherited diagnostics exercise unchanged B2/B5/D3/BB/DF rendering with the documented camp values; no new maximum-width probe, natural transaction, party effect or SRAM validation claimed.')
(O/'qa-runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('Bus, boot and inherited variable diagnostic pages done')

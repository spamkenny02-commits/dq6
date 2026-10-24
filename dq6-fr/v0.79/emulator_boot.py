"""Cold boot and ROM-bus check; read VRAM, never inject font bytes."""
from common import *
import argparse,subprocess
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--runner',type=Path,required=True);a=p.parse_args();rom=(a.out/'result.sfc').read_bytes();assert sha(rom)==read(O/'build-report.json')['ROM_sha256'];runner=a.runner.resolve();layout=a.out/'bus-layout.json'
subprocess.run([sys.executable,str(O/'bus_layout.py'),'--rom',str((a.out/'result.sfc').resolve()),'--out',str(layout.resolve())],check=True,capture_output=True)
# libretro RETRO_MEMORY_VIDEO_RAM=3. Temporary instrumentation only dumps it.
script=runner.read_text();needle='core.retro_unload_game();core.retro_deinit()';assert script.count(needle)==1
script=script.replace(needle,"(P/'v079-vram.bin').write_bytes(C.string_at(core.retro_get_memory_data(3),core.retro_get_memory_size(3)))\n"+needle)
probe=runner.parent/'v079_read_vram_private.py';probe.write_text(script)
seq=[dict(frames=360),dict(button='a',frames=1,press=1),dict(frames=120),dict(button='a',frames=1,press=1),dict(frames=120)]
try:
 proc=subprocess.run([sys.executable,str(probe),'--rom',str((a.out/'result.sfc').resolve()),'--reset','--session','v079-cold','--tag','v079-cold','--check-layout',str(layout.resolve()),'--sequence',json.dumps(seq)],capture_output=True,timeout=90);assert proc.returncode==0,proc.stderr.decode()
finally:probe.unlink(missing_ok=True)
vram=(runner.parent/'v079-vram.bin').read_bytes();assert len(vram)==65536
for b in range(256):
 for y in range(8):assert vram[0x6000+b*32+y*2]==rom[parent.parent.font.FONT+b*16+y*2],(b,y)
q=dict(release='v0.79',ROM_sha256=sha(rom),fresh_boot=True,reset=True,load_state=False,VRAM_modified=False,all256_native_font_foregrounds_loaded_from_ROM=True,native_font_ROM_offset=parent.parent.font.FONT,VRAM_font_offset=0x6000,VRAM_sha256=sha(vram),bus=read(runner.parent/'bus-verification.json'),screenshot_sha256=sha((runner.parent/'v079-cold.png').read_bytes()),sequence=seq,natural_battle_or_travel=False)
(O/'qa-bus-boot.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q))

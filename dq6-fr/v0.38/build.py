"""Build an 8 MiB ExHiROM with duplicated original mappings and direct text pointers.
Only the known original main-script regions in each copy are used for payloads.
"""
from pathlib import Path
import json,struct,hashlib,zlib
import names
P=Path(__file__).resolve().parents[1];O=P/'v0.38';BASE=0x400000;PAY=0x37175b;END=0x3b8703;TBL=0x15bb5
raw=(P/'clean-base/vf-base-headered.sfc').read_bytes()[512:];rom=bytearray(raw);root=struct.unpack_from('<H',raw,0x2bfb)[0];n=root//2+1;left,right=[struct.unpack_from('<'+str(n)+'H',raw,a) for a in [0x167be,0x1700e]]
def original_decode():
 out=[]
 for g in range(870):
  e=int.from_bytes(raw[TBL+3*g:TBL+3*g+3],'little');pos=PAY+(e>>3);bit=e&7
  for _ in range(8):
   ts=[]
   while True:
    v=root|32768
    while v&32768:
     b=(raw[pos]>>bit)&1;bit-=1
     if bit<0:pos+=1;bit=7
     v=(left,right)[b][(v&32767)//2]
    t=v&8191;ts.append(t)
    if t in [0xac,0xae]:break
   out.append(ts)
 return out
name_changes,verified_name_entries=names.apply(rom,P)
# Naming window descriptor 147: gain one column on the left, keep its right edge.
# The text and all its byte-coded controls remain exactly as in the supplied IPS.
window=0x57b5c+147*14
assert window==0x58366 and rom[window:window+4]==bytes.fromhex('02051c0d')
assert rom[window+11:window+14]==bytes.fromhex('dc51c3')
rom[window]=1;rom[window+2]=29
expected_name_pool=bytes(rom[END:0x3bc712]);expected_name_pointers=bytes(rom[0x165e7:0x167be])
original=original_decode();msgs=[x[:] for x in original];rows=json.loads((O/'insertion-candidates-all.json').read_text())
for x in rows:msgs[x['id']]=x['tokens']
selected_ids={r['id'] for r in rows}
# Reuse the two existing, now-unused glyph slots. They are not in the byte charset.
for code in [0x248,0x249,0x24a,0x24b]:
 assert all(struct.unpack_from('<H',raw,0x11100+2*b)[0]!=code for b in range(256))
 assert all(code not in msg for i,msg in enumerate(msgs) if i not in selected_ids)
font_specs={0x248:['    ##    ','   #      ','  #       ','  #       ',' #        ',' #        ',' #        ',' #        ',' #        ','  #       ','  #       ','   #      ','    ##    ','          ']}
font_specs[0x249]=[s[::-1] for s in font_specs[0x248]]
font_specs[0x24a]=['          ','          ','  ## ##   ',' #######  ',' #######  ',' #######  ','  #####   ','  #####   ','   ###    ','   ###    ','    #     ','          ','          ','          ']
font_specs[0x24b]=['      #   ','      ##  ','      ### ','      # # ','      #   ','      #   ','      #   ','      #   ','   ####   ','  #####   ','  #####   ','   ###    ','          ','          ']
font_ranges=[]
for code,shape in font_specs.items():
 first=0x201
 for group in range(51):
  nw,off,hh=struct.unpack_from('<HHB',raw,0x159d2+group*5);count=nw&4095;w=nw>>12;h=hh>>2
  if first<=code<first+count:break
  first+=count
 assert w==10 and h==14
 start=(0x10000+off)*8+(code-first)*w*h
 assert all(len(row)==w for row in shape) and len(shape)==h
 if code in [0x24a,0x24b]:font_ranges.append([start//8,(start+w*h+7)//8])
 for y,row in enumerate(shape):
  for x,pixel in enumerate(row):
   b=start+y*w+(w-1-x);a,shift=divmod(b,8);mask=1<<shift;rom[a]=(rom[a]&~mask)|(mask if pixel=='#' else 0)
 for y,row in enumerate(shape):
  for x,pixel in enumerate(row):
   b=start+y*w+(w-1-x);assert bool((rom[b//8]>>(b%8))&1)==(pixel=='#')
# Retain ID>>3 addressing and the original skip-N-strings loop, but load a direct
# 24-bit CPU address from the table and initialize the bit mask to 0x80.
a=0x2b7e;end=raw.index(bytes.fromhex('ad1e5a'),a)
expected=bytes.fromhex('bfb55bc185a0290700da aabfcc2bc029ff0085a4fa bfb75bc129ff004a66a04a66a04a66a085a2 a5a018695b1785a0 a5a269f70085a2')
assert raw[a:end]==expected
loader=bytes.fromhex('bfb55bc185a0bfb75bc129ff0085a2a9800085a418')
assert len(loader)<=end-a;rom[a:end]=loader+b'\xea'*(end-a-len(loader))
# Copy the complete patched mapping, including low-bank code/vectors/SRAM metadata.
# ExHiROM maps C0..FF to copy 1, and 00..3F-high / 40..7D to copy 2.
rom[0xffd5]=0x35;rom[0xffd7]=0x0d;rom.extend(rom)
codes={}
def collect(node,bits):
 for bit in [0,1]:
  v=(left,right)[bit][node//2]
  if v&32768:collect(v&32767,bits+[bit])
  else:codes.setdefault(v&8191,bits+[bit])
collect(root,[])
blobs=[]
for g in range(870):
 bits=[b for msg in msgs[g*8:g*8+8] for t in msg for b in codes[t]];blob=bytearray((len(bits)+7)//8)
 for i,b in enumerate(bits):
  if b:blob[i//8]|=1<<(7-i%8)
 blobs.append(bytes(blob))
regions=[[PAY,END],[BASE+PAY,BASE+END]];placements=[]
for g,blob in enumerate(blobs):
 region=next((r for r in regions if r[0]+len(blob)<=r[1]),None);assert region,'Translation exceeds both reserved main-script areas'
 off=region[0];region[0]+=len(blob);rom[off:off+len(blob)]=blob
 cpu=(off|0xc00000) if off<BASE else off
 assert cpu>>16 not in [0x7e,0x7f]
 for copy in [0,BASE]:rom[copy+TBL+3*g:copy+TBL+3*g+3]=cpu.to_bytes(3,'little')
 placements.append(dict(group=g,file_offset=off,cpu_address=cpu,size=len(blob)))
# Verify pools and tree data in both mappings.
for copy in [0,BASE]:
 assert rom[copy+END:copy+0x3bc712]==expected_name_pool
 assert rom[copy+0x165e7:copy+0x167be]==expected_name_pointers
 assert rom[copy+0x167be:copy+0x1785e]==raw[0x167be:0x1785e]
# Decode through the new direct-address table, independently of placements.json.
check=[]
for g in range(870):
 cpu=int.from_bytes(rom[TBL+g*3:TBL+g*3+3],'little')
 pos=(cpu&0x3fffff) if cpu>=0xc00000 else cpu;bit=7
 for _ in range(8):
  ts=[]
  for _ in range(100000):
   v=root|32768
   while v&32768:
    b=(rom[pos]>>bit)&1;bit-=1
    if bit<0:pos+=1;bit=7
    v=(left,right)[b][(v&32767)//2]
   t=v&8191;ts.append(t)
   if t in [0xac,0xae]:break
  else:raise ValueError('unterminated')
  check.append(ts)
assert check==msgs
changes=[i for i,(a,b) in enumerate(zip(original,check)) if a!=b];unchanged=[r['id'] for r in rows if r['tokens']==original[r['id']]];assert changes==sorted(r['id'] for r in rows if r['id'] not in unchanged)
s=sum(rom)&65535
for copy in [0,BASE]:struct.pack_into('<HH',rom,copy+0xffdc,s^65535,s)
assert sum(rom)&65535==s
source=(P.parent/'upload/Dragon Quest VI - Maboroshi no Daichi (Japan).sfc').read_bytes();assert hashlib.sha256(source).hexdigest()=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e'
(O/'result.sfc').write_bytes(rom)
# BPS: SourceRead for unchanged first-copy bytes, SourceCopy for mirrored bytes.
def vint(v):
 out=bytearray()
 while True:
  b=v&127;v>>=7
  if not v:out.append(b|128);return out
  out.append(b);v-=1
def mode(i):return (0 if i<BASE else 2) if rom[i]==source[i%BASE] else 1
bps=bytearray(b'BPS1')+vint(len(source))+vint(len(rom))+vint(0);i=0;rel=0
while i<len(rom):
 kind=mode(i);a=i;i+=1
 while i<len(rom) and (i!=BASE) and mode(i)==kind:i+=1
 bps+=vint(((i-a-1)<<2)|kind)
 if kind==1:bps+=rom[a:i]
 elif kind==2:
  origin=a%BASE;delta=origin-rel;bps+=vint((abs(delta)<<1)|int(delta<0));rel=origin+i-a
bps+=struct.pack('<II',zlib.crc32(source),zlib.crc32(rom));bps+=struct.pack('<I',zlib.crc32(bps));(O/'DQVI-FR-DS-v0.38-BASE-JP-PARTIEL.bps').write_bytes(bps)
# IPS alternative, with explicit target length after EOF.
ips=bytearray(b'PATCH');i=0
while i<len(rom):
 if i<BASE and rom[i]==source[i]:i+=1;continue
 a=i;i+=1
 while i<len(rom) and (i>=BASE or rom[i]!=source[i]) and i-a<65535:i+=1
 ips+=a.to_bytes(3,'big')+(i-a).to_bytes(2,'big')+rom[a:i]
ips+=b'EOF'+len(rom).to_bytes(3,'big');(O/'DQVI-FR-DS-v0.38-BASE-JP-PARTIEL.ips').write_bytes(ips)
report=dict(status='PARTIEL_A_TESTER',visible_messages=6957,ds_validated=len(rows),ds_replacements=len(changes),already_identical_ids=unchanged,new_replacements=len(rows)-5905,remaining_visible_messages=6957-len(rows),script_entries_verified=len(check),all_tokens_verified=True,mapper='ExHiROM',new_font_glyph_ranges=font_ranges,rom_bytes=len(rom),payload_bytes=sum(map(len,blobs)),script_capacity_bytes=2*(END-PAY),upper_copy_groups=sum(p['file_offset']>=BASE for p in placements),huffman_tree_unchanged=True,default_name_entries_changed=len(name_changes),name_entries_verified=verified_name_entries,other_name_strings_unchanged_except_reviewed_names_places_credit_and_menu_labels=True,additional_character_names_changed=1,spell_action_entries_changed=20,place_entries_changed=8,removed_credit_sid=0x9c,shortened_slot_label_sid=0xe7,shortened_settings_label_sid=0xe9,source_sha256=hashlib.sha256(source).hexdigest(),result_sha256=hashlib.sha256(rom).hexdigest(),checksum=f'{s:04X}',emulator_tested=False)
(O/'noms-personnages.json').write_text(json.dumps(name_changes,ensure_ascii=False,indent=2));(O/'validation.json').write_text(json.dumps(report,indent=2));(O/'placements.json').write_text(json.dumps(placements,indent=2));(O/'insertion-candidates.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(json.dumps(report,indent=2))

"""Reproducible native bindings and technical-label preparations. No ROM output."""
from common import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--jp',required=True,type=Path);a=p.parse_args();jp=a.jp.read_bytes();base,rows=prepare(jp);r=read(O/'build-report.json');g=module('g64',R/'dq6-fr/v0.63/source_guard.py');source=g.checked_rows(jp,R)
bindings=[]
for label,at,size,meaning in [('C6_flag',0x691dc,7,'C6 sets WRAM5A1C=1 then RTL; no glyph and no damage mutation.'),('XP_conditional_each',0x2af21,11,'CMP2; BCC skips54 below2 beneficiaries. Two54/55 fragments share this context.'),('XP_amount_and55',0x2af2c,19,'254D/254F copied to5A2E/5A30, then inline55,RTS.'),('stats_native_five_fields',0x2b006,60,'485B→60,485F→61,4861→62,485D→63,4863→64. This source order is preserved.'),('rank_primary_pair',0x2b2dc,18,'Inline76, load4877 toB2, inline77. First B2 is vocation; second is rank.'),('rank_secondary_pair',0x2fa56,18,'Same76/77 pair and4877 binding, second native caller.')]:
 # These guarded snippets are metadata; no claim about reachability of all contexts.
 bindings.append(dict(label=label,offset=at,size=size,JP_sha256=sha(jp[at:at+size]),base_v063_sha256=sha(base[at:at+size]),JP_and_base_identical=jp[at:at+size]==base[at:at+size],meaning=meaning))
assert base[0x691dc:0x691e3]==bytes.fromhex('a901008d1c5a6b')
assert int.from_bytes(base[(0xc6-0xab)*3:(0xc6-0xab)*3+3],'little')==0xc691dc
for at,mid in [(0x2af26,54),(0x2af38,55),(0x2b00c,60),(0x2b018,61),(0x2b024,62),(0x2b030,63),(0x2b03c,64),(0x2b2dc,76),(0x2b2e8,77),(0x2fa56,76),(0x2fa62,77),(0x2ac16,36)]:assert jp[at:at+6]==base[at:at+6]==bytes.fromhex('22162ac0')+mid.to_bytes(2,'little')
assert base[0x2af21:0x2af26]==bytes.fromhex('c902009006')
q=dict(release='v0.64',JP_sha256=sha(jp),base_v063_sha256=sha(base),bindings=bindings,C6_dispatch_offset=(0xc6-0xab)*3,C6_handler=0xc691dc,plus_byte='0C',plus_main_glyph='0208',plus_tile_sha256=sha(base[0x56b5c+192:0x56b5c+208]),plus_tile_visually_reviewed=True,font_modified=False,engine_modified=False,frames_are_diagnostic=True,natural_battle_reachability=False)
(O/'audit-bindings.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
codec=Codec(base,read(R/'dq6-fr/v0.56/charset.json'));old=dict((i,b) for i,at,b in decode_pool(base,BASE['placement']));prepared=[];p57=module('p64',R/'preparations/combat-v057/prepare.py')
for mid,plan in plans.PREPARED.items():
 p57.validate_plan(plan,source[mid]['private_tokens']);enc=codec.encode(plan);assert codec.decode(enc)==plan
 prepared.append(dict(id=mid,status='PREPARE_NON_INSERE',source_message_sha256=source[mid]['source_message_sha256'],source_text_sha256=source[mid]['source_text_sha256'],previous_message_sha256=sha(old[mid]),french_plan=plan,encoded_hex=enc.hex(),review='Traduction littérale du libellé technique JP et de son numéro. Aucun rapprochement DS établi ; contexte appelant à tracer avant insertion.',blocking_reason=plans.DEFERRED[mid],included_in_two_remaining=True,emulator_tested=False))
(O/'prepares-non-inseres.json').write_text(json.dumps(prepared,ensure_ascii=False,indent=2)+'\n')
# A byte-pattern survey is a bounded static search, NOT a proof of no caller.
scan=[]
for entry,op in [('C02A16',bytes.fromhex('22162ac0')),('C02A3C',bytes.fromhex('223c2ac0'))]:
 found=[dict(offset=i,id=int.from_bytes(jp[i+4:i+6],'little')) for i in range(0x20000,0x30000-6) if jp.startswith(op,i)]
 scan.append(dict(entry=entry,candidate_count=len(found),candidate_ID_max=max(x['id'] for x in found) if found else None,technical27=[x['offset'] for x in found if x['id']==27],technical277=[x['offset'] for x in found if x['id']==277],outside603_607=[x for x in found if 603<=x['id']<=607],scope='Raw opcode-pattern candidates in bankC2; inline shape confirmed for this lot only. Dynamic dispatch,other banks and data false positives are not resolved.'))
(O/'audit-static-candidates.json').write_text(json.dumps(dict(release='v0.64',scans=scan,absence_does_not_prove_unreachable=True,source_boundary_audit_kept='dq6-fr/v0.63/audit-frontiere-source.json',unresolved_opaque_slots=list(range(603,608))),ensure_ascii=False,indent=2)+'\n')
print('11 source bindings guarded; two technical labels PREPARE_NON_INSERE; five opaque slots reserved')

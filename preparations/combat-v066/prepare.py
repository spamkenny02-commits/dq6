"""Prepare DS whole-name mappings for the SFC two-fragment invented spells.
No ROM,patch,SRAM or emulator-state output. Preserve unresolved composition issues.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json,re,struct,sys
O=Path(__file__).resolve().parent;R=O.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(p.read_text())
PREFIX=[0x61f,0x36b,0x36c,0x36d];SUFFIX=[0x36e,0x36f,0x370,0x371]
FRENCH=[['Kavlan','Kapoum','Kabing','Kabang'],['Supersoins','Ultrasoins','Insomnisoins','Dépann-soins'],['Fournaise','Explotron','Survoltage','Foudrintense'],['Katastrof','Ténébror','Kaboum','Flatutranse']]
def name_entry(rom,sid):
 a=0x3b8703+int.from_bytes(rom[0x165e7+3*(sid>>4):0x165ea+3*(sid>>4)],'little')
 assert 0x3b8703<=a<0x3bc712
 for _ in range(sid&15):a=rom.index(0xac,a)+1
 end=rom.index(0xac,a);assert end<0x3bc712
 return a,rom[a:end]
def plain_factorizations(rows):
 first=rows[0];common=''
 for chars in zip(*first):
  if len(set(chars))!=1:break
  common+=chars[0]
 valid=[]
 for n in range(len(common)+1):
  suffix=[s[n:] for s in first];prefixes=[first[0][:n]];ok=True
  for row in rows[1:]:
   candidates=[]
   for text,tail in zip(row,suffix):
    if not text.endswith(tail):ok=False;break
    candidates.append(text[:-len(tail)] if tail else text)
   if not ok or len(set(candidates))!=1:ok=False;break
   prefixes.append(candidates[0])
  if ok:valid.append(dict(prefixes=prefixes,suffixes=suffix))
 return common,len(common)+1,valid
def generate(jp):
 assert sha(jp)=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e','Wrong intact JP source'
 spec=importlib.util.spec_from_file_location('bps66',R/'dq6-fr/upstream/refill/patchRM.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 bps=(R/'patches/DQVI-FR-DS-v0.58-BASE-JP-PARTIEL.bps').read_bytes();assert sha(bps)=='5befcf673b17641193065f8b42413faa844401f39fce61be43648b1da4122439'
 base=bytes(m.apply_bps(jp,bps));assert sha(base)=='ce2a8d5a657bb304a2ed6bc2313d96b0179b5b32aad6410f016cb61b443e1d60'
 assert jp[0x26759:0x26796]==base[0x26759:0x26796]
 assert jp[0x26769:0x2676f]==bytes.fromhex('22162ac0f101') and jp[0x2677f:0x26785]==bytes.fromhex('22162ac0f201')
 assert jp[0x26759:0x26769]==bytes.fromhex('22970ec02903000aaabf8667c28d285a')
 assert jp[0x2676f:0x2677f]==bytes.fromhex('22970ec02903000aaabf8e67c28d285a')
 assert [int.from_bytes(jp[0x26786+2*i:0x26788+2*i],'little') for i in range(4)]==PREFIX
 assert [int.from_bytes(jp[0x2678e+2*i:0x26790+2*i],'little') for i in range(4)]==SUFFIX
 glyphs=struct.unpack_from('<256H',jp,0x11100);table={int(k,16):v for l in (R/'dq6-fr/upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines() if '=' in l for k,v in [l.split('=',1)] if len(k)<=4}
 def japanese_name(sid):return ''.join(table[glyphs[b]] for b in name_entry(jp,sid)[1])
 prefix=[japanese_name(s) for s in PREFIX];suffix=[japanese_name(s) for s in SUFFIX]
 assert prefix==['メラ','ベホ','バキ','マホ'] and suffix==['トテカ','チーマ','ソニア','ペッチ']
 ja={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-ja.json')};fr={(x['file'].replace('/FR/','/JA/'),x['id']):x for x in read(R/'dq6-fr/clean-base/ds-fr.json')}
 def ref(file,mid):
  j=ja[file,mid];f=fr[file,mid]
  return dict(JA_file=file,FR_file=f['file'],id=mid,JA_text_sha256=sha(j['text'].encode()),FR_text_sha256=sha(f['text'].encode()))
 def label(row):
  match=re.fullmatch(r'@1([^@]+)@',row['text']);assert match,'Unexpected DS label commands';return match[1]
 spec=importlib.util.spec_from_file_location('codec66',R/'tools/combat-v058/codec.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c);codec=c.BattleCodec(base,read(R/'dq6-fr/v0.56/charset.json'),False)
 aliases={}
 for sid in range(2512):aliases.setdefault(name_entry(base,sid)[0],[]).append(sid)
 assert len(aliases)==2048
 fragments=[]
 for sid in PREFIX+SUFFIX:
  at,data=name_entry(base,sid);fragments.append(dict(SID=f'{sid:04X}',source_JA=japanese_name(sid),source_name_sha256=sha(name_entry(jp,sid)[1]),current_project_label=codec.decode(data),current_name_sha256=sha(data),runtime_SID_aliases=[f'{s:04X}' for s in aliases[at]],current_name_file_offset=f'{at:06X}',French_fragment_translation_approved=False))
 file='data/MENULIST6/JA/b1005000.mpt';records=[];accent_ids=[]
 for i in range(4):
  for j in range(4):
   mid=352+4*i+j;dsja=label(ja[file,mid]);dsfr=label(fr[file,mid]);assert dsfr==FRENCH[i][j]
   native_ja=prefix[i]+suffix[j];exact=native_ja==dsja
   assert exact or (i==2 and dsja=='バギ'+suffix[j])
   try:encoded=codec.encode(dsfr+'{AC}');assert codec.decode(encoded)==dsfr+'{AC}';encodable=True
   except c.CodecError:encodable=False;accent_ids.append(mid)
   records.append(dict(prefix_choice=i,suffix_choice=j,prefix_SID=f'{PREFIX[i]:04X}',suffix_SID=f'{SUFFIX[j]:04X}',SFC_composed_JA=native_ja,DS_complete_JA=dsja,French_complete_name=dsfr,DS_reference=ref(file,mid),status='PREPARE_NON_INSERE',semantic_status='CORRESPONDANCE_JA_EXACTE_RELUE' if exact else 'RESERVE_VARIANTE_SFC_BAKI_DS_BAGI',spelling_difference=None if exact else dict(SFC_prefix='バキ',DS_prefix='バギ',reason='Structural row correspondence and four exact suffixes; do not silently normalize the source.'),strict_existing_ASCII_roundtrip=encodable,native_render_approved=False))
 common,checked,factors=plain_factorizations(FRENCH);assert common=='Ka' and checked==3 and factors==[] and accent_ids==[359,365]
 # Context proves the DS passes a whole invented name,not four independent suffix labels.
 context_file='data/MESS6/JA/0802.p';assert '%a002640' in ja[context_file,279]['text'] and '%a002640' in fr[context_file,279]['text']
 real_file='data/MENULIST6/JA/b1003000.mpt';assert ja[real_file,0]['text']=='@1メラ@' and '@4Flamme@' in fr[real_file,0]['text']
 sys.path.insert(0,str(R/'preparations/combat-v057'));spec=importlib.util.spec_from_file_location('source66',R/'preparations/combat-v057/prepare.py');p57=importlib.util.module_from_spec(spec);spec.loader.exec_module(p57);source=p57.source_rows(jp)
 data=dict(checkpoint='combat-v066',release_unchanged='v0.58',new_main_integrated=0,new_battle_integrated=0,new_native_name_SIDs_integrated=0,prepared_complete_name_combinations=16,exact_JA_correspondences=12,reserved_spelling_variant_correspondences=4,not_in_main_6957=True,source_battle_sequence=[496,497,498],prefix_fragments=fragments[:4],suffix_fragments=fragments[4:],combinations=records,DS_context_references=[ref(context_file,n) for n in [276,279,280]],shared_ordinary_spell_reference=ref(real_file,0),shared_SID_warning='061F is the ordinary メラ/Blaze label,DS Flamme; do not globally rewrite it to a fake-spell prefix.',source_messages=[dict(id=i,source_message_sha256=source[i]['source_message_sha256'],native_commands=[f'{b:02X}' for b in source[i]['private_tokens'] if 0xab<=b<=0xc8]) for i in [496,497,498]],caller=dict(first_B2_call='C26769 -> C02A16 /497',second_B2_call='C2677F -> C02A16 /498',B2_SID_WRAM='5A28',prefix_table='C26786',suffix_table='C2678E',caller_range_file_offset='026759',caller_range_bytes=61,caller_sha256=sha(jp[0x26759:0x26796]),prefix_table_sha256=sha(jp[0x26786:0x2678e]),suffix_table_sha256=sha(jp[0x2678e:0x26796]),native_497_ends_with_AE=True,native_498_starts_with_B2=True),plain_four_prefix_four_suffix_factorization=False,factorization_proof=dict(first_French_row_common_prefix=common,possible_first_prefix_lengths_checked=checked,solutions=factors,scope='Plain concatenation of four fixed prefix strings and four fixed suffix strings; exact equality only.'),inventory=dict(name_pool_runtime_SIDs=2512,name_pool_physical_entries=2048,name_pool_aliases=464,source_fragment_runtime_SIDs=8,source_fragment_physical_entries=len({name_entry(base,s)[0] for s in PREFIX+SUFFIX}),prepared_virtual_combinations=16,native_complete_name_SIDs_created=0,existing_ASCII_name_roundtrips=14,unsupported_accent_DS_ids=accent_ids),insertion_blockers=['Whole-name pair-aware rendering or another reviewed representation needed; four suffix translations alone cannot reproduce the DS matrix.','Preserve B2/B2,AE and other native commands; both fragment choices must be available without rewriting shared061F.','Audit all aliases/callers of the eight existing SIDs before any global name edit.','Four BAKI/BAGI spelling variants remain reserved.','é in Dépann-soins and Ténébror is outside the approved native ASCII codec.','No French full-chain native rendering,natural battle or joint RNG reachability of all16 pairs tested.','The earlier v0.59 single-message diagnostics do not validate497+498 composition.'])
 qa=dict(checkpoint='combat-v066',prepared_complete_name_combinations=16,exact_JA_correspondences=12,reserved_correspondences=4,DS_refs_verified=20,caller_and_tables_identical_in_JP_and_v058=True,factorization_rejected_by_exhaustive_first_prefix_check=True,strict_ASCII_roundtrips=14,accent_blocked_names=2,new_inserted=0,Snes9x_executed=False,full_chain_rendered=False,ROM_output_written=False,baseline_ROM_sha256=sha(base),baseline_BPS_sha256=sha(bps),main_selected_unchanged=6957,battle_pool_integrated_unchanged=36,battle_prepared_unchanged=71,name_pool_confirmed_FR_unchanged=37,name_pool_grammar_helpers_unchanged=4,full_main_reread_progress=0,data_sha256=sha(json.dumps(data,ensure_ascii=False,sort_keys=True).encode()))
 return data,qa
def main():
 p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--verify',action='store_true');a=p.parse_args();raw=a.jp.read_bytes();data,qa=generate(raw)
 try:generate(bytes([raw[0]^1])+raw[1:])
 except AssertionError:qa['wrong_JP_source_rejected']=True
 else:raise AssertionError('Bad source accepted')
 files={'noms-composes-prepares.json':data,'qa-preparation.json':qa}
 for name,value in files.items():
  b=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode();path=O/name
  if a.verify:assert path.read_bytes()==b,'Preparation differs:'+name
  else:path.write_bytes(b)
 print('16 complete DS names prepared:12 exact,4 spelling reserves;0 inserted;no ROM/emulator output')
if __name__=='__main__':main()

"""Current, conservative name-pool census. Exact DS candidates are never approvals."""
from common import *
import argparse,collections,unicodedata,re
p=argparse.ArgumentParser();p.add_argument('--rom',required=True,type=Path);p.add_argument('--jp',required=True,type=Path);a=p.parse_args();rom=a.rom.read_bytes();jp=a.jp.read_bytes();assert sha(rom)==read(O/'build-report.json')['ROM_sha256'];assert sha(jp)=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e'
active_names=names;tab=LogicalTable(rom);names=active_names(rom);codec=Codec(rom,read(R/'dq6-fr/v0.56/charset.json'));glyphs=struct.unpack_from('<256H',jp,0x11100);jt={int(k,16):v for l in (R/'dq6-fr/upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines() if '=' in l for k,v in [l.split('=',1)] if len(k)<=4}
confirmed={156,231,233,781,1845,1846,1847,1848,1849};vk=lambda v:tuple(map(int,v.lstrip('v').split('.')))
for pattern in ['v*/revue-lieux-v*.json','v*/revue-noms-v*.json','v*/revue-sorts-v*.json']:
 for f in (R/'dq6-fr').glob(pattern):
  if vk(f.parent.name)<=vk('v0.78'):confirmed.update(x['position'] for x in read(f))
confirmed.update(PREVIOUS_CONFIRMED);confirmed.update(PLANS);confirmed.update(UNCHANGED);assert len(confirmed-{156})==367
norm=lambda s:''.join(c for c in unicodedata.normalize('NFKC',s.replace(';','')) if unicodedata.category(c)[0] in 'LN')
def field(s):
 m=re.search(r'@(?:1|4)([^@]+)',s);return m.group(1).replace(';','').strip() if m else None
fr={(r['file'].replace('/FR/','/JA/'),r['id']):r['text'] for r in read(R/'dq6-fr/clean-base/ds-fr.json')};lookup=collections.defaultdict(set)
for row in read(R/'dq6-fr/clean-base/ds-ja.json'):
 if '/MENULIST6/JA/' not in row['file'] or row['file'].endswith('b1090000.mpt'):continue
 ja=field(row['text']);ff=field(fr.get((row['file'],row['id']),''))
 if ja and ff:lookup[norm(ja)].add(ff)
regions=[('grille_menus',0,414),('lieux',415,543),('monstres_entites',544,803),('arene_et_debug',804,835),('casino',836,869),('menus_titres_monstres',870,918),('rangs_vocation',919,1062),('reserve_technique',1063,1102),('sorts_actions',1103,1325),('fragments_descriptions',1326,1603),('objets',1604,1823),('vocations_options',1824,1844),('noms_recrutables',1845,1924),('tactiques',1925,1930),('liste_noms_usage_a_tracer',1931,2005),('slots_vides_dynamiques_opaques',2006,2047)]
by=collections.defaultdict(list)
for sid,(at,b) in enumerate(names):by[tab.position(sid)].append(sid)
rows=[];meta=[]
for pos,sids in sorted(by.items()):
 sid=sids[0];at,b=names[sid]
 try:text=codec.decode(b)[:-4];unapproved=False
 except Exception:text=tab.text(sid);unapproved=True
 src_at=0x3b8703+int.from_bytes(jp[0x165e7+3*(sid>>4):0x165ea+3*(sid>>4)],'little')
 for _ in range(sid&15):src_at=jp.index(0xac,src_at)+1
 raw=jp[src_at:jp.index(0xac,src_at)];ja=''.join(jt.get(glyphs[x],'<UNKNOWN>') for x in raw);candidates=lookup.get(norm(ja),set());exact=any(re.sub(r'\s+',' ',text.replace('|',' ')).strip()==re.sub(r'\s+',' ',v.replace('|',' ')).strip() for v in candidates)
 if pos==156:status='CREDIT_RETIRE_CONFORME'
 elif pos in confirmed:status='FR_CONFIRME_PROJET'
 elif exact and text:status='FR_DS_IDENTIQUE_A_VERIFIER_EN_CONTEXTE'
 elif 2007<=pos<=2041:status='STRUCTURE_DYNAMIQUE_WRAM'
 elif pos==2006:status='RESERVE_VIDE_A_TRACER'
 elif pos>=2042:status='SOURCE_JP_OPAQUE_VF_VIDE'
 elif not text:status='VIDE_A_QUALIFIER'
 elif re.fullmatch(r'(?:M|\*)[0-9A-F]{2,4}',text):status='IDENTIFIANT_NON_TRADUIT'
 elif re.search('[\u3040-\u30ff\u4e00-\u9fff]',text):status='JAPONAIS_DETECTE'
 else:status='AUTRE_TEXTE_A_REVOIR'
 region=next(name for name,lo,hi in regions if lo<=pos<=hi);rows.append(dict(position=pos,sids=sids,status=status,region=region,text=text,unique_candidate=len(candidates)==1,unapproved_native_decode=unapproved,has_native_controls=any(0xab<=v<=0xc8 for v in b[:-1])));meta.append(dict(position=pos,sids=sids,offset=at,size=len(b),sha256=sha(b)))
counts=dict(collections.Counter(x['status'] for x in rows));counts.setdefault('JAPONAIS_DETECTE',0);assert len(rows)==2048 and counts['FR_CONFIRME_PROJET']==367
widths={}
for name,lo,hi,limit in [('actions',1103,1325,9),('descriptions',1326,1603,12),('menus',192,319,18),('lieux',415,543,20)]:
 rr=[x for x in rows if lo<=x['position']<=hi];known=[x for x in rr if not x['unapproved_native_decode'] and not x['has_native_controls']];widths[name]=dict(reference_width=limit,entries_checked=len(known),unmapped_skipped=len(rr)-len(known),exceeding_reference_positions=[x['position'] for x in known if max(map(len,x['text'].split('|')))>limit],not_a_runtime_window_test=True)
q=dict(release='v0.78',ROM_sha256=sha(rom),runtime_SIDs=2512,physical_entries=len(rows),aliases=464,counts=counts,by_region={name:dict(physical_entries=sum(x['region']==name for x in rows),counts=dict(collections.Counter(x['status'] for x in rows if x['region']==name))) for name,lo,hi in regions},candidate_entries_not_validated=sum(x['unique_candidate'] for x in rows),prepared_places_remaining=2,inserted_this_pass=87,existing_french_reviewed_this_pass=6,physical_positions_examined_this_pass=87,next_position=2048,native_grammar_helpers_previous=4,compound_spell_names_previous=16,unapproved_native_decode_positions=[x['position'] for x in rows if x['unapproved_native_decode']],native_control_positions=[x['position'] for x in rows if x['has_native_controls']],pointer_groups=157,reachable_pool_bytes=sum(len(names[x['sids'][0]][1]) for x in meta),reachable_pool_offset=NAME,name_allocation_limit=NAME_LIMIT,legacy_pool_preserved_offset=POOL,old_pool_end_reference=0x3bc712,uninterpreted_tail_must_not_be_reclaimed=True,inherited_tail_prefix_consumed_bytes=0,restored_tail_bytes=2050,table_bound_native_SIDs_checked=2477,dynamic_native_SIDs_excluded=35,tail_reserve_report='../v0.65/qa-storage.json',all_offset_alias_hash_metadata_sha256=sha(json.dumps(meta,sort_keys=True).encode()),width_reference_audit=widths,limits=['AUTRE includes English,French inherited,proper names and technical labels; language is not inferred automatically.','No Japanese characters does not prove French.','Empty entries are not automatically missing; placeholders are explicit unresolved labels.','Exact DS candidates still need source context,alias,length,command and window review.','All other resources and natural paths still need exhaustive inventory; these2512 SIDs do not cover all resources.','Reference widths are documentation thresholds,not measured runtime window bounds.'])
q.update(parsed_VF_SIDs=2512,runtime_entry_count_proven=False,source_JP_opaque_SIDs=list(range(2506,2512)),observed_region_boundaries_reclassified=True,region_classification_not_a_ROM_change=True)
(O/'inventaire-noms-v078.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(json.dumps(counts),len(rows),'physical',464,'aliases')

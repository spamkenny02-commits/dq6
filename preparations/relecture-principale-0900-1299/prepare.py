"""Reproduce manual review900–1299 without inventing native tests."""
from pathlib import Path
import json,hashlib,re,collections
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,d):(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
notes=read(P/'notes.json');assert set(map(int,notes))==set(range(900,1300));sel=read(R/'dq6-fr/v0.56/insertion-candidates.json');byid={x['id']:x for x in sel};assert len(sel)==6957
jp={x['id']:x for x in read(R/'dq6-fr/clean-base/sfc-jp.json')};ja={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-ja.json')};fr={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-fr.json')}
norm=lambda t:t.replace('\\n','\n').replace('\\t','\t').replace('\\u3000','\u3000')
extras={969:[('data/MESS6/FR/0088.p',807)]}
def refs_for(row):
 links={};ns=row.get('ds_id',[]);ns=[ns] if isinstance(ns,int) else ns
 for n in ns:links[(row['ds_file'],n)]=['REFERENCE_DE_LA_SELECTION_PUBLIEE']
 for ref in row.get('ds_references',[]):
  j=ja[(ref['file'],ref['id'])];f=fr[(ref['file'].replace('/JA/','/FR/'),ref['id'])];assert norm(ref['ja'])==j['text'] and norm(ref['fr'])==f['text'],(row['id'],ref['id'])
  links.setdefault((f['file'],ref['id']),[]).append(ref.get('scope','REFERENCE_EXPLICITE'))
 for key in extras.get(row['id'],[]):links.setdefault(key,[]).append('COMPARAISON_VARIANTE_OU_COMPOSITION_NON_INSEREE')
 out=[]
 for (file,n),scopes in links.items():
  f=fr[(file,n)];j=ja[(file.replace('/FR/','/JA/'),n)];out.append(dict(FR_file=file,JA_file=j['file'],id=n,FR_text=f['text'],JA_text=j['text'],scopes=scopes,FR_record_sha256=sha(json.dumps(f,ensure_ascii=False,sort_keys=True).encode()),JA_record_sha256=sha(json.dumps(j,ensure_ascii=False,sort_keys=True).encode())))
 return out
changes={int(k):v for k,v in read(P/'decisions.json').items()};assert len(changes)==55
semantic={955,961,1002,1003,1012,1045,1082,1105,1131};orthography={1018,1151,1181,1252};context=semantic|orthography
reserves={916,918,921,934,935,936,938,939,940,943,944,960,969,970,983,984,989,998,1002,1003,1004,1008,1010,1012,1021,1028,1032,1035,1037,1045,1048,1062,1066,1078,1079,1080,1082,1085,1086,1092,1095,1096,1105,1107,1116,1119,1124,1125,1131,1132,1134,1135,1137,1138,1140,1144,1145,1150,1152,1155,1156,1158,1159,1161,1177,1178,1179,1181,1182,1188,1190,1196,1197,1198,1199,1200,1201,1203,1206,1212,1213,1218,1222,1223,1224,1232,1234,1236,1237,1238,1247,1249,1250,1259,1261,1262,1263,1267,1268,1269,1270,1274,1278,1279,1281,1282,1289,1291,1295,1296,1297,1298,1299}
ledger=[];proposals=[];glyph_ids=[]
for mid in range(900,1300):
 row=byid[mid];th=sha(json.dumps(row['tokens'],separators=(',',':')).encode());refs=refs_for(row)
 for ref in refs:
  if mid==989:ref['scopes']=['APPUI_LEXICAL_AUTRE_FICHIER_SCENE_NON_ETABLIE']
  if mid==969:ref['scopes']=['VARIANTE_EDITION_DS_JUS_VS_VIN_SFC_COMPARAISON_SEULEMENT']
 entry=dict(id=mid,status='PREPARE_NON_INSERE',review_outcome='PROPOSITION_REVISION' if mid in changes else ('RELU_AVEC_RESERVES' if mid in reserves else 'RELU_TEXTE_CONSERVE'),old_text=row['text'],old_tokens=row['tokens'],old_tokens_sha256=th,source_selection_file='dq6-fr/v0.56/insertion-candidates.json',source_japanese=row.get('source_japanese'),JP_record_sha256=sha(json.dumps(jp[mid],ensure_ascii=False,sort_keys=True).encode()),secondary_IPS_text=row.get('sfc_previous'),DS_references=refs,note=notes[str(mid)],native_tested=False,full_reread_final_accepted=False)
 if mid in changes:
  proposed=row['text']
  for before,after in changes[mid]:assert proposed.count(before)==1,(mid,before);proposed=proposed.replace(before,after)
  controls=lambda text:re.findall('[\ue000-\ue0ff]',text)
  assert proposed!=row['text'] and controls(proposed)==controls(row['text'])
  needs_glyph=bool((set(proposed)-set(row['text']))&{'À','Ç','œ'})
  if needs_glyph:glyph_ids.append(mid)
  kind='SENS_OU_CONSIGNE' if mid in semantic else ('ORTHOGRAPHE_OU_PONCTUATION' if mid in orthography else 'TYPOGRAPHIE_SOUS_RESERVE_DE_GLYPHE')
  blockers=['ROM absente : aucune nouvelle sélection encodée,insertion,réapplication BPS/IPS ou émulation.']
  if needs_glyph:blockers.append('Glyphe À/Ç/œ absent du charset principal v056 : ne pas insérer sans extension et rendu vérifiés.')
  if mid in context:blockers.append('Formulation,commande,contexte et pagination à tester sur la scène SFC ; diagnostic distinct du parcours naturel.')
  if mid in [1105,1131]:blockers.append('Différence géographique entre langues/éditions : carte SFC et chemin natif non inspectés dans ce lot.')
  proposals.append(dict(id=mid,status='PREPARE_NON_INSERE',kind=kind,glyph_dependent=needs_glyph,old_text=row['text'],proposed_text=proposed,old_tokens_sha256=th,native_baseline_tokens_preserved=row['tokens'],replacements=[dict(before=a,after=b) for a,b in changes[mid]],reason=notes[str(mid)],blockers=blockers,new_selection_generated=False,new_tokens_generated=False,integrated=False,native_tested=False));entry['proposal']=proposed
 ledger.append(entry)
assert [x['id'] for x in ledger]==list(range(900,1300)) and len(proposals)==55
assert not {'Ç','œ','À'}&set(read(R/'dq6-fr/v0.56/charset.json').values())
# One readable representation disagrees with its token field; preserve both as evidence.
r=byid[1179];assert r['text'].count(chr(0xe000))==1 and chr(0xe0c9) not in r['text'] and r['tokens'].count(0xc9)==1
assert byid[1177]['source_japanese'].count('[CODE D4]')==15
variable_audit=dict(status='ECART_REPRESENTATION_PUBLIEE_A_REDECODER',id=1179,readable_text=r['text'],old_tokens=r['tokens'],old_tokens_sha256=sha(json.dumps(r['tokens'],separators=(',',':')).encode()),source_japanese=r['source_japanese'],DS_references=refs_for(r),readable_PUA={'U+E000':1,'U+E0C9':0},token_field_C9=1,compiled_ROM_defect_proven=False,compiled_ROM_redecoded=False,tokens_modified=False,proposed_new_tokens=None,required_action='Redécoder la ROM reconstruite depuis source intacte,comparer C9 à la sélection et au rendu de Judith ; ne pas réencoder le texte lisible divergent sans résolution.')
route_ids=[955,960,961,962,1001,1002,1003,1010,1012,1018,1038,1045,1105,1131,1135,1137,1150,1252,1291]
route=[]
for mid in route_ids:
 row=byid[mid];route.append(dict(id=mid,source_japanese=row['source_japanese'],old_text=row['text'],old_tokens_sha256=sha(json.dumps(row['tokens'],separators=(',',':')).encode()),DS_references=refs_for(row),proposed_text=next((x['proposed_text'] for x in proposals if x['id']==mid),None),note=notes[str(mid)]))
route_audit=dict(status='OUVERT_PREPARE_NON_INSERE',scope='Comparaison des consignes/objets/éditions dans les400positions, pas parcours naturel.',comparison_rows=route,cap_direction1105=dict(SFC_JP='北西:nord-ouest',DS_JP='北西:nord-ouest',DS_FR='nord-est',proposal='nord-ouest',SFC_map_verified=False),inherited1135=dict(actual_full_preparatory_reread_this_batch=True,SFC_action='放てば:lancer/libérer',DS_action='かざせば:lever/exposer',text_kept=True,cap_sea_orb_native_sequence_verified=False,reserve_closed=False),right_barrel_or_sleep_effect_verified=False,capture_confiscation_or_keys_tested=False,global_direction_replace_performed=False,northeast1291_retained=True,required_tests=['961: point arrière et déclenchement exact avant Magnus ; ne pas confondre consigne avec route962.','1002/1003/1045: vin offert au capitaine,confiscation puis sommeil sans mort des gardes.','1105/1131/1135: carte SFC,cap,orientation,objet orbe et action naturelle,avec mauvais emplacement et mauvais objet comme diagnostics séparés.','Variantes équipe seule/groupe,noms longs,DA/DB/D4/D3/C4,pagination et glyphes.'])
save('registre-relecture.json',ledger);save('revisions-preparees-non-inserees.json',proposals);save('audit-consignes-orbe-vin.json',route_audit);save('audit-variable-1179.json',variable_audit)
save('qa-preparation.json',dict(baseline_commit='62a18d6e1d209a39c6b6e5b6f7c3caf6045b4f3a',baseline_release='v0.78',reviewed_positions=list(range(900,1300)),reviewed_positions_count=400,silence_composition_IDs=[1138,1178],new_prepared_existing_main_revisions=55,glyph_dependent_proposals=len(glyph_ids),glyph_dependent_IDs=glyph_ids,semantic_proposals=len(semantic),orthography_punctuation_proposals=len(orthography),mixed_semantic_and_glyph_IDs=sorted(set(glyph_ids)&semantic),main_prepared_revisions_previous=71,main_prepared_revisions_current=126,names_prepared_unchanged=419,semantic_review_pending_runtime_cumulative=900,full_main_reread_final_accepted_added=0,new_encoded_selections=0,new_integrated=0,new_translations=0,ROM_sources_available=False,ROM_rebuilt=False,emulator_executed=False,inherited1135_closed=False,variable1179_ROM_bug_proven=False,source_selection_sha256=sha((R/'dq6-fr/v0.56/insertion-candidates.json').read_bytes()),DS_JA_sha256=sha((R/'dq6-fr/clean-base/ds-ja.json').read_bytes()),DS_FR_sha256=sha((R/'dq6-fr/clean-base/ds-fr.json').read_bytes()),notes_sha256=sha((P/'notes.json').read_bytes()),decisions_sha256=sha((P/'decisions.json').read_bytes()),all_original_tokens_preserved_not_reencoded=True))
print('400 positions;55 proposals;glyph-dependent',len(glyph_ids),';0 integrated;0 native tests')

"""Reproduce manual review800–899 without inventing native tests."""
from pathlib import Path
import json,hashlib,re,collections
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,d):(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
notes=read(P/'notes.json');assert set(map(int,notes))==set(range(800,900));sel=read(R/'dq6-fr/v0.56/insertion-candidates.json');byid={x['id']:x for x in sel};assert len(sel)==6957
jp={x['id']:x for x in read(R/'dq6-fr/clean-base/sfc-jp.json')};ja={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-ja.json')};fr={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-fr.json')}
norm=lambda t:t.replace('\\n','\n').replace('\\t','\t').replace('\\u3000','\u3000')
extras={852:[('data/MESS6/FR/0088.p',n) for n in [109,110,111]]}
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
changes={804:[('ça fait plaisir','Ça fait plaisir')],815:[('à une époque','À une époque'),('soeur','sœur'),('coeur','cœur')],817:[('à Morneville','À Morneville'),('ça fait cinq','Ça fait cinq')],823:[('Soeur','Sœur'),('ça, par exemple','Ça, par exemple'),('âME','ÂME')],824:[('Soeur','Sœur')],825:[('Soeur','Sœur')],826:[('Soeur','Sœur')],832:[('ça ne va pas','Ça ne va pas')],842:[('coeur','cœur')],846:[('ça fait un siècle','Ça fait un siècle')],848:[('coeur','cœur')],852:[("mieux vaudrait d'abord vous laisser capturer pour observer les lieux.","mieux vaudrait d'abord faire semblant d'être en captivité pour observer les lieux.")],875:[('Soyez très prudents !','Faites preuve de la plus grande prudence !')],876:[('soyez prudents.','faites preuve de prudence.')],879:[('Soeur','Sœur')],883:[('soeur','sœur')],888:[('augmenter le rationnement','augmenter les rations')],895:[('ça ne va pas la tête','Ça ne va pas la tête')]}
context={852,875,876,888};reserves={807,814,817,819,825,826,828,833,836,838,841,845,848,849,850,851,855,866,867,868,869,871,873,874,875,876,885,886,887,897,898};ledger=[];proposals=[]
for mid in range(800,900):
 row=byid[mid];th=sha(json.dumps(row['tokens'],separators=(',',':')).encode());refs=refs_for(row)
 for ref in refs:
  if mid==828:ref['scopes']=['LEXIQUE_SEULEMENT_REFERENCE_HERITEE_RECEVOIR_VS_PRESENTER']
 entry=dict(id=mid,status='PREPARE_NON_INSERE',review_outcome='PROPOSITION_REVISION' if mid in changes else ('RELU_AVEC_RESERVES' if mid in reserves else 'RELU_TEXTE_CONSERVE'),old_text=row['text'],old_tokens=row['tokens'],old_tokens_sha256=th,source_selection_file='dq6-fr/v0.56/insertion-candidates.json',source_japanese=row.get('source_japanese'),JP_record_sha256=sha(json.dumps(jp[mid],ensure_ascii=False,sort_keys=True).encode()),secondary_IPS_text=row.get('sfc_previous'),DS_references=refs,note=notes[str(mid)],native_tested=False,full_reread_final_accepted=False)
 if mid in changes:
  proposed=row['text']
  for before,after in changes[mid]:assert proposed.count(before)==1,(mid,before);proposed=proposed.replace(before,after)
  controls=lambda text:re.findall('[\ue000-\ue0ff]',text)
  assert proposed!=row['text'] and controls(proposed)==controls(row['text'])
  blockers=['ROM absente : aucun nouvel encodage,insertion,patch ou rendu natif.']
  blockers.append('Contexte,pagination,noms variables à tester naturellement.' if mid in context else 'Glyphes À/Ç/Â/œ requis à auditer ; aucune extension effectuée.')
  proposals.append(dict(id=mid,status='PREPARE_NON_INSERE',kind='CONTEXTE_OU_NEUTRALITE' if mid in context else 'TYPOGRAPHIE_SOUS_RESERVE_DE_GLYPHE',old_text=row['text'],proposed_text=proposed,old_tokens_sha256=th,native_baseline_tokens_preserved=row['tokens'],replacements=[dict(before=a,after=b) for a,b in changes[mid]],reason=notes[str(mid)],blockers=blockers,new_selection_generated=False,new_tokens_generated=False,integrated=False,native_tested=False));entry['proposal']=proposed
 ledger.append(entry)
assert len(ledger)==100 and len(proposals)==18
assert not {'Ç','œ','À','Â'}&set(read(R/'dq6-fr/v0.56/charset.json').values())
audit=dict(status='OUVERT_PREPARE_NON_INSERE',scope='Comparaison textuelle828/852/875/876/888, aucun événement natif exécuté.',reference828=dict(source_action='Présenter la pipe',inherited_DS_action='Recevoir la pipe',scope='LEXIQUE_SEULEMENT',text_kept=True),capture852=dict(JP_phrase='とらえられたフリ',DS_reference='data/MESS6/FR/0088.p:110',old='se laisser capturer',proposed="faire semblant d'être en captivité",DB_tokens_preserved=byid[852]['tokens'].count(0xdb),native_state_verified=False),gender_neutral_revisions=[875,876],rations888=dict(JP_phrase='もうすこし 食べものを',old='augmenter le rationnement',proposed='augmenter les rations',official_DS_lexical_revision=True),event_flags_inspected=False,natural_scene_executed=False,required_tests=['Pipe: réponses oui/non,présentation à Airain,remise des outils.','Captivité feinte,captures réelles,clé,tenues et infiltration.','DA/DB/D4 et D3/C4: gardiens,Croisefer,réincarcération.','Nouvelles phrases,noms variables,pagination et glyphes.'])
assert audit['capture852']['DB_tokens_preserved']==3
save('registre-relecture.json',ledger);save('revisions-preparees-non-inserees.json',proposals);save('audit-pipe-captivite-rations.json',audit)
save('qa-preparation.json',dict(baseline_commit='76a6d06ef60ba08dbdaf0b7d910c3b8897872d4f',baseline_release='v0.78',reviewed_positions=list(range(800,900)),reviewed_positions_count=100,silence_composition_IDs=[897],new_prepared_existing_main_revisions=18,glyph_dependent_proposals=14,context_or_neutrality_proposals=4,main_prepared_revisions_previous=53,main_prepared_revisions_current=71,names_prepared_unchanged=419,semantic_review_pending_runtime_cumulative=500,full_main_reread_final_accepted_added=0,new_encoded_selections=0,new_integrated=0,new_translations=0,ROM_sources_available=False,ROM_rebuilt=False,emulator_executed=False,source_selection_sha256=sha((R/'dq6-fr/v0.56/insertion-candidates.json').read_bytes()),DS_JA_sha256=sha((R/'dq6-fr/clean-base/ds-ja.json').read_bytes()),DS_FR_sha256=sha((R/'dq6-fr/clean-base/ds-fr.json').read_bytes()),notes_sha256=sha((P/'notes.json').read_bytes()),all_original_tokens_preserved_not_reencoded=True))
print('100 positions;18 proposals;0 integrated;0 native tests')

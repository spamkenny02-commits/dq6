"""Reproduce manual dialogue review and a separate mechanical provenance diagnostic."""
from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,d):(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
notes=read(P/'notes.json');assert set(map(int,notes))==set(range(500,600));selected=read(R/'dq6-fr/v0.56/insertion-candidates.json');assert len(selected)==6957
jp={x['id']:x for x in read(R/'dq6-fr/clean-base/sfc-jp.json')};ja={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-ja.json')};fr={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-fr.json')};BB=chr(0xe0bb)
changes={501:[('ça fait du bien','Ça fait du bien')],507:[('ça a un succès','Ça a un succès')],521:[('à boire! Je veux à boire!','À boire! Je veux à boire!')],531:[('ça fait des années','Ça fait des années')],546:[("C'est la dernière fois que je prends un poste à temps partiel.","C'est la dernière fois que j'embauche quelqu'un à temps partiel.")],547:[('la paix va revenir dans le monde','la paix est revenue dans le monde')],556:[('je pourrais lui demander','je pourrai lui demander')],560:[("l'oeil de Lynx","l'œil de Lynx")],561:[('un oeil à votre inventaire','un œil à votre inventaire')],565:[('un oeil à la poignée','un œil à la poignée')],570:[('à Colombourg,','À Colombourg,')],574:[('Le tarif de la nuit en or est de '+BB+'.',"Le tarif est de "+BB+" pièces d'or la nuit, je crois.")]}
kinds={546:'ROLE_DU_LOCUTEUR_EMPLOYEUR',547:'TEMPS_DU_FAIT_RAPPORTE',556:'PROJECTION_FUTURE',574:'FORMULATION_DU_TARIF_VARIABLE'};glyphs={560:['œ'],561:['œ'],565:['œ'],501:['Ç'],507:['Ç'],521:['À'],531:['Ç'],570:['À']};reserves={500,532,541,545,554,562,576,581,582,598,599};ledger=[];proposals=[]
for row in selected:
 mid=row['id']
 if not 500<=mid<600:continue
 ns=row.get('ds_id',[]);ns=[ns] if isinstance(ns,int) else ns;links=[(row['ds_file'],n,'REFERENCE_DE_LA_SELECTION_PUBLIEE') for n in ns]
 if mid==500:links += [('data/MESS6/FR/0075.p',n,'COMPARAISON_VARIANTE_NON_INSEREE') for n in [973,974,975]]
 refs=[]
 for fpath,n,role in links:
  f=fr[(fpath,n)];j=ja[(fpath.replace('/FR/','/JA/'),n)];refs.append(dict(FR_file=fpath,JA_file=j['file'],id=n,FR_text=f['text'],JA_text=j['text'],role=role,FR_record_sha256=sha(json.dumps(f,ensure_ascii=False,sort_keys=True).encode()),JA_record_sha256=sha(json.dumps(j,ensure_ascii=False,sort_keys=True).encode())))
 th=sha(json.dumps(row['tokens'],separators=(',',':')).encode());entry=dict(id=mid,status='PREPARE_NON_INSERE',review_outcome='PROPOSITION_REVISION' if mid in changes else ('RELU_AVEC_RESERVES' if mid in reserves else 'RELU_TEXTE_CONSERVE'),old_text=row['text'],old_tokens=row['tokens'],old_tokens_sha256=th,source_japanese=row.get('source_japanese'),source_selection_file='dq6-fr/v0.56/insertion-candidates.json',JP_record_sha256=sha(json.dumps(jp[mid],ensure_ascii=False,sort_keys=True).encode()),secondary_IPS_text=row.get('sfc_previous'),DS_references=refs,note=notes[str(mid)],full_reread_final_accepted=False,native_tested=False)
 if mid in changes:
  text=row['text']
  for before,after in changes[mid]:assert text.count(before)==1,(mid,before);text=text.replace(before,after)
  controls=lambda t:re.findall('[\ue000-\ue0ff]',t)
  assert controls(text)==controls(row['text']) and text!=row['text']
  if mid==574:assert text.count(BB)==row['text'].count(BB)==1
  blockers=['Sources ROM absentes : encodage, sélections natives, largeur et pagination non validés.']
  if mid in glyphs:blockers.append('Caractère requis absent du charset principal v056 : '+','.join(glyphs[mid])+'. Pas de nouveau glyphe déclaré disponible.')
  if mid in [546,547,556]:blockers.append('Correction isolée du français hérité, qui diffère aussi du français DS ; contexte naturel à confirmer avant insertion.')
  proposal=dict(id=mid,status='PREPARE_NON_INSERE',kind=kinds.get(mid,'LIGATURE_SOUS_RESERVE_DE_GLYPHE' if mid in [560,561,565] else 'CAPITALE_SOUS_RESERVE_DE_GLYPHE'),old_text=row['text'],proposed_text=text,old_tokens_sha256=th,native_baseline_tokens_preserved=row['tokens'],replacements=[dict(before=a,after=b) for a,b in changes[mid]],reason=notes[str(mid)],blockers=blockers,new_selection_generated=False,new_tokens_generated=False,integrated=False,native_tested=False)
  proposals.append(proposal);entry['proposal']=text
 ledger.append(entry)
assert [x['id'] for x in ledger]==list(range(500,600)) and len(proposals)==12
charset=read(R/'dq6-fr/v0.56/charset.json');assert not {'Ç','À','œ'}&set(charset.values())
# A method name is not sufficient evidence of a usable DS link in that selection row.
gaps=[dict(id=x['id'],method=x['method'],selection_record_sha256=sha(json.dumps(x,ensure_ascii=False,sort_keys=True).encode()),ds_file=x.get('ds_file'),ds_id=x.get('ds_id'),ds_references=x.get('ds_references'),semantic_review_in_this_batch=500<=x['id']<600) for x in selected if 'references_DS_explicites' in x.get('method','') and not x.get('ds_references') and not x.get('ds_file')]
assert len(gaps)==315
save('registre-relecture.json',ledger);save('revisions-preparees-non-inserees.json',proposals)
save('diagnostic-provenance-selection.json',dict(scope='Champs de la sélection v056 seulement, pas tous les registres ou archives du projet.',mechanical_scan=True,new_semantic_reviews_from_scan=0,new_missing_translations_claimed=0,count=315,does_not_prove_absence_in_other_project_records=True,does_not_invalidate_all_translations=True,action='Rechercher les références dans les registres historiques ou qualifier explicitement les adaptations SFC ; ne pas considérer le nom de méthode comme preuve autonome.',entries=gaps))
q=dict(baseline_commit='ef5cf2071f53e47d532f096270ade31257d69e3a',baseline_release='v0.78',reviewed_positions=list(range(500,600)),reviewed_positions_count=100,silence_composition_IDs=[532],new_prepared_existing_main_revisions=12,glyph_dependent_proposals=8,isolated_context_grammar_or_formulation_proposals=4,new_encoded_selections=0,new_integrated=0,new_translations=0,names_prepared_unchanged=419,main_prepared_revisions_previous=11,main_prepared_revisions_current=23,semantic_review_pending_runtime_cumulative=200,full_main_reread_final_accepted_added=0,ROM_sources_available=False,ROM_rebuilt=False,emulator_executed=False,all100_native_tested=False,provenance_metadata_gap_count=315,metadata_scan_not_semantic_review=True,source_selection_sha256=sha((R/'dq6-fr/v0.56/insertion-candidates.json').read_bytes()),DS_JA_sha256=sha((R/'dq6-fr/clean-base/ds-ja.json').read_bytes()),DS_FR_sha256=sha((R/'dq6-fr/clean-base/ds-fr.json').read_bytes()),charset_sha256=sha((R/'dq6-fr/v0.56/charset.json').read_bytes()),notes_sha256=sha((P/'notes.json').read_bytes()))
save('qa-preparation.json',q);print('100 positions;12 proposed revisions;315 metadata gaps diagnosed separately;0 integrated')

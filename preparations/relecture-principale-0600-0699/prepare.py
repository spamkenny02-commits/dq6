"""Reproduce manual review600–699 and a non-runtime text audit of inherited reserve610."""
from pathlib import Path
import json,hashlib,re,collections
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,d):(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
notes=read(P/'notes.json');assert set(map(int,notes))==set(range(600,700));sel=read(R/'dq6-fr/v0.56/insertion-candidates.json');byid={x['id']:x for x in sel};assert len(sel)==6957
jp={x['id']:x for x in read(R/'dq6-fr/clean-base/sfc-jp.json')};ja={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-ja.json')};fr={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-fr.json')}
norm=lambda t:t.replace('\\n','\n').replace('\\t','\t').replace('\\u3000','\u3000')
def refs_for(row):
 links=[];ns=row.get('ds_id',[]);ns=[ns] if isinstance(ns,int) else ns
 for n in ns:links.append((row['ds_file'],n,'REFERENCE_DE_LA_SELECTION_PUBLIEE'))
 for r in row.get('ds_references',[]):
  j=ja[(r['file'],r['id'])];f=fr[(r['file'].replace('/JA/','/FR/'),r['id'])]
  assert norm(r['ja'])==j['text'] and norm(r['fr'])==f['text'],(row['id'],r['id'],'escaped_reference')
  links.append((f['file'],r['id'],r.get('scope','REFERENCE_EXPLICITE')))
 out=[]
 for file,n,scope in links:
  f=fr[(file,n)];j=ja[(file.replace('/FR/','/JA/'),n)];out.append(dict(FR_file=file,JA_file=j['file'],id=n,FR_text=f['text'],JA_text=j['text'],scope=scope,FR_record_sha256=sha(json.dumps(f,ensure_ascii=False,sort_keys=True).encode()),JA_record_sha256=sha(json.dumps(j,ensure_ascii=False,sort_keys=True).encode())))
 return out
changes={605:[("ça doit être ça, d'être un sage.","Ça doit être ça, d'être un sage.")],610:[('Il y est question de détenir la vérité, je crois...',"Il y est question d'avoir le coeur pur, je crois..."),('ça parle de lame et de galets, je crois ? Enfin, vous voyez.','Une lame qui cache sa force, peut-être ? Enfin, vous voyez.')],623:[("ça n'a plus d'importance.","Ça n'a plus d'importance.")],625:[('Kad Abra. à votre mine','Kad Abra. À votre mine')],626:[('Leur oeuvre est','Leur œuvre est')],630:[('à une époque,','À une époque,')],633:[('ça va me coûter','Ça va me coûter')],647:[('à la vôtre!','À la vôtre!')],652:[('ça nous fait un total','Ça nous fait un total')],657:[('à la prochaine,','À la prochaine,')],659:[('à la prochaine!','À la prochaine!')],669:[('ça va de mal en pis','Ça va de mal en pis')],671:[('ça fait un bail','Ça fait un bail')],677:[("à ce qu'on dit, il n'achète que des informations. Il reçoit en échange des renseignements pour s'enrichir, à ce qu'on dit...","Il reçoit en échange des renseignements pour s'enrichir.")],681:[('à moins, bien sûr,','À moins, bien sûr,')],684:[('Mon oeil, ouais!','Mon œil, ouais!')],686:[("ça vous dirait de l'acheter?","Ça vous dirait de l'acheter?")],694:[('au coeur de la mine','au cœur de la mine'),('à moins que...','À moins que...')]}
reserves={601,602,610,618,638,641,649,650,663};ledger=[];proposals=[]
for row in sel:
 mid=row['id']
 if not 600<=mid<700:continue
 refs=refs_for(row);th=sha(json.dumps(row['tokens'],separators=(',',':')).encode());entry=dict(id=mid,status='PREPARE_NON_INSERE',review_outcome='PROPOSITION_REVISION' if mid in changes else ('RELU_AVEC_RESERVES' if mid in reserves else 'RELU_TEXTE_CONSERVE'),old_text=row['text'],old_tokens=row['tokens'],old_tokens_sha256=th,source_selection_file='dq6-fr/v0.56/insertion-candidates.json',source_japanese=row.get('source_japanese'),JP_record_sha256=sha(json.dumps(jp[mid],ensure_ascii=False,sort_keys=True).encode()),secondary_IPS_text=row.get('sfc_previous'),DS_references=refs,note=notes[str(mid)],native_tested=False,full_reread_final_accepted=False)
 if mid in changes:
  proposed=row['text']
  for before,after in changes[mid]:assert proposed.count(before)==1,(mid,before);proposed=proposed.replace(before,after)
  assert proposed!=row['text'] and re.findall('[\ue000-\ue0ff]',proposed)==re.findall('[\ue000-\ue0ff]',row['text'])
  glyphs=sorted(set(proposed)&set('ÇÀœ'));kind='HARMONISATION_INDICES_SFC_SOUS_RESERVE_NATURELLE' if mid==610 else ('SIMPLIFICATION_ADAPTATION_HERITEE' if mid==677 else 'TYPOGRAPHIE_SOUS_RESERVE_DE_GLYPHE')
  blockers=['Sources ROM absentes : aucun encodage,insertion,reconstruction ou essai natif.']
  if mid==610:blockers.append('Ordre des réponses,branches de succès/échec,relecture des trois menus/échos et pagination des dix propos à tester naturellement ; réserve610 ouverte.')
  elif mid==677:blockers.append('Vérifier le contexte et la pagination de la simplification avant insertion.')
  else:blockers.append('Caractères requis absents du charset principal actuel : '+','.join(glyphs))
  proposals.append(dict(id=mid,status='PREPARE_NON_INSERE',kind=kind,old_text=row['text'],proposed_text=proposed,old_tokens_sha256=th,native_baseline_tokens_preserved=row['tokens'],replacements=[dict(before=a,after=b) for a,b in changes[mid]],reason=notes[str(mid)],blockers=blockers,new_selection_generated=False,new_tokens_generated=False,integrated=False,native_tested=False));entry['proposal']=proposed
 ledger.append(entry)
assert [x['id'] for x in ledger]==list(range(600,700)) and len(proposals)==18
assert not {'Ç','À','œ'}&set(read(R/'dq6-fr/v0.56/charset.json').values())
# Supplementary seal comparison is not a full reread of all1307–1329 dialogues.
related=[]
for mid in range(1307,1330):
 row=byid[mid];related.append(dict(id=mid,text=row['text'],lines=row.get('lines'),source_japanese=row.get('source_japanese'),tokens_sha256=sha(json.dumps(row['tokens'],separators=(',',':')).encode()),nontext_tokens=[t for t in row['tokens'] if t<0x200],DS_references=refs_for(row)))
for mid in [610,1308,1309]:assert 'Frizzam' in byid[mid]['text']
groups=[]
for menu,echoes,semantic_choice in [(1312,[1313,1314,1315],1),(1317,[1318,1319,1320],3),(1322,[1323,1324,1325],2)]:
 lines=byid[menu]['lines'];assert len(lines)==3 and all(line.startswith(str(i)+' ') for i,line in enumerate(lines,1));opts=[]
 for i,echo in enumerate(echoes,1):
  assert byid[echo]['tokens'].count(0xd5)==1
  e=re.sub('[\ue000-\ue0ff]','',byid[echo]['text']);opts.append(dict(display_position=i,label=lines[i-1][2:],echo_id=echo,echo=e,same_visible_label=lines[i-1][2:]==e))
 groups.append(dict(menu_id=menu,options=opts,semantic_hypothesis_display_position=semantic_choice,success_branch_verified=False))
audit=dict(inherited_reserve_id=610,status='OUVERT_PREPARE_NON_INSERE',comparative_text_audit_only=True,password_spelling_same_in_610_1308_1309=True,password='Frizzam',hint_DS_references=refs_for(byid[610]),old_hint_text=byid[610]['text'],proposed_hint_text=next(x['proposed_text'] for x in proposals if x['id']==610),source_D4_count=byid[610]['tokens'].count(0xd4),source_commands=dict(collections.Counter(f'{t:02X}' for t in byid[610]['tokens'] if t<0x200)),choice_groups=groups,semantic_hypothesis_not_native_success_sequence=True,ROM_or_event_code_inspected=False,natural_scene_executed=False,all_related_IDs_counted_as_new_full_reread=False,related_texts=related,required_tests=['Play native Frizzam and both available player-voice paths.','Read all ten610 parts with their pauses.','Exercise every wrong response and restart.','Prove the actual accepted sequence and echo selection without inferring it solely from semantic labels.','Check success opens the door and preserves flags;diagnostic redirection is not natural play.'])
save('registre-relecture.json',ledger);save('revisions-preparees-non-inserees.json',proposals);save('audit-610-indices-selections.json',audit)
q=dict(baseline_commit='132dc8619e74db7e173df331ec15d4d1ca2ffe5a',baseline_release='v0.78',reviewed_positions=list(range(600,700)),reviewed_positions_count=100,supplementary_seal_comparison_IDs=list(range(1307,1330)),supplementary_not_new_full_reread_count=True,new_prepared_existing_main_revisions=18,glyph_dependent_proposals=16,contextual_harmonization_proposals=2,main_prepared_revisions_previous=23,main_prepared_revisions_current=41,names_prepared_unchanged=419,semantic_review_pending_runtime_cumulative=300,full_main_reread_final_accepted_added=0,reserve610_closed=False,new_encoded_selections=0,new_integrated=0,new_translations=0,ROM_sources_available=False,ROM_rebuilt=False,emulator_executed=False,main_selection_sha256=sha((R/'dq6-fr/v0.56/insertion-candidates.json').read_bytes()),DS_JA_sha256=sha((R/'dq6-fr/clean-base/ds-ja.json').read_bytes()),DS_FR_sha256=sha((R/'dq6-fr/clean-base/ds-fr.json').read_bytes()),notes_sha256=sha((P/'notes.json').read_bytes()),all_original_tokens_preserved_not_reencoded=True)
save('qa-preparation.json',q);print('100 positions;18 proposals;seal610 text audit still open;0 integrated')

"""Durable remaining-case register, exact source restoration and counts."""
from pathlib import Path
import json,hashlib,subprocess,sys
R=Path(__file__).resolve().parent;D=R/'dq6-fr';O=D/'v0.55';B=D/'v0.54';read=lambda p:json.loads(p.read_text());save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2))
jp=read(D/'clean-base/sfc-jp.json');vf=read(D/'clean-base/sfc-vf.json');new=read(O/'insertion-candidates.json');old=read(B/'insertion-candidates.json');done={x['id'] for x in new};remaining=[s for s in jp if s['id'] not in done]
assert len(new)==6941 and len(remaining)==16
proof=read(O/'qa-frontiere-6956.json');p=dict(id=6956,status='PREPARE_NON_INSERE',sfc_jp=jp[6956]['text'],sfc_vf_secondaire=vf[6956]['text'],proposed_french=proof['proposed_french'],blocker=proof['blocker'],ds_reference=proof['ds_reference']);save(O/'nouveaux-prepares-v055.json',[p]);subprocess.run([sys.executable,str(D/'pass55.py')],check=True)
prepared=read(O/'prepares-non-inseres.json');assert len(prepared)==13
blocks=[]
for s in remaining:
 mid=s['id'];reason=next((x['blocker'] for x in prepared if x['id']==mid),'Composition de noms C1 et raccord avec5698 déjà intégré à vérifier ; tester liste singulière/plurielle, noms longs, pagination et cas aucun porteur.')
 blocks.append(dict(id=mid,status='PREPARE_NON_INSERE' if mid in {x['id'] for x in prepared} else 'DIFFERE',sfc_jp=s['text'],sfc_vf_secondaire=vf[mid]['text'],blocker=reason,needed_evidence='Appel natif et contexte technique, effets/branches observables ; pas de validation sur traduction littérale seule.' if mid!=6956 else proof['blocker'],context=[dict(id=i,text=jp[i]['text']) for i in range(max(0,mid-2),min(len(jp),mid+3))]))
save(O/'qa-blocages-reliquat.json',dict(selected=6941,linguistic_selected=6932,structural_selected=9,remaining_linguistic=16,prepared_non_inserted=13,deferred=3,rows=blocks,exhaustive_french_reread_started=False))
struct=[]
for mid in [1,2,3,2358,5699,5700,5775,6213,6214]:
 row=next(x for x in new if x['id']==mid);assert row['tokens']==jp[mid]['tokens']
 struct.append(dict(id=mid,jp_tokens=jp[mid]['tokens'],ips_tokens=vf[mid]['tokens'],final_tokens=row['tokens'],ips_already_identical=vf[mid]['tokens']==jp[mid]['tokens'],linguistic_translation=False))
save(O/'qa-restaurations-structurelles.json',dict(count=9,rows=struct,isolated_legacy_audit='Corrects earlier assumption that every unselected structural entry was already safe in the IPS fallback. 5700/5775 contain unrelated shifted French text;5699/6213 differ in spaces/layout. Source exact restored, not new French translations. Existing6903 selections untouched.'))
sha=hashlib.sha256((O/'result.sfc').read_bytes()).hexdigest();pages=read(O/'qa-render-fixtures.json');comp=read(O/'qa-compositions.json');ids={x['id'] for x in pages['rows']}|{i for x in comp['rows'] for i in x['ids']};review=read(O/'revue-lot-v055.json');assert ids=={x['id'] for x in review if not x.get('structural_only')}
save(O/'qa-relecture-visuelle.json',dict(result_sha256=sha,new_texts=29,source_structures=9,accepted_final_pages=len(pages['rows']),composite_captures=len(comp['rows']),all_final_captures_reviewed=True,all_composite_captures_reviewed=True,reviewed_ids=sorted(ids),boot_menu_reviewed=True,review_method='Read29 standalone pages on3 contact sheets plus full610p13,42 compositions on4 contact sheets plus full1313/1318/1323, and cold boot Nouveau jeu/Journal1–3. No clipping observed. Source empty/control/name-only structures verified separately against JP tokens.',natural_scenes_verified=False,limits='Camp host inserts repeated asterisk labels in riddle echo fixtures; these are inherited host rendering state, not added source commands. Private terminal AF holds captures. This validates rendering/callback continuity, not actual riddle menu event, seal unlock, service dispatch or coordinate computation.'))
print('29 new linguistic +9 source structures;16 linguistic remain;13 prepared +3 deferred')

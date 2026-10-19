"""Reviewed Colombourg follow-up; preserve every previous selection."""
from pathlib import Path
import json,re,shutil
P=Path(__file__).resolve().parent;B=P/'v0.23';O=P/'v0.24'
def read(p):return json.loads(p.read_text())
def save(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
O.mkdir(exist_ok=True)
for name in ['init.py','prepare.py','build.py','verify.py','names.py']:
    if (O/name).exists():continue
    s=(B/name).read_text().replace('v0.23','v0.24')
    if name in ['prepare.py','verify.py']:s=s.replace('v0.22','v0.23').replace('v22','v23')
    if name=='prepare.py':s=s.replace('correspondance_revue_v23','correspondance_revue_v24')
    if name=='build.py':s=s.replace('len(rows)-5098','len(rows)-5128')
    (O/name).write_text(s)
for p in B.glob('*.json'):
    if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','progression-')):continue
    if not (O/p.name).exists():shutil.copy2(p,O/p.name)
choices={528:('0076.p',list(range(63,75))),531:('0076.p',[83,84]),532:('0076.p',[504]),536:('0076.p',[514,515]),547:('0076.p',[720,721]),553:('0076.p',[734,735]),556:('0076.p',[790,791,792,793]),557:('0076.p',[797,798,799]),558:('0076.p',[801]),560:('0076.p',list(range(807,813))),561:('0076.p',[814,815,816]),567:('0075.p',[501,502,503])}
notes={
528:'Recit complet de Lynx apres paiement : forgeron Charles, age 50 si vivant, depart dix ans auparavant, femme Ethel decedee, fille Martel formee a la forge, maison au nord du bar clandestin et tombe au sanctuaire nord. Douze segments JA/FR dans le meme ordre. Le raccourci ludique DS 72 reste sans changer la destination. Aucun nom variable.',
531:'Habitante regrettant de ne plus visiter la tombe de son vieux mari puis citant Martel en exemple. DS 83–84 meme japonais ; jiisan designe ici le mari dans la localisation feminine, et non un visiteur comme le suppose a tort la VF secondaire.',
532:'Silence de Martel avant la demande d’usage de l’epee : DS 504, suivi de 505–506 deja integres en 533. Pas le silence de la premiere rencontre 414. Label Martel conserve ; terminaison AE native.',
536:'Acceptation de la promesse : Martel exige un regard fixe puis silence, DS 514–515. Meme embranchement apres 510 et avant regard detourne 518 ; terminaison AE et commandes D4/D9 natives.',
547:'Visiteur sur le depart, recherche du forgeron infructueuse et doute sur la paix : DS 720–721, deux idees identiques. Aucun forgeron pretendument revenu comme dans la VF secondaire erronee.',
553:'Chercheur de Lynx apres nouvelles de l’epee : SFC et DS JA parlent des armes ET armures legendaires, mais FR 734 dit seulement epee. Adaptation minimale reliques legendaires, terme officiel DS utilise par Lynx en 810. Suite 735 conservee.',
556:'Admirateur de Seductra projetant le mariage dans dix ans apres la fin de carriere sur scene : DS 790–793 complet. Meme raisonnement maladroit que SFC, nom officiel Seductra sans remplacer par un nom variable.',
557:'Habitant apprend que le groupe a trouve l’epee, regrette que Charles ne les ait pas attendus puis rappelle les dix ans. DS 797–799, trois idees et ordre conserves.',
558:'Buveur apres la nouvelle sur Charles : ivresse DS 801, ancree entre 797–799 et la question sur Lynx 803 ; pas un hoquet de comptoir generique.',
560:'Lynx apres rencontre de Martel : service gratuit, quatre reliques, inscriptions clefs d’enigme puis reserve sur la fiabilite. DS 807–812 entier. Aucune demande de paiement ou d’objet comme la VF secondaire semble en ajouter.',
561:'Habitante avouant avoir fouille l’inventaire puis promettant le secret : DS 814–816 complet. Aucune commande d’inventaire ajoutee, c’est uniquement son discours.',
567:'Refus d’entree a Colombourg sans laissez-passer : DS 0075:501–503, identique au duplicata 0037:0–2. Contexte ancre par presentation du pendentif en 504 et accueil en 505, pas accueil interieur 510. Terminaison AE conservee.'}
jp={r['id']:r for r in read(P/'clean-base/sfc-jp.json')};vf={r['id']:r for r in read(P/'clean-base/sfc-vf.json')}
ja={(r['file'].split('/')[-1],r['id']):r for r in read(P/'clean-base/ds-ja.json') if '/MESS6/' in r['file']}
fr={(r['file'].split('/')[-1],r['id']):r for r in read(P/'clean-base/ds-fr.json') if '/MESS6/' in r['file']}
assert not {r['id'] for r in read(B/'insertion-candidates.json')}&set(choices)
reviews=[]
for mid,(file,ids) in choices.items():
    r=dict(id=mid,file=file,ids=ids,sfc_jp=jp[mid]['text'],sfc_vf_secondaire=vf[mid]['text'],ds_jp=[ja[(file,i)]['text'] for i in ids],ds_fr=[fr[(file,i)]['text'] for i in ids],review=notes[mid],status='RELU')
    if mid==553:
        parts=[]
        for i in ids:
            m=re.fullmatch(r'@a([^@]*)@b(.*?)\n?@c0@',fr[(file,i)]['text'],re.S);assert m
            s=m.group(2).strip();parts.append(s[3:] if s.startswith('*ⓢ ') else s)
        original=' '.join(parts);assert "l'épée légendaire" in original
        r.update(original_body=original,adaptation_body=original.replace("l'épée légendaire",'les reliques légendaires'),adaptation_review='Retablit armes et armures du japonais SFC/DS avec le terme DS officiel de 810 ; ne limite pas la question a la seule epee. Suite 735 inchangee.')
    reviews.append(r)
if (O/'revue-lot-v024.json').exists():assert read(O/'revue-lot-v024.json')==reviews
else:save('revue-lot-v024.json',reviews)
existing=read(O/'correspondances-revues.json');byid={r['id']:r for r in existing}
for r in reviews:
    if r['id'] in byid:assert byid[r['id']]==r
    else:existing.append(r)
save('correspondances-revues.json',existing)
adapt=read(O/'adaptations-francaises.json')
for r in reviews:
    if 'adaptation_body' not in r:continue
    row=dict(id=r['id'],file=r['file'],ids=r['ids'],original_body=r['original_body'],body=r['adaptation_body'],review=r['adaptation_review'])
    prior=next((a for a in adapt if a['id']==r['id']),None)
    if prior:assert prior==row
    else:adapt.append(row)
save('adaptations-francaises.json',adapt)
print('v0.24 reviewed input delta ready:',len(reviews),'messages')

"""Recreate the reviewed Colombourg delta while freezing prior selections."""
from pathlib import Path
import json,re,shutil
P=Path(__file__).resolve().parent;B=P/'v0.22';O=P/'v0.23'
def read(p):return json.loads(p.read_text())
def save(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
O.mkdir(exist_ok=True)
for name in ['init.py','prepare.py','build.py','verify.py','names.py']:
    if (O/name).exists():continue
    s=(B/name).read_text().replace('v0.22','v0.23')
    if name in ['prepare.py','verify.py']:s=s.replace('v0.21','v0.22').replace('v21','v22')
    if name=='prepare.py':s=s.replace('correspondance_revue_v22','correspondance_revue_v23')
    if name=='build.py':s=s.replace('len(rows)-5078','len(rows)-5098')
    (O/name).write_text(s)
for p in B.glob('*.json'):
    if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','progression-')):continue
    if not (O/p.name).exists():shutil.copy2(p,O/p.name)
choices={381:('0056.p',[804,805]),383:('0075.p',[510,511,512]),384:('0075.p',[518,519,520]),
385:('0075.p',[569]),388:('0075.p',[574]),389:('0075.p',[576,577]),390:('0075.p',[579,580,581,582]),
397:('0075.p',[621,622]),398:('0075.p',[548,549]),406:('0075.p',[590,591]),407:('0075.p',[601,602]),
417:('0075.p',[645]),429:('0075.p',[669,670,671]),434:('0075.p',[709]),437:('0075.p',[712]),
456:('0075.p',[536,537,538,539,540,541]),458:('0075.p',[768,769,770,771]),
459:('0075.p',[772,773,774,775]),460:('0075.p',[776,777]),482:('0075.p',[947,948]),
486:('0075.p',[919]),489:('0075.p',[924,925,926]),490:('0075.p',[928,929,930]),
503:('0076.p',[0,1]),508:('0076.p',[5]),513:('0076.p',[11,12,13,14,15]),514:('0076.p',[19]),
515:('0076.p',[20,21,22]),518:('0076.p',[26]),526:('0076.p',[56,57,58,59])}
notes={
381:'Habitant de Sorceria apres restauration du tapis : magie retrouvee et exploration du monde. DS 804–805, distinct de la branche 322/323 en audit. Le souhait final de prudence SFC est conserve par adaptation courte.',
383:'Entree a Colombourg : visages inconnus, soupcon de crimes puis invitation a se cacher. DS 510–512, pas la salutation ulterieure 902–904. Branche plurielle ces sales tronches retenue car SFC dit あんたら, sans variable de nom.',
384:'Regle de Colombourg : chacun a un passe, ne pas enqueter sur les autres, seule regle de la ville. Trois segments DS dans le meme ordre, sans interrogation ou embranchement ajoute.',
385:'Premier barman avant cocktail maison : 酒かい? correspond a DS 569, suivi du cocktail 570–571. Contexte confirme par le comptoir, pas par une replique courte isolee ; distinct du faux barman en 503/508.',
388:'Meme premier barman quand on passe derriere le comptoir : refus d’informations et ordre de sortir. DS 574 entier ; garde le role, sans le nom de Lynx que la source SFC ne revele pas.',
389:'Visiteur venu pour le forgeron legendaire mais habitants muets. DS 576–577 ; deux idees et meme interlocuteur, pas le discours du vieil habitant qui suit.',
390:'Vieil habitant : arrivee ancienne, bagarres, survie car mauvais combattant, disparition des gros durs. DS 579–582 relus ensemble ; la localisation redistribue la derniere idee sur les deux derniers segments mais le groupe complet conserve le propos.',
397:'Habitante de la petite maison : sa propre demeure et maison en face petite malgre sa facade. DS 621 conserve la seconde description ; 622 est une question ajoutee a la DS. Premiere plainte SFC conservee en reprenant la VF secondaire, ponctuation seulement normalisee.',
398:'Vieil interlocuteur aborde par les voyageurs puis evoquant le forgeron legendaire. DS 548–549 ; premiere phrase neutralisee pour supprimer les branches voyageur/voyageuse et fabrique/fabriquent.',
406:'Poursuivant de Lynx venu en ville : informateur cache et maitre du deguisement. DS 590–591, pas sa replique ulterieure 0076:734 portant sur les armes legendaires.',
407:'Proprietaire se plaint de squatters dans une partie de son logement. SFC indique la piece du dessous, DS 601 le terrain derriere : adaptation spatiale explicite appuyee aussi sur la premiere phrase de la VF IPS. Seconde phrase DS 602 conservee.',
417:'Spectateur du theatre demandant une demonstration. SFC reclame de se deshabiller, DS 645 parle de mouvement des hanches et le francais reste une incitation generale a montrer son talent. Meme spectateur et scene, aucun controle ou nom ajoute.',
429:'Habitante etablie depuis douze ans, venue du chateau de Gandino/Brigandia, refuse de reparler de son cauchemar. DS 669–671, meme anciennete ; ne pas ajouter la reaction silencieuse de Mireille en 672.',
434:'Buveur apres le conseil payant sur l’equipement : demande un autre verre, DS 709. Dans la meme sequence que le refus 710 et le hoquet 712 ; pas une nouvelle commande d’achat de boisson.',
437:'Hoquet et rire du meme buveur, DS 712, voisin de 709 et du renseignement sur Lynx a l’etage 714. Replique courte ancree dans cette sequence, pas dans une taverne generique.',
456:'Premier entretien avec Lynx : ignorance du forgeron, arrivee recente, reconfort, enquete possible, habitants peu bavards puis depart. Six labels japonais ホック identiques ; nom DS Lynx conserve une fois.',
458:'Lynx aborde le paiement : recherche couteuse, tarif 50000, pas de versement immediat et proposition de pari. DS 768–771 ; montant identique a SFC, pas de variable monetaire ou debit ajoute.',
459:'Regles du defi : deguisement en ville, trois costumes, reconnaissance des trois donnant remise a 2000 depuis 50000, puis demande d’accord. DS 772–775 ; les deux tarifs et trois etapes restent identiques a SFC.',
460:'Accord au defi : Lynx se deguisera en ville puis souhaite bonne chance et part. DS 776–777 ; ne pas utiliser la branche de refus 783–784.',
482:'Conseil au joueur du defi : Lynx pro du deguisement puis parler au plus de monde possible. DS 947–948, entre deux deguisements, aucun lieu de cachette revele.',
486:'Homme parlant de la pauvre Sarii/Martel au pretre : voudrait l’aider mais ignore comment. DS 919, entre la compassion 917 et le faux pretre 920. Nom absent de cette replique SFC, donc non ajoute.',
489:'Faux pretre avant sa premiere demasquade : consultation, priere mal prononcee, excuse de l’alcool. DS 924–926, etiquettes 神父 identiques. Conserve le label Pretre, sans reveler Lynx avant 490.',
490:'Lynx demasque la premiere fois : annonce sa reconnaissance, prochaine plus difficile puis informations collectees et depart. DS 928–930 ; ne pas inclure revelation du deguisement feminin 973.',
503:'Lynx deguise en second barman : offre du cocktail ブラブラムンムン, puis invitation a se plaindre. DS 0076:0–1, cocktail officiel lune saignante. Ne pas confondre avec la lune sanglante du premier bar en 0075:570.',
508:'Branche negative a la boisson chez le faux barman : cherche quelqu’un? DS 0076:5, entre l’offre derriere le comptoir 3–4 et la reconnaissance 9. Meme question SFC, sans nom revele.',
513:'Troisieme demasquade : Lynx reconnu, enquete terminee, epier les deux hommes, venir chez lui avec l’or puis entendre les informations. DS 11–15 complet, un seul locuteur. Les indications correspondent a la sequence 514 puis 515.',
514:'Narration avant conversation surprise des deux hommes : DS 0076:19, suivie du recit sur le forgeron en 20. Pas de nom de locuteur, acteur ou variable ajoute.',
515:'Premier vieux client : talent de Cobre/Charles, renommee lui montant a la tete puis desir de voir une epee legendaire. DS 20–22 relus ensemble, meme sujet et meme suite ; ne pas inclure reponse du second homme 23.',
518:'Second vieux client reagissant a la souffrance de la famille abandonnee. DS 26, juste apres 24–25, reponse distincte de 23. Replique breve ancree dans la conversation surprise qui suit 514.',
526:'Chez Lynx apres les trois reconnaissances : accueil, or reclame, tarif 50000 abandonne car trois deguisements reconnus, remise promise a 2000. DS 56–59 ; nombres et terminator AE conserves, aucune branche d’argent insuffisant 61 ajoutee.'}
jp={r['id']:r for r in read(P/'clean-base/sfc-jp.json')};vf={r['id']:r for r in read(P/'clean-base/sfc-vf.json')}
ja={(r['file'].split('/')[-1],r['id']):r for r in read(P/'clean-base/ds-ja.json') if '/MESS6/' in r['file']}
fr={(r['file'].split('/')[-1],r['id']):r for r in read(P/'clean-base/ds-fr.json') if '/MESS6/' in r['file']}
oldids={r['id'] for r in read(B/'insertion-candidates.json')};assert not oldids&set(choices)
def body(file,ids):
    parts=[]
    for did in ids:
        m=re.fullmatch(r'@a([^@]*)@b(.*?)\n?@c0@',fr[(file,did)]['text'],re.S);assert m
        s=m.group(2).strip();parts.append(s[3:] if s.startswith('*ⓢ ') else s)
    return ' '.join(parts)
reviews=[]
for mid,(file,ids) in choices.items():
    r=dict(id=mid,file=file,ids=ids,sfc_jp=jp[mid]['text'],sfc_vf_secondaire=vf[mid]['text'],ds_jp=[ja[(file,i)]['text'] for i in ids],ds_fr=[fr[(file,i)]['text'] for i in ids],review=notes[mid],status='RELU')
    original=body(file,ids);replacement=None;why=None
    if mid==381:
        replacement=original+' Prenez soin de vous.';why='Conserve la formule finale de prudence du japonais SFC, omise dans les deux segments DS ; corps francais DS integral.'
    elif mid==383:
        tag='%H0860%Xcette sale tronche%Yces sales tronches%Z';assert tag in original
        replacement=original.replace(tag,'ces sales tronches');why='Branche plurielle officielle DS retenue pour あんたら SFC ; aucune commande conditionnelle DS inseree.'
    elif mid==397:
        replacement="C'est rude de vivre dans une si petite maison... "+body(file,[621]);why='Premiere plainte reprise de la VF IPS secondaire et verifiee au japonais SFC. Conserve ensuite la description DS de la maison voisine ; retire la question DS ajoutee 622.'
    elif mid==398:
        replacement='Que faites-vous à Colombourg? '+body(file,[549]);why='Adresse neutre au groupe a la place des branches de genre et de nombre DS dans 548 ; suite officielle 549 conservee.'
    elif mid==407:
        replacement='La pièce du dessous est aussi à moi... '+body(file,[602]);why='Conserve la piece inferieure SFC, appuyee par la VF secondaire, a la place du terrain derriere de la carte DS. Aucune deplacement d’un lieu du jeu ; seconde phrase DS conservee.'
    if replacement is not None:r.update(original_body=original,adaptation_body=replacement,adaptation_review=why)
    reviews.append(r)
if (O/'revue-lot-v023.json').exists():assert read(O/'revue-lot-v023.json')==reviews
else:save('revue-lot-v023.json',reviews)
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
print('v0.23 reviewed input delta ready:',len(reviews),'messages')

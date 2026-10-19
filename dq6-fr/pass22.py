"""Recreate the reviewed Sorceria delta without replacing previous selections."""
from pathlib import Path
import json,re,shutil
P=Path(__file__).resolve().parent;B=P/'v0.21';O=P/'v0.22'
def read(p):return json.loads(p.read_text())
def save(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
O.mkdir(exist_ok=True)
for name in ['init.py','prepare.py','build.py','verify.py','names.py']:
    if (O/name).exists():continue
    s=(B/name).read_text().replace('v0.21','v0.22')
    if name in ['prepare.py','verify.py']:s=s.replace('v0.20','v0.21').replace('v20','v21')
    if name=='prepare.py':
        s=s.replace('correspondance_revue_v21','correspondance_revue_v22')
        assert 'SPECIFIC_SPEAKERS={374:' in s
        s=s.replace('SPECIFIC_SPEAKERS={374:',"SPECIFIC_SPEAKERS={373:('カルベ','カルベ夫人'),374:")
    if name=='build.py':s=s.replace('len(rows)-5058','len(rows)-5078')
    (O/name).write_text(s)
for p in B.glob('*.json'):
    if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','progression-')):continue
    if not (O/p.name).exists():shutil.copy2(p,O/p.name)
choices={283:('0034.p',[499,500,501,502]),296:('0034.p',[554,555,556,557,558]),
298:('0056.p',[501,502,503]),302:('0056.p',[517,518,519,520,521]),305:('0056.p',[533]),
309:('0056.p',[543]),313:('0056.p',[560,561]),318:('0056.p',[573,574,575,576,577]),
319:('0056.p',[579,580,581]),320:('0056.p',[590,591,592,593]),328:('0056.p',[621,622]),
336:('0056.p',[632,633,634]),338:('0056.p',[644,645,646,647]),347:('0056.p',[689]),
361:('0056.p',[741,742,743,744]),366:('0056.p',[753,754,755]),372:('0056.p',[776]),
373:('0056.p',[784,785]),376:('0056.p',[792,793,794,795]),380:('0056.p',[800])}
notes={
283:'Aridea apres liberation : habitants revenus mais vegetation toujours sterile ; les quatre segments DS reprennent retour, desert, echec des plantations et crainte du mal. Meme ordre, pas de conclusion de guerison ajoutee.',
296:'Seb Tique apres Jamirus : reflexion sur l’ile, nom du chef, dernier murmure, fragment du nom du maitre et interrogation. Les cinq labels japonais マハメド sont identiques ; nom et indice francais de la DS conserves.',
298:'Accueil a Sorceria apres destruction du demon du temple sous-marin. Trois segments ; retrait du seul vocatif a branches de genre DS. Ne pas ajouter le segment 506 sur la fondation de la ville.',
302:'Destruction de Sorceria en deux temps : monde reel brule, refuge des ames dans les reves, puis nouveau sceau sur l’ile. Cinq segments japonais et francais relus ; aucune confusion avec le retour recent de la ville.',
305:'Exclamation de la fillette qui s’arrete brusquement, avant la plainte du camarade DS 537 puis les braises 538. DS 533 Mmm? est cette reaction, pas une replique generique choisie hors scene ; style D9 initial conserve.',
309:'Dans la scene des chataignes, le garcon cherche le sort DS 541 puis prononce メラ en 543 pour rallumer le feu. Flamme est le nom officiel DS ; pas de commande de sort ajoutee au texte.',
313:'Fillette voyant les coudes ecorches de son camarade (DS 559), remarque puis ホイミ/Premiers secours (560–561). La confirmation de guerison 562 correspond a la replique suivante et n’est pas ajoutee ici.',
318:'Gardien de l’Aieule : age de 200 ans/deux siecles, faiblesse, sables pour le repos, sol devant deuxieme porte et demande d’informations aux habitants. Cinq segments DS concordants, meme seconde porte ; aucune indication de lieu modifiee.',
319:'Maison des Soren : couple creant des objets magiques, fatigue apres levee du sceau, seul appel de l’Aieule susceptible de les reveiller. Trois segments relus ; aucun dialogue de reveil premature.',
320:'Branche avec tapis dans les bagages : reconnaissance, perte de pouvoir, fabricants Soren, possibilite de restauration par eux. Les quatre segments DS 590–593 concordent dans les deux langues. Distinct de la branche 322–323 differee.',
328:'Armurier sorcerien : armes enchantees puis invitation a les manier avec creativite. DS 621–622 ; ne change ni statistiques ni commande Utiliser des objets.',
336:'Histoire d’Explosion magique : Laurelda inventrice, puissance rarement maitrisee, Tenjadice seule heritiere vivante. Trois segments ; noms localises DS, aucune modification des tables de sorts.',
338:'Protection de la maison par les sables, urne pour les retirer, urne perdue dans les profondeurs puis interrogation. Quatre segments, meme ordre ; aucune promesse d’acces sans l’objet.',
347:'Magicien metamorphe : question juste avant transformation Morph en DS 690. Source SFC n’affiche pas de nom ; label DS vide et prefixe DA natif conserves, aucun nom de personnage revele.',
361:'Explication par Tenjadice : Explosion magique libere tout le pouvoir, epuise la magie en une utilisation, urgence face au demon supreme et yeux a fermer. Quatre segments relus ; pas de cout numerique invente ni changement de mecanique.',
366:'Aieule apres transmission : apaise l’inquietude, mission accomplie avant intervention ennemie, confie l’avenir au nouveau chef. DS 753–755 ; marqueurs de souffle DS uniquement retimes, sans ajouter l’adieu 759.',
372:'Habitante apres l’incident chez l’Aieule : malaise et reveil des Soren. DS 776 est cette transition ; aucune variable de nom ni texte du couple ajoute.',
373:'Premiere moitie du discours suivi de 374 : patronyme SFC カルベ commun aux deux epoux, DS distingue カルベ夫人 en 784–787. 374 est deja identifie et affiche Madame Soren (786–787). Utilise la meme identification pour 373/784–785, sans modifier les tokens de 374.',
376:'Monsieur Soren reconnaissant le tapis : question, nostalgie, long eloignement et examen. Quatre segments DS 792–795, tous etiquetes カルベ ; ne pas inclure incantation 796 ni resultat 798.',
380:'Monsieur Soren apres restauration du tapis : commodite et transport facile. DS 800 correspond a cette conclusion, avec image d’ailes propre a la localisation ; aucune restriction du moteur changee.'}
jp={r['id']:r for r in read(P/'clean-base/sfc-jp.json')};vf={r['id']:r for r in read(P/'clean-base/sfc-vf.json')}
ja={(r['file'].split('/')[-1],r['id']):r for r in read(P/'clean-base/ds-ja.json') if '/MESS6/' in r['file']}
fr={(r['file'].split('/')[-1],r['id']):r for r in read(P/'clean-base/ds-fr.json') if '/MESS6/' in r['file']}
old={r['id']:r for r in read(B/'insertion-candidates.json')};assert not set(old)&set(choices)
def body(file,ids):
    parts=[]
    for did in ids:
        m=re.fullmatch(r'@a([^@]*)@b(.*?)\n?@c0@',fr[(file,did)]['text'],re.S);assert m
        s=m.group(2).strip();parts.append(s[3:] if s.startswith('*ⓢ ') else s)
    return ' '.join(parts)
reviews=[]
for mid,(file,ids) in choices.items():
    r=dict(id=mid,file=file,ids=ids,sfc_jp=jp[mid]['text'],sfc_vf_secondaire=vf[mid]['text'],ds_jp=[ja[(file,i)]['text'] for i in ids],ds_fr=[fr[(file,i)]['text'] for i in ids],review=notes[mid],status='RELU')
    if mid==298:
        first=body(file,[501]);start=first.index('%H0860');end=first.index('. Comme on dit')
        r.update(original_body=body(file,ids),adaptation_body=first[:start].rstrip(', ')+first[end:]+' '+body(file,[502,503]),adaptation_review='Supprime seulement le vocatif cher voyageur/chere voyageuse a branches DS ; conserve la bienvenue, le dicton, la liberation et l’attente.')
    reviews.append(r)
if (O/'revue-lot-v022.json').exists():assert read(O/'revue-lot-v022.json')==reviews
else:save('revue-lot-v022.json',reviews)
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
save('audit-tapis-reordonne.json',dict(status='DIFFERE_A_REVOIR',new_insertion_deferred=322,previous_selection_to_audit=323,previous_tokens_preserved=True,sfc_jp={str(i):jp[i]['text'] for i in [321,322,323]},previous_fr=old[323]['text'],ds_file='0056.p',ds_context=[dict(id=i,ja=ja[('0056.p',i)]['text'],fr=fr[('0056.p',i)]['text']) for i in range(583,589)],finding='Le francais DS reordonne les informations entre 584–588 : 584/585 decrit le vol et la rumeur du possesseur, tandis que 586–588 traite de la fabrication et de la disparition. Une correspondance des seuls textes japonais ne suffit pas. Le message SFC 323 deja integre a recu le second groupe francais ; revoir ensemble les branches 322/323. Aucun ancien token change dans ce lot. Cette anomalie semantique reste ouverte avant toute declaration de finalisation.'))
print('v0.22 reviewed input delta ready:',len(reviews),'messages; carpet branch audit recorded')

"""Recreate the reviewed v0.21 delta; preserve existing inputs and old selections."""
from pathlib import Path
import json,re,shutil

P=Path(__file__).resolve().parent;B=P/'v0.20';O=P/'v0.21'
def read(p):return json.loads(p.read_text())
def save(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
O.mkdir(exist_ok=True)
for name in ['init.py','prepare.py','build.py','verify.py','names.py']:
    if (O/name).exists():continue
    s=(B/name).read_text().replace('v0.20','v0.21')
    if name in ['prepare.py','verify.py']:s=s.replace('v0.19','v0.20').replace('v19','v20')
    if name=='prepare.py':s=s.replace('correspondance_revue_v20','correspondance_revue_v21')
    if name=='build.py':s=s.replace('len(rows)-5040','len(rows)-5058')
    (O/name).write_text(s)
for p in B.glob('*.json'):
    if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','progression-')):continue
    if not (O/p.name).exists():shutil.copy2(p,O/p.name)

choices={
205:('0030.p',[77,78,79,80,81]),220:('0031.p',[6,7,8,9,10,11]),
237:('0021.p',[604]),241:('0021.p',[609]),244:('0021.p',[625,626]),
246:('0021.p',[629,630,631]),248:('0021.p',[641,642]),249:('0021.p',[638,639,640]),
250:('0021.p',[646,647,648,649]),251:('0021.p',[672,673]),
255:('0021.p',[655,656,657,658]),256:('0021.p',[664,665,666,667]),
258:('0021.p',[798,799]),259:('0021.p',[801]),267:('0022.p',[703,704,705]),
277:('0022.p',[739,740,741]),278:('0022.p',[745,746]),279:('0022.p',[748,749,750]),
282:('0022.p',[765,766,767,768]),295:('0034.p',[547,548])}
notes={
205:'Vallonclair reel : regret pour les Redon, promesse de Panon/Tom Foolery, insigne, ascension impossible au locuteur, indication du nord-est. Cinq segments DS relus ; orientation conservee.',
220:'Harris/M. Redon reconnait le fragment, demande sa provenance, apprend ascension et danger, remercie et annonce fabrication de l’insigne. Six segments DS, tous du meme pere ; D4 repete ne change pas de locuteur.',
237:'Reponse du buveur de Calcado/Aridea a la remarque sur l’alcool. JP そうかい et ごちゅうこくありがとうよ ; DS 604 se trouve entre sa question diurne 603 et son explication sur sa femme partie 605–606. Replique courte choisie par cette branche, pas par seule ressemblance.',
241:'Habitant presse de rejoindre l’ile : exclamation puis depart urgent, juste apres question sur presence de l’ile au cap ouest (DS 608). DS 609 est bien cette reponse, pas la reponse au retour bredouille 611.',
244:'Habitante qui prend les heros pour recruteurs : elle est heureuse ici, refuse l’ile et les renvoie vers ceux qui souhaitent partir. Deux segments DS, un seul locuteur, pas de choix ajoute.',
246:'Vieil homme confond les voyageurs avec les recruteurs de l’ile puis plaisante sur son age. DS 629–631 suit son refus 628. Neutralisation de la seule formule voyageur/voyageuse pour conserver adresse au groupe SFC.',
248:'Branche negative de la question sur la rumeur de l’ile : simple passage en ville, puis cap ouest. DS 641–642, distinct de branche affirmative 638–640 ; accords venu/venue neutralises.',
249:'Branche affirmative : soupcon confirme, voyageurs jamais revenus, espoir de bonheur. DS 638–640 uniquement ; ne pas ajouter la branche du simple passage 641.',
250:'Fille malade abandonnee par son pere parti chercher un remede sur l’ile : toux, espoir du medicament, depart malgre objections, attente. Quatre segments dans le meme ordre, pas de diagnostic ni de variable ajoute.',
251:'Presentation du guerrier Mahamed/Seb Tique a l’armurerie, puis rumeur de l’ile flottante. La SFC n’imprime pas de label D4 : le nom reste dans la presentation du corps DS, sans etiquette ajoutee.',
255:'Habitant decrit apparition a la pleine lune, provenance revendiquee, bonheur sans soucis et possibilite de retour ce soir. Quatre segments JP/FR relus, contexte avant depart.',
256:'Visiteur venu prendre l’ile : arrivee difficile, bateau attendu, impatience et projet de loisirs. Quatre segments DS ; le detail de gratuite vient de l’adaptation officielle DS et n’altere aucun prix du moteur.',
258:'Conversation nocturne de Calcado : lune pleine puis habitants qui partiront cette nuit. DS 798–799, pas les repliques diurnes sur l’ile a venir.',
259:'Habitant nocturne se plaint du froid desertique. DS 801 contigue a 798–799, meme scene et heure, phrase breve revue en contexte.',
267:'Apres liberation : rehabilitation du puits, etonnement d’y avoir renonce, distraction par l’ile. DS 703–705, pas les dialogues de creusement qui suivent.',
277:'Apres liberation : rejet d’un paradis ailleurs, bonheur a chercher dans sa propre vie et bonheur offert trompeur. DS 739–741, meme conclusion dans le meme ordre.',
278:'Fille apres retour de son pere : amelioration de son etat et apaisement de l’inquietude. DS 745–746 ; fait suite a sa replique anterieure 646–649 (message 250).',
279:'Pere revenu : regret d’avoir abandonne sa fille, engagement a agir lui-meme et determination. DS 748–750 ; la soupe est une image de localisation DS, sans insertion d’objet ni commande de soin.',
282:'Mahamed/Seb Tique decide de proteger la ville et confie aux heros l’aide aux gens au-dela de l’ocean. Quatre labels JP identiques, meme guerrier ; nom DS conserve.',
295:'Religieux apres l’ile : puissance malefique encore presente, souhait d’un monde sur pour les enfants. DS 0034:547–548 ; aucune reference ajoutee a un ennemi nomme.'}
jp={r['id']:r for r in read(P/'clean-base/sfc-jp.json')}
vf={r['id']:r for r in read(P/'clean-base/sfc-vf.json')}
ja={(r['file'].split('/')[-1],r['id']):r for r in read(P/'clean-base/ds-ja.json') if '/MESS6/' in r['file']}
fr={(r['file'].split('/')[-1],r['id']):r for r in read(P/'clean-base/ds-fr.json') if '/MESS6/' in r['file']}
oldids={r['id'] for r in read(B/'insertion-candidates.json')};assert not oldids&set(choices)
def body(file,ids):
    out=[]
    for did in ids:
        m=re.fullmatch(r'@a([^@]*)@b(.*?)\n?@c0@',fr[(file,did)]['text'],re.S);assert m
        s=m.group(2).strip();out.append(s[3:] if s.startswith('*ⓢ ') else s)
    return ' '.join(out)
reviews=[]
for mid,(file,ids) in choices.items():
    r=dict(id=mid,file=file,ids=ids,sfc_jp=jp[mid]['text'],sfc_vf_secondaire=vf[mid]['text'],ds_jp=[ja[(file,i)]['text'] for i in ids],ds_fr=[fr[(file,i)]['text'] for i in ids],review=notes[mid],status='RELU')
    if mid in [246,248]:
        original=body(file,ids)
        first=body(file,[ids[0]]);tail=body(file,ids[1:])
        replacement='Oh? Vous êtes en voyage? Excusez-moi.' if mid==246 else 'Vous êtes juste de passage, alors? Je vois pas ce qui vous amène dans cette ville misérable sinon...'
        r.update(original_body=original,adaptation_body=replacement+' '+tail,adaptation_review='Remplace uniquement la premiere phrase avec branches de genre DS par une formulation neutre ; conserve les autres phrases officielles, l’adresse vous et le cap ouest si present.')
    reviews.append(r)
if (O/'revue-lot-v021.json').exists():assert read(O/'revue-lot-v021.json')==reviews
else:save('revue-lot-v021.json',reviews)
existing=read(O/'correspondances-revues.json');byid={r['id']:r for r in existing}
for r in reviews:
    if r['id'] in byid:assert byid[r['id']]==r
    else:existing.append(r)
save('correspondances-revues.json',existing)
adapt=read(O/'adaptations-francaises.json')
for r in reviews:
    if 'adaptation_body' not in r:continue
    row=dict(id=r['id'],file=r['file'],ids=r['ids'],original_body=r['original_body'],body=r['adaptation_body'],review=r['adaptation_review'])
    old=next((a for a in adapt if a['id']==r['id']),None)
    if old:assert old==row
    else:adapt.append(row)
# Adjacent apostrophe and DS quote marker would print l''ile on the native renderer.
original=body('0021.p',[655,656,657,658])
assert "l'ⓥîle des Souriresⓦ" in original
row=dict(id=255,file='0021.p',ids=[655,656,657,658],original_body=original,
         body=original.replace("l'ⓥîle des Souriresⓦ","l'île des Sourires"),
         review='Retire seulement les marqueurs de citation DS autour du nom de l’ile apres l’apostrophe : evite une double apostrophe dans le rendu SFC. Les mots et le nom officiel restent identiques.')
old=next((a for a in adapt if a['id']==255),None)
if old:assert old==row
else:adapt.append(row)
save('adaptations-francaises.json',adapt)
print('v0.21 reviewed input delta ready:',len(reviews),'messages')

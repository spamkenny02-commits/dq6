"""Explicit DS French adaptations. The DS original is retained for each row."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parent;O=P/'v0.10';O.mkdir(exist_ok=True)
for name in ['prepare.py','build.py','verify.py','names.py','init.py','correspondances-revues.json','adaptations-francaises.json','dialogues-multilocuteurs.json','variantes-orthographiques.json','commandes-verifiees.json','decisions-alignement.json']:
 s=(P/'v0.9'/name).read_text()
 if name.endswith('.py'):s=s.replace('v0.9','v0.10').replace('v0.8','v0.9').replace('v08','v09').replace('len(rows)-4279','len(rows)-4338').replace('correspondance_revue_v09','correspondance_revue_v10')
 (O/name).write_text(s)
# Extract outer condition spans, but do not select their branches. Each accepted
# replacement below is explicit and tied to a message ID and exact source body.
def spans(text):
 toks=list(re.finditer(r'%[A-Z]\d*',text));out=[];start=None;depth=0
 for t in toks:
  code=t.group()
  if re.fullmatch('%[A-W]\\d+',code):
   if depth==0:start=t.start()
   depth+=1
  elif code=='%Z':
   depth-=1
   if depth==0 and start is not None:out.append((start,t.end(),text[start:t.end()]));start=None
 assert depth==0,(text,depth)
 merged=[]
 for a,b,part in out:
  if merged and merged[-1][1]==a:merged[-1]=(merged[-1][0],b,merged[-1][2]+part)
  else:merged.append((a,b,part))
 return merged
# Replacement of complete sentences when their grammar surrounds a condition.
FULL={
14:'Un escalier secret vient d’être découvertⓠ',
16:'Quelle chanceⓠ Un passage secretⓠ S’aventurer à l’intérieurⓡ',
19:'Il ne semble pas voir %a000120.\nFaire une petite prière rapideⓡ',
76:'Votre reflet apparaît dans la glace. On dirait qu’il s’agit d’un miroir ordinaire...',
79:'La voix mélodieuse de Marine se fait entendre...',
179:'Bonjourⓠ Bienvenue à Vallonclairⓠ',
213:'Vous avez entenduⓡ Le pic du Destin a été escaladé pour tenir la promesse faite au petit Ed. Je tire mon chapeau devant un tel acte de bravoureⓠ',
234:'Du voyage, ici, à Aridéaⓡ Hé ben... J’espère que vous aimez rien car on a que ça ici... rien.',
242:'Quel mensonge... l’île n’était pas encore là.',
247:'Ah, encore de la visite. Laissez-moi devinerⓢ vous êtes dans le coin à cause de l’île des Sourires, pas vraiⓡ',
343:'Merci de votre visiteⓠ',
427:'Oh, vous avez fait le déplacement pour me voirⓡ N’oubliez pas que vous ne pouvez toucher qu’avec les yeux. C’est la règleⓠ Ⓟ',
431:'Je ne vous connais pas. N’allez pas raconter ce que vous voyez dans le coin, c’est comprisⓡ Cet endroit est réservé à certaines personnes.',
496:'Hi hiⓠ Vous êtes quiⓡ Vous aimez m’admirerⓡ',
552:'Scoopⓠ Dernière nouvelleⓠ La ville abrite la fine fleur de l’aventureⓢ l’épée légendaire a été retrouvéeⓠ',
579:'Pas de réponse. Mais un journal ouvert est posé sur la table. Écrire discrètement une entrée dans le journalⓡ',
590:'Vous avez fait le voyage jusqu’à ce sanctuaire, heinⓡ Alors que je vous l’avais déconseillé...',
621:'Vous avez rendu visite à Angèle, heinⓡ',
694:'Je vois. Votre aventure au cœur de la mine n’a donc servi à rien. Ma foi, si ça vous chante de perdre votre temps... Bon, hors de ma vue maintenantⓠ À moins que... vous n’ayez changé d’avis au sujet des 5000 pièces d’orⓡ',
736:'Des... achatsⓡ Pincez-moi, je rêveⓠ Pourquoi prenez-vous la peine de faire des achats alors que vous avez ce charmant lagon à disposition, à l’ouestⓡ C’est si... si... apaisant.',
836:'Commentⓡ La livraison vient donc de cette visiteⓡ',
849:'%3Vous avez attendu cette visite. Il est temps d’affronter le démon suprême.%4',
850:'%3Voici la lumière dont a besoin notre monde. Qu’on ouvre la porteⓠ%4',
855:'Quelle bonne surpriseⓠ De nouvelles arrivéesⓠ On n’attendait pas de nouvelles victimes, mais plus on est de fous, plus on ritⓠ',
856:'Je m’occupe de cette visite. Tu peux aller patrouiller.',
858:'Héⓠ On a du nouveau pour les cellules. Allons installer toute cette royautéⓠ Ha haⓠ',
862:'Escortez cette nouvelle arrivée jusqu’aux cellulesⓠ',
878:'Vous avez besoin de quelque choseⓡ Si vous ne savez plus où aller sur le chemin de la vie, n’hésitez pas à venir me voir. Même si je doute d’avoir l’autorisation d’en dire beaucoup plus que ça...',
869:'V-㈢㈢vousⓠ Vous faites partie de la bande qui accompagne %a000090ⓠ',
997:'Il y avait même une clef et une tenue de gardeⓠ',
1003:'%3La clef du geôlier et l’équipement de garde sont rendus. Retour aux cellules.%4',
1004:'%3La fatigue se fait sentir après tous ces événements. Un profond sommeil s’ensuit jusqu’à l’aube...%4',
1074:'Seigneur Noirkeur, nous allons nous occuper de cette intrusion.',
1078:'Mmpf. Je n’ai jamais accordé d’importance à cette prophétie. De toute façon, cette visite s’arrête ici.',
1084:'Seigneur Noirkeur, voilà du retourⓠ',
1085:'On dirait que la leçon n’a pas été comprise. Ça mérite peut-être une autre petite leçonⓡ Cette fois-ci, personne ne s’en remettra. Ce sera le dernier combatⓠ Ha haⓠ',
1295:'AAHⓠ Une visite humaineⓠ Que vient faire l’humanité sur ma propriété sous-marineⓡⓐ Non, ne me dites pasⓠ Laissez-moi deviner... vous êtes ici pour vaincre le grand Gracos et libérer Sorcéria, n’est-ce pasⓡ',
1341:'Je vais vous donner une raison de pleurer, misérable engeance humaineⓠ',
1454:'Oh, la Déesse soit louée, vous avez enfin ouvert les yeux. À vous voir remuer comme ça, j’ai bien cru que le démon vous possédaitⓠ La ville d’Aridéa est située à l’ouest.\nFaites bon voyageⓠ',
1533:'Oh ça, pour sûrⓠ Mais je le dois à tant d’héroïsme.',
1614:'Très bien. Madame Luce comprend. %0%a002010, la visite s’achève. Occupe-toi du retour.',
1703:'Magnifiqueⓠ Je vois que vous avez des mini médailles. Laissez-moi les examiner.',
1735:'Ah, l’équipe qui accompagne %a000090ⓠ Engluez-vous bien, OKⓡ',
1789:'Ooh, pas de chance au dressageⓠ Vous ferez mieux la prochaine foisⓠ',
1798:'V-vous avez réussiⓠ Par la Déesse, le titre est remportéⓠ Un tel exploit mérite une récompense très, très, très spécialeⓠ',
1805:'Tout ce que j’ai à dire, c’est qu’on vit une drôle d’époqueⓠ J’en reviens pas que le titre ait été remporté par du tourismeⓠ',
1825:'Oh, je sais que c’est difficile de se séparer d’un tel talent, mais je promets de bien m’en occuper. Marché concluⓡ',
1839:'Vous acceptezⓡ Ravi de l’entendreⓠ Vous savez quoiⓡ Vous me plaisezⓠ',
1863:'Mmmⓡ Ma foi, je vous trouve une allure de victoire gluante.',
1871:'Héⓠ Qu’est-ce que vous faites ici sans personne pour vous accompagnerⓡ Vous avez perdu votre maître ou quoiⓡ',
1875:'Salutⓠ Voici le comptoir des récompenses. C’est ici qu’on récupère ses récompenses après une victoire dans l’arène.',
1876:'Bienvenue dans la salle d’avant-match des combattants gluants. (slurp) Dis, tu n’as pas pris part à cette série de matches, siⓡ Tu es libre de gluer ici tant que tu veux, mais tâche de ne gêner personne. (slurp)',
1900:'Oh, vous devez être %a000120. Vous connaissez %a002070, c’est çaⓡ J’espère qu’il ne se laisse pas faire là où il estⓠ Dites-lui que tout glue à merveille ici, vous voulez bienⓡ (slurp)',
1901:'Je parie que la victoire attire des tonnes d’amis, pas vraiⓡ',
1930:'C’est quand vous voulez. Tout est prêtⓡ',
1949:'Navré, mais l’accès à cet escalier est interdit aux passagers. Veuillez profiter du voyage dans cette splendide cabine principale.',
1979:'Vos voyages ont dû vous épuiser, %a000120. Vous avez dormi comme un loir durant tout le voyage. Tous les villageois sont rentrés, désormais.',
1982:'Vos voyages ont dû vous exténuer. Souhaitez-vous vous reposerⓡ',
2010:'Il n’y a pas d’autre réservation à bord de ce beau navire aujourd’hui. On va jeter l’ancreⓠ On est parés pour notre voyage jusqu’à Port Abbri.\nAlors, vous montez à bordⓡ',
2012:'On s’amuse à jouer la comédie, heinⓡ Eh ben, rira bien qui rira le dernierⓠ Pas question de prendre des clandestins à bordⓠ',
2072:'Hé héⓠ Pas question de rester là sans rien faireⓠ Dépêchez-vous de vous emparer du trésor avant que quelqu’un d’autre ne le fasseⓠ',
2113:'Une étrange sensation se fait sentir.',
2157:'Oui, mon frère. La lumière que notre monde attend se trouve ici.',
2237:'Par la Déesseⓠ Je vois un cheval ailé galopant dans le cielⓠ Êtes... êtes-vous en mission pour la Déesseⓡ㈢ Pourtant, vous n’en avez pas l’air. C’est étrange...',
2249:'Les blessures de l’équipe guérissentⓠ',
2258:'Bah ha hahⓠ Le voyage était agréableⓡ Ouah ha hahⓠ À la revoyureⓠ Quelles têtes de piocheⓠ Hah ha hahⓠ (sifflement) Désolé. C’est la loi du plus fort, et le plus fort ici, c’est moiⓠ Amusez-vous bien à remonterⓠ Bah ha hahⓠ',
2267:'Nonⓡ Mmpf. Faites un bon détour. Quel manque de courageⓠ',
2268:'Pas si viteⓠ Voyons si ce long détour vous a donné un peu d’enduranceⓠ',
2399:'Je constate que les profondeurs de l’océan ne sont pas votre habitat naturel. Voilà bien des années que nous n’avions pas reçu de visite humaine.',
2410:'Vous comptez vous battre pour empocher ce trésorⓡ',
2413:'%0%a000090. Je savais qu’un jour, tu viendrais ici avec de la compagnie. Je m’appelle Rubiss. Mon rôle est de surveiller et de protéger ce monde. As-tu entendu ma voix t’appelerⓡ',
2613:'Oh, vous connaissez %a000090, n’est-ce pasⓡ Ravie de vous voir ici. Je n’ai pas grand-chose, mais faites comme chez vous.',
2616:'Et voici sûrement l’escorte qui accompagne %a000090ⓠ',
2627:'Ohⓠ Vous connaissez %a000090ⓡ Faites-moi le plaisir de le saluer de ma part.',
2629:'Même ici, on a eu vent de vos exploits. L’esprit de la montagne veillait sur vous, pour sûrⓠ',
2634:'Oh, salutⓠ Allez-y, buvez un coupⓠ C’est la maison qui régale, pour sûrⓠ',
2639:'Ah, vous connaissez %a000090, n’est-ce pasⓡ Ravi de vous rencontrer. Permettez-moi de vous féliciterⓠ Au nom du village, je vous remercie du fond du cœur.',
2669:'Avec %a000090 ici pour nous protéger, les attaques de monstres me dérangeraient pasⓠ',
2679:'%a000090 va bien, j’espère... On a entendu des tas d’histoires sur ses exploits de soldat somnien. C’est vraiment un sacré numéroⓠ',
2850:'L’autre moitié de notre héros, %0%a000090, hurle à l’intérieur.',
2903:'Mon mari est étrange ces derniers temps. Quand je mentionne %a000090, il me dit de faire comme s’il n’avait jamais existé... Qu’est-ce qui s’est passéⓡ',
2943:'Pfff. Comme vous voulez. Quelle avarice.',
2953:'Vraimentⓡ Dommage.\nAllez, Mesdames et Messieurs, approchezⓠ\nC’est l’affaire du siècle et tout et toutⓠ',
3140:'Eh bien, voilà qui me réjouitⓠ Revenez quand vous voulez à Puidebourgⓠ Repassez quand vous voulez, d’accordⓡ',
3147:'Bonjour à vousⓠ Bienvenue à Pierrebruteⓠ',
3150:'Voyons un peu ce qu’on a là...\nOh, voilà de la jeunesse qui respire la santéⓠ Ça vous dirait de me donner un coup de main avec la récolteⓡ',
3154:'Ça vaⓡ Ces récoltes se vendent à bon prix au château de Pierreforteⓠ Vous voulez savoir où est le château de Pierreforteⓡ Dirigez-vous vers l’ouest et vous tomberez pile dessusⓠ',
3339:'Quand on voyage comme vous, on a toujours un air mystérieux... Je ne peux pas bien le définir... Oh, pardon. Je ne sais pas ce que je disⓠ Ne faites pas attention.',
3384:'Nous n’attendons plus que votre arrivée. Quand vous serez à bord, on lèvera l’ancre. Tout est prêtⓡ Direction le cap de Somniaⓠ',
3436:'J’ai vu le mal de mer vous toucher. C’est pas facile de pas avoir le pied marin. Prenez soin de vous.',
3616:'Oh, vous voyageяⓠ Moi jalouseⓠ Vous visiteя tout le moиde, heiиⓡ Moи иom Svetlaиa. Moi êtяe chasseuse de tяésoяs célèbяe plus taяd. Vous voiяⓠ',
3774:'Mais qui nous rend visiteⓡ Je ne sens pas la présence de l’esprit de la Déesse ici.',
3781:'%3Tu ne dois pas refuser cette visite...\nTon destin est de l’accompagner...%4',
3787:'Attendsⓠ Si tu dis vrai, voilà donc l’héroïsme dont parle la légendeⓠ',
3903:'Le retour est prévu pour la nuit...',
4069:'Nonⓡ Eh bien, tant mieux. Une déception vous attendait sans doute.',
4578:'Gardesⓠ Emparez-vous de cette visite indésirableⓠ',
4729:'Ah, voilà l’entourage du princeⓠ Nous vous attendionsⓠ',
4752:'%0%a000090, ce soir, oublions nos soucis et régalons-nous. Toute ta compagnie peut se joindre à nous. Festin pour tout le mondeⓠ À tout à l’heureⓠ',
4754:'%3Cette nuit-là, pour la plus grande joie de ses sujets, le roi Somnus proclama le vrai prince de Somniaⓢ %a000090.%4',
4908:'Mmmⓡ Oh, de la visite. Bienvenue... Le roi vous attendⓡ',
4962:'Oui, Louis. Et tout cela grâce à vous et à votre compagnie.',
5175:'Bienvenue au château de Pierreforteⓠ C’est un honneur de vous recevoir. Je vous en prie, faites comme chez vousⓠ',
5204:'Je ne vous connais pas. C’est votre première fois iciⓡ',
5305:'Ah bonⓡ Je suis sûr qu’il serait enchanté de vous rencontrer et de parler de vos intrépides aventures.',
5500:'Mais... Tu t’es fait battre par ce guerrier...\nEt après, tu as encore perdu contre la visite qui est là...',
5517:'On n’a encore jamais rencontré de héros de cette trempe... Je parle de %a002040... C’est pas drôle tous les jours d’être un poète sans muse. Comment voulez-vous que je rime sans source d’inspirationⓡ',
5571:'D’où venez-vousⓡ Du monde inférieurⓡ Oh, je veux tout savoirⓠ C’est joli là-basⓡ',
5595:'Le seigneur Zénith m’a demandé de vous attendre. Je vous en prie, faites attention.',
5618:'Hiiiiⓠ Si vous avez réussi à entrer dans le château, c’est que votre humanité n’a rien d’ordinaireⓠ',
5626:'%3Poussez-vousⓠ Laissez le passage.%4',
5628:'Vousⓡ Une visite de marque pour le seigneur Dragoreⓡ',
5679:'Mais c’est une visite de marque pour Dragore. Mmpf. Bon, qu’est-ce que vous attendezⓡ Entrezⓠ',
5869:'%0%a000120 essaie de regarder ce qu’il y a dans la commode. Impossible de l’ouvrir par l’arrière.',
5886:'Mais la hauteur empêche de distinguer quoi que ce soitⓠ',
5893:'%0%a000120 examine les alentours.',
5901:'La porte est fermée et aucune de vos clefs ne permet de l’ouvrir.',
5936:'Une guérison miraculeuse a lieuⓠ',
5957:'Bizarrement, un regain de courage se fait sentir.',
6354:'Vous devrez recommencer votre aventure à partir de votre dernière confession.\nEst-ce vraiment ce que vous voulezⓡ',
6399:'Adieu. Que votre périple se déroule sans encombre.',
6473:'Je suis vraiment désolée, mais notre chambre forte est pleine. Nous ne pouvons plus accepter de dépôt.',
6480:'Eh bien, c’est une sacrée sommeⓠ Le problème, c’est que j’ai pas assez en banque... euh...',
6581:'Alorsⓡ On veut bien parader pour nousⓡ',
6601:'Oh, par la Déesse... Encore un manque d’expérience qui va me faire perdre mon tempsⓡ Écoutez bien. C’est moi, le juge principal ici. Mes goûts en matière de mode sont incontestables.',
6633:'Eh bienⓠ Voyez donc çaⓠ Nous accueillons du beau monde de Paco’Style aujourd’huiⓠ Installez-vous confortablement et profitez de toute cette modeⓠ',
6655:'La nervosité empêche de parler.',
6746:'Oh... Vous voulez me faire pleurerⓡ Peut-être que vous vous amuserez plus la prochaine fois. Revenez viteⓠ',
6896:'Mon frèreⓠ㈢ Oh... Je dois peut-être t’appeler Prince %a000090 maintenantⓡ',
6931:'Et qui va avoir la chance de recevoir ce cadeauⓡ',
}
# Keep the more delicate storytelling passages for context review rather than
# reducing the identity or scope of their participants.
for mid in [552,836,849,850,856,862,1084,1085,1533,1805,1863,2157,2413,3140,3436,3774,3781,3787,3903,4578,4962,5305,5500,5936,5957,6633]:FULL.pop(mid,None)
# Local phrases retain the rest of the DS sentence verbatim.
PHRASES={146:['en quête d’aventure'],299:[''],660:[''],706:[''],809:['quelle stupidité'],845:['la force'],1132:['la force qui se dressera'],1680:[''],1717:[''],1732:[],1759:[''],1792:['',''],1821:['',''],2046:['sur vos gardes'],2105:['Du voyage'],2237:[],2261:[''],2606:[],2703:[''],3616:[],4421:['gens d’aventure'],4747:[],4753:[]}
# Only these complete replacements, with their surrounding grammar, are used.
SPECIAL={
299:[('Bienvenue à Sorcéria, {0}.','Bienvenue à Sorcéria.')],
660:[('Bienvenue, {0}ⓠ','Bienvenueⓠ')],
706:[('la nouvelle, {0}ⓡ','la nouvelleⓡ')],
809:[('continuez si ça vous chante, {0}ⓠ','continuez si ça vous chanteⓠ Quelle stupiditéⓠ')],
845:[('Est-ce que c’est vous {0} que mon frère attendaitⓡ','Est-ce que c’est votre force que mon frère attendaitⓡ')],
1680:[('Merci bien, {0},','Merci bien')],
1717:[('toutes, {0}.','toutes.')],
1759:[('Trente ans, {0}...','Trente ans...')],
1792:[('Salut, {0}.','Salut.'),('Bonne chance, {1}.','Bonne chance.')],
1821:[('Salut, {0}.','Salut.'),('récompenses, {1}.','récompenses.')],
2046:[('soyez toujours très {0}, comprisⓡ','faites toujours preuve de prudence, comprisⓡ')],
2261:[('ce coffre, {0}.','ce coffre.')],
2703:[('Bonjour, {0}ⓠ','Bonjourⓠ')],
4421:[('les {0} comme vous','les gens d’aventure comme vous')],
}
review=json.loads((P/'v0.9/a-revoir.json').read_text());adapt=json.loads((O/'adaptations-francaises.json').read_text());byid={r['id']:r for r in adapt};new=[]
for r in review:
 if r['reason']!='variables_ou_commandes_DS':continue
 mid=r['id'];c=r['ds'];old=c['body'];body=old
 if mid in FULL:body=FULL[mid]
 elif mid in SPECIAL or mid in [146,1132,2105]:
  ss=spans(old)
  if mid in SPECIAL:
   for a,b in SPECIAL[mid]:
    for k,(_,_,part) in enumerate(ss):a=a.replace('{'+str(k)+'}',part)
    # normalize apostrophes only for finding an explicitly named phrase
    normalized=body.replace("'",'’');a=a.replace("'",'’')
    assert a in normalized,(mid,a,body)
    body=normalized.replace(a,b)
  else:
   replacements=PHRASES[mid];assert len(ss)==len(replacements),(mid,ss)
   for (a,b,part),value in reversed(list(zip(ss,replacements))):body=body[:a]+value+body[b:]
 if body==old:continue
 row=dict(id=mid,file=c['file'].split('/')[-1],ids=c['ids'],original_body=old,body=body,method='Adaptation française explicite, relue, sans choisir un sexe ou un nombre ; formulation impersonnelle si la SFC ne fournit pas le nom ajouté sur DS.')
 byid[mid]=row;new.append(row)
(O/'adaptations-francaises.json').write_text(json.dumps(list(byid.values()),ensure_ascii=False,indent=2));(O/'adaptations-passage-10.json').write_text(json.dumps(new,ensure_ascii=False,indent=2));print('Adaptations',len(new))

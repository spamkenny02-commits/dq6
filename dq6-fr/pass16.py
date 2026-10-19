"""Reviewed DS agreements and SFC-specific character references, pass 16."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parent;O=P/'v0.16';O.mkdir(exist_ok=True)
for name in ['prepare.py','build.py','verify.py','names.py','init.py','correspondances-revues.json','adaptations-francaises.json','dialogues-multilocuteurs.json','variantes-orthographiques.json','commandes-verifiees.json','decisions-alignement.json','credits-retires.json','libelles-journaux.json','liaisons-variables-natives.json','commandes-BB-C1.json']:
 s=(P/'v0.15'/name).read_text()
 if name.endswith('.py'):s=s.replace('v0.15','v0.16').replace('v0.14','v0.15').replace('v14','v15').replace('len(rows)-4762','len(rows)-4788').replace('correspondance_revue_v15','correspondance_revue_v16')
 (O/name).write_text(s)
rs=json.loads((P/'v0.15/a-revoir.json').read_text());lookup={r['id']:r for r in rs}
full={
552:"Scoopⓠ Dernière nouvelleⓠ L'équipe qui a mis la main sur l'épée légendaire est dans cette villeⓠ",
836:"Commentⓡ C'est donc cette équipe qui l'a apportéeⓡ",
849:"%3Vous avez attendu cette équipe. La voilà devant vous pour affronter le démon suprême.%4",
850:"%3Cette équipe brille de la lumière dont a besoin notre monde. Qu'on ouvre la porteⓠ%4",
856:"Je m'occupe de l'accueil. Tu peux aller patrouiller.",
862:"Emmenez tout le monde jusqu'aux cellulesⓠ",
877:"Continuez comme çaⓠ",
1083:"Grrrⓠ Quelle misèreⓠ",
1084:"Seigneur Noirkeur, notre visite est de retourⓠ",
1085:"On dirait que la leçon a du mal à entrer. Ça mérite peut-être une autre petite leçonⓡ Cette fois-ci, ce sera le dernier combat. Personne ne s'en remettraⓠ Ha haⓠ",
1533:"Oh ça, pour sûrⓠ Mais je le dois à cette équipe héroïque.",
1617:"Faites attention à vous.",
1732:"Bienvenue au grand Gluodrome de Boss, l'arène où les gluants les plus violents se réduisent en gélatine. Mais avant toute chose, vous devez inscrire votre équipe, OKⓡ Quel est le nom de votre chefⓡ %a000090, c'est çaⓡ\nParfait. Amusez-vous bienⓠ",
1805:"Tout ce que j'ai à dire, c'est qu'on vit une drôle d'époqueⓠ J'en reviens pas que le titre ait été remporté à l'occasion d'une simple visite touristiqueⓠ",
1842:"Je vous confie %a002070 pour l'entraînement. Je vous souhaite bonne chanceⓠ",
1854:"Si vous voulez un bon conseil, abandonnezⓠ Ça vaut mieux pour vous si vous tenez à la vieⓠ Votre allure est bien trop flasque et manque de force. (slurp) Vous finirez en gelée si vous vous avenglurez dans l'arèneⓠ",
1863:"Mmmⓡ Ma foi, je vous trouve une allure digne de la victoire.",
1937:"BIIIIENVENUE, MA CHÈRE COMPAGNIE ENNEMIE...㈢\n...ⓠⓐⓐ",
2157:"Oui, mon frère. Cette équipe a pour destinée d'apporter la lumière dans ce monde.",
2233:"Bienvenue. Avez-vous perdu votre route sur le chemin de la vieⓡ",
2413:"%0%a000090. Je savais que ton chemin te mènerait ici un jour. Je m'appelle Rubiss. Mon rôle est de surveiller et de protéger ce monde. As-tu entendu ma voix t'appelerⓡ",
2606:"Ah, tu connais donc %a000090ⓠ Comment va %a000090ⓡ J'espère qu'il se porte bien. Passe-lui le bonjour de son meilleur ami le maire.",
2667:"J'ai entendu dire qu'il y a de plus en plus de monstres au-delà des limites du village. Vous avez voyagé, heinⓡ Alors, c'est vraiⓡ Il y a vraiment encore plus de monstresⓡ",
2701:"De la visite étrangèreⓡ Incroyable...",
2783:"Ha haⓠ Préparez-vous à mourirⓠ",
2793:"Ha haⓠ Préparez-vous à mourirⓠ",
2809:"Je m'occupe de cet endroit. Occupez-vous des monstres à l'extérieurⓠ",
2905:"Je comprends... Je sais que je ne pourrai jamais remplacer %a000090.",
2951:"En voilà une affaire bien menéeⓠ Merciⓠ",
3140:"Eh bien, quel retour héroïqueⓠ Vous aurez toujours votre place à Puidebourgⓠ Repassez quand vous voulez, d'accordⓡ",
3436:"J'ai vu le mal de mer toucher votre compagnie. C'est pas facile de pas avoir le pied marin. Prenez soin de vous.",
3736:"Encore de l'étroitesse d'esprit, à ce que je voisⓠ Je vous prouverai à tous que j'ai raisonⓠ Ça leur apprendra à me traiter de cingléⓠ",
3774:"Mais qui nous rend visiteⓡ Ce groupe ne semble pas imprégné de l'esprit de la Déesse.",
3775:"Ce groupe m'a apporté une missive de la part du roi Somnus de Somnia. Il veut qu'on lui prête notre navire sacré, la Providence.",
3781:"%3Tu ne dois pas renvoyer ce groupe...\nTon destin est d'être à ses côtés...%4",
3787:"Attendsⓠ Si tu dis vrai, voici donc l'escorte héroïque dont parle la légendeⓠ",
3903:"L'équipe menée par %a000120 décide de passer la nuit ici...",
4035:"Hé, mais ze vous connaisⓠ Meurtor, mon maître, a envoyé vos âmes dans le royaume des rêvesⓠ Vous auriez dû y resterⓠ Quelle stupiditéⓠ",
4104:"Ouhⓠ Vous dormez ou quoiⓡ Faites gaffeⓠ",
4119:"C'est pas un hasard si on appelle cet endroit la tour de Korvedgard. Je vais vous tester. Espérons que vous soyez à la hauteur.",
4578:"Gardesⓠ Mettez fin à cette imposture et procédez aux arrestationsⓠ",
4747:"En résumé, en affrontant Meurtor, tu as perdu ta mémoire et ta forme physique... Mais tu sembles les avoir retrouvéesⓠ Tu es redevenu toi-même, %a000090, comme nous te connaissons et comme nous t'aimons. C'est bien cela, n'est-ce pasⓡ",
4749:"Et pourtant... C'est peut-être mon imagination, mais tu n'es plus tout à fait comme dans mon souvenir, %a000090...",
4874:"Je veux devenir une princesse marshmallowⓠ Quand j'aurai réussi, t'auras droit à tous les marshmallows que tu voudrasⓠ",
4962:"Oui, Louis. Et tout cela grâce à vous et à votre entourage.",
5305:"Ah bonⓡ Je suis sûr qu'il serait enchanté de vous rencontrer et d'entendre le récit de vos intrépides aventures.",
5361:"V-Votre Majesté, ce n'est que du monde de passage.",
5362:"Quel plaisirⓠ Que cette escorte entreⓠ",
5500:"Mais... Tu t'es fait battre par ce guerrier...\nEt après, tu as perdu contre cette équipe...",
5536:"(bave) Moi... attendre ici... Moi vaincue par... guerrier solitaire... (crache)",
5537:"(grogne) Moi vaincue... Mon destin... vous suivre... D'accordⓡ (crache)",
5538:"(grogne) Moi vaincue... Mon destin... vous suivre... D'accordⓡ (crache)",
5540:"(bave) Moi... attendre ici... (grogne)",
5541:"(crache) Grrrarghⓠ Moi... me battre pour toute l'équipeⓠ (grogne)",
5544:"Mais le chariot est déjà pleinⓠ Braséria part à la recherche du Carré de Tulipe, la chef d'équipe.",
5633:"Hiiiiiiⓠ C'est la puissance de vos désirs qui a guidé vos pas jusqu'iciⓡ",
5635:"Hé hé hé... L'aide humaine qui nous est arrivée récemment s'est révélée très utile. On n'en attendait pas moinsⓠ À vous de faire aussi bienⓠ Hiiiiⓠ",
5639:"Vous êtes au courantⓡ",
5936:"Tout le monde est miraculeusement guériⓠ",
5957:"Bizarrement, un regain de courage se fait sentir.",
6397:"Bienvenue dans notre aubergeⓠ",
6420:"Vous pouvez y aller.",
6633:"Eh bienⓠ Voyez donc çaⓠ La fine fleur de Paco'Style est parmi nous aujourd'huiⓠ Installez-vous confortablement et profitez de toute cette modeⓠ",
6726:"Oh, il y a plein de candidatos hommes aujourd'huiⓠ Mamma miaⓠ Hé, ciao numéro %a002300... Ciaoⓠ J'adore les ragazzi stylés et costauds, esattamente comme vousⓠ",
}
old=lookup[4753]['ds']['body'];a="redevenir %G0090%Xl'%Yle %Z%a000090 que tu étais";assert a in old;full[4753]=old.replace(a,'redevenir toi-même')
adapt=json.loads((O/'adaptations-francaises.json').read_text());byid={r['id']:r for r in adapt};new=[]
for mid,body in full.items():
 c=lookup[mid]['ds'];a=dict(id=mid,file=c['file'].split('/')[-1],ids=c['ids'],original_body=c['body'],body=body,method='Texte DS adapté explicitement à la réplique SFC : accord collectif, vouvoiement ou première personne, sans choix de sexe calculé. Identités et références natives conservées ; origine Braséria vérifiée dans MENULIST6.')
 byid[mid]=a;new.append(a)
(O/'adaptations-francaises.json').write_text(json.dumps(list(byid.values()),ensure_ascii=False,indent=2));(O/'adaptations-passage-16.json').write_text(json.dumps(new,ensure_ascii=False,indent=2))
bind=json.loads((O/'liaisons-variables-natives.json').read_text());bind['5616']={'%a000140':0xd2};bind['5799']={'%a020180':0xc1};(O/'liaisons-variables-natives.json').write_text(json.dumps(bind,ensure_ascii=False,indent=2))
# Verify the literal identity instead of substituting a different DS recruit.
ja=json.loads((P/'clean-base/ds-ja.json').read_text());fr=json.loads((P/'clean-base/ds-fr.json').read_text());j=next(r for r in ja if r['file']=='data/MENULIST6/JA/b1001000.mpt' and r['id']==7);f=next(r for r in fr if r['file']=='data/MENULIST6/FR/b1001000.mpt' and r['id']==7);assert j['text']=='@1ドランゴ@' and f['text']=='@0F@1Braséria@9N@'
(O/'identite-braseria.json').write_text(json.dumps(dict(sfc_message=5544,source_sfc_jp=lookup[5544]['sfc_jp'],ds_japanese_name=j,ds_french_name=f,reason='La réplique SFC nomme littéralement ドランゴ ; la proposition DS initiale concernait un autre recrutement, donc son tag %a002090 est écarté. Le nom français par défaut correspondant est Braséria.'),ensure_ascii=False,indent=2))
print('Explicit adaptations',len(new),'plus scoped D2/C1 bindings and safe hyphen wrapping')

p=O/"prepare.py";s=p.read_text();a=s.index("  for word in part.split():");b=s.index("  if line:lines.append(line)",a);s=s[:a]+"  def word_width(word):return sum(8 if ch==marker(0xbb) else 14 if ch in map(marker,VARS) else 1 for ch in word)\n  words=[]\n  for word in part.split():\n   if word_width(word)>24 and '-' in word:\n    pieces=word.split('-')\n    words.extend((piece+('-' if k<len(pieces)-1 else ''),k>0) for k,piece in enumerate(pieces))\n   else:words.append((word,False))\n  for word,linked in words:\n   n=word_width(word)\n   if n>24:raise ValueError('mot_trop_long')\n   limit=22 if not lines else 24\n   gap=1 if line and not linked else 0\n   if line and cols+gap+n>limit:lines.append(line);line=word;cols=n\n   else:line+=(' ' if gap else '')+word;cols+=gap+n\n"+s[b:];p.write_text(s)
p=O/"verify.py";s=p.read_text().replace(" assert r['tokens'][-1] in [0xac,0xae]"," assert r['tokens'][-1] in [0xac,0xae]\n if i not in old:assert ''.join(r['lines']).replace(' ','')==r['text'].replace(' ',''),(i,'glyph sequence changed while wrapping')");p.write_text(s)

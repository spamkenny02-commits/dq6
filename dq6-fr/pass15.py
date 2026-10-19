"""Scope native decimal BB and target-name C1 bindings to reviewed messages."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent;O=P/'v0.15';O.mkdir(exist_ok=True)
for name in ['prepare.py','build.py','verify.py','names.py','init.py','correspondances-revues.json','adaptations-francaises.json','dialogues-multilocuteurs.json','variantes-orthographiques.json','commandes-verifiees.json','decisions-alignement.json','credits-retires.json','libelles-journaux.json']:
 s=(P/'v0.14'/name).read_text()
 if name.endswith('.py'):s=s.replace('v0.14','v0.15').replace('v0.13','v0.14').replace('v13','v14').replace('len(rows)-4761','len(rows)-4762').replace('correspondance_revue_v14','correspondance_revue_v15')
 (O/name).write_text(s)
rs=json.loads((P/'v0.14/a-revoir.json').read_text());lookup={r['id']:r for r in rs}
BB=chr(0xe0bb);C1=chr(0xe0c1)
num={574:'%a000510',1494:'%a000740',1706:'%a000600',1707:'%a000590',1711:'%a000600',1714:'%a000590',1782:'%a002200',5705:'%a000750',5830:'%a000610',5840:'%a000500',6398:'%a000510',6479:'%a000480',6485:'%a000480',6487:'%a002150',6492:'%a002150',6547:'%a000730',6710:'%a002300',6719:'%a002330',6726:'%a002300',6738:'%a002300',6739:'%a002300'}
bindings={mid:{tag:0xbb} for mid,tag in num.items()}
for mid in [5800,5801,5802]:bindings[mid]={'%a020180':0xc1}
full={
1494:"%3S'il vous a fallu "+BB+" tours pour gagner la bataille, vous ne pourrez pas prétendre à la victoire.%4",
2602:'Son prix en or est de '+BB+". C'est la fierté de ma boutique. Un sacré trésor. Ça vous tenteⓡ",
2946:'Vous voulez saisir cette offre en orⓡ Prixⓢ '+BB+" pièces d'or. Vous achetezⓡ",
5705:'Sa valeur en or dans un magasin est de '+BB+'.',
5801:'%0%a020180 ne souffre plus du poison.',5802:'%0%a020180 ne souffre plus du poison.',
5830:'Le nombre de trésors à découvrir dans ce niveau est de '+BB+'.',
5840:'Quelle veineⓠ Le montant d’or trouvé est de '+BB+'ⓠ',
5864:'Le montant d’or obtenu par %a000120 est de '+BB+'.',
6479:'Votre solde en or est de '+BB+'.\nCombien voulez-vous retirer aujourd’huiⓡ',
6547:'Le nombre de jetons demandé est de '+BB+'ⓡ',
}
full.update({
574:"Vous voulez rester ici aussiⓡ Le tarif de la nuit en or est de "+BB+". Je ferais bien de récolter l'argent.",
1494:"%3Votre score en tours pour gagner la bataille est de "+BB+". Vous ne pourrez donc pas prétendre à la victoire.%4",
1706:"Quand le total de vos mini médailles atteindra "+BB+", je pourrai vous récompenser avec... un prix tellement secret que je n'ose vous le révélerⓠ ㈡ Bonne chanceⓠ",
1711:"Quand le total de vos mini médailles atteindra "+BB+", je pourrai vous récompenser avec... un prix tellement secret que je n'ose vous le révélerⓠ ㈡ Bonne chanceⓠ",
1707:"Ho hoⓠ Regardez ça, %a000120ⓠ Le total de vos médailles est de "+BB+", ce qui signifie que vous avez bien mérité un fabuleux prixⓠ",
1714:"Ho hoⓠ Regardez ça, %a000120ⓠ Le total de vos médailles est de "+BB+", ce qui signifie que vous avez bien mérité un fabuleux prixⓠ",
1782:"Parfait. Le total en or est de "+BB+".",
2946:"Vous voulez saisir cette offre en orⓡ Le prix en or est de "+BB+". Vous achetezⓡ",
6398:"Notre tarif pour la nuit en or est de "+BB+". Vous restezⓡ",
6485:"Votre solde en or dans notre chambre forte est actuellement de "+BB+". Merci beaucoup.",
6719:"J'adoreⓠ C'est pour ça que votre bonus de points s'élève à "+BB+"ⓠ",
})
adapt=json.loads((O/'adaptations-francaises.json').read_text());byid={r['id']:r for r in adapt};new=[]
for mid,body in full.items():
 c=lookup[mid]['ds'];record=dict(id=mid,file=c['file'].split('/')[-1],ids=c['ids'],original_body=c['body'],body=body,method='Adaptation DS explicite au nombre BB ou au nom cible C1 natif ; les valeurs viennent du moteur SFC et les accords de sexe/nombre sont évités.')
 byid[mid]=record;new.append(record)
(O/'adaptations-francaises.json').write_text(json.dumps(list(byid.values()),ensure_ascii=False,indent=2));(O/'adaptations-passage-15.json').write_text(json.dumps(new,ensure_ascii=False,indent=2));(O/'liaisons-variables-natives.json').write_text(json.dumps(bindings,ensure_ascii=False,indent=2))
p=O/'prepare.py';s=p.read_text();s=s.replace("|{0xc0};ALLOWED", "|{0xc0,0xc1,0xbb};ALLOWED")
s=s.replace("ADAPTATIONS={r['id']:r", "BINDINGS=read(O/'liaisons-variables-natives.json')\nADAPTATIONS={r['id']:r")
s=s.replace("variable_map=ACTORS.copy();present={t for t in ts if t in VARS}","variable_map=ACTORS.copy();present={t for t in ts if t in VARS}\n for tag,code in BINDINGS.get(str(s['id']),{}).items():\n  assert code in present,(s['id'],tag,code)\n  variable_map[tag]=code")
s=s.replace("n=sum(14 if ch in map(marker,VARS) else 1 for ch in word)","n=sum(8 if ch==marker(0xbb) else 14 if ch in map(marker,VARS) else 1 for ch in word)")
s=s.replace(" return dict(tokens=tokens,text=text,lines=lines", " for control in [0xbb,0xc1]:\n  if ts.count(control)!=tokens.count(control):raise ValueError('variable_native_non_reliee_'+hex(control))\n return dict(tokens=tokens,text=text,lines=lines")
p.write_text(s)
p=O/'verify.py';s=p.read_text().replace('protected={0xda,0xd5,0xb0,0xd6}','protected={0xda,0xd5,0xb0,0xd6,0xbb,0xc1}');p.write_text(s)
# Audited routine bytes: C6:935A loads the 24-bit amount from 7E:5A2E;
# C6:937A calls C0:1055 and emits up to eight decimal characters.
rom=(P.parent/'upload/Dragon Quest VI - Maboroshi no Daichi (Japan).sfc').read_bytes();vf=(P/'clean-base/vf-base-headered.sfc').read_bytes()[512:]
proof=[]
for code,a,n,meaning in [(0xbb,0x6935a,16,'Nombre : charge 5A2E/5A2F dans A6/A7, puis conversion décimale.'),(0xc1,0x69351,9,'Nom cible : charge 3B2F puis rejoint 93F7, routine commune aux noms de personnages.')]:
 b=rom[a:a+n];assert b==vf[a:a+n];proof.append(dict(control=f'{code:02X}',file_offset=a,bytes_hex=b.hex(),identical_in_ips=True,meaning=meaning))
(O/'commandes-BB-C1.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2))

"""Lot 19 : B2 limité aux répliques relues ; deuxième nombre natif C5."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parent;O=P/'v0.19'
def read(p):return json.loads(p.read_text())
def save(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
jp={r['id']:r for r in read(P/'clean-base/sfc-jp.json')}
ja={(r['file'].split('/')[-1],r['id']):r for r in read(P/'clean-base/ds-ja.json') if '/MESS6/' in r['file']}
fr={(r['file'].split('/')[-1],r['id']):r for r in read(P/'clean-base/ds-fr.json') if '/MESS6/' in r['file']}
choices={1764:('0059.p',[882,883]),1808:('0060.p',[19,20]),1809:('0060.p',[22,23]),
1811:('0060.p',[27]),1816:('0060.p',[41,42]),1822:('0060.p',[63,64,65]),
1823:('0060.p',[70]),1824:('0060.p',[71]),1826:('0060.p',[75]),1828:('0060.p',[77]),
1832:('0060.p',[78]),1835:('0060.p',[79]),1883:('0060.p',[207,208]),1890:('0060.p',[247,248]),
2111:('0090.p',[8]),2112:('0090.p',[9]),2114:('0090.p',[18]),2117:('0090.p',[35]),2134:('0090.p',[120]),2135:('0090.p',[114]),3487:('0016.p',[50]),
6215:('0815.p',[38]),6510:('0815.p',[38]),6517:('0830.p',[6]),
6580:('0074.p',[70]),6593:('0074.p',[381]),6639:('0074.p',[177,178,179]),
6656:('0838.p',[70]),6657:('0838.p',[72]),6658:('0838.p',[74]),6659:('0838.p',[76]),
6660:('0838.p',[78]),6661:('0838.p',[80]),6662:('0838.p',[82]),6663:('0838.p',[84]),
6699:('0074.p',[266]),6705:('0074.p',[282]),6714:('0074.p',[308,309]),6724:('0074.p',[324]),6729:('0074.p',[348,349])}
tags={1764:'002180',1808:'002240',1809:'002240',1811:'002240',1816:'002240',
1822:'002240',1823:'002240',1824:'002240',1826:'002240',1828:'002240',1832:'002240',1835:'002240',1883:'002250',1890:'002240',
2111:'002000',2112:'002010',2114:'002010',2117:'002000',2134:'002040',2135:'002010',3487:'002010',
6517:'000180',6580:'002260',6593:'002350',6639:'002260',
6656:'002280',6657:'002280',6658:'002280',6659:'002280',6660:'002280',6661:'002280',6662:'002280',6663:'002280',
6699:'002310',6705:'002340',6714:'000180',6724:'002340',6729:'002340'}
adapt={
1808:("C'est censé être une statue de l'ancien champion après sa défaite contre %a002240... Mouais... Pour moi, tous les gluants se ressemblent. Je sais pas comment fait ce minus pour les distinguer.", 'Préposition neutre devant le nom, sans condition phonétique DS.'),
1809:("Regardez-moi qui voilà. Pour sûr, vous faites partie de l'équipe de %a002240! Un combat pareil, ça marque les esprits. Je suis pas près de l'oublier, croyez-moi!", 'La SFC nomme le champion ; restaure cette référence native, à la place du rôle entraîneur/entraîneuse DS.'),
1822:("Ma parole! C'est vous! Vous avez réussi! Vous avez enfin réussi! Votre partenaire a cassé la baraque! C'est quoi son nom, déjà? Mon Moloss n'avait aucune chance! Minute! %a002240, c'est ça? Quel nom! Un nom digne de la victoire! Compris?", 'Reformule les accords champion/championne, tueur/tueuse en expressions neutres ; conserve la victoire, la demande du nom et le nom B2.'),
1823:('Dites, vous voudriez pas me vendre %a002240, par hasard?', 'La SFC nomme explicitement le gluant proposé à la vente ; restaure B2 au lieu du nom commun DS.'),
1883:("(soupir) %a002250 m'a réduit en gelée lors de notre dernière rencontre...", 'Supprime seulement le déterminant conditionnel Ce/Cet DS.'),
6215:('Le style passe de %a000821 à %a000822!', 'La SFC omet le nom : conserve uniquement les deux nombres BB et C5.'),
6699:('Numéro %a002300! Le numéro %a002300, %a002310! Félicitations!', 'Conserve deux nombres BB puis un nom B2, comme en SFC ; la DS répète le nom au lieu du numéro.'),
6724:('%a002340, la parole est à vous!', 'La DS fixe Gianni ; la SFC utilise un nom de juge dynamique. Conserve le contrôle B2 source.')}
def body(file,ids):
 parts=[]
 for did in ids:
  m=re.fullmatch(r'@a([^@]*)@b(.*?)\n?@c0@',fr[(file,did)]['text'],re.S);assert m
  s=m.group(2).strip()
  if s.startswith('*ⓢ '):s=s[3:]
  parts.append(s)
 return ' '.join(parts)
existing=read(O/'correspondances-revues.json')
for r in existing:
 if r['id'] in choices:assert (r['file'],r['ids'])==choices[r['id']]
existing=[r for r in existing if r['id'] not in choices]
bindings=read(O/'liaisons-variables-natives.json');adaptations=read(O/'adaptations-francaises.json')
reviews=[]
for mid,(file,ids) in choices.items():
 assert str(mid) not in bindings
 original=body(file,ids)
 if mid in tags:bindings[str(mid)]={'%a'+tags[mid]:0xb2}
 else:bindings[str(mid)]={'%a000821':0xbb,'%a000822':0xc5}
 if mid==6510:bindings[str(mid)]['%a000180']=0xc0
 if mid==6699:bindings[str(mid)]['%a002300']=0xbb
 for code in bindings[str(mid)].values():assert code in jp[mid]['tokens']
 r=dict(id=mid,file=file,ids=ids,sfc_jp=jp[mid]['text'],ds_jp=[ja[(file,i)]['text'] for i in ids],ds_fr=[fr[(file,i)]['text'] for i in ids],
 native_bindings={tag:f'{code:02X}' for tag,code in bindings[str(mid)].items()},
 review='Japonais et rôle du locuteur relus. Les différentes formulations DS courtes sont choisies d’après leur sens et la scène SFC ; noms dynamiques SFC conservés, sans nom fixe introduit.')
 if mid in adapt:
  replacement,note=adapt[mid]
  adaptations.append(dict(id=mid,file=file,ids=ids,original_body=original,body=replacement,review=note));r['adaptation']=note
 existing.append(r);reviews.append(r)
save('correspondances-revues.json',existing);save('revue-lot-v019.json',reviews)
save('liaisons-variables-natives.json',bindings);save('adaptations-francaises.json',adaptations)
source=(P.parent/'upload/Dragon Quest VI - Maboroshi no Daichi (Japan).sfc').read_bytes()
vf=(P/'clean-base/vf-base-headered.sfc').read_bytes()[512:]
assert source[0x69206:0x6920c]==vf[0x69206:0x6920c]==bytes.fromhex('20c095ad285a')
assert vf[0x6920c:0x6920f]==bytes.fromhex('4cf0fd')
assert vf[0x6fdf0:0x6fdfa]==bytes.fromhex('9cb459a00000c9a709b0')
c5=bytes.fromhex('20c095ad325a85a6ad335a85a74c7a93')
assert source[0x6936a:0x6936a+len(c5)]==vf[0x6936a:0x6936a+len(c5)]==c5
save('commandes-B2-C5-verifiees.json',dict(B2=dict(file_offset=0x69206,read_field='5A28',common_prefix_hex='20c095ad285a',vf_extension_cpu='C6:FDF0',vf_extension_file=0x6fdf0,notes='La VF décompresse la chaîne nommée via son extension existante. Aucun changement du code natif ; uniquement ajout du contrôle déjà présent dans la réplique source.',scoped_ids=sorted(tags)),C5=dict(file_offset=0x6936a,bytes_hex=c5.hex(),read_field='5A32/5A33',format='Même conversion décimale que BB, au plus huit chiffres.')))
p=O/'prepare.py';s=p.read_text().replace('|{0xc0,0xc1,0xbb,0xb3}', '|{0xc0,0xc1,0xbb,0xb3,0xb2,0xc5}')
s=s.replace("if any(t not in ALLOWED for t in controls):raise ValueError('commandes_SFC_non_adaptees')", "if any(t not in ALLOWED for t in controls):raise ValueError('commandes_SFC_non_adaptees')\n if 0xb2 in controls and 0xb2 not in BINDINGS.get(str(s['id']),{}).values():raise ValueError('B2_non_revu')\n if 0xc5 in controls and 0xc5 not in BINDINGS.get(str(s['id']),{}).values():raise ValueError('C5_non_revu')")
s=s.replace('8 if ch==marker(0xbb)', '8 if ch in [marker(0xbb),marker(0xc5)]')
s=s.replace('for control in [0xbb,0xc1]:','for control in [0xbb,0xc1,0xb2,0xc5]:')
p.write_text(s)
p=O/'verify.py';s=p.read_text().replace('0xbb,0xc1,0xb3}', '0xbb,0xc1,0xb3,0xb2,0xc5}')
p.write_text(s)
print(json.dumps(dict(reviewed=len(reviews),adaptations=len(adapt))))

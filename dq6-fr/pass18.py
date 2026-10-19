"""Revue explicite du lot 18. Ne modifie aucun token des lots précédents."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parent;O=P/'v0.18'
def read(p):return json.loads(p.read_text())
def save(name,value):(O/name).write_text(json.dumps(value,ensure_ascii=False,indent=2))
jp={r['id']:r for r in read(P/'clean-base/sfc-jp.json')}
ja={(r['file'].split('/')[-1],r['id']):r for r in read(P/'clean-base/ds-ja.json') if '/MESS6/' in r['file']}
fr={(r['file'].split('/')[-1],r['id']):r for r in read(P/'clean-base/ds-fr.json') if '/MESS6/' in r['file']}
choices={
 7:('0006.p',[800]),77:('0010.p',[683]),87:('0012.p',[174]),
 1204:('0009.p',[727]),1211:('0009.p',[742]),1377:('0026.p',[565]),
 1413:('0020.p',[226]),1635:('0007.p',[138]),
 1780:('0837.p',[36]),1785:('0837.p',[54]),1786:('0837.p',[54]),
 1795:('0059.p',[978]),1800:('0060.p',[2]),
 2074:('0086.p',[565]),2099:('0019.p',[300,301]),
 2153:('0091.p',[0]),2174:('0091.p',[75]),2182:('0091.p',[0]),
 2210:('0004.p',[630,631]),2342:('0801.p',[842]),2372:('0008.p',[404]),
 2496:('0002.p',[518]),2672:('0065.p',[519]),3270:('0006.p',[531]),
 3672:('0009.p',[742]),3673:('0009.p',[727]),3978:('0044.p',[589]),
 4016:('0000.p',[128]),4181:('0004.p',[65]),4223:('0005.p',[76]),
 4685:('0015.p',[509]),4798:('0068.p',[142]),4813:('0068.p',[513]),
 4950:('0043.p',[523,524]),5102:('0024.p',[465]),5104:('0024.p',[14]),
 5207:('0058.p',[246]),5210:('0058.p',[254]),5442:('0019.p',[755]),
 5566:('0079.p',[523]),5751:('0807.p',[88]),
 5779:('0803.p',[119]),5780:('0803.p',[130]),5781:('0803.p',[132]),
 5782:('0803.p',[139]),5784:('0803.p',[147]),5785:('0803.p',[150]),
 5819:('0803.p',[119]),5875:('0806.p',[16]),5938:('0803.p',[196]),
 5944:('0801.p',[975]),5945:('0801.p',[977]),5958:('0803.p',[234]),
 5960:('0803.p',[244]),5961:('0803.p',[245]),5966:('0803.p',[260]),
 5969:('0803.p',[269]),6291:('0810.p',[63]),6295:('0813.p',[0]),
 6350:('0818.p',[8]),6353:('0818.p',[22]),6358:('0818.p',[34]),
 6412:('0831.p',[10]),6428:('0816.p',[12]),6430:('0816.p',[28]),
 6431:('0816.p',[30]),6433:('0816.p',[18]),6442:('0816.p',[50]),
 6443:('0816.p',[52]),6444:('0816.p',[54]),6503:('0815.p',[22]),
 6553:('0822.p',[10]),6932:('0810.p',[31]),6933:('0822.p',[51]),
 6951:('0816.p',[52]),6953:('0816.p',[18])}
bindings={}
def bind(mid,**values):bindings[mid]={'%a'+tag:code for tag,code in values.items()}
for mid in [1780,1785,1786,1795,1800]:bindings[mid]={'%a002190':0xc0}
bindings[2342]={'%a020010':0xd3}
bindings[5566]={'%a000180':0xd3}
for mid in [5779,5780,5781,5782,5784,5785,5819,5938,5958,5960,5961,5969]:
 bindings[mid]={'%a020010':0xc0}
bindings[5938]['%a000810']=0xbb
bindings[5944]={'%a000180':0xc0,'%a000770':0xbb}
bindings[5945]={'%a000180':0xc0,'%a000810':0xbb}
bindings[5966]={'%a002020':0xc0}
bindings[6358]={'%a000060':0xc0,'%a000080':0xbb}
for mid in [6412,6430,6431,6433,6442,6443,6444,6932,6933,6951,6953]:
 bindings[mid]={'%a000180':0xc0}
bindings[6428]={'%a002020':0xc0}
adapted={
 7:('Il fait nuit et la porte est verrouillée.', 'La SFC précise la nuit ; porte verrouillée dans les deux sources.'),
 77:('%a000140 sort la rosée onirique et en verse quelques gouttes sur %a002020.', 'La SFC nomme Laura au lieu du démonstratif DS ; conserve C0 et CC.'),
 1785:('Félicitations, %a002190! Tu as gagné la manche 1. Passons à la manche 2!', 'Les numéros 1 et 2 sont littéraux dans la SFC.'),
 1786:('Félicitations, %a002190! Tu as gagné la manche 2. Passons à la manche 3!', 'Les numéros 2 et 3 sont littéraux dans la SFC.'),
 2372:("'Prix bradés! Allez à Port Abbri pour seulement 50 pièces d'or par passager!'", 'Le pictogramme monétaire DS est développé en mots ; montant 50 G confirmé en japonais SFC.'),
 3978:('Vous ne devriez pas être là, vous savez. Ah!', 'Ajoute uniquement la surprise finale présente dans la SFC.'),
 4685:('Allons, allons. Pas de fausse modestie.', 'La suite DS du don est déjà traitée dans les autres répliques SFC ; extrait les deux premières phrases.'),
 5944:('%a000180 gagne %a000770 PV maximum!', 'Reformule la branche de genre française, sans perdre C0 ni BB.'),
 5945:('%a000180 gagne %a000810 PM maximum!', 'Reformule la branche de genre française, sans perdre C0 ni BB.'),
 6358:("%a000060, mon enfant! Le nombre de points d'expérience nécessaires pour passer au niveau supérieur est de %a000080.", 'Évite le suffixe DS singulier/pluriel tout en conservant le nom C0 et le nombre BB.'),
 6430:("Mmm... Ce n'est pas très bien vu dans le milieu des chefs d'équipe, mais je vais garder le cercueil contenant %a000180. ㈡ C'est bien parce que c'est vous.", 'Supprime uniquement la flexion de la préposition précédant le nom ; cercueil confié à Tulipe confirmé en japonais.'),
 6431:("Eh bien, dans ce cas, faites preuve d'un peu de respect et ressuscitez %a000180!", 'Rétablit le nom C0 explicitement présent en SFC, à la place du pronom genré DS.'),
 6444:('Le cercueil contenant %a000180 est chargé dans le chariot.', 'Évite la préposition DS dépendante du genre du nom ; conserve C0.'),
 6933:("Entendu, je vais remettre le prix à %a000180 qui est dans le chariot.", 'Préposition neutre devant le nom natif ; aucune modification de la destination du prix.')}
def body(file,ids):
 parts=[]
 for i in ids:
  m=re.fullmatch(r'@a([^@]*)@b(.*?)\n?@c0@',fr[(file,i)]['text'],re.S);assert m
  s=m.group(2).strip()
  if s.startswith('*ⓢ '):s=s[3:]
  parts.append(s)
 return ' '.join(parts)
existing=read(O/'correspondances-revues.json');seen={r['id'] for r in existing}
old={r['id'] for r in read(P/'v0.17/insertion-candidates.json')};assert not old.intersection(choices)
review=[]
for mid,(file,ids) in choices.items():
 assert mid not in seen
 r=dict(id=mid,file=file,ids=ids,sfc_jp=jp[mid]['text'],
        ds_jp=[ja[(file,i)]['text'] for i in ids],ds_fr=[fr[(file,i)]['text'] for i in ids],
        review='Comparaison japonaise relue : mêmes paroles, variantes kana/kanji, petite particule, ponctuation ou découpage DS. Les noms de locuteurs et variables sont contrôlés séparément à la préparation.')
 if mid in bindings:r['native_bindings']={tag:f'{code:02X}' for tag,code in bindings[mid].items()}
 if mid in adapted:r['review']=adapted[mid][1]
 review.append(r);existing.append(r)
save('correspondances-revues.json',existing);save('revue-lot-v018.json',review)
b=read(O/'liaisons-variables-natives.json')
for mid,mapping in bindings.items():
 assert str(mid) not in b
 for code in mapping.values():assert code in jp[mid]['tokens']
 b[str(mid)]=mapping
save('liaisons-variables-natives.json',b)
a=read(O/'adaptations-francaises.json');aids={x['id'] for x in a}
for mid,(replacement,note) in adapted.items():
 assert mid not in aids
 file,ids=choices[mid]
 a.append(dict(id=mid,file=file,ids=ids,original_body=body(file,ids),body=replacement,review=note))
save('adaptations-francaises.json',a)
# Keep a machine-readable proof of unchanged native dispatchers.
source=(P.parent/'upload/Dragon Quest VI - Maboroshi no Daichi (Japan).sfc').read_bytes()
vf=(P/'clean-base/vf-base-headered.sfc').read_bytes()[512:]
proof=[]
for code,offset,hexbytes,meaning in [
 ('C0',0x69348,'20c095ad2d3b4cf793','Nom contextuel, charge le champ 3B2D avant le formateur commun 93F7.'),
 ('BB',0x6935a,'20c095ad2e5a85a6ad2f5a85a74c7a93','Nombre contextuel 24 bits via 5A2E/5A2F ; huit chiffres maximum.')]:
 raw=bytes.fromhex(hexbytes);assert source[offset:offset+len(raw)]==raw==vf[offset:offset+len(raw)]
 proof.append(dict(control=code,file_offset=offset,bytes_hex=hexbytes,meaning=meaning,unchanged_in_ips=True))
save('commandes-C0-lot18.json',dict(dispatchers=proof,bindings={str(k):v for k,v in bindings.items()},limits='Liaisons limitées aux identifiants relus. Aucune équivalence globale des variables DS.'))
print(json.dumps(dict(reviewed=len(review),scoped_bindings=len(bindings),adaptations=len(adapted))))

"""Deuxième lot : noms B3 natifs, boutiques et églises ; aucun ancien token modifié."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parent;O=P/'v0.18'
def read(p):return json.loads(p.read_text())
def save(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
jp={r['id']:r for r in read(P/'clean-base/sfc-jp.json')}
ja={(r['file'].split('/')[-1],r['id']):r for r in read(P/'clean-base/ds-ja.json') if '/MESS6/' in r['file']}
fr={(r['file'].split('/')[-1],r['id']):r for r in read(P/'clean-base/ds-fr.json') if '/MESS6/' in r['file']}
choices={23:('0014.p',[182]),868:('0088.p',[74]),872:('0088.p',[84]),1124:('0089.p',[611]),
 1988:('0005.p',[914,915,916,917]),1990:('0011.p',[601,602,603,604]),
 1992:('0011.p',[605]),1996:('0066.p',[505]),
 6361:('0818.p',[38]),6362:('0818.p',[42,44]),6363:('0818.p',[46]),
 6365:('0818.p',[50]),6366:('0818.p',[54]),6385:('0819.p',[38]),
 6386:('0819.p',[42,44]),6388:('0819.p',[50]),6389:('0819.p',[54])}
groups=[('0811.p',[6222,6226,6229,6230,6231,6233]),
 ('0812.p',[6249,6253,6255,6256,6257,6259]),
 ('0810.p',[6275,6279,6281,6282,6283,6285]),
 ('0813.p',[6301,6305,6307,6308,6309,6311])]
for file,mids in groups:
 for mid,did in zip(mids,[16,29,31,33,35,43]):choices[mid]=(file,[did])
# SFC has one additional colloquial shop voice. DS uses the same generic shop script.
for mid,did in zip([6327,6331,6333,6334,6336],[16,29,33,35,43]):choices[mid]=('0813.p',[did])
assert len(choices)==46
def body(file,ids):
 parts=[]
 for did in ids:
  m=re.fullmatch(r'@a([^@]*)@b(.*?)\n?@c0@',fr[(file,did)]['text'],re.S);assert m
  s=m.group(2).strip()
  if s.startswith('*ⓢ '):s=s[3:]
  parts.append(s)
 return ' '.join(parts)
adapt={}
for mid in [6222,6249,6275,6301,6327]:
 adapt[mid]=('Vous ne pouvez rien porter de plus, %a000180.', 'La SFC ne propose pas de réorganisation automatique des objets ; seule la première information DS est conservée, avec formulation neutre.')
for mid in [6230,6256,6282,6308,6333]:
 verb="J'ai mis" if mid==6230 else 'Je vais mettre'
 adapt[mid]=(verb+' ce que vous avez acheté dans le cercueil contenant %a000180.', 'Remplace la préposition DS genrée par une relative neutre ; nom B3 conservé.')
adapt[6362]=('Ô grande et bienveillante Déesse! Je t\'implore de ramener à la vie notre fidèle %a000180!', 'Notre fidèle remplace les branches DS ton fidèle serviteur / ta fidèle servante.')
adapt[6363]=('%a000180 a retrouvé la vie!', 'Forme passée sans accord de genre, équivalente au message DS de résurrection.')
adapt[6366]=('Grande et bienfaisante Déesse! Débarrasse notre fidèle %a000180 de ce poison impie!', 'Notre fidèle remplace les branches de genre DS, sans perdre le destinataire.')
adapt[6385]=('Vous devez vous tromper. %a000180 semble bien en vie!', 'En vie remplace vivant/vivante, conformément au texte japonais.')
adapt[6389]=('Ô grande Déesse, montre-nous ton immense pouvoir! ㈡ Débarrasse notre fidèle %a000180 du poison qui s\'est répandu dans son corps!', 'Notre fidèle remplace ton/ta fidèle ; conserve le changement de page DS.')
existing=read(O/'correspondances-revues.json')
for r in existing:
 if r['id'] in choices:assert (r['file'],r['ids'])==choices[r['id']]
existing=[r for r in existing if r['id'] not in choices];seen={r['id'] for r in existing}
bindings=read(O/'liaisons-variables-natives.json');adaptations=read(O/'adaptations-francaises.json')
reviews=[]
for mid,(file,ids) in choices.items():
 assert mid not in seen and str(mid) not in bindings
 original=body(file,ids)
 tag='%a000140' if mid in [868,872,1124] else '%a000090' if mid in [1988,1990,1992,1996] else '%a000180'
 assert tag in original and jp[mid]['tokens'].count(0xb3)==1
 bindings[str(mid)]={tag:0xb3}
 r=dict(id=mid,file=file,ids=ids,sfc_jp=jp[mid]['text'],
  ds_jp=[ja[(file,i)]['text'] for i in ids],ds_fr=[fr[(file,i)]['text'] for i in ids],
  native_bindings={tag:'B3'},review='Japonais relu : même action et même destinataire contextuel. B3 est conservé avec son champ natif 5A24 ; aucune substitution par un nom fixe.')
 if mid>=6200 and mid<6350:r['review']+=' Les variantes de politesse SFC reprennent le texte générique DS correspondant au même service.'
 if mid in adapt:
  replacement,note=adapt[mid]
  adaptations.append(dict(id=mid,file=file,ids=ids,original_body=original,body=replacement,review=note))
  r['adaptation']=note
 existing.append(r);reviews.append(r)
save('correspondances-revues.json',existing);save('revue-lot-v018-B3.json',reviews)
save('liaisons-variables-natives.json',bindings);save('adaptations-francaises.json',adaptations)
source=(P.parent/'upload/Dragon Quest VI - Maboroshi no Daichi (Japan).sfc').read_bytes()
vf=(P/'clean-base/vf-base-headered.sfc').read_bytes()[512:]
offset=0x692ce;raw=bytes.fromhex('20c095ad245a4cf793')
assert source[offset:offset+len(raw)]==raw==vf[offset:offset+len(raw)]
save('commande-B3-verifiee.json',dict(control='B3',file_offset=offset,bytes_hex=raw.hex(),
 meaning='Appelle 95C0, charge le mot à 5A24, rejoint le formateur commun des noms 93F7.',
 unchanged_in_ips=True,scoped_ids=sorted(choices),occurrences_per_source=1))
path=O/'prepare.py';s=path.read_text();s=s.replace('|{0xc0,0xc1,0xbb}', '|{0xc0,0xc1,0xbb,0xb3}');path.write_text(s)
path=O/'verify.py';s=path.read_text().replace('protected={0xda,0xd5,0xb0,0xd6,0xbb,0xc1}', 'protected={0xda,0xd5,0xb0,0xd6,0xbb,0xc1,0xb3}');path.write_text(s)
print(json.dumps(dict(reviewed=len(reviews),adaptations=len(adapt))))

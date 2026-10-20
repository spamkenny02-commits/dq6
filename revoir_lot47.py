"""Review of debug/progression labels; lexical DS references are not dialogue matches."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;P=R/'dq6-fr';O=P/'v0.47';O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2))
jp=read(P/'clean-base/sfc-jp.json');vf=read(P/'clean-base/sfc-vf.json')
ja=read(P/'clean-base/ds-ja.json');fr={(x['file'].replace('/FR/','/JA/'),x['id']):x for x in read(P/'clean-base/ds-fr.json')}
draft=read(R/'preparation-initiale-v047.json')
held={6040:'Fonction exacte de キャンセル歩行 à vérifier dans le code et le contexte debug.',6041:'Même fonction que6040.',6042:'Même fonction que6040.',6046:'Identité du niveau インチキフロア à établir.',6047:'Même niveau que6046.',6048:'Opposition au niveau6046 à établir.',6157:'Nom français du château はざまの城 à établir.',6207:'Terminologie et variante du poker ハイロー à confirmer.'}
fix={6057:'Hélas, les indicateurs requis manquent. ㈡ Obtenez le chariot normalement.',6067:"Accès interdit au public. ㈡ Les testeurs sont particulièrement priés de s'abstenir.",6113:"Pierre s'est enfui de la grotte Sacrée",6119:'Demande du roi Louis entendue',6144:'Fusion de Pégase terminée',6158:'Vers la séquence de fin',6165:'Hélas, les indicateurs requis manquent. ㈡ Amenez Olivier normalement.'}
# Explicit lexical correspondences, read in both DS languages. No fuzzy dialogue alignment.
lex=[('精霊のかんむり','精霊のかんむり','couronne sacrée'),('くじけぬ','くじけぬ','coeur impétueux'),('ミレーユ','ミレーユ','Émilie'),('夢見のしずく','ゆめみのしずく','rosée onirique'),('エリザ','エリザ','Alyzée'),('バーバラ','バーバラ','Laura'),('ラーの鏡','ラーの鏡','miroir de Râ'),('シェーラ','シェーラ','Apnéa'),('地底魔城','地底魔城','Fort-Terreur'),('ムドー','ムドー','Meurtor'),('ゲント','ゲント','Paradisia'),('アモス','アモス','Amos'),('テリー','テリー','Tommy'),('旅人の洞窟','旅人の洞','col des Voyageurs'),('ジャミラス','ジャミラス','Jamirus'),('ホルス','ホルス','Pierre'),('洗礼の洞窟','洗礼の洞','grotte Sacrée'),('黄金のつるはし','おうごんのつるはし','pioche dorée'),('勇気のかけら','ゆうきのかけら','fragment de courage'),('フォーン王','フォーン','Louis'),('ミラルゴ','ミラルゴ','Méphisto'),('イリカ','イリカ','Cristal'),('ディーネ','ディーネ','Ondine'),('マーメイドハープ','マーメイドハープ','harpe de Calypso'),('グラコス','グラコス','Gracos'),('砂の器','すなのうつわ','urne de sable'),('マダンテ','マダンテ','Explosion magique'),('ゴラン','ゴラン','Saul Ytaire'),('ライフコッド','ライフコッド','pic des Tisseurs'),('サリイ','サリイ','Martel'),('ラミアス','ラミアス','Ramias'),('ヘルクラウド','ヘルクラウド','Typhonia'),('レイドック','レイドック','Somnia'),('モルガン','モルガン','Fortuné Friquet'),('ドグマ','ドグマ','Dogmus'),('ゾゾゲル','ゾゾゲル','Marcus'),('しんじつのオーブ','真実のオーブ','orbe de vérité'),('クリムト','クリムト','Blaise'),('ムーア','ムーア','Mortamor'),('ハッサン','ハッサン','Olivier'),('ファルシオン','ファルシオン','Céleste')]
def ref(term,translation):
 for x in ja:
  y=fr.get((x['file'],x['id']))
  if term in x['text'].replace(';','') and y and translation.casefold().replace('œ','oe') in y['text'].replace(';','').casefold().replace('œ','oe'):return dict(file=x['file'],id=x['id'],ja=x['text'],fr=y['text'],scope='LEXIQUE_SEULEMENT : pas une correspondance du libellé debug SFC complet.')
 return None
lexrefs={a:ref(b,c) for a,b,c in lex}
rows=[]
for d in draft:
 i=d['id']
 if i in held:continue
 b=fix.get(i,d['adaptation_body']);refs=[]
 for a,j,f in lex:
  if a in d['sfc_jp'] and lexrefs[a]:refs.append(lexrefs[a])
 if i in [6081,6082]:
  x=next(x for x in ja if x['file']=='data/MESS6/JA/0006.p' and x['id']==490);y=fr[x['file'],x['id']]
  assert 'Ella' in y['text'] and 'Johan' in y['text']
  refs.append(dict(file=x['file'],id=x['id'],ja=x['text'],fr=y['text'],scope='Noms seulement : サンディ SFC correspond à メラニィ DS/Ella ; ジョセフ/Johan.'))
 reason='Libellé technique/progression SFC relu directement : sujet, action et chronologie conservés. FR DS utilisé pour le lexique confirmé, pas comme dialogue équivalent. Ancien IPS secondaire relu mais ses identifiants ou phrases décalées ne valident pas le sens.'
 if i==6113:reason+=' Le brouillon « grotte du Baptême » est corrigé en « grotte Sacrée », attestée par la table DS洗礼の洞くつ.'
 if i==6119:reason+=' 聞いた indique que la demande a été entendue, pas que la quête a déjà été accomplie.'
 if i in [6057,6067,6165]:reason+=' Les indicateurs debug manquants restent explicites ; la commande de pause native est conservée par le compilateur.'
 if i==6162:reason+=' Question debug de point de départ ; aucune donnée ni routine de crédits retirée n’est réintroduite.'
 if i in [6080,6088,6098,6104,6106,6114,6151,6154]:reason+=' Identifiant technique M/C conservé littéralement, sans inventer un nom de lieu.'
 if i in [6209,6210,6211,6212]:reason+=' Message de démonstration SFC conservé comme tel, pas transformé en remerciement de fin de jeu.'
 rows.append(dict(id=i,file='SFC_ORIGINAL',ids=[],status='RELU',compile_mode='SFC_REVIEWED_ADAPTATION',sfc_jp=jp[i]['text'],sfc_vf_secondaire=vf[i]['text'],ds_references=[],ds_lexical_references=refs,ds_reference_scope='Adaptation directe du libellé SFC ; références DS lexicales seulement, aucun dialogue DS équivalent validé.',original_body=b,adaptation_body=b,native_bindings={},adaptation_speaker='',adaptation_review=reason,review=reason,sfc_context=d['sfc_context']))
assert len(rows)==142
save(O/'revue-lot-v047.json',rows)
save(O/'blocages-brouillons-v047.json',[{**d,'blocker':held[d['id']]} for d in draft if d['id'] in held])
save(O/'qa-relecture-lexicale.json',dict(reviewed=142,full_ds_dialogue_matches=0,with_explicit_ds_lexical_references=sum(bool(x['ds_lexical_references']) for x in rows),corrected_draft_ids=list(fix),held_ids=list(held),missing_exact_lexical_ref=[a for a,x in lexrefs.items() if x is None]))
print('REVIEWED',len(rows),'HELD',len(held))

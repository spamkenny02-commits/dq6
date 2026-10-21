"""Create a new reviewed lot; never reuse the previous review as new approval."""
from pathlib import Path
import json,shutil,hashlib,importlib.util
from plans50 import PLANS
R=Path(__file__).resolve().parent;D=R/'dq6-fr';B=D/'v0.49';O=D/'v0.50';O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2))
jp=read(D/'clean-base/sfc-jp.json');vf=read(D/'clean-base/sfc-vf.json');ja=read(D/'clean-base/ds-ja.json');fr=read(D/'clean-base/ds-fr.json');fi={(x['file'].replace('/FR/','/JA/'),x['id']):x for x in fr};old={x['id']:x for x in read(B/'insertion-candidates.json')}
# These exact source entries establish lexical choices, not whole-message matches.
lex={
'ソルディ':('data/MESS6/JA/0003.p',456),'スラッジ':('data/MESS6/JA/0059.p',879),'ドガ':('data/MESS6/JA/0000.p',934),'ボガ':('data/MESS6/JA/0001.p',0),'イリア':('data/MESS6/JA/0009.p',725),'ロブ':('data/MESS6/JA/0044.p',600),'フランコ':('data/MESS6/JA/0067.p',616),'ホルテン':('data/MESS6/JA/0024.p',65),'レイドック王':('data/MESS6/JA/0005.p',93),'トム':('data/MESS6/JA/0008.p',622),'ブラスト':('data/MESS6/JA/0019.p',709),'カルベ':('data/MESS6/JA/0056.p',789),'ルイーダ':('data/MESS6/JA/0006.p',394),'ホルコッタ':('data/MENULIST6/JA/b1005000.mpt',43),'デュラン':('data/MENULIST6/JA/b1002000.mpt',227),'クラウド城':('data/MESS6/JA/0079.p',34),'ゼニス王':('data/MESS6/JA/0078.p',5),'カルベローナ':('data/MENULIST6/JA/b1005000.mpt',11),'インパス':('data/MENULIST6/JA/b1003000.mpt',180),
'ターニア':('data/MESS6/JA/0062.p',522),'ランド':('data/MESS6/JA/0062.p',522),'サンディ':('data/MESS6/JA/0006.p',490),'ジョセフ':('data/MESS6/JA/0006.p',490),'エリザ':('data/MESS6/JA/0008.p',27),'シェーラ':('data/MESS6/JA/0012.p',265),'イリカ':('data/MESS6/JA/0043.p',538),'フォーン王':('data/MESS6/JA/0041.p',593),'ドランゴ':('data/MENULIST6/JA/b1001000.mpt',7),'グランマーズ':('data/MENULIST6/JA/b1008000.mpt',46),'ディーネ':('data/MENULIST6/JA/b1001000.mpt',15),'アクバー':('data/MENULIST6/JA/b1002000.mpt',233)}
lookup={(x['file'],x['id']):x for x in ja}
specific={300:('0056.p',[514]),445:('0075.p',[733,735]),752:('0082.p',[55]),852:('0088.p',[110]),871:('0088.p',[82]),873:('0088.p',[86]),875:('0088.p',[89]),876:('0088.p',[99]),2432:('0000.p',[601])}
notes={
2432:'La phrase reprise du voisin2431 est une exclamation affirmative, 大役じゃない. DS0000:601 confirme grand honneur ; ne pas reproduire la négation erronée de l’ancien IPS.',
300:'Origine de CC, sceau de Sorcéria et perte de mémoire. Quatre CC conservés, aucune Laura figée ; esprit projeté ailleurs, pas corps transporté inventé.',
445:'Pouf-pouf SFC sur le visage. La chanson Trois petits chats de la VF DS ne remplace pas ces phrases SFC. D9 répétés, trois B0 et quatre AF explicites conservés.',
752:'DF natif appelle011C (vide en français) seulement au pluriel ; Vous reste littéral. E0, et non DF, produit vous/vous tous. Huit tours du prêtre et tous les AF conservés.',
784:'B2 décrit le présent près du lit, B5 reste objet acquis natif. Deux D3 gardés. Aucun objet DS fixé ne remplace les variables.',
1177:'Quinze tours Sylvain/héros distingués. Tous les C9, y compris ceux du nom de locuteur, gardés dans l’ordre. Mélodie conforme DS, deux silences du héros non supprimés.',
1833:'Boss confirmé スラッジ DS0059:879. B2 n’est pas figé au nom Gus.',
1841:'Boss et D0 natif. Cinq tours gardés ; D0 n’est pas remplacé par le nom d’un monstre supposé.',
2304:'La rosée n’est pas nommée dans cette réplique SFC ; ne pas y importer le nom DS ni une instruction absente.',
3260:'サンディ SFC est メラニィ DS, Ella ; Johan confirmé dans le dialogue DS0006:490. Trois tours conservés.',
4745:'C4 conditionnel garde et Cie. Formulation nominale pour éviter suit/suivent figé ; le groupe suit Frank vers la salle du trône.',
5125:'ホルコッタ est Pierrebrute (DSb1005000:43), pas un nom supposé. Deux D3 conservés ; exigences et refus de massacre gardés.',
5588:'Titre seigneur Zénith conforme DS et anciens dialogues ; quatre légendes, pas quatre objets tous matériels ajoutés.',
5592:'クラウド城 est Zénithia (DS0079:34), pas une traduction littérale inventée du nom.',
5632:'Zénithia et seigneur Zénith confirmés ; cinq DA et quatre AF, esprit anonyme, sceau et château à rendre au monde des rêves.',
5652:'デュラン est Dragore (DSb1002000:227). D2 reste destinataire natif, pas le nom héroïque DS figé.',
5668:'テリー est littéral dans le SFC : Tommy littéral, et non CD ajouté. Deux CB natifs, deux B0 et AF gardés.',
5688:'インパス SFC est Coup d’oeil (DSb1003000:180). C0 puis B5 restent variables ; aucun objet ni porteur figé.',
5854:'Consigne SFC du bouton bleu conservée, pas le bouton DS. Mémorisation des paroles ; pas un test d’écriture réelle.',
5855:'Bouton vert SFC et bouton pratique ; ne pas importer touche DS.',
6576:'Formulation nominale devant D3/C4 pour ne pas figer un accord singulier/pluriel.',
6806:'カルベ est Monsieur Soren (DS0056:789) ; ne pas confondre avec la réplique de son épouse. CC reste variable.',
6850:'Six tours CA/CE, et C9/CB destinataires finaux, tous conservés. Métier de charpentier conformément au japonais.',
6882:'Sept tours du roi et d’Apnéa. C9 cité deux fois dans les rôles natifs ; jeune fille anonyme à la fin, pas de nom ajouté.',
6948:'Tulipe confirmée DS0006:394. Trois C0 et un D3, trois AF ; ajout à l’équipe non exécuté par le banc de rendu.',
}
# Ambiguous debug imagery is prepared separately, without insertion approval.
held={6019,6184,6185,6186,6193,6194,6195}
review=[];prepared=[]
for mid,plan in PLANS.items():
 refs=[]
 for word,key in lex.items():
  if word not in jp[mid]['text']:continue
  j=lookup[key];f=fi[key];refs.append(dict(scope='LEXIQUE_SEULEMENT',source_word=word,file=j['file'],id=j['id'],ja=j['text'],fr=f['text']))
 if mid in specific:
  name,ids=specific[mid]
  for i in ids:
   key=('data/MESS6/JA/'+name,i);j=lookup[key];refs.append(dict(scope='FRAGMENT_OU_FORMULATION_A_ADAPTER_AU_SFC',file=j['file'],id=j['id'],ja=j['text'],fr=fi[key]['text']))
 note=notes.get(mid,'Japonais SFC, variables et tours relus directement avec leur contexte. Lexique DS explicite lorsqu’il est établi ; pas d’équivalent DS complet déclaré. IPS secondaire relu sans reprendre ses lacunes ou décalages.')
 x=dict(id=mid,file='SFC_NATIVE_REVIEW',ids=[],status='RELU',compile_mode='NATIVE_PLAN_REVIEWED',sfc_jp=jp[mid]['text'],sfc_vf_secondaire=vf[mid]['text'],native_plan=plan,original_body=plan,adaptation_body=plan,adaptation_speaker='',adaptation_review=note,review=note,ds_references=refs,native_bindings={f'native_{t:02X}':t for t in jp[mid]['tokens'] if t<0x200 and t not in [0xad,0xaf,0xac,0xae]},sfc_context=[dict(id=i,text=jp[i]['text']) for i in range(max(0,mid-2),min(len(jp),mid+3))],prior_integrated_context=[dict(id=i,text=old[i]['text']) for i in range(mid-2,mid+3) if i in old])
 if mid in held:
  x.update(status='PREPARE_NON_INSERE',blocker='Fragment de confirmation DE à raccorder à son appel natif avant insertion.' if mid==6019 else 'Imagerie de débogage, drapeau/rosée/fusion : relire l’événement et sa fonction avant validation contextuelle. Traduction littérale seule non admise.');prepared.append(x)
 else:review.append(x)
save(O/'revue-lot-v050.json',review);save(O/'nouveaux-prepares-v050.json',prepared)
for name in ['init.py','prepare.py','build.py','verify.py','names.py','spells.py','native_helpers.py','native_plan.py','test_render.py','render_fixtures.py']:
 s=(B/name).read_text()
 if name not in ['names.py','spells.py','native_helpers.py','native_plan.py']:
  s=s.replace('v0.49','v0.50').replace('v0.48','v0.49').replace('v049','v050').replace('v48','v49')
 if name=='build.py':s=s.replace('len(rows)-6672','len(rows)-6729')
 if name=='verify.py':s=s.replace('len(checked)==57',f'len(checked)=={len(review)}')
 if name=='native_plan.py':s=s.replace('0xdf:9','0xdf:0')
 (O/name).write_text(s)
s=(D/'pass49.py').read_text().replace('v0.49','v0.50').replace('v0.48','v0.49').replace('v0.47','v0.48').replace('v049','v050').replace('v048','v049').replace('v47','v48')
(D/'pass50.py').write_text(s)
print(len(review),'reviewed;',len(prepared),'prepared without insertion')

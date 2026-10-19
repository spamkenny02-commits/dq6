"""Reviewed Montgivre follow-up; preserve every previous selection."""
from pathlib import Path
import json,re,shutil
P=Path(__file__).resolve().parent;B=P/'v0.24';O=P/'v0.25'
def read(p):return json.loads(p.read_text())
def save(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
O.mkdir(exist_ok=True)
for name in ['init.py','prepare.py','build.py','verify.py','names.py']:
    if (O/name).exists():continue
    s=(B/name).read_text().replace('v0.24','v0.25')
    if name in ['prepare.py','verify.py']:s=s.replace('v0.23','v0.24').replace('v23','v24')
    if name=='prepare.py':s=s.replace('correspondance_revue_v24','correspondance_revue_v25')
    if name=='build.py':s=s.replace('len(rows)-5128','len(rows)-5140')
    (O/name).write_text(s)
for p in B.glob('*.json'):
    if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','progression-')):continue
    if not (O/p.name).exists():shutil.copy2(p,O/p.name)
choices={571:('0070.p',[496,502]),584:('0070.p',[551,552,553,554]),591:('0070.p',[580,581,582]),592:('0072.p',[0,1,2]),597:('0072.p',[14]),603:('0072.p',[26,27,28,29,30]),605:('0072.p',[37,38,39,40,41,42]),607:('0072.p',[46,47,48,49,50,51]),616:('0072.p',[86,87]),623:('0072.p',list(range(108,116))),624:('0072.p',[116,117,118,119]),626:('0073.p',[5,6,7,8])}
notes={
571:'Narration partagee des habitants geles. DS 496 et 502 ont le meme japonais mais deux francais il/elle : variantes, pas deux paroles consecutives. Adaptation neutre cette personne pour le seul message SFC partage.',
584:'Premier entretien avec le vieillard avant degel : silence, pourquoi venir, tous geles sauf lui, ordre de partir. DS 551–554 entier ; son nom n’est pas encore revele.',
591:'Saul reproche la visite du sanctuaire apres avertissement : jeunesse imprudente, ne jamais revenir, eviter son sort. DS 580–582. Distinct de 579 deja integre en 590.',
592:'Voyageur expulse de l’auberge apres degel : fonte soudaine, aubergiste furieuse, expulsion malgre paiement. DS 0072:0–2. Balai de la localisation conserve ; aucun paiement reel ajoute.',
597:'Chien de Montgivre reveille : DS 14, entre enfant joyeux 12 et boisson 19. Replique courte ancree dans la scene, pas un aboiement quelconque.',
603:'Buveur se rappelle Saul, revelation de la dame des neiges, porte claquee et bourrasque, froid et amnesie puis boisson. DS 26–30 complet. Ne remplace pas la boisson SFC par le the de la sequence distincte 19–24.',
605:'Visiteur du sage Kad Abra : le croyait mort, voulait sa tombe, le trouve vivant et admire sa vitalite. DS 37–42 entier ; six idees et meme ordre.',
607:'Kad explique epee dans grotte nord, porte scellee, formule necessaire, sa connaissance de celle-ci et demande de l’entendre. DS 46–51 entier. Nord conforme aux deux japonais, pas nord-est de la VF secondaire. Indices de formule 610 exclus.',
616:'Eternuement puis constat de froid : DS 86–87 juste avant soupe refroidie 89. Meme paire que SFC, pas un eternuement isole.',
623:'Confession de Saul : pardon d’Angele, boisson avec ami, secret trahi malgre promesse, colere et village gele sauf lui, cinquante annees seul. DS 108–115 complet. VF secondaire omet le pardon initial, DS prioritaire.',
624:'Suite de Saul : erreurs de jeunesse, suivre sa voie pour grandir, sens de sa faute et doute apres cinquante ans. DS 116–119 ; ne reprend pas le faux recit d’aventurier de la VF secondaire.',
626:'Kad indique Colombourg au sud de l’ancienne abbaye des Vocations, ville louche et lignee de forgerons, information ancienne incertaine. DS 0073:5–8 avant cadeau du pendentif ; duplicata 13–16 identique. Terminaison AE native.'}
jp={r['id']:r for r in read(P/'clean-base/sfc-jp.json')};vf={r['id']:r for r in read(P/'clean-base/sfc-vf.json')}
ja={(r['file'].split('/')[-1],r['id']):r for r in read(P/'clean-base/ds-ja.json') if '/MESS6/' in r['file']}
fr={(r['file'].split('/')[-1],r['id']):r for r in read(P/'clean-base/ds-fr.json') if '/MESS6/' in r['file']}
assert not {r['id'] for r in read(B/'insertion-candidates.json')}&set(choices)
reviews=[]
for mid,(file,ids) in choices.items():
    r=dict(id=mid,file=file,ids=ids,sfc_jp=jp[mid]['text'],sfc_vf_secondaire=vf[mid]['text'],ds_jp=[ja[(file,i)]['text'] for i in ids],ds_fr=[fr[(file,i)]['text'] for i in ids],review=notes[mid],status='RELU')
    if mid==571:
        parts=[]
        for i in ids:
            m=re.fullmatch(r'@a([^@]*)@b(.*?)\n?@c0@',fr[(file,i)]['text'],re.S);assert m
            parts.append(m.group(2).strip())
        r.update(original_body=' '.join(parts),adaptation_body='Pas de réponse. Cette personne est gelée...',adaptation_review='DS 496/502 sont deux variantes de genre du meme message partage en SFC ; reprise neutre sans juxtaposer deux variantes ni deduire un genre absent.')
    reviews.append(r)
if (O/'revue-lot-v025.json').exists():assert read(O/'revue-lot-v025.json')==reviews
else:save('revue-lot-v025.json',reviews)
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
print('v0.25 reviewed input delta ready:',len(reviews),'messages')

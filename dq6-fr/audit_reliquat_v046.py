"""Read-only remaining-text inventory; word matches are NOT validations."""
from pathlib import Path
import json,re,collections,unicodedata
P=Path(__file__).resolve().parent;O=P/'v0.46'
read=lambda p:json.loads(p.read_text())
sources=read(P/'clean-base/sfc-jp.json');ja=read(P/'clean-base/ds-ja.json');fr={(r['file'].replace('/FR/','/JA/'),r['id']):r for r in read(P/'clean-base/ds-fr.json')}
done={r['id'] for r in read(O/'insertion-candidates.json')}
def key(text):
 text=re.sub(r'\[CODE D4\](?:\[CODE [A-F0-9]+\])*[^「]{0,80}「','',text)
 text=re.sub(r'^@a[^@]*@b','',text);text=re.sub(r'@c\d+@','',text);text=re.sub(r'^[^「]{0,30}「','',text)
 text=re.sub(r'%a\d{6}|\[CODE (?:B2|B5|BB|C0|C1|C3|C5|C7|C9|CA|CB|CC|CD|CE|CF|D0|D1|D2|D3|D8)\]','変数',text)
 text=re.sub(r'\[[^\]]*\]|%[A-Za-z][0-9]*|%[0-9]','',text)
 text=text.replace('㈡','').replace('㈢','')
 return ''.join(c for c in unicodedata.normalize('NFKC',text) if unicodedata.category(c)[0] in 'LN')
records=collections.defaultdict(list)
for r in ja:
 if '/MESS6/' not in r['file'] or (r['file'],r['id']) not in fr:continue
 if not re.fullmatch(r'@a[^@]*@b.*\n?@c0@',fr[r['file'],r['id']]['text'],re.S):continue
 records[r['file']].append(r)
index=collections.defaultdict(list)
for file,rs in records.items():
 for i in range(len(rs)):
  for n in range(1,7):
   chunk=rs[i:i+n]
   if len(chunk)!=n:break
   k=''.join(key(r['text']) for r in chunk)
   if 3<=len(k)<=500:index[k].append(dict(file=file.replace('/JA/','/FR/'),ids=[r['id'] for r in chunk]))
rows=[];codes=collections.Counter()
for s in sources:
 if s['id'] in done:continue
 controls=sorted({t for t in s['tokens'] if t<0x200});codes.update(controls)
 rows.append(dict(id=s['id'],status='A_TRADUIRE_NON_VALIDE',native_codes=[f'{t:02X}' for t in controls],word_only_proposals=index.get(key(s['text']),[])[:6]))
assert len(done)==6387 and len(rows)==570
report=dict(version='v0.46',integrated=len(done),remaining=len(rows),prepared_main=161,prepared_main_reviewed_fragments=11,prepared_main_drafts=150,method='Japanese words normalized; variables genericized only for discovery, speaker labels and layout ignored.',warning='PROPOSITIONS_NON_VALIDEES. Same words do not prove roles, scene, spelling, timing or French meaning. No entry in this report may be auto-inserted.',rows_with_word_only_proposals=sum(bool(r['word_only_proposals']) for r in rows),native_code_message_counts={f'{k:02X}':v for k,v in sorted(codes.items())},open_inherited_audits=[dict(ids=[322,323,1836,4095],status='INTEGRES_MAIS_SCENES_NATURELLES_NON_VERIFIEES'),dict(ids=[610,1135,2404,5341,5351],status='INDICES_ET_CHOIX_A_REVOIR_ENSEMBLE'),dict(source='v0.34/nouveaux-cas-differes.json',status='CONSERVER_LES_26_CAS_DIFFERES'),dict(scope='tables',status='ALPHABET_ACCENTUE_ET_FENETRES_NATIVES_OUVERTS')],rows=rows)
historical=read(P/'v0.34/nouveaux-cas-differes.json');historical_ids={r['id'] for r in historical}
report['historical_v034']=dict(examined_then=len(historical),resolved_ids=sorted(historical_ids&done),remaining_ids=sorted(historical_ids-done),remaining_count=len(historical_ids-done),resolution_references={'2368':'v0.41/revue-lot-v041.json: inscription relue contre les deux japonais','6265':'v0.41/revue-lot-v041.json: remerciement relu, pas le poème ajouté en DS FR'})
report['open_inherited_audits'][2]['status']='CONSERVER_LES_CAS_NON_RESOLUS, voir historical_v034'
for i in [5761,5778,5816,5818,5844,5851]:report['historical_v034']['resolution_references'][str(i)]='v0.46/revue-lot-v045.json: sens SFC et différences DS/VF relus.'
for i in [6338,6465]:report['historical_v034']['resolution_references'][str(i)]='v0.46/revue-lot-v046.json: question sur l’objet ou contexte funéraire SFC, pas proposition DS erronée.'
(O/'qa-reliquat.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(len(rows),'untranslated;',report['rows_with_word_only_proposals'],'word-only proposals, no validation;',report['historical_v034']['remaining_count'],'historical cases remain')

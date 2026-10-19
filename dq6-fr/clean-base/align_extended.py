from pathlib import Path
import json,re,unicodedata,collections
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
P=Path(__file__).parent
src=json.loads((P/'sfc-jp.json').read_text());ds=json.loads((P/'ds-ja.json').read_text());fr=json.loads((P/'ds-fr.json').read_text());fi={(r['file'].replace('/FR/','/JA/'),r['id']):r for r in fr}
def norm(s):
 s=re.sub(r'\[[^\]]*\]','',s);s=re.sub(r'%[A-Za-z][0-9]*|%0','',s);s=re.sub(r'@[a-zA-Z][0-9]*','',s)
 return ''.join(c for c in unicodedata.normalize('NFKC',s) if unicodedata.category(c)[0] in 'LN')
records=[]
for x in ds:
 if '/MESS6/' not in x['file']:continue
 f=fi.get((x['file'],x['id']))
 if not f:continue
 n=norm(x['text'])
 if len(n)<5:continue
 records.append(dict(file=x['file'],id=x['id'],norm=n,jp=x['text'],fr=f['text']))
# Merge identical Japanese + French records to avoid duplicate matches hiding the confidence margin.
bytext=collections.defaultdict(list)
for i,r in enumerate(records):bytext[r['norm']].append(i)
unique=list(bytext)
vec=TfidfVectorizer(analyzer='char',ngram_range=(2,3),dtype=np.float32,sublinear_tf=True)
D=vec.fit_transform(unique);Q=vec.transform([norm(r['text']) for r in src]);results=[]
for start in range(0,len(src),128):
 scores=(Q[start:start+128]@D.T).toarray()
 for j,row in enumerate(scores):
  r=src[start+j];n=norm(r['text']);top=np.argsort(row)[-5:][::-1];cs=[]
  for k in top:
   if row[k]<=0:continue
   matches=[records[i] for i in bytext[unique[k]]];cs.append(dict(score=round(float(row[k]),5),exact=n==unique[k],matches=matches))
  results.append(dict(id=r['id'],sfc_jp=r['text'],norm_length=len(n),candidates=cs))
(P/'alignement-jp-top5.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
stats=collections.Counter()
for r in results:
 if not r['candidates']:continue
 c=r['candidates'][0];margin=c['score']-(r['candidates'][1]['score'] if len(r['candidates'])>1 else 0)
 if c['exact'] and r['norm_length']>=10:stats['exact']+=1
 elif c['score']>=.9 and margin>=.08 and r['norm_length']>=20:stats['fuzzy_high_review_required']+=1
 elif c['score']>=.75:stats['fuzzy_075_review_required']+=1
 else:stats['low_confidence']+=1
print(dict(stats))
for mid in [100,101,102,103,104,1000,2000,4000,6950]:
 r=results[mid];c=r['candidates'][0];print(mid,c['score'],c['matches'][0]['file'],c['matches'][0]['id'],r['sfc_jp'][:45],c['matches'][0]['jp'][:45])

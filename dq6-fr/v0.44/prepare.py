"""Extend translation using exact Japanese bodies and consecutive DS messages.
No fuzzy match is inserted. Preserve v0.43 selections as the regression baseline.
"""
from pathlib import Path
import json,re,unicodedata,collections,struct
P=Path(__file__).resolve().parents[1];O=P/'v0.44'
def read(p):return json.loads(p.read_text())
def save(name,v):(O/name).write_text(json.dumps(v,ensure_ascii=False,indent=2))
src=read(P/'clean-base/sfc-jp.json');vf=read(P/'clean-base/sfc-vf.json');ja=read(P/'clean-base/ds-ja.json');fr=read(P/'clean-base/ds-fr.json');previous=read(P/'v0.43/insertion-candidates.json');oldids={r['id'] for r in previous}
fi={(r['file'].replace('/FR/','/JA/'),r['id']):r for r in fr}
ACTORS={'%a000090':0xc9,'%a002000':0xca,'%a002010':0xcb,'%a002020':0xcc,'%a002040':0xcd,'%a002030':0xce,'%a002050':0xcf,'%a002070':0xd0,'%a002360':0xd1}
STYLE={0xd4,0xd9,0xda,0xdb,0xde};TRAIL={0xad,0xaf,0xb0,0xd5,0xd6};VARS=set(range(0xc9,0xd4))|{0xc0,0xc1,0xbb,0xb3,0xb2,0xc5,0xb5};ALLOWED=STYLE|VARS|TRAIL|{0xac,0xae}
marker=lambda code:chr(0xe000+code)
rom=(P/'clean-base/vf-base-headered.sfc').read_bytes()[512:]
mapping={int(k,16):v for k,v in read(P/'v0.3/charset.json').items()};mapping.update({0x248:'(',0x249:')',0x24a:'♥',0x24b:'♪'})
rev={v:k for k,v in mapping.items()};rev[' ']=0x200
for code in VARS:rev[marker(code)]=code
for byte,s in [(2,'0123456789'),(0x10,'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),(0x42,'abcdefghijklmnopqrstuvwxyz')]:
 for i,c in enumerate(s):rev[c]=struct.unpack_from('<H',rom,0x11100+2*(byte+i))[0]
rev.update({'.':0x242,',':0x243,'!':0x241,'?':0x228,"'":0x250,'-':0x236})
PUNCT=str.maketrans({'и':'n','я':'r','И':'N','Я':'R','Ⓟ':'♥','Ⓠ':'♪','Ⓡ':'♪','ⓚ':'-','ⓛ':'-','ⓠ':'!','ⓡ':'?','ⓢ':',','ⓥ':"'",'ⓦ':"'",'ⓐ':'','ⓣ':',','’':"'",'‘':"'",'…':'...','œ':'oe','Œ':'OE','À':'à','Â':'â','Ê':'ê','Î':'î','Ù':'ù','Û':'û','Ç':'ç','«':"'",'»':"'",'–':'-','—':'-','\u00a0':' ','\u202f':' '})

def parse_ds(text):
 m=re.fullmatch(r'@a([^@]*)@b(.*?)\n?@c0@',text,re.S)
 if not m:raise ValueError('commandes_DS')
 speaker,body=m.groups()
 if re.search(r'\bdummy\b',body,re.I):raise ValueError('texte_DS_dummy')
 if body.startswith('*ⓢ '):body=body[3:]
 return speaker,body.strip()

DS_LABELS={m.group(1).strip() for j in ja for m in [re.match(r'^@a[^@]*@b([^「]{0,24})「',j['text'])] if m}

ORTHOGRAPHY=read(O/'variantes-orthographiques.json')

LITERAL_ACTORS={'ハッサン':0xca,'ミレーユ':0xcb,'バーバラ':0xcc,'テリー':0xcd,'チャモロ':0xce,'アモス':0xcf,'ターニア':0xd1}
SPEAKER_ALIASES={'サンディ':'メラニィ','テリー':'%a002040'}
SPECIFIC_SPEAKERS={6750:('司会','＊'),6748:('司会','＊'),6751:('司会','＊'),1111:('弟','＊'),6749:('司会','＊'),5252:('神父','＊'),6804:('カルベ','カルベ夫人'),373:('カルベ','カルベ夫人'),374:('カルベ','カルベ夫人'),6807:('カルベ','カルベ夫人')}
SPECIFIC_SPEAKERS.update({6646:('司会','＊'),6647:('司会','＊')})
SPECIFIC_SPEAKERS.update({6646:('司会','＊'),6647:('司会','＊')})
def speaker_key(label,mid):
 if mid in SPECIFIC_SPEAKERS and label==SPECIFIC_SPEAKERS[mid][0]:label=SPECIFIC_SPEAKERS[mid][1]
 return SPEAKER_ALIASES.get(label,label)

def jbody(text):
 is_ds=text.startswith('@a')
 # DS layout/pacing symbols are excluded before compatibility normalization.
 text=text.replace('㈡','').replace('㈢','')
 for symbol in ['Ⓟ','Ⓠ','Ⓡ','ⓚ','ⓛ']:text=text.replace(symbol,'')
 # Keep words, erase the speaker label before opening quote at the start and after D4.
 text=re.sub(r'\[CODE D4\](?:\[CODE [A-F0-9]+\])*[^「]{0,24}「','',text)
 text=re.sub(r'^@a[^@]*@b','',text);text=re.sub(r'@c\d+@','',text)
 m=re.match(r'^([^「]{0,24})「',text)
 if m and (is_ds or m.group(1).strip() in DS_LABELS):text=text[m.end():]
 # Keep character references in the matching key: equal words with a different
 # named character are not an exact match.
 for name,code in LITERAL_ACTORS.items():text=text.replace(name,'VAR'+f'{code:02X}'+'REF')
 for tag,code in ACTORS.items():
  sentinel='VAR'+f'{code:02X}'+'REF'
  text=text.replace(tag,sentinel).replace('[CODE '+f'{code:02X}'+']',sentinel)
 for tag in ['%a000120','%a000140']:text=text.replace(tag,'VARDYNAMICREF')
 for code in [0xc0,0xd2,0xd3]:text=text.replace('[CODE '+f'{code:02X}'+']','VARDYNAMICREF')
 text=re.sub(r'\[[^\]]*\]','',text);text=re.sub(r'%[A-Za-z][0-9]*|%[0-9]','',text)
 text=''.join(c for c in unicodedata.normalize('NFKC',text) if unicodedata.category(c)[0] in 'LN')
 for before,after in ORTHOGRAPHY:text=text.replace(before,after)
 return text

def spoken_len(key):return len(re.sub(r'VAR(?:C[9A-F]|D[0-3])REF|VARDYNAMICREF','',key))

records=collections.defaultdict(list);index=collections.defaultdict(list)
for j in ja:
 f=fi.get((j['file'],j['id']))
 if f and '/MESS6/' in j['file']:
  try:sp,body=parse_ds(f['text'])
  except ValueError:continue
  records[j['file']].append(dict(index=j['index'],file=f['file'],id=f['id'],ja=j['text'],speaker=sp,body=body,norm=jbody(j['text'])))
# Adjacent entries are considered only within the same original DS file.
for file,rs in records.items():
 for i in range(len(rs)):
  for n in range(1,9):
   chunk=rs[i:i+n]
   if len(chunk)!=n or any(chunk[k+1]['index']!=chunk[k]['index']+1 for k in range(n-1)) or (n>1 and any(not r['norm'] for r in chunk)):continue
   key=''.join(r['norm'] for r in chunk)
   if spoken_len(key)<(4 if n==1 else 10) or len(key)>1000:continue
   speakers={r['speaker'] for r in chunk if r['speaker']}
   if len(speakers)>1:continue
   index[key].append(dict(file=chunk[0]['file'],ids=[r['id'] for r in chunk],speaker=next(iter(speakers),''),body=' '.join(r['body'] for r in chunk),ja=[r['ja'] for r in chunk]))

manual={
 110:('0014.p',[702,703]),111:('0014.p',[705,706]),112:('0014.p',[714]),113:('0014.p',[716]),114:('0014.p',[717]),115:('0014.p',[718]),
 116:('0014.p',[722,723]),117:('0014.p',[724]),118:('0014.p',[725]),119:('0014.p',[726]),120:('0014.p',[727]),121:('0014.p',[736,737]),
 122:('0014.p',[728]),123:('0014.p',[732]),124:('0014.p',[739]),125:('0014.p',[740]),126:('0014.p',[742]),127:('0014.p',[743]),
 128:('0000.p',[29,30]),129:('0000.p',[32,33,34]),130:('0014.p',[753]),131:('0014.p',[755,756]),132:('0014.p',[758,759,760,761])}

manual.update({int(r['id']):(r['file'],r['ids']) for r in read(O/'correspondances-revues.json')})

BINDINGS=read(O/'liaisons-variables-natives.json')
ADAPTATIONS={r['id']:r for r in read(O/'adaptations-francaises.json')}
manual.update({mid:(r['file'],r['ids']) for mid,r in ADAPTATIONS.items()})

def manual_candidate(file,ids):
 rs=records['data/MESS6/JA/'+file];chunk=[next(r for r in rs if r['id']==i) for i in ids]
 return dict(file=chunk[0]['file'],ids=ids,speaker=chunk[0]['speaker'],body=' '.join(r['body'] for r in chunk),ja=[r['ja'] for r in chunk])

def convert(c,s):
 ts=s['tokens'];controls=[t for t in ts if t<0x200]
 if any(t not in ALLOWED for t in controls):raise ValueError('commandes_SFC_non_adaptees')
 if 0xb2 in controls and 0xb2 not in BINDINGS.get(str(s['id']),{}).values():raise ValueError('B2_non_revu')
 if 0xc5 in controls and 0xc5 not in BINDINGS.get(str(s['id']),{}).values():raise ValueError('C5_non_revu')
 # D5, B0 and D6 are passed through only in the existing control suffix.
 last_data=max((i for i,t in enumerate(ts[:-1]) if t>=0x200 or t in VARS),default=-1)
 if any(t in TRAIL-{0xad,0xaf} for t in ts[:last_data+1]):raise ValueError('commandes_SFC_internes_non_adaptees')
 labels=re.findall(r'\[CODE D4\]([^「]{0,80})「',s['text'])
 labels_clean=[re.sub(r'\[CODE (?:D9|DA|DB|DE)\]','',x).strip() for x in labels]
 if len(set(labels_clean))>1:raise ValueError('plusieurs_locuteurs_SFC')
 prefix=[]
 for t in ts:
  if t not in STYLE:break
  prefix.append(t)
 if 0xda in ts[len(prefix):]:raise ValueError('commande_DA_interne_non_adaptee')
 actor=None
 if labels_clean:
  m=re.fullmatch(r'\[CODE ([A-F0-9]+)\]',labels_clean[0])
  if m and int(m.group(1),16) in VARS:actor=int(m.group(1),16)
 if s['id']==2300:actor=None # Anonymous opening before her name is spoken.
 speaker={6750:'Présentateur',6748:'Présentateur',6751:'Présentateur',1111:'Le frère',6749:'Présentateur',5252:'Prêtre'}.get(s['id'],c['speaker']);body=c['body']
 if s['id'] in ADAPTATIONS:
  change=ADAPTATIONS[s['id']]
  assert body==change['original_body'],s['id']
  body=change['body']
  if 'speaker' in change:speaker=change['speaker']
  if 'speaker' in change:speaker=change['speaker']
 # Adapt DS paragraph boundaries to SFC pages; omit the inline pacing marker.
 body=re.sub(r'(㈡\s*)\*ⓢ\s*',r'\1',body)
 body=body.replace('㈡',' \ue100 ').replace('㈢',' ')
 # These early choices address one hero; retain the official singular branch.
 if s['id']==124:body=body.replace('%H0860%XTu as%YVous avez%Z','Tu as')
 if s['id']==126:body=body.replace('%H0860%Xtu aies%Yvous ayez%Z','tu aies')
 if body.startswith('%3') and body.endswith('%4'):body=body[2:-2]
 # Display-only capitalization is unnecessary for the SNES name controls.
 body=re.sub(r'%0(?=%a\d{6})','',body);speaker=re.sub(r'%0(?=%a\d{6})','',speaker)
 variable_map=ACTORS.copy();present={t for t in ts if t in VARS}
 for tag,code in BINDINGS.get(str(s['id']),{}).items():
  assert code in present,(s['id'],tag,code)
  variable_map[tag]=code
 context_tags={tag for tag in ['%a000120','%a000140'] if tag in body or tag in speaker}
 if 0xc0 in present and (len(context_tags)>1 or present&{0xd2,0xd3}) and not (present&{0xc0,0xd2,0xd3})<=set(BINDINGS.get(str(s['id']),{}).values()):raise ValueError('variables_contextuelles_multiples')
 for tag in ['%a000120','%a000140']:
  if 0xc0 in present:variable_map[tag]=0xc0
  elif 0xd3 in present and 0xd2 not in present:variable_map[tag]=0xd3
  elif tag=='%a000120' and 0xd2 in present and 0xd3 not in present:variable_map[tag]=0xd2
 if 0xc9 not in present and 0xd3 in present:variable_map['%a000090']=0xd3
 for tag,code in variable_map.items():body=body.replace(tag,marker(code));speaker=speaker.replace(tag,marker(code))
 if '%' in body or '@' in body:raise ValueError('variables_ou_commandes_DS')
 if actor is not None:speaker=marker(actor)
 elif not labels_clean:speaker='' # Do not reveal a DS speaker omitted in the SFC scene.
 if '%' in speaker or '@' in speaker:raise ValueError('nom_DS_non_adapte')
 # Consolidate repeated labels only when the original names the same speaker throughout.
 text=(speaker+'. ' if speaker else '')+body
 text=' '.join(text.translate(PUNCT).split())
 for ch in text:
  if ch not in rev and ch!='\ue100':raise ValueError('glyphe_non_identifie_'+f'{ord(ch):04x}')
 lines=[]
 paragraphs=text.split('\ue100')
 for part_no,part in enumerate(paragraphs):
  line='';cols=0
  def word_width(word):return sum(24 if ch==marker(0xb5) else 22 if ch==marker(0xb2) else 8 if ch in [marker(0xbb),marker(0xc5)] else 14 if ch in map(marker,VARS) else 1 for ch in word)
  words=[]
  for word in part.split():
   if word_width(word)>24 and '-' in word:
    pieces=word.split('-')
    words.extend((piece+('-' if k<len(pieces)-1 else ''),k>0) for k,piece in enumerate(pieces))
   else:words.append((word,False))
  for word,linked in words:
   n=word_width(word)
   if n>24:raise ValueError('mot_trop_long')
   limit=22 if not lines else 24
   gap=1 if line and not linked else 0
   if line and cols+gap+n>limit:lines.append(line);line=word;cols=n
   else:line+=(' ' if gap else '')+word;cols+=gap+n
  if line:lines.append(line)
  if part_no<len(paragraphs)-1:
   while len(lines)%3:lines.append('')
 text=' '.join(text.replace('\ue100',' ').split())
 tokens=prefix[:]
 for i,line in enumerate(lines):
  if i:
   if i%3==0:tokens.append(0xaf)
   tokens.append(0xad)
  tokens.extend(rev[ch] for ch in line)
 tail=[]
 for t in reversed(ts[:-1]):
  if t not in TRAIL:break
  tail.append(t)
 tokens+=list(reversed(tail))+[ts[-1]]
 for control in [0xbb,0xc1,0xb2,0xc5,0xb5]:
  if ts.count(control)!=tokens.count(control):raise ValueError('variable_native_non_reliee_'+hex(control))
 return dict(tokens=tokens,text=text,lines=lines,source_prefix=prefix,source_actor=actor,source_terminator=ts[-1])

MULTI=read(O/'dialogues-multilocuteurs.json')

def convert_multi(source,plan):
 ts=source['tokens'];starts=[i for i,t in enumerate(ts) if t==0xd4]
 texts=re.split(r'(?=\[CODE D4\])',source['text']);texts=[t for t in texts if t]
 assert starts[0]==0 and len(starts)==len(texts)==len(plan['turns'])
 starts.append(len(ts));parts=[];allids=[]
 for k,ids in enumerate(plan['turns']):
  fragment=ts[starts[k]:starts[k+1]]
  if k<len(plan['turns'])-1:
   assert fragment[-2:]==[0xaf,0xad]
   fragment=fragment+[0xae]
  c=manual_candidate(plan['file'],ids)
  overrides=plan.get('overrides',{})
  if str(k) in overrides:
   override=overrides[str(k)];assert c['body']==override['expected'];c['body']=override['body']
  sub=dict(source,tokens=fragment,text=texts[k])
  assert jbody(sub['text'])==''.join(jbody(t) for t in c['ja']),(source['id'],k,'Japanese turn mismatch')
  result=convert(c,sub);result['ds_ids']=ids;parts.append(result);allids+=ids
 tokens=[]
 for k,part in enumerate(parts):tokens+=part['tokens'] if k==len(parts)-1 else part['tokens'][:-1]
 return dict(id=source['id'],tokens=tokens,text=' '.join(r['text'] for r in parts),lines=[line for r in parts for line in r['lines']],parts=parts,ds_file='data/MESS6/FR/'+plan['file'],ds_id=allids,method='locuteurs_et_repliques_alignes_manuellement',source_japanese=source['text'],sfc_previous=vf[source['id']]['text'],source_terminator=ts[-1])

REVIEWED_NEW_IDS={r['id'] for r in read(O/'revue-lot-v044.json')}
baseline_by_id={r['id']:r for r in previous}
def anchor_ids(mid,c):
 result=[]
 for offset in [-4,-3,-2,-1,1,2,3,4]:
  a=baseline_by_id.get(mid+offset)
  if not a or a['ds_file']!=c['file']:continue
  old=a['ds_id'] if isinstance(a['ds_id'],list) else [a['ds_id']]
  if min(abs(i-j) for i in c['ids'] for j in old)<=16:result.append(a['id'])
 return result
accepted={r['id']:r.copy() for r in previous};review=[];new=[]
# All prior selections are retained byte-for-byte.
revisit=set()
for s in src:
 mid=s['id']
 if mid not in oldids and mid not in REVIEWED_NEW_IDS:
  review.append(dict(id=mid,reason='hors_lot_revu',sfc_jp=s['text']));continue
 if mid in oldids and mid not in revisit:continue
 if str(mid) in MULTI:
  accepted[mid]=convert_multi(s,MULTI[str(mid)]);new.append(mid);continue
 key=jbody(s['text']);cs=index.get(key,[]) if spoken_len(key)>=4 else []
 method='japonais_variantes_orthographiques_exact'
 if mid in manual:cs=[manual_candidate(*manual[mid])];method='correspondance_revue_v44'
 if not cs:review.append(dict(id=mid,reason='correspondance_non_etablie',sfc_jp=s['text']));continue
 if mid not in manual and spoken_len(key)<10:
  anchored=[dict(c,context_anchors=anchor_ids(mid,c)) for c in cs if anchor_ids(mid,c)]
  if not anchored:review.append(dict(id=mid,reason='replique_courte_sans_contexte_confirme',candidates=cs,sfc_jp=s['text']));continue
  cs=anchored

 # For a literal named speaker, require the same Japanese label, not just identical words.
 labels=re.findall(r'\[CODE D4\]([^「]{0,80})「',s['text'])
 label=re.sub(r'\[CODE (?:D9|DA|DB|DE)\]','',labels[0]).strip() if labels else ''
 if label and '[CODE' not in label:
  same=[]
  for c in cs:
   m=re.match(r'^@a[^@]*@b([^「]{0,24})「',c['ja'][{3256:1,1203:2,5036:2,5040:1}.get(mid,0)])
   if m and speaker_key(m.group(1).strip(),mid)==speaker_key(label,mid):same.append(c)
  if same:cs=same
  else:review.append(dict(id=mid,reason='nom_locuteur_non_aligne',sfc_jp=s['text'],candidates=cs));continue
 # Prefer a direct match over a longer sequence containing equivalent punctuation.
 min_parts=min(len(c['ids']) for c in cs);cs=[c for c in cs if len(c['ids'])==min_parts]
 # French bodies must agree. Speaker names are reconstructed from the SFC label.
 bodies={c['body'] for c in cs}
 if len(bodies)>1:review.append(dict(id=mid,reason='plusieurs_traductions_DS',candidates=cs,sfc_jp=s['text']));continue
 # Prefer the shortest exact sequence, then stable path/id order.
 c=min(cs,key=lambda c:(len(c['ids']),c['file'],c['ids']))
 try:r=convert(c,s)
 except ValueError as e:review.append(dict(id=mid,reason=str(e),ds=c,sfc_jp=s['text']));continue
 r.update(id=mid,ds_file=c['file'],ds_id=c['ids'],method=method,source_japanese=s['text'],sfc_previous=vf[mid]['text'])
 if 'context_anchors' in c:r['context_anchors']=c['context_anchors'];r['method']='japonais_court_exact_et_contexte_voisin'
 accepted[mid]=r
 if mid not in oldids:new.append(mid)
rows=[accepted[i] for i in sorted(accepted)]
save('insertion-candidates-all.json',rows);save('a-revoir.json',review);save('nouveaux-messages.json',[r for r in rows if r['id'] in new]);save('charset.json',{f'{k:04X}':v for k,v in mapping.items()})
summary=dict(previous=len(previous),prepared=len(rows),new_prepared=len(new),remaining_unmapped_or_unadapted=len(review),reasons=dict(collections.Counter(r['reason'] for r in review)),revised_existing_ids=sorted(revisit))
save('couverture-preparation.json',summary);print(json.dumps(summary,indent=2))

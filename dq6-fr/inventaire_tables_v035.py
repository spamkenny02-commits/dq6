"""Reproducible conservative inventory of the separate runtime name pool.
Run audit_tables.py VERSION first. No ROM or translation is inserted here.
"""
from pathlib import Path
import argparse,json,re,collections,hashlib
P=Path(__file__).resolve().parent;a=argparse.ArgumentParser();a.add_argument('version');v=a.parse_args().version;O=P/v
r=json.loads((O/'audit-noms-menus.json').read_text());by=collections.defaultdict(list)
for x in r:by[x['current_position']].append(x)
# Ranges are physical entry positions, not runtime SIDs; aliases are not counted twice.
regions=[('grille_noms_et_menus',0,415),('lieux',416,543),('monstres_et_personnages',544,831),('menus_casino_titres_et_rangs',832,1087),('sorts_et_actions',1088,1279),('fragments_descriptions',1280,1631),('objets',1632,1823),('vocations_noms_et_reserves',1824,2047)]
confirmed={156,231,233,781,1845,1846,1847,1848,1849}
version_key=lambda value:tuple(map(int,value.lstrip('v').split('.')))
for review_path in P.glob('v*/revue-lieux-v*.json'):
 if version_key(review_path.parent.name)<=version_key(v):confirmed.update(x['position'] for x in json.loads(review_path.read_text()))
for review_path in P.glob('v*/revue-noms-v*.json'):
 if version_key(review_path.parent.name)<=version_key(v):confirmed.update(x['position'] for x in json.loads(review_path.read_text()))
out=[]
for pos,xs in sorted(by.items()):
 x=xs[0];text=x['current_text'];n=lambda s:re.sub(r'\s+',' ',s.replace('|',' ')).strip()
 exact=any(n(text)==n(c['fr']) for y in xs for c in y['ds_candidates'])
 if pos==156:status='CREDIT_RETIRE_CONFORME'
 elif pos in confirmed:status='FR_CONFIRME_PROJET'
 elif exact and text:status='FR_DS_IDENTIQUE_A_VERIFIER_EN_CONTEXTE'
 elif not text:status='VIDE_A_QUALIFIER'
 elif re.fullmatch(r'(?:M|\*)[0-9A-F]{2,4}',text):status='IDENTIFIANT_NON_TRADUIT'
 elif re.search('[\u3040-\u30ff\u4e00-\u9fff]',text):status='JAPONAIS_DETECTE'
 else:status='AUTRE_TEXTE_A_REVOIR'
 out.append(dict(position=pos,sids=[y['sid'] for y in xs],jp=x['jp'],current=text,status=status,unique_ds_french=any(y['unique_french'] for y in xs),unknown_glyphs=bool(re.search(r'<[0-9A-F]{2}>',text)),region=next(t for t,lo,hi in regions if lo<=pos<=hi)))
summary=dict(version=v,sids=len(r),reachable_entries=len(out),aliases=len(r)-len(out),counts=dict(collections.Counter(x['status'] for x in out)),by_region={t:dict(entries=sum(x['region']==t for x in out),statuses=dict(collections.Counter(x['status'] for x in out if x['region']==t))) for t,_,_ in regions},exact_ds_candidates=sum(x['unique_ds_french'] for x in out),unmapped_glyph_entries=sum(x['unknown_glyphs'] for x in out),limits=['La catégorie AUTRE ne signifie pas anglais : elle inclut du français hérité non relu, des noms et des labels internes. Aucune détection automatique ne prouve la langue ou la correction.', 'VIDE ne signifie pas manquant : certaines réserves sont intentionnelles.', 'Les 906 rapprochements exacts ne sont pas 906 traductions validées.', 'Les descriptions sont des fragments composés au runtime ; les traduire avec leur composition, pas isolément.', 'Caps documentés : actions 9, descriptions 12, menus 18, lieux 20 caractères par ligne. Les fenêtres réelles et les sauts natifs doivent être testés.', 'Pointeurs 157 groupes de 16, 2512 SIDs, 2048 entrées ; préserver les alias et le dictionnaire binaire.'],pool={'start':'0x3b8703','end':'0x3bc712','bytes':0x3bc712-0x3b8703},inserted_this_audit=0)
(O/'inventaire-tables.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
for t,_,_ in regions:(O/('inventaire-'+t+'.json')).write_text(json.dumps([x for x in out if x['region']==t],ensure_ascii=False,indent=2))
# French place labels reviewed against the exact Japanese MENULIST6 entries.
places=[]
for pos,xs in sorted(by.items()):
 x=xs[0]
 if 416<=pos<=543 and x['unique_french'] and pos not in confirmed:
  cs=x['ds_candidates'];places.append(dict(sid=x['sid'],position=pos,sfc_jp=x['jp'],current=x['current_text'],ds_sources=cs,french=cs[0]['fr'],status='PREPARE_NON_INSERE',review='Nom de lieu JP identique à la liste DS, libellé officiel FR relu ; aucun rapprochement flou.',remaining_checks='Encodage accentué, largeur réelle de la fenêtre, alias, repacking et rendu du nom dans son écran.'))
(O/'lieux-prepares-non-inseres.json').write_text(json.dumps(places,ensure_ascii=False,indent=2));summary['places_prepared_not_inserted']=len(places);(O/'inventaire-tables.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False,indent=2))
# Complete pointer/storage and conservative width diagnostics from the rebuilt ROM.
import importlib.util
spec=importlib.util.spec_from_file_location('name_table_inventory',P/'upstream/refill/tools/nametable.py');nt=importlib.util.module_from_spec(spec);spec.loader.exec_module(nt)
t=nt.Table(O/'result.sfc');end=nt.NT_BASE+sum(len(x)+1 for x in t.entries[:t.reachable])
summary['counts'].setdefault('JAPONAIS_DETECTE',0)
summary['pool'].update(reachable_bytes=end-nt.NT_BASE,tail_bytes=nt.NT_END-end,tail_is_all_ff=all(b==255 for b in t.rom[end:nt.NT_END]),note='Ne pas considérer le tail comme libre sans l’auditer ; le repacker actuel préserve ce tail depuis l’IPS et refuse le débordement.')
summary['width_audit']={}
for name,lo,hi,limit in [('actions',1088,1279,9),('descriptions',1280,1631,12),('menus',192,319,18),('lieux',416,543,20)]:
 texts=[(i,t.at(i)) for i in range(lo,hi+1)];plain=[(i,x) for i,x in texts if not re.search(r'<[0-9A-F]{2}>',x)]
 too=[dict(position=i,text=x,longest=max(map(len,x.split('|')))) for i,x in plain if max(map(len,x.split('|')))>limit]
 summary['width_audit'][name]=dict(reference_width=limit,entries_checked=len(plain),unknown_glyph_entries_skipped=len(texts)-len(plain),exceeding_reference=len(too),rows=too,limit='Seuil observé dans la documentation du projet anglais, pas preuve des dimensions réelles de chaque fenêtre.')
(O/'inventaire-tables.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))

from pathlib import Path
import json,re,importlib.util
O=Path('dq6-fr/v0.72');assert not (O/'manifest.json').exists(),'Version finale déjà sauvegardée : utiliser ses scripts prepare/build/verify, pas le générateur préparatoire.';P=Path('dq6-fr/v0.71');O.mkdir(exist_ok=True)
sp=importlib.util.spec_from_file_location('b71',P/'common.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
for p in P.glob('*.py'):
 s=p.read_text().replace('v0.71','ZZCURRENTZZ').replace('v0.70','v0.71').replace('ZZCURRENTZZ','v0.72').replace('v071','v072').replace('parent71','parent72').replace('plans71','plans72');(O/p.name).write_text(s)
intents=json.loads(Path('preparations/table-finale-v072/intentions.json').read_text());chosen={x['position']:x for x in intents['rows']};corrections={1234,1635,1826,1833,1835,1838,1928};unchanged={1836,1837,1850};previous=set(old.PREVIOUS_CONFIRMED)|set(old.PLANS)|set(old.UNCHANGED)
jp=Path('../upload/Dragon Quest VI - Maboroshi no Daichi (Japan)(2).sfc').read_bytes();bps=old.module('base72bps',Path('dq6-fr/upstream/refill/patchRM.py'));base=bytes(bps.apply_bps(jp,Path('patches/DQVI-FR-DS-v0.71-BASE-JP-PARTIEL.bps').read_bytes()));tab=old.LogicalTable(base);glyphs=old.struct.unpack_from('<256H',jp,0x11100);jt={int(k,16):v for l in Path('dq6-fr/upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines() if '=' in l for k,v in [l.split('=',1)] if len(k)<=4}
ja=json.loads(Path('dq6-fr/clean-base/ds-ja.json').read_text());fr={(x['file'].replace('/FR/','/JA/'),x['id']):x for x in json.loads(Path('dq6-fr/clean-base/ds-fr.json').read_text())};lookup={}
for j in ja:
 if '/MENULIST6/JA/' in j['file'] and old.field(j['text']):lookup.setdefault(old.field(j['text']),[]).append(j)
def french(s):
 f=old.field(s);return f if f and not re.search('[\u3040-\u30ff\u4e00-\u9fff]',f) else None
plans={};prep={};sidmap={}
for pos in range(1200,2048):
 sids=[sid for sid in range(2512) if tab.position(sid)==pos];sid=sids[0];a=old.POOL+int.from_bytes(jp[0x165e7+3*(sid>>4):0x165ea+3*(sid>>4)],'little')
 for _ in range(sid&15):a=jp.index(0xac,a)+1
 src=''.join(jt.get(glyphs[b],'<%04X>'%glyphs[b]) for b in jp[a:jp.index(0xac,a)]) if pos<2042 else '[SOURCE_JP_OPAQUE_APRES_SID_09C9]'
 refs=[(j,fr[(j['file'],j['id'])]) for j in lookup.get(src,[]) if (j['file'],j['id']) in fr and french(fr[(j['file'],j['id'])]['text'])];vals={french(f['text']) for j,f in refs}
 if pos in chosen:
  c=chosen[pos];assert src==c['sfc_jp'],(pos,src,c['sfc_jp']);matches=[(j,f) for j,f in refs if french(f['text'])==c['french']];assert matches,pos;j,f=matches[0];plans[pos]=(c['french'],j['file'].split('b100')[1].split('.')[0],j['id'],c['review']+' SourceJP exacte etfrançaisDS complet ; largeur non augmentée,aucune commande nouvelle. Contexte naturel àvérifier.');sidmap[pos]=sids
 elif pos not in previous and pos not in unchanged and not 1254<=pos<=1603 and pos<1931 and len(vals)==1:prep[pos]=next(iter(vals))
assert len(plans)==21
(O/'plans.py').write_text('PLANS='+repr(plans)+'\nUNCHANGED='+repr(sorted(unchanged))+'\nPREPARED='+repr(prep)+'\nCORRECTED_EXISTING='+repr(sorted(corrections))+'\nPOSITION_SIDS='+repr(sidmap)+'\nCORRECTED_EXISTING_SIDS='+repr([s for p,ss in sidmap.items() if p in corrections for s in ss])+'\n')
s=(O/'common.py').read_text();a=s.index('PREVIOUS_CONFIRMED=');b=s.index('\n\ndef prepare',a);s=s[:a]+'PREVIOUS_CONFIRMED='+repr(sorted(previous))+s[b:];s=s.replace('range(800,1200)','range(1200,2048)').replace('len(ledger)==400','len(ledger)==848').replace('NEW_SIDS=sorted(PLANS)','NEW_SIDS=sorted(sid for pos in PLANS for sid in plans.POSITION_SIDS[pos])').replace('len(sids)==1 and sid==pos','len(sids)==1 and sid in plans.POSITION_SIDS[pos]')
a=s.index("   if f=='6000':");b=s.index('   helper=parent',a);s=s[:a]+s[b:]
s=s.replace("  raw=jp[a:jp.index(0xac,a)];source=", "  source_at=a;raw=jp[a:jp.index(0xac,a)];source=")
s=s.replace('  if pos in PLANS:\n',"  if pos>=2042:source='[SOURCE_JP_OPAQUE_APRES_SID_09C9]'\n  if pos in PLANS:\n")
s=s.replace("reason='イオ : Bang, explosion de base ; nom français DS identique, distinct de Superbang et Mégabang. Aucune modification ni nouvelle traduction ; fenêtre naturelle non parcourue.'","reason='Vocation Sage/Ranger oupersonnage Amos : JP etFRDS exacts, rôle relu ; pas de nouvelle traduction ni scène naturelle revendiquée.'")
a=s.index('  elif 836<=pos<=845:');b=s.index('  ledger.append',a)
s=s[:a]+'''  elif pos>=2042:status='DIFFERE_SOURCE_JP_OPAQUE';reason='VFvide ; JP séquentiel aprèsSID09C9 entre dans des octets non qualifiés comme texte dès3BC76D. Limite source inférée,consommateurs àauditer ; ne pas traduire le décodage de code/données.'
  elif 2007<=pos<=2041:status='STRUCTURE_DYNAMIQUE_WRAM';reason='SID09A7..09C9 redirigé parC44FDF versWRAM ; slotvide conservé,pas un dialogue àtraduire ni une preuve de rendu français dynamique.'
  elif pos==2006:status='RESERVE_VIDE_A_TRACER';reason='SID09A6 statique vide avant les35SIDs dynamiques ; accès àtracer,aucune traduction inventée.'
  elif pos>=1931:status='DIFFERE_LISTE_NOMS_A_TRACER';reason='Séquence de termes de saisie etnoms propres,potentiellement fonctionnelle ; ne pas traduire sans tracer le consommateur ni supposer du texte visible.'
  elif 1326<=pos<=1602:status='DIFFERE_COMPOSITION_NATIVE';reason='Fragment de description assemblée : voisinageJP/FR relu,anglais parfois faux. Adapter une phrase complète après traçage natif, pas un fragment d’après un nomDS homonyme.'
  elif 1254<=pos<=1325:status='DIFFERE_ACTION_SPECIFIQUE';reason='Commande mémoire ouaction technique/dejeu ; plusieursDS sont des échosjaponais,pas du français. Usage/chaîne àétablir.'
  elif not cur:status='VIDE_A_QUALIFIER';reason='Slotvide,rôle àconfirmer ; aucune traduction inventée.'
  elif re.fullmatch(r'[M*][0-9A-F]{3}',cur):status='DIFFERE_IDENTIFIANT';reason='Identifiant hérité,usage ettraduction àqualifier.'
  elif 1824<=pos<=1844:status='DIFFERE_VOCATION_GENRE';reason='Vocation ouoptionDS genrée/multiple : résoudre sans choix arbitraire.'
  elif 1851<=pos<=1924:status='DIFFERE_NOM_RECRUTABLE';reason='NompropreSFC sanscorrespondanceDS univoque ; pas une francisation phonétique seule.'
  else:status='DIFFERE_TEXTE_CONTEXTE';reason='Texte examiné,référenceDS/largeur/glyphes/commandes àétablir avant intégration.'
''' +s[b:]
s=s.replace("JP_message_sha256=sha(raw),status=", "JP_message_sha256=sha(raw),JP_source_offset=source_at,JP_source_length=len(raw),status=")
(O/'common.py').write_text(s)
for name in ['prepare.py','build.py','verify.py','emulator_consumers.py','emulator_render_names.py','audit_blockages.py']:
 p=O/name;s=p.read_text().replace('0800-1199','1200-2047').replace('positions=[800,1199]','positions=[1200,2047]').replace('physical_positions_examined=400','physical_positions_examined=848').replace('new_label_insertions=32','new_label_insertions=21').replace('new_translations=17','new_translations=14').replace('existing_french_revisions=15','existing_french_revisions=7').replace('existing_french_source_reviewed=1','existing_french_source_reviewed=3').replace('existing_french_qualified=1','existing_french_qualified=3').replace('new_labels_checked=32','new_labels_checked=21').replace('diagnostic_dialogues=64','diagnostic_dialogues=42').replace('all32_changed','all21_changed').replace('other2480','other2491').replace('next_position_to_examine=1200','next_position_to_examine=2048').replace('32 before/after','21 before/after').replace('secondary_IPS_positions_checked=400','secondary_IPS_positions_checked=848').replace('sid not in plans.CORRECTED_EXISTING','sid not in plans.CORRECTED_EXISTING_SIDS').replace('sid in plans.CORRECTED_EXISTING','sid in plans.CORRECTED_EXISTING_SIDS');p.write_text(s)
p=O/'prepare.py';s=p.read_text();needle="counts=dict(collections.Counter";i=s.index(needle);s=s[:i]+'''for lo,hi in [(1200,1600),(1600,2000),(2000,2048)]:
 subset=[x for x in m['ledger'] if lo<=x['position']<hi];assert [x['position'] for x in subset]==list(range(lo,hi));(O/f'registre-positions-{lo:04d}-{hi-1:04d}.json').write_text(json.dumps(subset,ensure_ascii=False,indent=2)+'\\n')
''' +s[i:];s=s.replace('all400_semantically_validated=False','all_positions_semantically_validated=False');p.write_text(s)
p=O/'inventory_names.py';s=p.read_text().replace('==161','==185').replace('inserted_this_pass=32','inserted_this_pass=21').replace('existing_french_reviewed_this_pass=1','existing_french_reviewed_this_pass=3').replace('physical_positions_examined_this_pass=400','physical_positions_examined_this_pass=848').replace('next_position=1200','next_position=2048');s=s.replace("elif not text:status='VIDE_A_QUALIFIER'","elif 2007<=pos<=2041:status='STRUCTURE_DYNAMIQUE_WRAM'\n elif pos==2006:status='RESERVE_VIDE_A_TRACER'\n elif pos>=2042:status='SOURCE_JP_OPAQUE_VF_VIDE'\n elif not text:status='VIDE_A_QUALIFIER'");p.write_text(s)
print('21selected,7revisions,3unchanged,',len(prep),'new proposals,848positions')

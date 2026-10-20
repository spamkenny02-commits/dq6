from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parent;O=R/'dq6-fr/v0.46';sha=lambda b:hashlib.sha256(b).hexdigest();read=lambda p:json.loads(p.read_text());save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2))
initial=read(O/'qa-render-initial-v046.json');proof=read(O/'qa-initial-rendered-token-hashes.json');current={x['id']:x for x in read(O/'insertion-candidates.json')};old={x['id']:x['tokens_sha256'] for x in proof['rows']};th=lambda t:sha(json.dumps(t,separators=(',',':')).encode());changed={i for i in old if old[i]!=th(current[i]['tokens'])};assert changed=={6472}
a=(O/'initial-before6472.sfc').read_bytes();b=(O/'result.sfc').read_bytes();assert sha(a)==proof['capture_rom_sha256'];skip=[]
for c in [0,0x400000]:skip.extend([(c+0x37175b,c+0x3b8703),(c+0x15bb5,c+0x165e7),(c+0xffdc,c+0xffe0)])
start=0
for lo,hi in sorted(skip):assert a[start:lo]==b[start:lo],hex(start);start=hi
assert a[start:]==b[start:]
fixed=read(O/'qa-render-fix6472.json');assert len(fixed['rows'])==1;assert fixed['result_sha256']==sha(b)
rows=[]
for r in initial['rows']:
 if r['id']==6472:continue
 r.update(capture_rom_sha256=sha(a),tokens_sha256=old[r['id']],final_tokens_identical=True);rows.append(r)
for r in fixed['rows']:r.update(capture_rom_sha256=sha(b),tokens_sha256=th(current[r['id']]['tokens']));rows.append(r)
rows.sort(key=lambda r:(r['id'],r['page']));assert len(rows)==166;assert len({r['id'] for r in rows})==111
q=dict(result_sha256=sha(b),rows=rows,all_captures_on_final_rom=False,provenance='110 messages captured on initial build8ada with identical tokens, fonts, names and engine; 6472 retested on final build after shortening. Both final decoding and current placement bus verified. No natural scenes or real transactions tested.',initial_capture_rom_sha256=sha(a),only_changed_message=6472,non_payload_pointer_checksum_bytes_equal=True,diagnostic_RAM=fixed['diagnostic_RAM'])
save(O/'qa-render-fixtures.json',q);save(O/'qa-correction-rendu6472.json',dict(initial_result_sha256=sha(a),result_sha256=sha(b),reason='The long welcome left a prior line visible after pagination. A single-window welcome retains D3 and native D5.',only_message_tokens_changed=[6472],other_110_rendered_tokens_identical=True,all_engine_font_name_and_other_data_unchanged=True,rejected_initial_captures=[r for r in initial['rows'] if r['id']==6472],new_capture=fixed['rows'][0]))
shutil.copy2(O/'layout-engine-current.json',O/'layout-engine-check.json');shutil.copy2(R/'dq6-fr/v0.45/layout-engine-current.json',O/'qa-retrospective-v045-layout.json')
p=R/'dq6-fr/package_system_v046.py';s=p.read_text().replace('167','166');s=s.replace("assert stress['target_pages']==1", "assert stress['target_pages']==1 and stress['result_sha256']==sha(O/'result.sfc')")
s=s.replace("real_transactions_or_naming_writes_tested=False,limits=", "real_transactions_or_naming_writes_tested=False,all_captures_on_final_rom=False,render_provenance='110 texts rendered on initial build with identical tokens and engine;6472 rerendered on final build, initial overlap captures rejected.',limits=")
s=s.replace('Diagnostics au camp, aucune scène naturelle', '110 messages capturés sur le premier binaire avec tokens, police, noms et moteur identiques ; 6472 raccourci puis recapturé sur le binaire final. Les deux captures initiales chevauchées sont rejetées. Diagnostics au camp, aucune scène naturelle')
s=s.replace('bus 880 plages/', 'bus des 870 placements courants plus noms/moteur, 880 plages/')
s=s.replace('Ouverts : assemblage', 'Le contrôle bus hérité utilisait un ancien catalogue de plages : il comparait réellement leurs octets, mais les positions n’étaient pas actualisées. Nouveau contrôle de tous les placements v0.46 et contrôle rétrospectif v0.45 conservés dans les rapports.\n\nOuverts : assemblage')
p.write_text(s);print('166 accepted pages;110 unchanged messages plus final6472; final SHA',sha(b))

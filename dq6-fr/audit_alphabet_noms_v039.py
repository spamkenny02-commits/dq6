"""Read-only inventory for the accent blocker. Never assigns a byte or glyph."""
from pathlib import Path
import argparse,json,struct,importlib.util,hashlib
P=Path(__file__).resolve().parent;a=argparse.ArgumentParser();a.add_argument('version');v=a.parse_args().version;O=P/v
spec=importlib.util.spec_from_file_location('nt_audit',P/'upstream/refill/tools/nametable.py');nt=importlib.util.module_from_spec(spec);spec.loader.exec_module(nt)
t=nt.Table(O/'result.sfc');raw=t.rom;used=set(b for e in t.entries[:t.reachable] for b in e)
# Include bytes emitted by dictionary expansion, not only the packed strings.
dictionary_bytes=set()
for i in range(len(t.dict)):
 dictionary_bytes.update(raw[t.dict_at+i*2:t.dict_at+i*2+2])
glyphs=struct.unpack_from('<256H',raw,0x11100)
charset={int(k,16):value for k,value in json.loads((O/'charset.json').read_text()).items()}
accents={ch:[f'{code:04X}' for code,value in charset.items() if value==ch] for ch in 'éèêàâîïôùûÉç'}
known=set(nt.GLYPHS)|set(range(2,12))|set(range(0x10,0x2a))|set(range(0x42,0x5c))
unobserved=[b for b in range(1,0x7f) if b not in used|dictionary_bytes|known]
rows=[dict(byte=f'{b:02X}',current_glyph=f'{glyphs[b]:04X}',main_charset_interpretation=charset.get(glyphs[b]),occurrences_in_reachable_names=sum(e.count(b) for e in t.entries[:t.reachable]),safe_to_reassign=False) for b in unobserved]
report=dict(version=v,rom_sha256=hashlib.sha256(raw).hexdigest(),inserted=0,mutation_performed=False,reachable_name_entries=t.reachable,packed_byte_values_used=len(used),dictionary_first=f'{t.dict_first:02X}',dictionary_entries=len(t.dict),glyph_table_file_offset='011100',accent_glyphs_in_main_charset=accents,unobserved_low_bytes=rows,all_candidates_blocked=True,blockers=['Un octet absent des noms atteignables n’est pas prouvé inutilisé par les variables, noms personnalisés, saisie ou autres interfaces.', 'Le tableau 011100 et les appels du décodeur sont à tracer avant toute réaffectation ; ne pas changer silencieusement une commande ou un glyphe partagé.', 'La présence d’un accent dans le script Huffman ne prouve pas son encodage dans la table de noms à octets.', 'Exiger ensuite gardes binaires, dictionnaire/sauts/pointeurs inchangés, anciennes chaînes et noms personnalisés, rendu B2 et fenêtres natives, et reconstruction exacte.'],decision='DIAGNOSTIC_NON_INSERE — aucune affectation de code proposée comme sûre')
(O/'audit-alphabet-noms.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(dict(unobserved_candidates=len(rows),inserted=0,all_blocked=True),ensure_ascii=False))

"""v0.44: isolated native-command restoration; no new main-script selections."""
from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;B=P/'v0.43';O=P/'v0.44';O.mkdir(exist_ok=True)
for name in ['init.py','prepare.py','build.py','verify.py','names.py','spells.py']:
 if (O/name).exists():continue
 s=(B/name).read_text()
 if name not in ['names.py','spells.py']:
  s=s.replace('v0.43','__NEW__').replace('v0.42','__BASE__').replace('__NEW__','v0.44').replace('__BASE__','v0.43').replace('v42','v43')
 if name=='prepare.py':s=s.replace('v043','v044').replace('correspondance_revue_v43','correspondance_revue_v44')
 if name=='build.py':
  s=s.replace('import names','import names\nimport native_helpers')
  s=s.replace('name_changes,verified_name_entries=names.apply(rom,P)','name_changes,verified_name_entries=names.apply(rom,P)\nnative_helper_entries=native_helpers.apply_names(rom)')
  s=s.replace('codes={}\ndef collect','root,left,right=native_helpers.restore_commands(rom,root,left,right)\ncodes={}\ndef collect')
  s=s.replace("assert rom[copy+0x167be:copy+0x1785e]==raw[0x167be:0x1785e]","native_helpers.verify_tree(rom,raw,copy)")
  s=s.replace('len(rows)-6102','len(rows)-6165').replace('huffman_tree_unchanged=True','huffman_tree_unchanged=False,native_huffman_commands_restored=[196,223],native_helper_entries_changed=native_helper_entries')
 if name=='verify.py':
  s=s.replace('len(checked)==63','len(checked)==0')
  s=s.replace('+extra_sids+spell_sids)', '+extra_sids+spell_sids+[0x118,0x11c,0x11d,0x11e])')
  s=s.replace('for sid in range(2512))','for sid in range(2512) if sid not in [0x118,0x11c,0x11d,0x11e])')
  s=s.replace("allowed += [(copy+0x58366,copy+0x5836a)]","allowed += [(copy+0x58366,copy+0x5836a),(copy+0x4b,copy+0x4e),(copy+0x2bfb,copy+0x2bfd),(copy+0x167be,copy+0x1785e)]")
  s+="\nimport native_helpers\nfor base in [0,0x400000]:native_helpers.verify_tree(expected,name_source,base)\nassert expected[0x4b:0x4e]==source[0x4b:0x4e]\nfor sid,(_,new_text) in native_helpers.HELPERS.items():assert name_entry(expected,sid)==native_helpers.encode(new_text)\n"
 (O/name).write_text(s)
for p in B.glob('*.json'):
 if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','audit-noms','audit-tables','inventaire-','lieux-prepares')):continue
 if not (O/p.name).exists():shutil.copy2(p,O/p.name)
(O/'revue-lot-v044.json').write_text('[]')
for n in ['correspondances-revues.json','adaptations-francaises.json','liaisons-variables-natives.json']:(O/n).write_bytes((B/n).read_bytes())
(O/'revues-preparatoires-remplacees.json').write_text('[]')
print('v0.44 isolated correction inputs ready, zero new selections')

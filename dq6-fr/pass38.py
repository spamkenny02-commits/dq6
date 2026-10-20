"""Restore 20 reviewed separate spell/action labels, no main-script additions."""
from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;B=P/'v0.37';O=P/'v0.38';O.mkdir(exist_ok=True)
for name in ['init.py','prepare.py','build.py','verify.py','names.py']:
 if (O/name).exists():continue
 s=(B/name).read_text()
 if name!='names.py':
  s=s.replace('v0.37','__NEW__').replace('v0.36','__BASE__').replace('__NEW__','v0.38').replace('__BASE__','v0.37').replace('v36','v37')
 if name=='prepare.py':s=s.replace('v037','v038').replace('correspondance_revue_v37','correspondance_revue_v38')
 if name=='build.py':s=s.replace('len(rows)-5854','len(rows)-5905').replace('additional_character_names_changed=1','additional_character_names_changed=1,spell_action_entries_changed=20')
 if name=='names.py':s=s.replace(' source_end=START+',' from spells import apply_reviewed_spells\n apply_reviewed_spells(entries,groups,changed,root,encode)\n source_end=START+',1)
 if name=='verify.py':
  s=s.replace('assert changed_name_ids==sorted(',"spell_reviews=json.loads((O/'revue-sorts-v038.json').read_text());spell_sids=sorted({sid for r in spell_reviews for sid in r['runtime_sids']})\nassert len(spell_sids)==20\nfor row in spell_reviews:\n for sid in row['runtime_sids']:assert name_entry(expected,sid).hex()==row['new_bytes']\nassert changed_name_ids==sorted(")
  s=s.replace('+place_sids+extra_sids),changed_name_ids','+place_sids+extra_sids+spell_sids),changed_name_ids')
  s=s.replace('for sid in range(2512))','for sid in range(2512) if sid not in spell_sids)')
 (O/name).write_text(s)
for p in B.glob('*.json'):
 if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','audit-noms','audit-tables','inventaire-','lieux-prepares')):continue
 if not (O/p.name).exists():shutil.copy2(p,O/p.name)
assert json.loads((O/'revue-lot-v038.json').read_text())==[]
assert len(json.loads((B/'insertion-candidates.json').read_text()))==5905
print('v0.38 inputs ready: 20 separate labels; zero main additions')

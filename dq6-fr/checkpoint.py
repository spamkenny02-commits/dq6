"""Create a reproducible partial checkpoint. Never includes ROMs or saves."""
from pathlib import Path
import argparse,json,re,zipfile,hashlib
P=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('version');ap.add_argument('--notes',required=True);args=ap.parse_args();O=P/args.version
v=json.loads((O/'validation.json').read_text());coverage=json.loads((O/'couverture-preparation.json').read_text());baseline=re.search(r"previous=read\(P/'([^']+)/insertion-candidates.json'\)",(O/'prepare.py').read_text()).group(1)
state={'release':args.version,'status':'PARTIEL','main_script':{'validated':v['ds_validated'],'visible_total':6957,'new_this_pass':coverage['new_prepared'],'remaining':v['remaining_visible_messages']},'separate_tables':'Noms, menus, objets, sorts, combat : audit et traduction encore nécessaires, hors compte du script principal.','baseline':baseline,'rom_bytes':v['rom_bytes'],'notes':args.notes,'next':'Poursuivre sans attendre une relance ; sauvegarder le prochain passage.'}
(O/'etat-projet.json').write_text(json.dumps(state,ensure_ascii=False,indent=2))
readme=f'''# Dragon Quest VI — VF DS — {args.version} PARTIELLE

{v['ds_validated']} messages sur 6 957 du script principal validés sur les textes DS fournis, dont {coverage['new_prepared']} nouveaux. Les sélections {baseline} sont conservées avec leurs tokens identiques. Il reste {v['remaining_visible_messages']} messages du script principal, plus les tables séparées de menus, noms, objets, sorts et combat. Ces comptes ne sont pas un pourcentage global du jeu.

{args.notes}

## Appliquer

Appliquer DQVI-FR-DS-{args.version}-BASE-JP-PARTIEL.bps directement sur la ROM japonaise intacte sans en-tête de copieur :

- Dragon Quest VI - Maboroshi no Daichi (Japan).sfc
- Taille 4 194 304 octets ; CRC32 33304519
- SHA256 90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e

Ne pas préappliquer un ancien patch. Ne pas utiliser dquest6.smc. L'IPS alternatif attend la même source mais ne contrôle pas son empreinte. Le résultat reste à 8 388 608 octets (ExHiROM), en attendant l'étude des 4 Mo après les textes.

SHA256 du résultat : {v['result_sha256']}

## Vérifications et limites

Les 6 960 entrées techniques sont redécodées et comparées aux tokens attendus. Les patchs BPS/IPS sont relus indépendamment. Les anciennes sélections sont comparées au JSON de référence inclus ; la comparaison supplémentaire des octets hors script nécessite la ROM précédente locale. Les commandes natives protégées sont conservées. Les rapports qa-*.json et validation.json précisent les essais effectués.

Les captures d'émulation proviennent de l'ouverture ou de bancs temporaires qui redirigent un message vers un texte choisi. Elles contrôlent le rendu, pas la progression naturelle jusqu'à chaque scène. Le parcours complet, les achats, les combats et la sauvegarde en église ne sont pas déclarés validés.

## Reproduire

Placer les trois sources fournies dans upload/ à côté de dq6-fr/ (ROM japonaise intacte, ROM DS et Dq6f.ips), puis :

```bash
python dq6-fr/{args.version}/init.py
python dq6-fr/{args.version}/prepare.py
python dq6-fr/{args.version}/build.py
python dq6-fr/{args.version}/verify.py
```

Ces quatre étapes utilisent Python standard. Les essais d'émulation demandent numpy, Pillow et un cœur Snes9x libretro compilé. Les noms personnalisés de sauvegarde ne sont pas réécrits. Aucune ROM, SRAM ni sauvegarde d'état n'est incluse.

Sources techniques : https://github.com/ButThouMust/dq6-sfc et https://github.com/RadMageIRL/DQVI_SCRIPT_REFILL. Source française principale : ROM DS fournie ; source secondaire : IPS fourni. Les adaptations explicites conservent le corps DS d'origine ; les propositions de rapprochement ne sont pas automatiquement validées.
'''
(O/'LISEZ-MOI.md').write_text(readme)
files={}
def add(f,arc=None):files[arc or str(f.relative_to(P.parent))]=f
for f in O.iterdir():
 if f.suffix in {'.py','.json','.md','.bps','.ips'}:add(f)
add(P/baseline/'insertion-candidates.json');add(P/'v0.3/charset.json')
for name in ['extract.py','probe.py','checkpoint.py','audit_tables.py','render_fixtures.py','emulator-tests/run_core.py','emulator-tests/peek_extension.cpp','clean-base/ds-fr.json','clean-base/ds-ja.json','clean-base/sfc-jp.json','clean-base/sfc-vf.json','clean-base/nds-files.json','clean-base/validation.json','clean-base/decode_vf.py','clean-base/table-vf-provisoire.json','clean-base/alignement-jp-top5.json','clean-base/align_extended.py','upstream/refill/patchRM.py','upstream/refill/tools/nametable.py','upstream/refill/docs/NAME-TABLE.md','upstream/refill/docs/BATTLE-POOL.md']:
 f=P/name
 if f.exists():add(f)
for f in O.glob('screenshots/*.png'):add(f)
for f in P.glob('pass*.py'):add(f)
add(O/'LISEZ-MOI.md','LISEZ-MOI.md')
if (P.parent/'REPRISE-AUTOMATIQUE.md').exists():add(P.parent/'REPRISE-AUTOMATIQUE.md','REPRISE-AUTOMATIQUE.md')
target=P.parent/f'DQVI-FR-DS-{args.version}-BASE-JP-PARTIEL.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for arc,f in sorted(files.items()):z.write(f,arc)
 # Preserve the supplied glyph table and its provenance without an older ZIP.
 for f in sorted((P/'upstream/dq6-sfc').iterdir()):
  if f.name in ['dq6 jp.tbl','README.md']:
   arc=str(f.relative_to(P.parent))
   if arc not in files:z.write(f,arc)
with zipfile.ZipFile(target) as z:
 assert z.testzip() is None
 assert not any(Path(n).suffix.lower() in {'.sfc','.smc','.nds','.state','.srm'} for n in z.namelist())
print(json.dumps({'path':str(target),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}))

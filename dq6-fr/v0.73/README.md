# v0.73 — douze noms de monstres résolus

Les positions 626,627,629,630,631,632,634,636,637,642,643,645 préparées en v070 sont désormais intégrées : spectrokane, feudjoie, fournèze, zombinator, karkassor, désosseur, kangouffre, démonstre, verminator, arbomage, arbomancien, écorcheur. Lecture JP SFC, japonais et français DS complets, contexte de noms d’espèces et ancien IPS secondaire. Aucun rapprochement flou ne valide une entrée. Les accords/pluriels DS ne sont pas transférés ni déclarés validés : le contexte grammatical SFC reste à contrôler naturellement.

197 entrées françaises qualifiées / 2048 positions physiques ; 574 propositions non insérées. Ces douze résolutions ne constituent pas un nouveau parcours des 2048 ni une relecture exhaustive. Principal : 6957 sélections dont 6948 linguistiques et 9 structures, inchangées. Combat séparé : 597 qualifiées, 2 préparées, 5 opaques et 4 structures, inchangé. Aucun audit hérité clôturé. Fragments composés, glyphes manquants, noms longs, genres et autres ressources restent ouverts.

## Recette

Depuis la racine, DQ6_JP, DQ6_DS, DQ6_IPS désignent les trois sources privées vérifiées et DQ6_OUT une sortie privée hors Git :

```sh
python restore_sources.py
python dq6-fr/v0.73/prepare.py --jp "$DQ6_JP" --ds "$DQ6_DS" --ips "$DQ6_IPS"
python dq6-fr/v0.73/build.py --jp "$DQ6_JP" --out "$DQ6_OUT"
python dq6-fr/v0.73/verify.py --jp "$DQ6_JP" --out "$DQ6_OUT"
python dq6-fr/v0.73/inventory_names.py --jp "$DQ6_JP" --rom "$DQ6_OUT/result.sfc"
```

prepare vérifie les empreintes des sources, le JP SFC, les 24 champs JA/FR directement dans les MPT de la ROM DS et les 12 libellés secondaires IPS. build reconstruit depuis BPS v072, remplace uniquement les douze SIDs et conserve les 464 alias. verify redécode, réapplique BPS/IPS à JP intacte, rejette les mauvaises sources, vérifie les 2500 autres chaînes brutes et les zones protégées. ROM 8 Mio ; table relocalisée 7AF000..7B27A2 (14242 octets), capacité réservée jusqu’à 7B8703. Ancienne table et miroir, fin de table 2050 octets, moteur, polices, dictionnaire, script principal et pool combat intacts.

## Diagnostics réellement exécutés

Les trois scripts emulator_names_probe.py, emulator_consumers.py, emulator_render_names.py acceptent --out, --runner et --camp ; consumers/render acceptent aussi --jp. Le lecteur est exécuté une fois normalement, une fois avec --mutate-pointer. Utiliser un seul émulateur, le cœur Snes9x local et le protocole run_core.py documenté en v026, ou reconstruire ce cœur et créer un nouvel état local. bus_layout.py génère les plages pour run_core.py --check-layout. Le démarrage utilise --reset et la séquence de qa-bus-boot.json, sans charger d’état.

2477 SIDs statiques lus, 35 dynamiques explicitement exclus, mutation SID16 détectée. Terrain C3763A et B2 C6FDF0 avant/après : glyphes, largeur et buffers vérifiés pour les douze noms. 24 dialogues B2 diagnostiques (trois répétitions chacun), 12 images après insertion relues visuellement ; accents et orthographe lisibles, pas de débordement dans cette fenêtre. Bus 4002 plages et Journal à froid. Les diagnostics ne constituent pas un parcours naturel de combat, de recrutement ou de menu compact ; ils ne valident pas tous les accords/pluriels ni tous les consommateurs. Les images, ROM et états restent privés hors Git.

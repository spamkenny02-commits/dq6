# DQVI FR v0.58 — noms variables dans les messages de combat

28 préparations intégrées dans le pool byte natif : voir revue-combat-v058.json et delta-combat-v058.json. Japonais SFC, français et références DS explicites relus ; 26 entrées ont une référence DS, 410/411 sont adaptées directement du SFC. Les rôles B7/B8, pauses et autres commandes natives restent dans leur ordre. Les anciennes préparations et les huit traductions v0.57 sont conservées. Aucun ajout au principal ni aux noms.

Le pool complet comporte 608 messages et 76 groupes de pointeurs. Les 580 autres messages, les 870 groupes principaux, les octets hors payload/pointeurs/checksum et le moteur restent identiques. Les deux copies des pointeurs relatifs à F6DEBD sont mises à jour. Réserver le pool déplacé indiqué dans build-report.json lors de toute future allocation du principal. La taille reste 8 Mio.

## Reconstruction

```sh
python restore_sources.py
python dq6-fr/v0.58/prepare.py --jp /chemin/JP-intacte.sfc
python dq6-fr/v0.58/build.py --jp /chemin/JP-intacte.sfc --out /chemin/prive
python dq6-fr/v0.58/verify.py --jp /chemin/JP-intacte.sfc --out /chemin/prive
python dq6-fr/v0.58/inventory.py --rom /chemin/prive/result.sfc
```

Les sources v0.58 sont suivies directement ; restore_sources.py restaure les extractions DS, la table v0.56 et les dépendances historiques. La recette applique le BPS v0.57 vérifié à la JP intacte, puis ce delta explicite. Ne pas repartir du seul BPS v0.56, ce qui perdrait les huit textes natifs précédents. Le BPS v0.58 autonome publié s’applique directement à la JP intacte SHA256 90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e. Les empreintes ROM/BPS/IPS figurent dans build-report.json. L’IPS vérifié reste privé avec la ROM ; aucune ROM, SRAM, capture du jeu ou sauvegarde d’émulation publiée.

prepare vérifie la source, les empreintes des références DS, le périmètre exact et les mots des préparations. Seuls les espaces et AD peuvent être adaptés. Le codec accepte l’alphabet ASCII relu sur la police résidente et les noms B7/B8 pour ce lot ; pas d’accent nouveau ni quantité, objet ou sort variable. Les anciens allers-retours du modèle Huffman ne valident pas tout le codec natif.

## Deux décisions explicites

543 débordait avec ses trois AD de paragraphe et des noms de 13/15 caractères : fin superposée. Les AD sont remplacés par des espaces ; mots, deux B7, deux B1, BC et AC identiques. Le texte complet est relu après correction. L’ancien plan et la décision restent dans la revue.

397 reste PREPARE_NON_INSERE. Les rôles distincts sont lisibles, mais le profil homonyme a affiché deux suffixes A au lieu de A/B. Voir blocage-397.json : tracer B8/C69315, C2B8D5, file des substitutions et contexte naturel avant insertion. Aucun moteur modifié pour masquer ce cas.

## Tests et portée

Les reconstructions répétées et réapplications BPS/IPS reproduisent le même résultat. Les mauvaises sources BPS (JP modifiée, en-tête copieur) sont rejetées. Redécodage indépendant des 608 entrées : exactement 28 changements, 580 identiques, notamment les huit anciennes traductions. Les 870 groupes du principal restent identiques, ainsi que Journal/Options, suppression du crédit et cadre du nom. Aucune correction silencieuse d’un audit hérité.

```sh
python dq6-fr/v0.58/emulator_probe.py --out /chemin/prive --runner /chemin/emulator-tests/run_core.py --camp /chemin/v026-camp.state --mode reader
python dq6-fr/v0.58/emulator_probe.py --out /chemin/prive --runner /chemin/emulator-tests/run_core.py --camp /chemin/v026-camp.state --mode reader --mutate-pointer
python dq6-fr/v0.58/emulator_probe.py --out /chemin/prive --runner /chemin/emulator-tests/run_core.py --camp /chemin/v026-camp.state --mode render --profile distinct
python dq6-fr/v0.58/emulator_probe.py --out /chemin/prive --runner /chemin/emulator-tests/run_core.py --camp /chemin/v026-camp.state --mode render --profile duplicate
```

Un seul émulateur à la fois. Les captures finales nécessitent une relecture visuelle : le script ne la déclare pas automatiquement. Le protocole regroupe dans une même session les attentes et deux acquittements, sans modifier le lecteur natif. Les fixtures privées redirigent C02AE2 vers un appel C02A29 qui initialise le lecteur, dans une zone libre mesurée. Appeler C02671 seule n’est pas une initialisation valide. Moteur et résolveur de noms de production inchangés.

B7 lit l’acteur WRAM2555, B8 la cible2559 ; C2B8D5 résout leurs noms. Les 24 fiches d’entités de pas 34hex sont effacées puis deux fiches sont initialisées. Le profil distinct donne SID02F1/Spotted Slime (13 caractères) et SID024F/Lipps (5 caractères). Le profil homonyme donne Spotted Slime-A/B (15 caractères). Ces noms anglais hérités servent à tester rôles et largeur ; ils ne sont pas comptés comme des noms français validés. Les SID retournés et empreintes de captures sont consignés. Les messages longs et phases de 523/543/548 sont relus sur leur rendu complet final.

Snes9x vérifie les 608 pointeurs et premiers octets ; une mutation volontaire du pointeur8 est détectée. Le bus ROM vérifie 871 segments / 499687 octets. Démarrage sans état, Nouveau jeu/Journal et cadre du nom relus séparément. Voir les rapports QA. Ces diagnostics en camp ne valident pas un combat atteint naturellement, le chemin des noms de personnages, la fenêtre compacte, toutes les longueurs ou toutes les compositions natives.

## Comptes et reprise

Combat : 36 français intégrés et relus en diagnostic, 71 préparés non insérés (69 relus sémantiquement, deux réserves464/465), 497 hérités non qualifiés, quatre structures. Parmi les 71 : 54 références DS et 17 adaptations directes SFC ; 64 cas avec accents non approuvés, six substitutions ASCII complexes (337/367/428/454/455/498) et 397 réservé. L’historique107 reste conservé ; inventory.py vérifie le reliquat actif.

Principal : 6957 sélections, dont 6948 linguistiques et neuf structures ; zéro reliquat. Relecture exhaustive enregistrée : zéro. Autre pool : 2512 SIDs / 2048 entrées physiques / 464 alias ; 37 français confirmés, quatre aides grammaticales, 25 lieux et un nom Céleste préparés, inchangés ici. L’absence de japonais n’est pas une validation du français. Restent les autres tables, la recherche des oublis, la relecture complète et les audits322/323,1836,4095,610/1135/2404/5341/5351, fragments, commandes rares et accents. Projet non finalisé ; 4 Mio à réexaminer seulement à la fin.

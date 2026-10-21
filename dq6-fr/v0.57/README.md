# DQVI FR v0.57 — premier lot natif de combat

Huit préparations sont intégrées dans le pool byte natif :51,427,429,494,519,520,536,538. Elles sont relues depuis le japonais SFC, avec les références DS disponibles ;494 se rattache à la fourmilière du message493. Les textes ne contiennent aucun nom, quantité, objet ou sort variable et ne nécessitent aucun accent nouveau. Les commandes natives, leur ordre et leur nombre sont conservés ; AD reste celui des préparations relues. Les43 anciens allers-retours de codec ne sont pas tous déclarés validés : seuls ces huit textes reçoivent une validation diagnostique de rendu.

Les6957 sélections du script principal (6948 linguistiques,9 structures), les600 autres entrées du pool et toutes les tables de noms restent inchangées. Le pool complet608 entrées/76 groupes est déplacé vers une zone libre mesurée parmi les réserves ExHiROM, sans recouvrir les870 groupes principaux. Les deux copies de la table de pointeurs reçoivent des offsets natifs relatifs àF6DEBD. Le moteur de production n’est pas modifié. La taille reste8 Mio.

## Reconstruction et restauration

Les sources de cette version sont suivies directement ; restore_sources.py restaure la base et tous les lots jusqu’àv0.56 nécessaires à cette recette. Elle applique le BPS v0.56 vérifié à la JP intacte, puis ce delta natif explicite et idempotent. Ne pas appliquer le delta à une ROM modifiée ni rejouer le lot comme huit nouvelles revues.

```sh
python restore_sources.py
python dq6-fr/v0.57/prepare.py --jp /chemin/JP-intacte.sfc
python dq6-fr/v0.57/build.py --jp /chemin/JP-intacte.sfc --out /chemin/prive
python dq6-fr/v0.57/verify.py --jp /chemin/JP-intacte.sfc --out /chemin/prive
```

La source exigée a pour SHA25690ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e. Le résultat8 Mio a pour SHA25637c4f78da7aa8466fabe59f8a135818996108e6dd68833d81c5c6e37fb542208. Le BPS autonome publié `patches/DQVI-FR-DS-v0.57-BASE-JP-PARTIEL.bps` s’applique à cette source JP intacte. Le build produit aussi un IPS vérifié, conservé uniquement dans le dossier privé avec la ROM. Aucun fichier ROM, SRAM, état ou capture n’est publié.

## Contrôles exécutés

Prepare/build répétés redonnent les mêmes empreintes. Les patchs BPS/IPS sont réappliqués et comparés au résultat ; les sources BPS modifiées ou avec en-tête copieur sont rejetées. Le redécodage indépendant des608 entrées trouve exactement les huit changements attendus. Les octets des870 groupes principaux et tous les octets hors payload/pointeurs/checksum restent identiques, notamment Journal/Options, suppression du crédit de traduction et cadre du nom. Aucun changement silencieux des audits hérités.

Snes9x exécute réellement le lecteur natif sur les608 IDs déplacés : pointeurs et premiers octets corrects. Une mutation volontaire du pointeur8 est détectée. Le bus ROM vérifie498815 octets dans871 segments (870 principaux et le pool natif). Un démarrage sans état atteint Nouveau jeu/Journal et le cadre du nom, relus à l’écran.

Les huit textes complets sont relus dans la fenêtre native viaC02A29. Contrairement à l’essai v058 rejeté, la ROM privée appelle l’entrée qui initialise le lecteur ; appeler C02671 seule ne suffit pas. Cette correction est limitée aux fixtures privées et ne touche pas le moteur du patch. Les pausesC2/AF, les délaisB1, BC/BD et les deux phases de536 ont été observés. Les images et leurs états restent privés ; leurs empreintes et le protocole sont conservés.

Une seconde série emploie l’API compacte C02A4F. Elle valide six textes ;427/429 y dépassent la zone et ne sont pas validés dans cette géométrie. Leurs appels source retrouvés aux adressesC2B3CA/C2B477 utilisent explicitement C02A16, correspondant à la grande fenêtre testée. Le51 est aussi appelé par C02A16 àC2AD4A. Ces sites sont contrôlés dans la JP intacte et la base ; aucun mode compact n’est imposé au jeu. Les cas de pagination d’autres familles et les commandes rares restent ouverts.

```sh
python dq6-fr/v0.57/emulator_probe.py --out /chemin/prive --runner /chemin/emulator-tests/run_core.py --camp /chemin/v026-camp.state --mode reader
python dq6-fr/v0.57/emulator_probe.py --out /chemin/prive --runner /chemin/emulator-tests/run_core.py --camp /chemin/v026-camp.state --mode reader --mutate-pointer
python dq6-fr/v0.57/emulator_probe.py --out /chemin/prive --runner /chemin/emulator-tests/run_core.py --camp /chemin/v026-camp.state --mode render
```

Les captures nécessitent ensuite une relecture visuelle ; le script ne l’invente pas. Ne jamais lancer plusieurs émulateurs ensemble. Aucun combat naturel ni validation de toutes les variables ou de tous les messages n’est déclaré.

## Comptes et reprise

Combat :8 français intégrés et relus en diagnostic,99 préparés non insérés (97 relus sémantiquement,2 réserves464/465),497 hérités non validés et4 structures. Les99 incluent80 références DS et19 adaptations directes SFC ; ne pas les additionner au principal. Les107 préparations historiques restent dans preparations/combat-v057 ; l’inventaire de cette version retire les huit IDs du reliquat actif. Noms :37 français confirmés,4 aides grammaticales,25 lieux et1 nom Céleste préparés, inchangés ici. Relecture exhaustive du principal :0 enregistrée.

Reprendre depuis cette version et conserver les huit IDs. Toute future allocation du principal doit réserver également le pool natif indiqué dans build-report.json : c.main_regions ne recense que le principal. Le lecteur c.pool des outils v058 attend la base v0.56 ; utiliser decode_pool de cette recette pour lire la v0.57 déplacée. Ne pas perdre ces traductions en repartant du seul BPS v0.56. Accents, substitutions natives, autres tables, recherche des oublis, relecture intégrale et audits322/323,1836,4095 et autres réserves restent ouverts.4 Mio sera réexaminé seulement à la fin.

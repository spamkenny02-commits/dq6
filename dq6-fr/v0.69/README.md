# v0.69 — premier lot des 2048 positions : 0000–0399

400 positions examinées et consignées individuellement, pas 400 textes traduits. 25 libellés modifiés, 13 français existants rapprochés des sources DS et relus, 35 propositions PREPARE_NON_INSERE. Les autres positions restent explicitement techniques ou différées ; aucune validation naturelle implicite. Prochain lot : 400–799, puis 800–1199, 1200–1599, 1600–1999, 2000–2047. Revenir ensuite sur les réserves consignées.

Exemples : Divination, Retrait, Tactique, Sac, Agilité, Vitalité, Défense, Accessoire, Hugo, Enzo, Cindy, Linda, Claire, Miroir de Râ. Les décisions et références DS japonaises/françaises figurent dans revue-table-v069.json. Correction héritée isolée : position218 affichait « Agilite: » pour みのまもり ; « Vitalité: » distingue cette caractéristique de l’agilité et de la défense équipée. Largeur inchangée9colonnes ; lecteurs natifs avant/après testés. Aucune correction des audits principaux hérités dans ce lot.

100 entrées françaises qualifiées sur2048 ; 1508 autres textes à revoir, 344 identifiants, 12 candidats français DS à qualifier, 83 vides à qualifier, 1crédit retiré. 464alias conservés/2512SIDs. Les35propositions ne s’ajoutent pas à2048 et restent distinctes des2lieux préparés438/479. Principal6957sélections (6948linguistiques/9structures), combat597qualifiés/2préparés/5opaques/4structures inchangés ; relecture exhaustive du principal0.

## Recette locale, sources privées

Depuis la racine du dépôt :

```sh
python restore_sources.py
python dq6-fr/v0.69/prepare.py --jp "$DQ6_JP" --ds "$DQ6_DS" --ips "$DQ6_IPS"
python dq6-fr/v0.69/build.py --jp "$DQ6_JP" --out "$DQ6_OUT"
python dq6-fr/v0.69/verify.py --jp "$DQ6_JP" --out "$DQ6_OUT"
python dq6-fr/v0.69/inventory_names.py --jp "$DQ6_JP" --rom "$DQ6_OUT/result.sfc"
```

DQ6_JP/DS/IPS désignent les trois sources privées avec les empreintes de qa-lot400.json ; DQ6_OUT doit rester hors Git. prepare vérifie72champs directement dans la ROM DS et400positions dans l’ancien IPS ; ces lectures secondaires ne valident pas automatiquement le sens.

8Mio conservés. Table active7AF000 de14361octets, capacité réservée jusqu’à7B8703. Pointeurs157groupes en deux copies ; lecteur obligatoire common.py::names/LogicalTable v068 ou ultérieur. Ancien pool3B8703..3BC712, miroir et tail2050octets intacts. Moteur, dictionnaire, polices,870groupes principaux et608slots combat inchangés. BPS/IPS réappliqués à la source intacte, sources erronées rejetées.

## Portée des tests

Lecteur2477SIDs statiques (35dynamiques exclus), mutation négativeSID16, lecteurs terrainC3763A/B2C6FDF0 avant/après25libellés ;50dialogues diagnostiques avec répétitionsB2, busROM et démarrage à froid. Les rapports distinguent exécution CPU, comparaisons pixels et revue visuelle. Ces redirections au camp ne prouvent pas les fenêtres naturelles des menus, le recrutement ou toutes les scènes. Les corrections n’augmentent aucune largeur développée ; cela ne remplace pas l’audit des fenêtres.

Le byte85 des en-têtes est conservé : deux-points dans la police native8x8, avec une divergence du charset historique qui nomme son glyphe0240 « point ». Le codec local accepte85 uniquement pour préserver ces en-têtes. Aucun nouveau glyphe ni changement de police ; les six en-têtes montrent bien un deux-points dans le diagnosticB2, sans validation des fenêtres naturelles. Voir qa-colon.json.

Restent les ambiguïtés du registre, les2lieux préparés, les autres ressources, les audits322/323,1836,4095,610/1135/2404/5341/5351, les consommateurs naturels, commandes rares, alphabet et relecture exhaustive. La tâche n’est pas finalisée.

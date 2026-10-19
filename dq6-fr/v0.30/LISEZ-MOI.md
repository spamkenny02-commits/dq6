# DQVI FR DS v0.30 — PARTIEL

114 nouveaux messages intégrés : 5730/6957, 1227 restants. Depuis v0.28 : 178 ajouts en deux lots sauvegardés. Principal préparé non inséré : 0. Tables : 33 lieux hérités de la préparation v0.29, 0 nouvelle insertion ; ne pas les compter deux fois. ROM ExHiROM 8 Mio, SHA256 16a920616d6c86767559dea03a9ce06c1f9986bb1349da88094a62a255db73a3.

Patch BPS sous patches/, à appliquer à la ROM japonaise intacte sans en-tête, CRC32 33304519. Aucun fichier ROM, SRAM ou état distribué. L'IPS se régénère par build.py.

47 adaptations explicites aux faits SFC, avec les paires JA/FR DS, le japonais SFC, l'IPS secondaire et les notes dans revue-lot-v030.json. Restaure les noms omis, les fins de réplique, les distinctions d'objets (carte contre clef), les effets accomplis (ouvrir la commode), l'indice du château laissé implicite, le motif de croix du bouclier de Valora et des propos de villageois inversés en VF DS. Le libellé Valora est confirmé dans MENULIST6/FR/b1000000.mpt:155 ; ne pas reprendre Sufida/Sufflair. Six autres propositions restent différées pour contexte/rituel/indices, sans intégration.

5616 anciennes sélections et octets hors zones autorisées inchangés. BPS/IPS réappliqués, 6960 entrées redécodées, rejet des mauvaises sources, contrôle des noms dans les 114 corps y compris C0, bus Snes9x : 870 groupes et 466984 octets. Démarrage à froid jusqu'à Journal, 40 pages de dix messages relues. En 5868, C0 affiche Olivier après injection RAM 3B2D=2 dans le seul banc de diagnostic. Aucun code de ROM finale modifié pour ce test. Ces redirections au camp ne prouvent pas les scènes naturelles ; aucun parcours complet annoncé.

Reprise : python restore_sources.py ; recette idempotente dq6-fr/pass30.py, delta lisible sources/lots/v0.30.json. Reconstruire avec init.py, prepare.py, build.py, verify.py dans v0.30. Pour les tables, lire l'inventaire reproductible v0.29 : 2048 entrées, 2512 SIDs, 464 alias ; descriptions fragmentées, encodage accentué et fenêtres à tester avant insertion. Audits 322/323, 1836, 5351 et nouveaux cas différés ouverts. Le projet reste partiel.

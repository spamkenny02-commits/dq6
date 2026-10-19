# DQVI FR DS v0.31 — PARTIEL

5731/6957 messages intégrés, 1226 restants. Ce lot : 1 nouveau (322), 1 correction héritée (323), sans compter la correction comme ajout. Depuis v0.28 : 179 nouveaux et 1 correction. Tables : 33 lieux PREPARE_NON_INSERE, 0 insertion. ROM 8 Mio, SHA256 bbe95ef6458b30cba8fe86942b150e15d94a6dfcf995836a2156522e67640b5c.

Le français DS réordonne les informations du tapis entre 0056:584–588. Le japonais SFC 322 traite de fabrication/disparition ; 323 de vol/propriétaire/rumeur. La revue croise les deux japonais, tous les français DS et l'ancien IPS secondaire, avec adaptations aux faits SFC. L'ancienne sélection 323 décrivait la fabrication à tort. Elle est corrigée explicitement ; aucune autre ancienne sélection ne change. Les preuves avant/après sont dans revisions-messages.json et revue-lot-v031.json.

La restauration accepte désormais des corrections manifestées, gardées par SHA256 des anciens tokens et égalité de l'ancien texte, avec motif obligatoire et ID inchangé. Sept tests unitaires vérifient les rejets et la compatibilité. 5729 anciens messages sont conservés, 1 nouveau et 1 révisé compilés. BPS et IPS réappliqués à la source japonaise intacte, mauvaises sources rejetées, zones protégées conservées, 6960 entrées redécodées. Snes9x : 870 groupes et 467014 octets contrôlés sur bus, démarrage Journal et 8 pages de 321/322/323 relues. Redirections au camp ; les branches naturelles ne sont pas parcourues. Aucun parcours complet annoncé.

Restaurer par python restore_sources.py, recette idempotente dq6-fr/pass31.py, delta sources/lots/v0.31.json avec replacements_file. Reconstruire init.py/prepare.py/build.py/verify.py dans v0.31. Le patch BPS est sous patches/. Aucun fichier ROM, SRAM ou état distribué.

322/323 corrigés sémantiquement avec limite de parcours ci-dessus. 1836 reste ouvert, de même que 5351 et les cas différés v0.30. Lire l'inventaire des tables v0.29 : 2048 entrées / 2512 SIDs / 464 alias ; encodage accentué, fenêtres et pointeurs encore à maîtriser. Le projet reste partiel.

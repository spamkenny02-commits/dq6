# Dragon Quest VI FR — v0.41 partielle

6031/6957 messages intégrés, 64 nouveaux ; 926 restants. Aucun préparé principal nouveau. Tables inchangées : 37 entrées françaises confirmées, 25 lieux préparés, hors compte principal. 8 Mio conservés.

Français DS fourni comme source principale, japonais SFC et DS relus, ancien IPS secondaire souvent décalé. Adaptations détaillées dans revue-lot-v041.json : le sort suprême et la cascade en 3724, le rôle de prêtre en 4993 et la direction du panneau en 2359 sont rétablis. Les cris ne reprennent pas les discours ajoutés dans FR DS. 6078/6118 n’ajoutent pas les locuteurs DS ; 2835 garde deux C9. 5974 emploie DS 0803:209 positif, pas la phrase de déception 0804:140. 4010 emploie l’appel DS 0000:111, pas le prince du rapprochement initial. 828 présente la pipe SFC, ne la reçoit pas. Les soldats 4778 répondent au capitaine Ferraille (トム), confirmé dans DS 0008:699/761/763. Le soldat 2411 reste Soldat, sans importer la désignation de garde du trésor d’un autre contexte.

Les 5967 anciennes sélections et 2512 noms sont inchangés. Recette idempotente pass41.py, base v0.40 ; restore_sources.py puis init.py, prepare.py, build.py, verify.py sous dq6-fr/v0.41. Périmètre strict de 64 IDs. BPS/IPS réappliqués à la source JP intacte, mauvaises sources rejetées, 6960 entrées redécodées, zones protégées et occurrences natives contrôlées. SHA256 résultat : 04cb2f15d3b560649822921312976813d0c392982fbd26fde7fc14ba6f07521f.

Snes9x : 71 pages relues pour les 64 textes, bus de 874 plages (script, noms, pointeurs et copie haute), démarrage/Journal. Redirections et RAM diagnostiques, pas les parcours naturels ni transactions. Les choix visibles sont ceux de l’hôte du camp. Aucun handler modifié. Aucun test global des tables revendiqué.

Appliquer patches/DQVI-FR-DS-v0.41-BASE-JP-PARTIEL.bps sur la ROM JP intacte sans en-tête, SHA256 90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e, sans ancien patch préalable. Aucune ROM, SRAM ni sauvegarde d’état publiée.

Scènes naturelles 322/323,1836,4095, indices différés, alphabet accentué et fenêtres natives des tables restent ouverts. Projet non finalisé.

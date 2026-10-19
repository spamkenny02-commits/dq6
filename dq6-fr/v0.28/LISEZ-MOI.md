# DQVI FR DS v0.28 — PARTIEL

150 textes ajoutés : 5552 / 6957 sélections intégrées du script principal, 1405 restantes. Préparés non insérés : 0. Les 65 autres propositions examinées restent différées, sans augmentation du compteur. Les tables menus, noms, objets, sorts et combats restent distinctes. Version ExHiROM 8 Mio.

Appliquer patches/DQVI-FR-DS-v0.28-BASE-JP-PARTIEL.bps à la ROM japonaise intacte sans en-tête (CRC32 33304519), sans autre patch préalable. Aucune ROM n’est publiée. Résultat SHA256 cb669821ed8207538b1fb90e5c70e93a61d4331cd6117a6586641be53725f0d4.

Les correspondances et notes par texte sont dans revue-lot-v028.json. Dix-neuf adaptations explicites : indications de la tour, statut réel du récit de Méphisto, bouton bleu X, occurrences des noms, morts dans les oubliettes, français et ponctuation, réprimande après défaite, paix en cours de retour, amélioration du forgeron, don du bouclier, arrivée de l’allié, retour de Pierre, Pégase lui-même comme clef et régénération en combat. Aucun événement binaire du jeu n’est modifié par ces formulations.

Les 5402 sélections v0.27 sont inchangées, ainsi que les octets hors zones autorisées. BPS/IPS réappliqués, 6960 entrées redécodées et mauvaises sources rejetées. Snes9x : 870 groupes, 456996 octets vérifiés sur le bus, démarrage à froid jusqu’au menu Journal et 72 pages de onze messages relues. Noms variables et pagination observés. Les redirections de diagnostic ne valent pas parcours naturel ; les choix du camp à la fin de certains bancs ne sont pas ceux des scènes traduites. Captures, ROM et états restent locaux.

Reprise : python restore_sources.py puis REPRISE-AUTOMATIQUE.md. Recette idempotente dq6-fr/pass28.py ; delta lisible sources/lots/v0.28.json. Avec les sources locales : init.py, prepare.py, build.py puis verify.py sous v0.28. L’IPS est régénéré par build.py. L’insertion est limitée aux 150 IDs relus ; aucune correspondance automatique hors lot ne peut entrer. L’ouverture anonyme puis nommée de Tulipe (3256) et l’alias de Madame Soren (6804) sont traités explicitement.

Audits 322/323 et blocage 1836 toujours ouverts. L’IPS ancien, consulté comme source secondaire, comporte de nombreux textes décalés ou lacunaires et ne remplace pas la lecture japonaise. Aucun parcours complet, aucune relecture sémantique globale de l’héritage ni traduction finalisée des tables annoncés.

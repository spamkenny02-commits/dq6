# DQVI FR DS v0.26 — PARTIEL

100 messages ajoutés, soit 5252 / 6957 messages du script principal (1705 restants). Les menus, noms, objets, sorts et combats restent à auditer et traduire séparément. ROM actuelle : ExHiROM 8 Mio.

Appliquer patches/DQVI-FR-DS-v0.26-BASE-JP-PARTIEL.bps directement à la ROM japonaise intacte sans en-tête (CRC32 33304519), sans aucun patch préalable. Aucune ROM n'est publiée. L'ancien dquest6.smc modifié n'est pas une source de construction.

Le lot reprend 100 dialogues longs, notamment Mélankolia/Noirgibet, la famille du héros, Somnia, l'histoire de Cristal et les souvenirs de Sergueï et Svetlana. Les correspondances et adaptations sont documentées dans revue-lot-v026.json. Cinq adaptations explicites : direction vers la chambre des soldats à l'étage ; duel contre le champion au dernier rang du Gluodrome ; habitants sauvés par les sages ; enquête réelle distincte d'un rêve sur l'abbaye ; retrait d'un nom absent de la SFC.

Les 5152 sélections v0.25 sont inchangées. Les BPS/IPS se réappliquent et 6960 entrées sont redécodées. 870 groupes sont contrôlés dans Snes9x. Les essais de rendu ciblés utilisent des redirections de diagnostic vers le premier dialogue du camp, sans constituer une progression naturelle dans les scènes traduites. Les ROM, SRAM et états restent locaux.

Reprise : python restore_sources.py, puis lire REPRISE-AUTOMATIQUE.md. La recette dq6-fr/pass26.py est idempotente. Avec les sources locales, exécuter init.py, prepare.py, build.py et verify.py sous v0.26. Les sélections se restaurent également sans ROM par le delta lisible sources/lots/v0.26.json.

Audits 322/323 (tapis) et blocage de rendu 1836 toujours ouverts. Le compte des sélections ne prouve pas une validation sémantique globale du script hérité. Aucun parcours naturel complet ni garantie de traduction finalisée.

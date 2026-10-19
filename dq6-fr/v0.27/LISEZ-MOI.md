# DQVI FR DS v0.27 — PARTIEL

150 messages ajoutés : 5402 / 6957 sélections intégrées du script principal, 1555 restantes. Les tables menus, noms, objets, sorts et combats restent distinctes. Version ExHiROM 8 Mio.

Appliquer patches/DQVI-FR-DS-v0.27-BASE-JP-PARTIEL.bps directement à la ROM japonaise intacte sans en-tête (CRC32 33304519), sans autre patch préalable. Aucune ROM n’est publiée.

Le lot couvre des dialogues de villes et châteaux, le recrutement, les vocations et des souvenirs de personnages. Les correspondances complètes sont dans revue-lot-v027.json. Huit adaptations explicites conservent les faits SFC : but lucratif des informations de Friquet, niveau conservé au changement de vocation, nettoyage du marqueur DS, bonus de style +1 au lieu de +5, nom D3 dans le remerciement de Pierrick, repère de carte retiré de Morneville, vin caché et noms du héros absents de SFC. Les règles et événements binaires du jeu ne sont pas modifiés par ces formulations.

Les 5252 sélections v0.26 sont inchangées. BPS/IPS réappliqués et 6960 entrées redécodées. Snes9x contrôle 870 groupes et 445461 octets sur le bus. Démarrage à froid jusqu’au menu Journal, 39 pages de neuf dialogues et un rendu C0 avec Olivier vérifiés. Ces essais sont des redirections temporaires au camp, avec injection RAM pour le nom C0 ; ils ne valident pas un parcours naturel des 150 scènes. Captures, ROM et états restent locaux.

Reprise : python restore_sources.py puis REPRISE-AUTOMATIQUE.md. La recette dq6-fr/pass27.py est idempotente ; le delta lisible sources/lots/v0.27.json restaure les sélections sans ROM. Avec les sources locales : init.py, prepare.py, build.py puis verify.py sous v0.27. L’IPS peut être régénéré par build.py.

Sept autres correspondances examinées restent différées dans differes-passage-v027.json. Audits 322/323 et blocage 1836 ouverts. Le nombre intégré ne prouve pas une validation sémantique globale du script hérité ; aucun parcours complet ni traduction finalisée annoncé.

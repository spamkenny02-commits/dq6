# Dragon Quest VI FR — v0.40 partielle

5967/6957 messages intégrés, 40 nouveaux ; 990 restants. Aucun préparé principal ajouté. Tables séparées inchangées : 37 entrées FR confirmées, 25 lieux préparés. 8 Mio conservés.

Source principale : français DS fourni, japonais DS et SFC relus avec contexte ; ancien IPS secondaire. Revue explicite dans revue-lot-v040.json. Les 5927 anciennes sélections et 2512 noms sont inchangés. B5 lit le nom d’objet natif depuis 5A2A ; pas de changement machine. B2 et B5 restent des variables, sans figer les récompenses. BB est initialisé sur trois octets lors des essais. Le 6509 indique la valeur finale du style SFC, contrairement à la hausse indiquée en DS. 3127 garde le retour de l’argent préparé, sans affirmer la ruine du père.

Reconstruction : restore_sources.py, puis init.py, prepare.py, build.py, verify.py sous dq6-fr/v0.40. Recette pass40.py, base v0.39. Nouvelle revue de 40 IDs uniquement. Toutes les 6960 entrées redécodées, patchs BPS/IPS réappliqués sur la source intacte, mauvaises sources rejetées, zones protégées et anciens tokens contrôlés. SHA256 résultat : 64e3e434e4f6fed7a9b7865d59f3ce6271b905fc4220132764b781132b8af92f.

Snes9x : 874 plages et 507626 octets vérifiés sur le bus ; démarrage/Journal. 75 pages relues pour les 40 textes, plus 11 pages sur cinq textes avec un nom d’objet de 24 cellules. Le banc privé échange deux entrées de noms, sans changer la ROM publiée. Les noms d’objets restent encore anglais dans les tables ; ne pas confondre ces insertions du script et la traduction des tables. Pas de parcours naturel ni transaction, et pas tous les noms possibles testés.

Appliquer patches/DQVI-FR-DS-v0.40-BASE-JP-PARTIEL.bps directement à la ROM JP intacte sans en-tête, SHA256 90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e. Ne pas préappliquer un ancien patch. Aucune ROM, SRAM, sauvegarde d’état ni archive de ROM n’est publiée.

Restent notamment les scènes naturelles 322/323,1836,4095, les indices différés, 26 cas v0.34, l’alphabet accentué et les fenêtres natives des tables. Projet non finalisé.

# DQVI FR DS v0.32 — PARTIEL

5732/6957 messages intégrés, 1225 restants. Ce lot : 1 nouveau (1836), 0 correction ancienne. Depuis v0.28 : 180 nouveaux et 1 correction isolée (323). Tables : 33 lieux PREPARE_NON_INSERE, 0 insertion nouvelle. ROM 8 Mio, SHA256 f92d0de32c6af93eb1628ebf13597a22308e65d889ad43db6b3ec0b59c01aea5.

1836 : japonais SFC et japonais DS 0060:84–85 relus ensemble ; ancien IPS consulté comme source secondaire. La VF DS omet B2 dans la première réplique et modifie les motivations dans la seconde. Adaptation fidèle : abandon, puis décision laissée à B2, avec ordre natif B2/D3/B2. Boss est le nom DS de スラッジ. Le deuxième nom B2 n'était pas visible dans l'ancien banc de trois pages. Il apparaît sur la quatrième page du nouveau texte à pagination explicite. Ce résultat ne démontre pas la cause précise de l'ancien échec. Aucun code moteur modifié.

Snes9x : six pages capturées et relues, Rookie (B2) page 1, AM (D3) page 3, Rookie (B2) page 4, puis choix hôte et message hôte suivant. RAM 5A28=0930 injectée uniquement dans le diagnostic. Redirection depuis le camp, pas la scène naturelle du recrutement. Journal vérifié au démarrage. BPS et IPS réappliqués, mauvaises sources rejetées, 6960 entrées redécodées, 5731 anciennes sélections et zones protégées inchangées, tout le script contrôlé sur le bus.

Sources restaurables par python restore_sources.py, recette idempotente pass32.py, delta sources/lots/v0.32.json. Le lot utilise les templates compilateurs v0.30 avec baseline de données v0.31 pour ne pas réappliquer la correction 323 ; celle-ci est conservée intégralement. Reconstruire init/prepare/build/verify dans v0.32. Patch BPS sous patches/ ; aucune ROM, SRAM ni état distribué.

322/323 et 1836 sont corrigés ou intégrés avec essais diagnostiques explicites. Leurs parcours naturels restent à vérifier. 5351/5341 et les nouveaux-cas-differes v0.30 restent ouverts. Les tables n'ont aucune nouvelle insertion ; lire inventaire v0.29. Projet partiel.

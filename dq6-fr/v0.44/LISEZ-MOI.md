# DQVI FR v0.44 — correction native isolée

6165/6957 messages intégrés, aucun nouvel ajout principal, 792 restants. Projet non finalisé, ROM de travail 8 Mio.

L'arbre Huffman VF ne proposait pas C4/DF. Deux feuilles rares D6/E1 sont scindées et la racine relocalisée ; tous les autres chemins de bits restent identiques. Tous les anciens tokens restent identiques. Le vecteur C4 retrouve la fonction originale japonaise C6927B. Quatre chaînes grammaticales sont adaptées séparément des 37 libellés français confirmés des tables. Le nom du sac 09C8 reste une donnée de sauvegarde : son emplacement ROM vide est intentionnel.

Recette idempotente pass44.py, puis init.py/prepare.py/build.py/verify.py. Restauration par restore_sources.py. 6960 messages redécodés, 6165 sélections inchangées, 2508/2512 noms identiques à v0.43, quatre différences explicites. BPS/IPS réappliqués à la source JP intacte et mauvaises sources rejetées. Arbre/vecteur et zones protégées contrôlés.

Snes9x : bus 880 plages / 516965 octets ; démarrage et menu Nouveau jeu ; 30 pages relues sur sept anciens messages, quatre sondes natives, trois branches plurielles forcées. Ce sont des diagnostics au camp, pas les scènes naturelles. Les sondes ne valident pas le calcul réel du nombre de compagnons. Aucun plantage pré-correction observé : l'encodage C4 échouait avant le lancement de l'émulateur.

SHA256 résultat : 289634cf8ccf362c9e11e645a6633154d91674a12b06d8c5acfc68846a8f3d1a. Patch BPS sur source JP sans en-tête, SHA256 90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e. Aucune ROM ni sauvegarde publiée.

Restent ouverts : scènes naturelles 322/323, 1836, 4095, indices ambigus, tables et leurs fenêtres/accents, 24 cas historiques différés.

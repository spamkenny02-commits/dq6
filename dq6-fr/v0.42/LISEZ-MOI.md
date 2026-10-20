# Dragon Quest VI FR — v0.42 partielle

6102/6957 messages intégrés, 71 nouveaux ; 855 restants. Aucun préparé principal nouveau. Tables inchangées : 37 entrées françaises confirmées, 25 lieux préparés. Toujours 8 Mio.

71 ajouts : utilisation, appréciation, équipement, transfert, abandon et rachat d’objets. Noms natifs B5 et rôles C0/C1/D3 explicitement liés ; la garde d’ambiguïté du compilateur ne s’ouvre que si tous les rôles contextuels sont liés par la revue. Contrôle indépendant de chaque occurrence conservé. 5917 garde ses deux C1, comme les deux japonais, sans réduire silencieusement la répétition. Objet et prix du marchand restent variables. Les objets fixes des descriptions DS sont remplacés par le B5 SFC, sans nom figé ni effet d’objet inventé.

Français DS fourni comme source principale, japonais SFC/DS et contexte relus, ancien IPS secondaire souvent décalé. Revue explicite revue-lot-v042.json. Les 6031 anciennes sélections et les 2512 noms sont inchangés. Aucun handler modifié. Recette idempotente pass42.py, base v0.41. Restaurer par restore_sources.py, puis init.py, prepare.py, build.py et verify.py sous dq6-fr/v0.42. Périmètre limité aux nouveaux IDs relus. BPS/IPS réappliqués à la source intacte, mauvaises sources rejetées, 6960 entrées redécodées, zones protégées et occurrences natives contrôlées.

SHA256 résultat : 47f3b81eff2ec6aa0b0a733230bce976cb4d64288f22d0162ee7241f585398db.

Snes9x : 99 pages de diagnostic relues pour les 71 textes ; bus de 874 plages et 508401 octets ; démarrage/Journal. 14 pages supplémentaires sur huit textes avec un nom d’objet de 24 cellules. Valeurs distinctes observées : C0 Emilie, C1 Olivier, D3 AM, B2 Gus, BB 12345. La permutation de deux noms est limitée aux bancs privés, pas la ROM publiée.

Limites : Redirections au camp et RAM diagnostique. Ni les scènes naturelles, ni les calculs d’effets, ni les transactions réelles, ni tous les noms possibles testés. Les choix visibles sont ceux de l’hôte ; tables encore partiellement anglaises.

Appliquer patches/DQVI-FR-DS-v0.42-BASE-JP-PARTIEL.bps directement sur la ROM JP intacte sans en-tête, SHA256 90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e. Aucun ancien patch préalable. Aucune ROM, SRAM, sauvegarde d’état ni archive de ROM publiée.

Scènes naturelles 322/323,1836,4095, indices différés, 26 cas v0.34, alphabet accentué et fenêtres natives des tables restent ouverts. Ne pas annoncer finalisé.

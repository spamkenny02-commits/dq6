# Dragon Quest VI FR — v0.43 partielle

6165/6957 messages intégrés, 63 nouveaux ; 792 restants. Aucun préparé principal nouveau. Tables inchangées : 37 entrées françaises confirmées, 25 lieux préparés. Toujours 8 Mio.

63 ajouts : cris, répliques courtes, noms variables de sorts et de vocations, appels aux compagnons. 6414 conserve deux C0, 6416 deux C0 et B2, 6441 deux C0 puis D3 ; 5281 deux C9. Noms de locuteurs natifs conservés. Les 26 cas différés historiques v0.34 sont réconciliés : 2368 et 6265 résolus explicitement en v0.41, 24 encore différés. Le reliquat reproductible compte 792 textes non validés et sépare les propositions de mots des validations.

Français DS fourni comme source principale, japonais SFC/DS et contexte relus, ancien IPS secondaire souvent décalé. Revue explicite revue-lot-v043.json. Les 6102 anciennes sélections et les 2512 noms sont inchangés. Aucun handler modifié. Recette idempotente pass43.py, base v0.42. Restaurer par restore_sources.py, puis init.py, prepare.py, build.py et verify.py sous dq6-fr/v0.43. Périmètre limité aux nouveaux IDs relus. BPS/IPS réappliqués à la source intacte, mauvaises sources rejetées, 6960 entrées redécodées, zones protégées et occurrences natives contrôlées.

SHA256 résultat : 118b388a0132150969fde5810ab4c6ca374fe09ccf42f35b7f8b57744b2d4a03.

Snes9x : 68 pages de diagnostic relues pour les 63 textes ; bus de 874 plages et 508443 octets ; démarrage/Journal. 68 pages cibles relues pour les 63 textes. Le protocole initial avait déjà avancé à la réponse du camp pour 21 textes très courts ; ces captures ne comptent pas comme validation. Reprise contrôlée avant la confirmation A du choix hôte, même ROM, puis contrôle du message cible 100. Rapports initial, correction et rapport final fusionné conservés. Maitre des Combats, Crame, Emilie, AM et Gus observés ; pas changement machine.

Limites : Redirections au camp et RAM diagnostique. Ni les scènes naturelles ni toutes les valeurs de noms ou branches ni les transactions réelles. Les 21 recaptures font partie des 68 pages finales, pas 21 nouveaux textes. Tables inchangées, alphabet accentué et fenêtres natives encore à traiter.

Appliquer patches/DQVI-FR-DS-v0.43-BASE-JP-PARTIEL.bps directement sur la ROM JP intacte sans en-tête, SHA256 90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e. Aucun ancien patch préalable. Aucune ROM, SRAM, sauvegarde d’état ni archive de ROM publiée.

Scènes naturelles 322/323,1836,4095, indices différés, 24 cas encore différés sur les 26 cas historiques v0.34, alphabet accentué et fenêtres natives des tables restent ouverts. Ne pas annoncer finalisé.

# DQVI FR v0.46 partielle

6387/6957 messages intégrés, 111 ajouts, 570 restants dont 11 fragments préparés et 150 brouillons non insérés. Projet non finalisé. Tables : 37 libellés français confirmés, quatre aides grammaticales v0.44, 25 lieux préparés. ROM de travail 8 Mio.

111 ajouts : commerces, achats/reventes, banque, Journal, vocations, compagnons, noms et concours. B3/C0/C9/D3, B2, BB, B5 et D8 restent variables. 66 formulations DS relues/adaptées ; 45 adaptations directes SFC sans équivalent DS validé. Aucun rapprochement flou seul admis. Onze fragments préparés non insérés en attente de test d’assemblage ; 150 brouillons de libellés techniques/progression sauvegardés séparément, sans validation d’insertion.

Japonais SFC, contexte voisin et ancien IPS secondaire conservés dans chaque revue ; références japonaises/françaises DS explicites quand valables. Le reste est traduit directement du SFC, sans prétendre à une correspondance DS. Achats et reventes, dépôt et retrait, accueil temporaire et séparation définitive sont distingués. La consigne de concours suit le présentateur sur scène SFC, pas l’agent DS près de la porte. BB et noms C0/B3/C9/D3/B2/B5/D8 restent natifs, sans nom figé. Journal/Options, retrait des crédits et cadre du nom conservés.

6276 anciennes sélections identiques, 6960 entrées redécodées, 2512 noms, Huffman et vecteur C4 identiques à v0.45. Commandes, occurrences, zones protégées, réapplication BPS/IPS à la source intacte et rejet de mauvaises sources contrôlés. Restauration propre et reconstruction identique vérifiées. Recette pass46.py, puis init.py/prepare.py/build.py/verify.py.

Snes9x : 166 pages ciblées relues pour les 111 ajouts, un stress B5 24 cases, bus des 870 placements courants plus noms/moteur, 880 plages/519830 octets, démarrage/menu Nouveau jeu. 110 messages capturés sur le premier binaire avec tokens, police, noms et moteur identiques ; 6472 raccourci puis recapturé sur le binaire final. Les deux captures initiales chevauchées sont rejetées. Diagnostics au camp, aucune scène naturelle ou transaction réelle validée par ces captures. Les valeurs injectées ne prouvent pas les calculs, les sauvegardes ou les changements de noms.

SHA256 résultat : 5c58c12eabce2edbe039f6028e7742493b77e0403ebe08b5430d5241641516ca. BPS sur JP sans en-tête SHA256 90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e. Aucune ROM, SRAM, sauvegarde d’état ou archive de ROM publiée.

Le contrôle bus hérité utilisait un ancien catalogue de plages : il comparait réellement leurs octets, mais les positions n’étaient pas actualisées. Nouveau contrôle de tous les placements v0.46 et contrôle rétrospectif v0.45 conservés dans les rapports.

Ouverts : assemblage 5820/5821 avec5822/5823 et5832 avec5833..5839 ; scènes naturelles322/323/1836/4095 ; 16 différés historiques v0.34 ; indices, tables, fenêtres et alphabet accentué. Voir qa-reliquat.json et prepares-non-inseres-v046.json.

# DQVI FR v0.63 — fin des dialogues de combat usuels et postgame

191 entrées du pool qualifiées dans ce lot :188 traductions de l'anglais,2 corrections françaises (4/5),1 fragment de parole497. Les191 ne sont pas191 nouvelles phrases autonomes. Le registre passe de395 à586 entrées françaises qualifiées. Les13 textes JP valides différés et5 emplacements VF hors frontière source restent séparés ;4 structures sans texte ne sont pas traduites. Zéro préparation supplémentaire non insérée.

Le principal reste à6957 sélections (6948 linguistiques et9 structures). Noms2512SIDs,2048 entrées physiques,464 alias,39 françaises+4 aides grammaticales et16 noms composés inchangés.25 lieux préparés. Le reste des tables doit toujours être qualifié : ces nombres ne prouvent pas tous les menus et noms français. La relecture exhaustive du principal reste0 ; le présent lot est une première revue de traduction du combat.

## Revue et corrections

plans.py donne chaque adaptation explicite ; insertion-combat.json porte les hashes source/ancien, la formulation encodée, les références DS et les réserves. Les concordances complètes sont japonaises normalisées, sans score flou ; les compositions DS265/416,les recrutements Tulipe et le postgame0099 ont des références séparées avec empreintes. Les rôles et commandes SFC prévalent sur les variantes DS. Le gag539 reste de mauvais coups, le jeu456 reste coquin SFC ; ne pas importer les réécritures DS. La forme de vieillard564 et la menace565 sont traduites directement du japonais.

Le lot comprend les dialogues Mortamor/Nokturnus566–602,quantités littérales578/9999/753 et sorts Mégabang/Mégaltération/Protection/Décuplo selon DS. Les deux Protection sont deux messages natifs distincts.591 garde le segment de colère SFC absent de la variante DS.592 garde la grande main SFC malgré les griffes DS.

26 anciennes séquences de commandes VF sont corrigées explicitement vers JP, toutes listées dans verification.json et delta-combat-v063.json. Notamment326 retrouve1 littéral sans BB,418 garde AF,265 retrouve les trois noms et deux fenêtres,568 retrouve un seul C2. Les AD de mise en page deviennent des espaces. Variables,pauses,AF,C2,BC/BD et fins AC/AE restent conformes au japonais borné. Les accords de genre sont évités pour les noms variables.

## Réserve nouvelle de frontière source

Le pool JP commence à0x36DEBD selon ses pointeurs relatifs. Le dernier message valide602 finit à0x37175B,limite déjà déclarée par tools/combat-v058/codec.py et début de la zone du script principal compressé. Le premier pointeur principal source est relatif7. Le lecteur historique v057 lisait malgré cela608 entrées : ses603–607 interprètent des données du script compressé comme des messages natifs. audit-frontiere-source.json reproduit les bornes et hashes sans publier ces données ; source_guard.py compare les603 entrées valides aux hashes historiques et rejette la préparation de603.

Il y a603 entrées JP bornées,599 avec texte et4 structures. La VF contient608 emplacements parsables ; les cinq derniers restent opaques et inchangés. Leur origine et leurs appelants doivent être audités. Ils ne sont ni comptés comme japonais traduisible établi,ni déclarés vides,structurels,inutilisés ou corrigés. Les diagnostics des608 pointeurs VF prouvent leur lecture,pas l'existence de608 textes japonais.

Les13 autres réserves (27,35,36,54,55,60–64,76,77,277) concernent appels techniques,C6,XP,statistiques,0C,AC/AE et compositions de rang. Voir blocages-restants.json.

## Reconstruction

```
python restore_sources.py
python dq6-fr/v0.63/prepare.py --jp /chemin/source-intacte.sfc
python dq6-fr/v0.63/build.py --jp /chemin/source-intacte.sfc --out /chemin/prive
python dq6-fr/v0.63/verify.py --jp /chemin/source-intacte.sfc --out /chemin/prive
python dq6-fr/v0.63/audit_source.py --jp /chemin/source-intacte.sfc
python dq6-fr/v0.63/inventory.py --rom /chemin/prive/result.sfc
```

La recette applique le BPS v0.62 dont le hash est vérifié,puis reconstruit les608 emplacements VF en ne modifiant que191IDs. Allocation nouvelle hors870 groupes du principal et moteur v0.61. Les417 autres emplacements,dont395 qualifiés et cinq opaques,restent identiques. Tous les noms et segments moteur,police,dictionnaire et cadres restent identiques.8Mio conservés. verify redécode les191,réapplique BPS/IPS,reproduit la ROM,rejet des sources incorrectes et contrôle des octets protégés/sommes SNES.

## Essais et limites

qa-emulator.json distingue190 messages autonomes,66 variantes avec noms longs/distincts,et16 compositions496/497/498 avec les deux choix RNG forcés dans les seules fixtures privées. Le fragment497 est relu dans ces16 compositions et n'est pas validé isolément. B4=1/2 désigne les espèces natives ; B3=1/2 est un sélecteur et non un SID. Les noms anglais hérités utilisés pour tester les largeurs ne deviennent pas des noms français qualifiés. Les captures intermédiaires des dialogues à plusieurs BC/C2 sont relues en plus des finales.

Lecteur CPU608,pointeur volontairement décalé ID8,bus1485 plages et démarrage neuf menu Journal sont contrôlés séparément. Un seul émulateur à la fois. Les rendus utilisent une redirection de camp et le rafraîchissement privé des sept tuiles d'accents de l'ancien état. Les16 branches déterministes ne prouvent pas toutes les combinaisons du RNG naturel. L'état,les ROM et les captures restent privés ; leurs hashes et la recette sont publiés.

Aucun parcours naturel de ces combats,recrutements ou fin de jeu n'est déclaré validé. Noms joueur,fenêtres compactes,autres tables,relecture exhaustive,audits principal322/323,1836,4095,610/1135/2404/5341/5351 et réserves nouvelles restent ouverts. Le projet n'est pas finalisé.

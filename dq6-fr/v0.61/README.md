# DQVI FR v0.61 — trois messages de combat, mots et sorts composés

Ajouts natifs464,465,498 : les107 identifiants manquants de l'inventaire initial sont maintenant traduits et insérés. Cela ne termine pas le combat :497 textes hérités restent à qualifier et relire ; quatre entrées sont structurelles. Le principal reste à6957 sélections, dont6948 linguistiques et neuf structures. Relecture exhaustive principale enregistrée : zéro.

## Revue et adaptation

Le shiritori japonais emploie quatre mots qui finissent parン et provoquent la défaite immédiate. La DS française le remplace par des virelangues et retire le mot variable. Ici, adaptation explicite en jeu de rimes : les quatre choix B2 et les deux noms B7 de la SFC restent variables, et l'acteur perd faute de rime. Le texte ne prétend pas que ces mots français finissent par une même lettre. Ce choix conserve la mécanique et le ressort comique SFC.

Les entrées contextuelles DS b1005000.mpt349/351 donnent Braséria et Céleste pour les SIDs036A/0369. « Dragon » serait une traduction générique sans tenir compte du mot utilisé dans cette scène. Ces deux noms physiques uniques sont remplacés ; les2510 autres SIDs gardent leurs octets,2048 entrées physiques et464 alias sont conservés.

Le sort inventé reste la composition des messages497 et498 et de deux choix natifs indépendants, sans modifier le vrai sort061F/Blaze. Les16 noms français complets de la DS ne se factorisent pas en quatre préfixes et quatre suffixes. La recette ajoute donc une table locale de16 chaînes et une chaîne vide, accessibles seulement par les SIDs virtuelsFF00..FF10 du lecteur B2. Le premier B2 est vide ; le second affiche le nom complet correspondant aux deux choix. Les deux appels natifs RNG, les deux appels de messages et la commande AE sont conservés ; la sortie restaure A, X, Y et5A28 attendus. Aucun octet de travail WRAM n'est réservé.

Douze noms japonais correspondent exactement. Pour les quatre autres, バキ SFC etバギ DS restent une différence explicitement documentée : même scène de sort inventé, même ligne du produit cartésien, quatre suffixes identiques et douze autres paires exactes. Le choix des quatre noms DS est une adaptation contextuelle relue, pas une identité japonaise ni un simple score flou. Références et empreintes dans revue-combat-v061.json.

## Modification localisée du moteur

pair_engine.py remplace seulement C69209 (LDA5A28) par un renvoi via le remplissage libre C6FEF0. L'entrée partagée C6920C et tout le lecteur C6FDF0 restent identiques. Les B2 ordinaires suivent l'ancien chemin. Les SIDs virtuels fournissent un pointeur au même lecteur d'octets/dictionnaire C6FE02. L'appelant C26759 rejoint une routine locale qui mémorise le premier choix sur la pile, effectue le second tirage, puis revient au RTS original C26785. Tables source, RNG original, police et dictionnaire inchangés. Les gardes rejettent un appelant, un hook ou un remplissage modifié.

Toute future allocation doit protéger à la fois placement et engine.allocation du build-report.json, en plus des groupes du principal.8Mio conservés.

## Reconstruction

Depuis la racine du dépôt, restaurer toutes les sources avec python restore_sources.py. Puis, avec JP intacte et son empreinte vérifiée :

```
python dq6-fr/v0.61/prepare.py --jp /chemin/source.sfc
python dq6-fr/v0.61/build.py --jp /chemin/source.sfc --out /chemin/prive
python dq6-fr/v0.61/verify.py --jp /chemin/source.sfc --out /chemin/prive
python dq6-fr/v0.61/inventory.py --rom /chemin/prive/result.sfc
```

prepare contrôle les références DS et les anciennes commandes, build est déterministe, verify réapplique BPS/IPS, redécode toutes les nouvelles chaînes et rejette les mauvaises sources et trois mutations de garde. Les605 autres messages natifs,870 groupes du principal,2510 autres noms et464 alias sont comparés, et toutes les modifications sont limitées aux zones autorisées.

## Tests et limites

Snes9x :608 pointeurs/lectures natives et mutation attendue surID8 ;2477 SIDs statiques lus par le CPU (35 SIDs dynamiques exclus du test de pointeurs fixes) ;2512 noms vérifiés sur fichier.29 diagnostics de rendu :16 paires forcées, quatre mots natifs, trois B2 ordinaires, une exécution avec les deux appels RNG originaux et cinq profils homonymes plus longs. Retour des API et registres de sortie vérifiés ; noms complets, accents et fin des phrases relus sur les captures finales, ainsi que l'introduction464. Les captures restent privées.

Les diagnostics utilisent un état de camp et une redirection privée, avec rafraîchissement des sept tuiles accentuées que cet ancien état conserve. Pour appeler directement les sous-routines de scène depuis le banc, leur RTS devient RTL dans les fixtures seulement. Les16 paires forcées remplacent deux appels RNG par des stubs privés ; le test random conserve les deux vrais appels. Le RTS et les deux RNG du patch de production restent natifs. Le test indépendant de démarrage neuf charge les256 tuiles depuis la ROM, sans injection. Bus ROM et démarrage jusqu'au menu Journal contrôlés.

Le premier lecteur candidat utilisait une valeur chargée en X au lieu de la constante #$00BA : il corrompait le contexte et ne revenait pas. Il a été rejeté avant publication ; le rapport négatif est conservé. Ce résultat ne valide aucun texte et ne fait pas partie des29 réussites.

Aucun combat naturel complet ni fenêtre compacte n'est validé. Le forçage des16 branches ne prouve pas l'accessibilité conjointe des16 paires avec le RNG naturel. Noms de joueur, consommateurs de SIDs codés en dur, autres tables,497 textes hérités, recherche exhaustive, relecture intégrale et audits historiques restent ouverts. Le projet n'est pas finalisé.

# v0.80 — révisions1003,1012,1252 et représentation1179

Base publiée v0.79 ab302ae56e260770bb3a000013b6572c06cac565. Sources reattachées(3), trois SHA256 vérifiés. Ancien workspace absent ; verrou flock exclusif dans le workspace courant pendant mutations/tests/publication.

1003 : とりあげられ signifie retirés/confisqués. « Sont rendus » hérité du français DS893 pouvait suggérer restitution volontaire ; « sont confisqués » suit SFC/DS japonais. Texte générique sans variable ajouté : les tokens publiés n'avaient déjà pas D3 malgré la source JP ; aucune restauration D3 inventée ici. 1012 : しかたない…やるか? devient « On n'a pas le choix… On y va? », avec le temps présent.1252 : ponctuation et ordre de l'apposition « Escortez-nous, ma reine et moi, … ». JP/FR/IPS et références DS exactes relus ; prepare vérifie dix champs JA/FR directement dans la ROM DS.

Les lignes remplacées sont uniques ; aucun token de commande, variable, rupture, pagination ou terminaison ajouté/supprimé.1003 conserve AF mais place « Retour aux cellules. » entier sur sa deuxième page. Trois groupes Huffman réencodés avec arbre existant ; groupes125 et156 relocalisés dans des intervalles libres sans croisement de banque, hors toutes allocations vivantes et réserves noms/menus/combat/moteur. Groupe126 en place. Les6957 autres slots techniques et867 autres groupes restent identiques.8Mio, tables et polices inchangées. Lire verification pour rejets mauvaises sources et mutations négatives pointeur/allocation.

1179 est un audit distinct : la source lisible portait U+E000 alors que le token compilé était C9. metadata-1179.json corrige texte/lignes en U+E0C9 seulement. Redécodage indépendant et deux pages Snes9x avec AAAAAAAA confirment C9 inchangé et rendu sans débordement observé. Deux champs DS347 vérifiés depuis ROM. Le contexte naturel de Judith n'a pas été joué.

## Reconstruction

Depuis le dépôt restaurer tous les lots par `python restore_sources.py`. Lancer prepare.py avec --jp/--ds/--ips vers les trois sources intactes, puis build.py et verify.py avec --jp et --out vers un répertoire privé. audit1179.py prend --jp/--ds/--out. current_main_selection superpose v079 puis v080 et metadata1179 à la basev056. Ne pas utiliser la seule sélectionv056 comme état actuel.

## Tests exécutés

Démarrage froid Snes9x,4016plages/573871octets relus sur bus réel,256glyphes résidents et Journal inchangé.6pages diagnostiques après et6avant ; toutes relues visuellement, seules quatre captures diffèrent,les deux premières pages1252 sont identiques. Deux pages supplémentaires1179 relues avec nom8lettres. Redirection du dialogue100 dans une copie privée depuis le camp créé par nouvelle partie ; aucune injection WRAM/VRAM. La sélection Oui/Non affichée appartient au camp hôte, pas à la scène cible. Les scènes naturelles de confiscation/combat/retour du roi ne sont pas validées par ces essais.

Le BPS public est réappliqué à la JP intacte ; IPS privé régénéré/réappliqué. Recette idempotente et restauration depuis contenu publié contrôlées par rapports séparés. Aucun ROM,état,SRAM ni archive de ROM publié.

## Progression

0traduction nouvelle,3révisions préparées résolues,0nouvelle position exhaustive. Script principal6948textes+9structurelles=6957sélections. Table2048positions examinées/2512SIDs/464alias,367FRqualifiées,419propositions restantes ; aucune modification de table ici. Combat608slots :597qualifiés,2préparés,5opaques,4structurels.118révisions principales préparées restantes.900positions400–1299 relues préparatoirement,0passe exhaustive finale acceptée. GlyphesÀ/Ç/œ,audits hérités,scènes naturelles et recherche exhaustive des oublis restent ouverts.

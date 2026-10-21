# Combat-v059 — lecteur natif vérifié, police encore à relever

Le lecteur byte natif de la ROM a réellement exécuté les608 identifiants sous Snes9x, après déplacement du pool dans une zone libre ExHiROM mesurée indépendamment des870 groupes Huffman. Tous les pointeurs et premiers octets correspondent. Un pointeur volontairement décalé pour l’ID8 est détecté précisément. Les routines natives C027B0/C027FF restent inchangées ; seule l’entrée de dialogue est redirigée dans la ROM privée de test. La boucle remet le mode de buffer à zéro et s’arrête après son marqueur de fin, avant tout retour au jeu.

Ce test vérifie l’adressage et les positions0..7 dans les76 groupes. Il ne lit pas à l’écran les608 messages complets, ne valide ni les variables, ni les commandes, ni la police, et n’insère aucun des107 textes préparés. ROM, état et mémoire de diagnostic restent locaux ; seuls scripts, empreintes et rapports sont publiés.

## Corriger la portée du contrôlev058

Le modèle v058 utilise la table C11100 du lecteur Huffman. Le dessinateur byte natif C029B0 additionne0300 au byte et combine les attributs1000 pour écrire une tuile ; il ne passe pas par cette table. Ses43 allers-retours sont donc seulement algébriques. Les64 propositions contenant des caractères absents du modèle ne prouvent pas l’absence de ces accents dans la police native. Ne pas conclure définitivement sur les glyphes7A/81 depuis la seule table Huffman.

La petite police résidente a été aperçue en mémoire vidéo lors du passage précédent, mais aucune carte de glyphes en contexte de combat n’est encore validée. Il faut la relever avant de fabriquer un encodeur de production ou d’étendre l’alphabet.

## Reproduction

Après `python restore_sources.py` et avec le cœur Snes9x documenté :

```sh
python tools/combat-v059/native_probe.py --jp /chemin/source-intacte.sfc --camp /chemin/v026-camp.state --runner /chemin/emulator-tests/run_core.py
python tools/combat-v059/native_probe.py --jp /chemin/source-intacte.sfc --camp /chemin/v026-camp.state --runner /chemin/emulator-tests/run_core.py --mutate-pointer
```

La seconde commande attend exactement le défaut injecté et enregistre son rapport dans un fichier privé au niveau racine. La première remplace le rapport positif. Les ROM temporaires sont supprimées après le test ; les états créés par run_core restent privés. Ne jamais publier cette ROM de diagnostic comme version jouable.

## Reprise et limites

Les107 propositionsv057 restent PREPARE_NON_INSERE :105 relues,2 réserves464/465 (shiritori remplacé par virelangue dans la DS ; B2 et deux B7 doivent être conservés dans la SFC). Aucun nouveau texte, aucune insertion, patchv0.56 inchangé,6957 sélections du principal dont9 structures. La relecture exhaustive du principal reste à0 entrée enregistrée.

Le passage précédent avait sauvegardé deux états privés sans ROM dans cette conversation sous DQVI-etats-tests-prives-059.zip : un point obtenu par entrées de jeu depuis le camp jusqu’au chemin de montagne, puis une copie de diagnostic avec flag WRAM3D3F modifié0C→2C pour contourner la quête du maire. Cette copie ne valide pas la quête naturelle. L’espace local a ensuite été réinitialisé ; l’archive existe dans les fichiers de cette conversation, mais son outil de lecture n’est pas exposé dans ce passage. Ne pas prétendre l’avoir récupérée ni être déjà en combat. Le transfert privé de l’archive des ROM avait échoué avant transfert faute d’authentification ; les ROM ne sont toujours pas garanties après réinitialisation.

Suite : retrouver ou obtenir un état avant combat, relever la police native, établir les valeurs B2 de465, préparer lignes/pagination et tester le rendu avant insertion. Les497 textes de combat hérités, autres tables, recherche des oublis, relecture complète et audits naturels restent ouverts.

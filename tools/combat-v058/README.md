# Contrôle du codec de combat — combat-v058-codec

Ce point ne crée aucune version ROM : patch v0.56 inchangé, zéro nouvelle traduction, zéro insertion. Les107 propositions de combat-v057 restent préparées non insérées (105 relues,2 réserves464/465). Le principal reste6957 sélections dont9 structures ; aucune nouvelle entrée de sa relecture exhaustive.

## Résultats reproductibles

Le codec strict lit l’alphabet et le dictionnaire de la ROM reconstruite depuis le BPS public et la source japonaise intacte vérifiée. Il ne réutilise pas l’encodeur Huffman. 43 propositions font un aller-retour textuel exact ;64 sont rejetées pour accents absents de l’alphabet byte sûr. Aucun accent n’est supprimé ou remplacé. `qa-codec.json` donne les IDs et les caractères manquants. Les réserves sémantiques restent distinctes.

11 mutations sont rejetées : source erronée, ROM modifiée, accent sans encodage, lettre PM fantôme, code de dictionnaire pris pour variable, macro DS, terminaison interne/manquante, pointeur hors zone, groupes superposés, terminaison perdue. Les76 groupes/608 messages restent bornés et sans alias physique ;11722 octets. Les870 groupes Huffman sont mesurés indépendamment pour exclure leur écrasement dans les expériences privées.

Attention : l’ancienne documentation anglaise est incompatible avec la police VF actuelle. Le tableau de glyphes donne `!` via byte7A/glyphe0241 et l’ellipse via byte81/glyphe0246. Les43 allers-retours sont des candidats d’encodage, pas une preuve de rendu. Les bytes0C..0F restent exclus comme lettres ordinaires, malgré leur apparence dans la table. Les autres bytes non approuvés des textes hérités sont inventoriés sans les réinterpréter.

## Snes9x réellement exécuté

Le bus ROM correspond sur608 plages de messages et11722 octets du patch inchangé. Un démarrage de300 images atteint ENIX PRESENTS. L’expérience privée redirigeant le camp vers le lecteur/afficheur byte natif atteint l’ID51 mais ne donne aucune fenêtre lisible : capture rejetée, zéro nouveau texte validé au rendu. `diagnostic_fixture.py` conserve la recette de cet échec pour diagnostic, et ne doit jamais servir de preuve d’insertion ni être publiée sous forme de ROM. Des essais intermédiaires d’ouverture de fenêtre ont aussi été rejetés. Il faut obtenir un état de combat et établir le contexte de fenêtre naturel avant de poursuivre ce test.

## Reproduction

Après restauration depuis Git :

```sh
python tools/combat-v058/verify.py --jp /chemin/source-intacte.sfc
python tools/combat-v058/bus_layout.py --jp /chemin/source-intacte.sfc --out /chemin/prive/bus.json
```

Le premier contrôle n’écrit aucune ROM. Le second ne produit que des adresses/longueurs pour `run_core.py --check-layout`. Pour reproduire l’expérience rejetée seulement : `diagnostic_fixture.py --jp ... --id 51 --out /chemin/prive/fixture.sfc`, puis le protocole camp : A pendant1 image sur4,330 images d’attente. Les ROM, SRAM, états et captures restent locaux ; seuls rapports, empreintes et recettes sont publiés.

## Prochain travail

Établir un alphabet byte accentué sans modifier les anciens consommateurs (noms, menus, contrôles, dictionnaire), avec preuve de non-régression ; sinon conserver les64 propositions bloquées. Résoudre464/465. Tester les43 candidats en contexte natif de combat avec noms/variables, pauses B1, BC/BD/C2, pagination et largeurs avant toute insertion. Relire les497 textes hérités puis compléter les autres tables, rechercher les ressources oubliées, relire intégralement le principal et terminer les audits naturels. Aucun blocage n’est clos par ce seul contrôle technique.

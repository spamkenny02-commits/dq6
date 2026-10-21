# Préparation du pool de combat — combat-v057

Point de reprise, sans nouvelle version ROM : le patch reste v0.56.

107 propositions françaises PREPARE_NON_INSERE pour les107 identifiants sans texte du pool séparé de608 entrées. 105 propositions relues japonais/français/contexte disponible ; deux adaptations de jeu de mots, IDs464/465, restent réservées. 85 propositions ont une référence DS explicite ;22 reposent sur le japonais SFC sans correspondance DS établie. L’ancien IPS n’est pas une validation.

Aucun texte intégré, aucun nouveau patch, aucune scène Snes9x exécutée. Le codec de ce pool diffère du script principal : encodage, accents, largeurs, pauses B1, commandes BC/BD/C2 et liaisons des variables doivent encore être prouvés en combat. Les497 textes hérités et4 structures restent inchangés. Les105 relectures linguistiques ne sont pas des validations d’insertion.

## Reproduction locale

Après `python restore_sources.py`, exécuter :

```sh
python preparations/combat-v057/prepare.py --jp /chemin/vers/source-intacte.sfc
python preparations/combat-v057/verify.py --jp /chemin/vers/source-intacte.sfc
```

Le générateur vérifie la source japonaise par SHA256 et les références DS restaurées. Le rapport vérifie l’idempotence, l’ordre et le nombre des commandes natives hors AD de mise en lignes, les terminateurs et six rejets de mutations. Le BPS public v0.56 est réappliqué en mémoire à la source intacte ; son résultat reste e14ebc5611642b229edd3e7becae27813c823ef8182e2d06058953d593f2375d. Aucune donnée ROM brute n’est exportée.

## Suite obligatoire

Établir un codec natif de combat avec réencodage exact et tests de pointeurs/limites ; adapter et mesurer les plans ; résoudre464/465 ; tester les variables, pagination et pauses dans Snes9x, puis seulement créer une recette d’insertion et un patch. Ne pas déclarer ces107 propositions intégrées. Ne pas compter ces entrées parmi les6957 du script principal. Relecture exhaustive du principal :0 entrée enregistrée dans cette passe ; audits naturels et recherche des autres ressources toujours ouverts.

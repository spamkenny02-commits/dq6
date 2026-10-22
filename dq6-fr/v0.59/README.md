# v0.59 — quatre messages natifs supplémentaires

IDs337,428,454,455 relus et intégrés sur le BPSv0.58 vérifié. Combat :40 traductions intégrées en diagnostic,67 préparées non insérées (65 relues,2 réserves464/465),497 héritées non qualifiées et4 structures. Principal6957 sélections inchangé (6948 linguistiques,9 structures). Tables de noms inchangées :37 français confirmés et4 aides grammaticales ;25 lieux etCéleste préparés. Les16 noms composéscombat-v066 restent un inventaire distinct, sans insertion. ROM8Mio.

## Revue et portée

337 : lancer l'objet nommé parB2, acteurB7. Le japonais décrit un jet, pas une incantation ; « lance » conserve ce sens. Source SFC directe, sans correspondance DS inventée.
428 : départ triste, B4 conservé. Même sens que le japonais ; la coupureAD source n'est pas imposée au français. L'appel source à0x2B3D0 est inchangé. B4 utilise5A22 etC2F119 : ce n'est pas le SID brut deB2.
454/455 : B7 ouB8 reste sous le charme de la voixB2 ; ordre SFC conservé. Référence DS0802.p:17 vérifiée enJA/FR. La DS française inverse les rôles dans la phrase ; la rédaction SFC maintient leur signification avec l'ordre des commandes natif. Les coupuresAD préparées sont conservées. B2 charge le SID5A28. La source de chaque message est vérifiée par empreinte.

Aucun moteur, police, nom, ancien message principal ni ancien message combat hors des quatre IDs n'est réécrit. Les contrôles hors disposition sont conservés dans le même ordre. Le message498 est exclu : son assemblage497+498 avec les noms composés nécessite une adaptation distincte. Ne pas publier l'ancien candidat privé à cinq messages comme s'il s'agissait de ce lot.

## Vérifications effectuées

- prepare/build/verify et inventaire : quatre allers-retours,604 autres messages combat identiques,870 groupes principaux identiques. Seuls le pool déplacé, ses pointeurs et les sommes de contrôle diffèrent.
- BPS etIPS réappliqués à la JP intacte ; mauvaiseJP et en-tête copieur rejetés parBPS, sourceJP contrôlée parSHA256 dans la recette ; patchs régénérés identiquement. Aucun mécanisme intrinsèque de rejet de source n'est revendiqué pour le formatIPS.
- Snes9x :608 pointeurs et premiers octets testés ; altération volontaire du pointeur du groupe8 détectée précisément. Ces tests ne prouvent pas le rendu de608 messages.
- Neuf rendus acceptés sur les quatre IDs : B2 court/long, acteur/cible distincts et homonymesA/B. B4 lookup1 donne Spotted Slime et2 Furrat. Un dixième testB4=0 donne un nom vide : cas de fixture mal initialisée enregistré, exclu des validations positives. Les libellés hérités servent aux tests de rôles/largeurs ; ils ne sont pas comptés comme nouvelles traductions de noms.
- Pagination, acquittements et retour de l'API contrôlés. Rendu parC02A29 depuis une redirection privée au camp : diagnostic, aucun combat naturel revendiqué. Chemin des noms de joueurs et fenêtre compacte non validés.
- BusROM :1478 plages,499773 octets (870 groupes principaux et608 messages combat). Démarrage sans état jusqu'au menu Nouveau jeu/Journal1/2/3 relu à l'écran.

Les captures, ROM de test et états restent privés et ne font pas partie de ce dépôt. qa-emulator.json consigne les limites et les empreintes des captures. Aucun test exhaustif de toutes les chaînes ou scènes n'est revendiqué.

## Reproduction depuis une copie neuve

```sh
python restore_sources.py
python dq6-fr/v0.59/prepare.py --jp '/chemin/source-jp.sfc'
python dq6-fr/v0.59/build.py --jp '/chemin/source-jp.sfc' --out '/chemin/prive'
python dq6-fr/v0.59/verify.py --jp '/chemin/source-jp.sfc' --out '/chemin/prive'
python dq6-fr/v0.59/inventory.py --rom '/chemin/prive/result.sfc'
```

Relancerbuild etverify doit garder les mêmesROM/BPS/IPS. Le BPSv0.59 est autonome sur la JP intacte ; la recette vérifie aussi son parentv0.58. variable_probe.py reproduit séquentiellement les diagnostics avec--out,--runner,--camp ; emulator_probe.py--mode reader et--mutate-pointer reproduisent les essais de lecteur. bus_layout.py fournit les plages à run_core.py--check-layout. Les JSON de capture régénérés nécessitent une nouvelle lecture visuelle, pas une approbation automatique.

## Suite

64 cas avec accents restent bloqués par le codec natif ;367 (arme),397 (suffixe homonyme aprèsAD),498 (composition) restent en préparation. Réserves464/465,16 noms composés dont4 variantesバキ/バギ,497 hérités non qualifiés, autres tables, recherche des oublis, relecture exhaustive et audits hérités restent ouverts. Une faute héritée rencontrée dans un autre menu est inscrite dans audit-rencontre-hors-lot.json sans correction silencieuse. Ce lot ne constitue pas une finalisation.

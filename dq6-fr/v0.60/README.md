# v0.60 — 64 textes natifs et sept accents

64 nouveaux messages du reliquat sont relus, intégrés et testés :104 traductions de combat intégrées au total,3 préparées non insérées (464,465,498),497 héritées non qualifiées et4 structures. Principal6957 sélections inchangé (6948 linguistiques et9 structures). Noms :37 français confirmés et4 aides grammaticales ;25 lieux etCéleste préparés. Les16 noms composés sont un inventaire distinct.8Mio conservés. Projet toujours partiel.

## Police native : extension isolée

Le combat utilise une police8x8 distincte de la police du script principal. Changer uniquement la table de glyphes ne suffit pas. La source des256 tuiles résidentes a été retrouvée à0x056B5C : chaque premier plan correspond exactement au chargementVRAM0x6000 observé. Sept nouvelles formes à/é/è/ê/î/â/û sont construites explicitement et relues à l'écran. Elles occupent les bytes2C,2D,30,33,34,35,3A. Leurs correspondances vers les glyphes principaux sont ajoutées à0x11100 ; les deux miroirsROM sont modifiés.

Avant allocation, chaque byte est absent des608 anciens messages de combat, des2512SIDs de noms (2048 physiques,464 alias) et des50 paires du dictionnaire.249 autres tuiles et mots de correspondance restent identiques, ainsi que tous les octets des noms et du dictionnaire. Sept mutations simulant un ancien consommateur de ces slots sont rejetées. Aucun moteur ni contrôle natif n'est modifié. Cet audit couvre les ressources connues ; il ne prétend pas avoir recensé tous les consommateurs codés en dur du jeu. Cette réserve reste dans l'audit final des ressources.

Un démarrage neuf de la ROM de production, sans état ni injectionVRAM, recharge correctement les256 premiers plans. Le menu Nouveau jeu/Journal1/2/3 est relu. Les anciens états d'émulateur conservent leur ancienne police : les diagnostics au camp la rafraîchissent explicitement depuis la ROM, et sont distingués du démarrage neuf. Pour jouer avec le patch, démarrer la ROM depuis un reset plutôt que charger un ancien état de l'émulateur.

## Revue et corrections de disposition

Lire revue-combat-v060.json, revisions.py et delta-combat-v060.json.64 textes JP/FR/contextes relus ;86 références DS uniques lues et vérifiées par empreinte lorsqu'établies. Les formulations DS sont adaptées aux rôles et commandes SFC. Aucun rapprochement flou seul ne valide une correspondance.

Les AD de disposition sont explicitement remplacés par des espaces dans ce lot : les noms longs et les blancs imposés provoquaient des chevauchements. B1 et toutes les autres commandes/variables restent dans leur ordre source. Six rédactions sont raccourcies et documentées (466,499,503,514,522,546), sans perdre l'action ou la réplique.503 conserve l'invitation à table et le repas prêt, avec à minuscule dans une phrase réordonnée.466 emploie en solo sans imposer un genre au personnage. Les variations SFC/DS (gag coquin, alcool, château, voix imitée et rôles) restent explicites et conformes au SFC.

367 : B5 reçoit deux valeurs d'objet et restitue Cypress Stick/Bamboo Spear par le résolveur natif. Ces noms hérités servent aux essais, sans compter comme traductions de la table des objets.
397 : seule la disposition AD devient un espace. Le rendu montre désormais acteurA puis cibleB pour les homonymes, puis Spotted Slime/Lipps dans un autre scénario. L'ancien constat A/A est conservé dans les versions précédentes. Ceci lève la réserve diagnostique de cette préparation, sans prétendre avoir validé sa scène naturelle ni isolé toute la cause du constat ancien. Aucun moteur réécrit silencieusement.

## Tests effectivement exécutés

- prepare/build/verify et inventaire :64 allers-retours,544 autres messages natifs identiques,870 groupes principaux identiques. Les seules différences autorisées sont le pool déplacé, ses pointeurs, les sept tuiles/mots de correspondance et les checksums.
- BPS/IPS réappliqués à la JP intacte ; mauvaiseJP et en-tête copieur rejetés parBPS. La recette exige la sourceJP parSHA256 ; aucune vérification intrinsèque de source n'est attribuée au formatIPS. ROM et patchs régénérés identiquement.
- Snes9x :608 pointeurs/premiers octets corrects ; altération volontaire du pointeur du groupe8 détectée. Cela ne valide pas le rendu des608 textes.
-64 IDs rendus avec noms homonymes ;4 scénarios complémentaires à noms distincts et autres voix/objets.68 scénarios,236 captures stables, texte complet relu sur leurs étapes intermédiaires. B3 est testé avec AM etOlivier, B5 avec deux objets, BB avec999PM. Les libellés anglais hérités ne sont pas comptés comme de nouvelles traductions.
- BusROM sur1478 plages principales/natives ; chargement neuf des256 tuiles de police vérifié séparément. qa-fresh-boot-font.json et qa-emulator.json donnent les nombres et empreintes.

Il s'agit de redirections diagnostiques au camp viaC02A29, sans parcours naturel de combat, sans validation de la fenêtre compacte ou de tous les chemins de noms de joueurs. Les copies privées ROM/états/captures ne sont jamais publiées. Les expériences rejetées (mode2 forcé bloqué, police non rechargée, chevauchements, initialisation superflue de variables) sont consignées dans diagnostics-rejetes.json ; elles ne comptent pas comme validations positives.

## Reproduction

```sh
python restore_sources.py
python dq6-fr/v0.60/prepare.py --jp '/chemin/source-jp.sfc'
python dq6-fr/v0.60/build.py --jp '/chemin/source-jp.sfc' --out '/chemin/prive'
python dq6-fr/v0.60/verify.py --jp '/chemin/source-jp.sfc' --out '/chemin/prive'
python dq6-fr/v0.60/verify_font.py --jp '/chemin/source-jp.sfc' --out '/chemin/prive'
python dq6-fr/v0.60/inventory.py --rom '/chemin/prive/result.sfc'
```

Le BPSv0.60 est autonome sur JP intacte. La recette applique son parentv0.59 vérifié, puis ce seul delta. emulator_pages.py reproduit séquentiellement les64 diagnostics avec--out,--runner,--camp ; ajouter--ids367,397,499,510 --b3 2 --b5 2 --profile distinct pour les quatre autres scénarios. Les captures exigent une nouvelle lecture visuelle, jamais une approbation automatique. emulator_probe.py--mode reader, puis--mutate-pointer testent le lecteur. bus_layout.py génère les plages à fournir à run_core.py--check-layout.

## Trois préparations restantes

464/465 : adapter le jeu verbal japonais à des mots français, régler les noms0369/036A encore provisoires, puis tester les quatre choix et la défaite comique.498 : vérifier l'assemblage497+498 et les16 noms DS, dont quatre variantesバキ/バギ réservées. Voir blocages-restants.json. Les497 textes hérités, autres tables, recherche exhaustive des oublis, relecture complète et audits naturels hérités restent ouverts. Aucune finalisation n'est annoncée.

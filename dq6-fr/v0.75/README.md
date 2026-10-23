# v0.75 — insertion groupée et relecture de 400 autres propositions

50 libellés préparés sont intégrés : **49 traductions et une correction de casse**. Le lot comprend 35 positions de monstres/personnages, six rangs de vocation et neuf objets sur deux lignes. Les six occurrences de デスタムーア et les trois occurrences de ダークドレアム du bloc des monstres sont traitées ensemble comme Mortamor et Nokturnus, sans fusionner leurs positions. Les sources exactes figurent dans `selection.json`, `revue-table-v075.json`, `preparations-resolues.json` et `delta-noms-v075.json`. La correction `Troll → troll` est isolée dans `revisions-heritees.json` ; elle ne compte pas comme une nouvelle traduction du mot.

La table compte maintenant **261 entrées françaises qualifiées sur 2048 positions physiques**. Sur les 560 propositions disponibles avant ce lot, 50 sont résolues et 510 restent non insérées. L’audit des 560 propositions et la relecture des 400 suivantes ne créent aucune nouvelle préparation ni traduction. Les 400 IDs distincts, leur japonais, le français DS disponible et les réserves figurent dans les deux registres `revue-propositions-400-part1.json` et `revue-propositions-400-part2.json`. La prochaine proposition du cycle est la position 1704 ; 110 restent à relire. Ce ne sont ni 400 positions nouvellement découvertes ni 400 approbations pour insertion.

La relecture compare le japonais, la proposition française et le contexte identifiable : monstre, titre, rang, action, objet ou menu. Les réserves sont maintenues pour les références absentes, la mise en page, les compositions et les genres. Exemples : かえる (287) peut signifier changer/échanger plutôt que « Jeter » ; まおうのこと (373) ne nomme pas explicitement Meurtor ; くばる (289) demande le contexte du menu de cartes ; モンスター (870) doit être rapproché du rôle adjectival proposé. Les signes `$` des propositions 708/731 sont des marqueurs du format DS à interpréter, pas des glyphes français à ajouter. « Cornacérée », « roi gluant » et « chef troll » demandent une vérification des articles et pluriels SFC. Aucun choix n’est forcé pour augmenter le nombre d’insertions.

## Reconstruction

Depuis la racine, `DQ6_JP`, `DQ6_DS`, `DQ6_IPS` désignent les trois sources privées vérifiées ; `DQ6_OUT` est une sortie privée hors Git :

```sh
python restore_sources.py
python dq6-fr/v0.75/prepare.py --jp "$DQ6_JP" --ds "$DQ6_DS" --ips "$DQ6_IPS"
python dq6-fr/v0.75/build.py --jp "$DQ6_JP" --out "$DQ6_OUT"
python dq6-fr/v0.75/verify.py --jp "$DQ6_JP" --out "$DQ6_OUT"
python dq6-fr/v0.75/inventory_names.py --jp "$DQ6_JP" --rom "$DQ6_OUT/result.sfc"
python dq6-fr/v0.75/review_pending.py --jp "$DQ6_JP" --ds "$DQ6_DS" --ips "$DQ6_IPS"
```

`prepare.py` vérifie les 50 japonais exacts, 100 champs JA/FR directement dans la ROM DS et 50 textes IPS. `review_pending.py` audite les 560 propositions : 560 sources JP, 560 sources IPS et 1004 champs DS distincts pour les 525 propositions disposant déjà de références. Les 35 sans référence DS établie ne sont pas approuvées. Aucun rapprochement flou ne valide une entrée.

`build.py` utilise le BPS v074. `verify.py` contrôle les 2462 autres chaînes inchangées, les 464 alias, le redécodage, la réapplication BPS/IPS, le rejet des mauvaises sources et les zones protégées. La ROM reste à 8 Mio. La table active commence à 7AF000 et occupe 14181 octets ; sa capacité jusqu’à 7B8703 reste réservée. L’ancienne table, son miroir, les 2050 octets de fin de table, le moteur, les polices, le dictionnaire, les 6957 sélections principales (6948 linguistiques et neuf structures) et les 608 slots de combat restent intacts. Le combat séparé compte toujours 597 entrées qualifiées, deux préparées, cinq opaques et quatre structures.

## Ruptures natives et tests

Les neuf objets conservent le nombre et la valeur exacte de leurs codes de rupture 91..9D. Leur première ligne garde sa longueur et la seconde n’est pas allongée ; les noms DS complets sont conservés sans abréviation. `audit-ruptures-preservees.json` documente les codes, les deux longueurs et les observations natives.

Le test précédent supposait une seule ligne. Il est étendu explicitement à la grille observée dans C3763A/C376F2 : seconde ligne en colonne 1 et curseur final égal à sa longueur plus un. Les 512 cases de chaque grille avant/après et les buffers B2 complets sont vérifiés. Aucun moteur n’est modifié. Dans le dialogue B2 diagnostique, les noms complets se composent sur une ligne et ont été relus visuellement. Ce diagnostic ne vaut pas validation d’un menu naturel d’inventaire.

`run_emulator_qa.py` accepte `--jp`, `--out`, `--runner` et `--camp`. Il exécute séquentiellement deux groupes CPU de 25 SIDs, le lecteur des 2477 SIDs statiques (35 dynamiques exclus), une mutation négative du pointeur SID16, 100 dialogues diagnostiques avant/après pour les 50 libellés (trois B2 chacun), puis les lectures du bus sur 4002 plages et le menu Journal à froid. Utiliser le protocole `run_core.py` et le cœur Snes9x documentés en v026, avec un état de camp privé ; à défaut, reconstruire le cœur et créer un nouvel état local. Les 50 images après insertion, leur orthographe et leurs accents ont été relus. ROM, SRAM, états, images et archives de sources restent hors Git.

Les scènes naturelles de combat, de voyage ou d’inventaire et tous les accords/pluriels ne sont pas exhaustivement validés. La recherche globale d’oublis, la relecture principale exhaustive (zéro entrée enregistrée), les fragments assemblés, les glyphes manquants, les commandes rares et les audits hérités 322/323, 1836, 4095, 610/1135/2404/5341/5351 restent ouverts. Le projet n’est pas finalisé.

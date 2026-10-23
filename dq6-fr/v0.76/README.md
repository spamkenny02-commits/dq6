# v0.76 — 110 propositions relues et 14 libellés intégrés

Les 110 propositions restantes du cycle v075 sont relues avec leurs japonais SFC et français DS, sans rejouer les 400 précédentes. Le registre contient les 110 IDs, les références exactes, les décisions et les limites. 110 sources JP/IPS et 220 champs DS sont contrôlés directement. Les 510 propositions de ce cycle ont donc été relues ; ce n’est pas une validation de leur insertion. 496 restent non insérées.

14 libellés sont intégrés : Rang bleu, Porte et pique, pieu d'os, épée du Rêve, épée du Massacre, fléau du Carnage, épée de Ramias, body d'ange, bouclier d'argent, bouclier royal, brassard kamikaze, bas résille, pierre brute, offrande rituelle. Sept proviennent des 110 nouvelles relectures et sept des 400 v075. Ce sont un rang d’arène, une compétence et 12 objets. 275 entrées françaises sont qualifiées sur 2048 positions déjà examinées. Aucun nouveau texte préparé, aucune relecture principale exhaustive ajoutée. Les 6957 sélections principales (6948 linguistiques,9 structures) et 608 slots de combat restent inchangés.

## Adaptation isolée des ruptures

Les codes 91..9D sont des métadonnées de longueur :90+nombre de glyphes de la première ligne. Le français raccourcit cette ligne ; conserver la valeur ancienne décalerait la suivante. Le lot recalcule ces 14 valeurs, sans ajouter/supprimer de rupture ni allonger l’une des lignes. Les noms DS complets sont conservés sans abréviation. `audit-metadonnees-rupture.json` donne chaque valeur avant/après, les longueurs et l’effet attendu. Cette adaptation ne modifie ni les commandes des scripts ni le moteur.

Les 512 cases des grilles C3763A/C376F2 et les buffers B2 sont contrôlés avant/après pour les 14 libellés. La seconde ligne commence en colonne 1 dans cette fixture. Un test négatif remplace 94 par 95 pour le SID805 : le curseur devient 4 au lieu de 5 et le contrôle rejette la fixture. La ROM de distribution n’est jamais modifiée par ce test. 28 dialogues B2 avant/après sont comparés ; les 14 images après insertion ont été relues, accents et noms complets lisibles. Les noms se composent sur une ligne dans le dialogue B2. Ces diagnostics ne valident pas tous les menus naturels d’arène, d’inventaire ou de combat.

## Reconstruction

Depuis la racine, avec les sources privées vérifiées `DQ6_JP`, `DQ6_DS`, `DQ6_IPS` et une sortie hors Git `DQ6_OUT` :

```sh
python restore_sources.py
python dq6-fr/v0.76/prepare.py --jp "$DQ6_JP" --ds "$DQ6_DS" --ips "$DQ6_IPS"
python dq6-fr/v0.76/build.py --jp "$DQ6_JP" --out "$DQ6_OUT"
python dq6-fr/v0.76/verify.py --jp "$DQ6_JP" --out "$DQ6_OUT"
python dq6-fr/v0.76/inventory_names.py --jp "$DQ6_JP" --rom "$DQ6_OUT/result.sfc"
python dq6-fr/v0.76/review_remaining.py --jp "$DQ6_JP" --ds "$DQ6_DS" --ips "$DQ6_IPS"
```

Les scripts `emulator_consumers.py`, `emulator_names_probe.py`, `emulator_render_names.py` acceptent `--out`, `--runner`, `--camp` ; consumers/render acceptent aussi `--jp`. Exécuter le lecteur normalement puis avec `--mutate-pointer`, et `test_break_negative.py` avec les mêmes arguments que consumers. Un seul émulateur à la fois ; utiliser le protocole v026, le cœur Snes9x et un état de camp privés, ou reconstruire le cœur et créer un nouvel état local. `bus_layout.py` produit les plages pour `run_core.py --check-layout`. Le démarrage utilise `--reset`, sans état chargé, avec la séquence de `qa-bus-boot.json`. Images, ROM, SRAM, états et archives restent hors Git.

Le lecteur vérifie 2477 SIDs statiques, exclut 35 dynamiques et détecte la mutation du pointeur SID16. Le bus vérifie 4002 plages et le menu Journal est relu à froid. `verify.py` contrôle les 2498 autres chaînes inchangées, les 464 alias, le redécodage, la réapplication BPS/IPS à JP intacte, le rejet des mauvaises sources et les zones protégées. ROM 8 Mio ; table active 7AF000 de 14140 octets, capacité jusqu’à 7B8703 réservée. Ancienne table, miroir, fin de table de 2050 octets, moteur, polices, dictionnaire et pool combat intacts.

Les réserves comprennent notamment 1820/1821 (objets de vocation à tracer : « Vitesse de dragon » est inhabituel face au japonais), 1797 (glyphe ancien 88), les glyphes manquants, genres/pluriels, largeurs et compositions. L’eau magique 1782 est distincte de la pierre philosophale 1784, contrairement à certains anciens noms anglais. Les 510 relectures ne doivent pas être recomptées ; poursuivre la résolution des 496 réserves. Recherche globale d’oublis,relecture principale exhaustive (0), audits hérités 322/323, 1836, 4095, 610/1135/2404/5341/5351 et scènes naturelles restent ouverts. Aucune finalisation annoncée.

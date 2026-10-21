# Combat-v060 — nom Céleste préparé et reprise du parcours

Repris depuis main0f935006f907eee7ed8cbc8c2bec5af6dee31c86. Les trois sources locales ont été vérifiées par SHA256 avant le travail ; restore_sources.py a restauré tous les lots. Le patch et la ROM restent v0.56, sans aucune insertion nouvelle.

## Nom utilisé dans le texte465

Le SID0369 contient encore M369 dans la ROM publiée. Son nom japonaisファルシオン est Céleste dans deux tables DS et dans la scène qui présente le cheval. La préparation `preparations/combat-v060/nom-celeste.json` conserve ces trois références et leurs empreintes. La table native mesure une seule entrée physique873 et un seul SID0369 pour ce nom. Cela ne valide pas encore tous ses appels. Un nouveau nom est préparé, non inséré ; ce n’est pas un108e message de combat. Les107 préparations de combat restent identiques, avec les réserves464/465.

Après restauration, reproduire le contrôle par :

```sh
python preparations/combat-v060/verify.py --jp /chemin/source-intacte.sfc
```

Le contrôle vérifie les trois références DS, la ROM de référence, le SID et ses alias. Deux exécutions gardent le fichier relu identique ; une source JP volontairement modifiée est rejetée. Aucun encodeur byte ni patch de production n’est ajouté.

## Parcours et relevé de tuiles

`natural-actions.json` conserve les entrées de manette depuis v026-camp.state vers le château de l’introduction, jusqu’au contrôle de la porte verrouillée. Aucun octet WRAM n’est édité. Ce parcours ne prouve pas le déroulement de la suite ni un combat. Le contrôle de rejeu compare le rendu final et la WRAM, sans publier les images, états ou données mémoire.

`resident_font_probe.py` crée une ROM temporaire privée depuis la source intacte et le BPS v0.56, puis relève des tuiles en VRAM via une copie temporaire du lanceur. Les images et données VRAM restent privées. Ce relevé est exploratoire : le bloc6000 contient bien une petite police latine. Le plan0 porte le dessin ; les plans1..3 remplis de palette masquent les lettres si on traite tout pixel non nul comme de l’encre. L’atlas privé a permis de relire les chiffres02..0B, majuscules10..29, minuscules42..5B et la ponctuation principale, dont7A=! et81=ellipse, indépendamment de C11100. Le rapport donne uniquement libellés et empreintes des tuiles. Cette lecture de la police résidente de terrain ne prouve pas son chargement ni le rendu des messages en combat ; aucune extension d’accents ou insertion n’est approuvée.

```sh
python tools/combat-v060/resident_font_probe.py --jp /chemin/source-intacte.sfc --camp /chemin/v026-camp.state --runner /chemin/emulator-tests/run_core.py --out /chemin/prive
```

Les scripts de test écrivent des états et captures privés à côté du lanceur ; ne jamais les ajouter à Git. Ne lancer qu’un émulateur à la fois.

## Comptes et suite

Principal6957 sélections :6948 linguistiques et9 structures ; aucune nouvelle relecture exhaustive enregistrée. Table de noms2512 SIDs/2048 entrées physiques :37 françaises confirmées,4 aides grammaticales,25 lieux préparés et1 nouveau nom préparé séparément. Combat608 entrées :107 préparées non insérées,497 héritées non relues,4 structures. Zéro insertion, pas de nouvelle version jouable. Continuer vers un vrai contexte de combat, relever sa police, vérifier les commandes/variables/pagination, puis intégrer les préparations et traiter les autres tables et audits hérités. Les états sauvegardés précédemment dans la conversation n’ont pas été récupérés ; aucune nouvelle sauvegarde durable des ROM n’est revendiquée.

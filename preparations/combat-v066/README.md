# Combat-v066 — noms complets des sorts inventés, préparation uniquement

16 libellés français DS relus ; 12 correspondances japonaises exactes et 4 réserves explicites. Statut PREPARE_NON_INSERE pour les 16. Aucun changement de ROM ou de patch. Aucun nouveau test Snes9x.

| Préfixe SFC | トテカ | チーマ | ソニア | ペッチ |
|---|---|---|---|---|
| メラ | Kavlan | Kapoum | Kabing | Kabang |
| ベホ | Supersoins | Ultrasoins | Insomnisoins | Dépann-soins |
| バキ (réserve : DS バギ) | Fournaise | Explotron | Survoltage | Foudrintense |
| マホ | Katastrof | Ténébror | Kaboum | Flatutranse |

Source principale : data/MENULIST6/JA et FR/b1005000.mpt, IDs352–367, mêmes positions, commandes @1 contrôlées. Contexte data/MESS6/JA et FR/0802.p IDs276,279,280 : invention du sort, nom complet variable %a002640, puis absence d'effet. La troisième ligne présente une différence バキ/バギ : conserver les quatre correspondances en réserve, sans normalisation silencieuse. L'ancien IPS n'est pas une validation.

## Composition native à résoudre

Les appels de messages497 et498 sont aux offsets source0x26769 et0x2677F. Deux tirages indépendants masqués par3 choisissent dans les tables0x26786 (061F,036B,036C,036D) et0x2678E (036E,036F,0370,0371), avant stockage du SID dans5A28. Le message497 imprime le préfixe et termine par AE ;498 imprime le suffixe via B2. Le code et les tables sont identiques entre la source JP etv0.58.

La matrice française ne se factorise pas en quatre préfixes et quatre suffixes par simple concaténation : les trois coupures possibles du préfixe commun « Ka » de la première ligne sont vérifiées exhaustivement. Il faut une représentation tenant compte des deux choix. Préserver B2/B2, AE et les autres commandes. Le SID061F sert aussi au véritable sort メラ, nommé Flamme sur DS : ne pas le réécrire globalement pour cette seule scène. Les alias physiques des huit SIDs sont consignés ; tous leurs appelants restent à auditer.

14 libellés passent le codec ASCII existant ; Dépann-soins et Ténébror nécessitent é, encore hors codec natif approuvé. Ces allers-retours ne valident pas leur rendu. Aucun assemblage français497+498, combat naturel ni accessibilité conjointe des16 couples par le générateur n'a été testé. Les anciens diagnostics isolésv0.59 ne prouvent pas cet assemblage.

## Reproduction

Après `python restore_sources.py`, lancer depuis la racine :

```sh
python preparations/combat-v066/prepare.py --jp '../upload/Dragon Quest VI - Maboroshi no Daichi (Japan)(2).sfc' --verify
```

Sans `--verify`, régénère les deux JSON déterministes. Vérifie SHA256 source JP, application du BPSv0.58 en mémoire, empreinte ROM reconstruite, instructions natives, tables,20 références DS, alias physiques, codec et rejet d'une source altérée. Aucune ROM n'est écrite.

Comptes inchangés : principal6957 sélections (6948 linguistiques,9 structures), combat608 entrées (36 intégrées,71 préparées,497 héritées non qualifiées,4 structures). Les16 noms composés ne s'ajoutent ni aux6957 ni aux608 ni aux2512 SIDs. Noms :37 français confirmés et4 aides grammaticales ; relecture exhaustive principale :0 entrée consignée. Les autres tables et audits hérités restent ouverts.

# v0.70 — lot 400–799 des 2048 positions physiques

400 positions examinées, 28 noms de monstres relus et intégrés, 216 propositions DS PREPARE_NON_INSERE.32positions étaient déjà qualifiées ; les autres restent différées avec leurs motifs. Prochain lot800–1199. 800positions consignées au total, pas800traductions ni800validations sémantiques complètes. Les216propositions sont des pistes documentées et non des textes approuvés ; elles ont référencesDS vérifiées mais largeur,glyphes,commandes,variantes ou sens détaillé à résoudre.

28noms : gluant marin,coquigluant,aquapode,dingopode,salchodron,toxinavet,gluante,méduse,iguaraptor,ombre,spectre,Milo,Kapout,limassif,limastard,mouillebave,porcinglé,rétroterreur,refléfatal,toxiguêpe,monte-gluant,cupitron,flammulus,cramulus,brumulus,mâchosaure,salgouille,malgouille. Références JP complètes et françaisDS au singulier@4, sans copier les articles/pluriels/balisesDS. Le sens et les familles sont relus dans revue-table-v070.json. Aucune largeur développée augmentée ; aucune commande introduite ni supprimée. Les variantesMortamor/Meurtor et autres noms homonymes restent à traiter ensemble.

128français qualifiés/2048,1480autres textes,344identifiants,12candidatsFR,83videsàqualifier,1créditretiré ;464alias/2512SIDs conservés. Préparations totales251noms (35v069+216v070),2lieux438/479 à part. Principal6957sélections/6948textes/9structures,combat597qualifiés/2préparés/5opaques/4structures inchangés. Relecture exhaustive principale0. Ne pas additionner les tables aux6957.

## Recette

Depuis la racine, avec variablesDQ6_JP,DQ6_DS,DQ6_IPS désignant les sources privées vérifiées etDQ6_OUT un dossier privé horsGit :

```sh
python restore_sources.py
python dq6-fr/v0.70/prepare.py --jp "$DQ6_JP" --ds "$DQ6_DS" --ips "$DQ6_IPS"
python dq6-fr/v0.70/build.py --jp "$DQ6_JP" --out "$DQ6_OUT"
python dq6-fr/v0.70/verify.py --jp "$DQ6_JP" --out "$DQ6_OUT"
python dq6-fr/v0.70/inventory_names.py --jp "$DQ6_JP" --rom "$DQ6_OUT/result.sfc"
```

prepare vérifie488champs dans la ROMDS et400positions dans l’ancienIPS. BPS/IPS réappliqués surJPintacte ; sources mauvaises rejetées ; moteur,polices,dictionnaire,870groupes principaux,608slotscombat et anciens noms non sélectionnés identiques.8Mio conservés. Tableactive7AF000,14329octets ; réserver capacitéjusqu’à7B8703,combat etmoteurv061. Ancienne table et miroir,tail2050octets préservés. Lecteur common.py::names/LogicalTable v068 ou ultérieur obligatoire.

## Tests et limites

Lecteur2477SIDs statiques,35dynamiques exclus,mutationSID16 ;terrainC3763A etB2C6FDF0 des28noms avant/après,56dialogues diagnostiques,revue visuelle,busROM etJournal àfroid. Ce sont des redirections au camp : pas des combats naturels ni une validation des accords,pluriels,menuscompacts,indicesmonstres ou de tous les consommateurs. Aucun changement grammatical/moteur n’est inclus. Les testsCPU,comparaisons pixels et revuevisuelle sont consignés séparément.

Les audits322/323,1836,4095,610/1135/2404/5341/5351 concernent le script principal ; ne pas confondre avec la position610 du présent lot. Aucun audit hérité clôturé par ces noms. Recherche exhaustive d’oublis,relecture principale et parcours naturels restent ouverts.

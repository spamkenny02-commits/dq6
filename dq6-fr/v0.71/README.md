# v0.71 — lot800–1199 des2048positions physiques

400positions examinées,32libellés modifiés (17traductions,15révisions d’un français hérité),1français inchangé relu source (Bang1109),80propositions PREPARE_NON_INSERE.19positions françaises déjà qualifiées sont conservées.1200positions consignées au total, pas1200traductions ni1200validations sémantiques complètes. Prochain lot1200–1599, puis1600–1999 et2000–2047 ; revenir ensuite aux réserves.

Ce lot couvre casino,monstres recrutables,rangs de vocation etsorts. Les32chaînes sélectionnées sont dans revue-table-v071.json avec JP,DS etdécision ; les15révisions héritées sont isolées dans revues-francais-herite.json. Exemples : Gagnés,monte-gluant,rafaltou,chef troll,Ceinture jaune,Moine,Parrain,Poids moyen,Mastodonte,Oracle,Libellule. Les rangs sont relus dans leur progression DS, pas traduits par rapprochement phonétique ou par le seul mot anglais. Pour les22rangs sélectionnés,les deux variantes DS sont vérifiées et donnent le même français : aucune préférence de genre inventée. Les autres rangs genrés restent différés. Les10mains de poker en glyphes spécialisés sont conservées ;22compositionscasino restent à auditer. blocages-v071.json conserve les347positions non résolues et leurs alternativesDS exactes issues des extractions Git, sans approbation supplémentaire. Les80propositions ne sont pas des traductions approuvées et ne s’ajoutent pas aux2048.

161entrées françaises qualifiées/2048,1448autres textes,344identifiants,11candidatsFR,83videsàqualifier,1créditretiré ;464alias/2512SIDs préservés. Préparationsnoms331 (35+216+80),2lieux438/479 séparés. Principal6957sélections/6948textes/9structures,combat597qualifiés/2préparés/5opaques/4structures inchangés. Relecture exhaustive du principal0. Ne pas additionner les tables aux6957.

## Recette reproductible

À la racine, DQ6_JP,DQ6_DS,DQ6_IPS désignent les trois sources privées vérifiées etDQ6_OUT un dossier privé horsGit :

```sh
python restore_sources.py
python dq6-fr/v0.71/prepare.py --jp "$DQ6_JP" --ds "$DQ6_DS" --ips "$DQ6_IPS"
python dq6-fr/v0.71/build.py --jp "$DQ6_JP" --out "$DQ6_OUT"
python dq6-fr/v0.71/verify.py --jp "$DQ6_JP" --out "$DQ6_OUT"
python dq6-fr/v0.71/inventory_names.py --jp "$DQ6_JP" --rom "$DQ6_OUT/result.sfc"
python dq6-fr/v0.71/audit_blockages.py
```

prepare vérifie270champs dans la ROMDS et400positions dans l’ancienIPS ; l’IPS secondaire ne valide pas le sens à lui seul. Les sources et leursSHA256 sont consignées dansqa-lot400.json. Le codec,dictionnaire,polices etmoteur restent identiques. Les32chaînes sélectionnées sont complètes,sans nouvelle commande ni augmentation de largeur ;2480autres flux bruts identiques. Les en-têtes français révisés ne ferment aucun audit du script principal.

8Mio conservés. Tableactive7AF000 de14282octets,capacité réservéejusqu’à7B8703 ;protéger aussicombat etmoteurv061. Pointeurs157groupes en deux copies ;ancienne table etmiroir,tail2050octets intacts. Lecteur common.py::names/LogicalTable v068 ou ultérieur obligatoire. prepare sélectionne le compresseur historique sans dépendre d’un nombre fixe de versions parentes ; sortie identique vérifiée par le build et les patchs.

## Portée des tests

Lecteur2477SIDs statiques et15175octets,35dynamiques exclus ;mutationSID16 détectée. Lecteurs terrainC3763A etB2C6FDF0 des32noms avant/après,64dialogues diagnostiques,revuevisuelle,busROM etJournal àfroid. BPS/IPS réappliqués surJPintacte,sources erronées rejetées,zones protégées inchangées. Les rapports distinguent contrôlesCPU,pixels etlecturevisuelle. Les redirections au camp ne valident pas les fenêtres naturelles ducasino,les rangs de vocation,recrutement,accords oucombats naturels. Ne pas déclarer les400positions traduites/testées.

Les audits322/323,1836,4095,610/1135/2404/5341/5351 du script principal,lescommandes rares,l’alphabet et tous les parcours naturels restent ouverts. Ne pas confondre les indices de cette table avec ceux du script principal.

# v0.72 — fin du parcours des positions1200–2047

Les848positions restantes ont été examinées et consignées en trois registres :1200–1599,1600–1999,2000–2047. Un patch commun intègre21libellés (14traductions et7révisions),3français existants sont relus sans modification,255propositionsDS restent PREPARE_NON_INSERE. Le parcours des2048positions est achevé ;la traduction complète de cette table ne l’est pas :185FRqualifiés seulement. Les propositions ne sont pas des textes approuvés etne s’ajoutent pas aux2048.

Intégrations : Bûcher,Frénésie,Gigaslash,lame de feu,boomerang,kilt de cuir,armure miroir,pyromanteau,diadème,tiare d’or,perle rose,charmélia,tapis volant,Mage,Gladiateur,Paladin,Sommité,Doc,Sans pitié,Me couvrir,Pas de magie. Sage,Ranger,Amos relus sans modification. JP exact etFRDS complet,aucune largeur augmentée ni commande ajoutée. Après les464alias,position1202 correspond àSID1666 ;les registres etplans préservent cette distinction.

Les277fragments de descriptions ne sont pas remplacés isolément. Les actions propres àSFC,échosDS japonais,noms longs,genres etlistes fonctionnelles restent en réserve. Les48derniers emplacements comprennent6noms réservés àtracer,1vide statique,35SIDs redirigés versWRAM et6slotsVFvides dont le JP séquentiel est opaque aprèsSID09C9. La limite3BC76D est inférée,pas une preuve d’inutilisation de tous les consommateurs. Aucun texte vide/code/donnée n’est présenté comme traduit. Lire audit-derniers-48.json etblocages-v072.json.

185FRqualifiés,1427autres textes,344identifiants,8candidatsFR,41videsàqualifier,1créditretiré,1réservevide,35structuresdynamiques,6sourcesJPopaques =2048positions.2512SIDs parsés,464alias ;nombre réel de consommateurs non prouvé. Les bornes de régions de l’inventaire sont rectifiées d’après l’ordre observé (sorts1103–1325,objets1604–1823,etc.),sans changementROM.586propositionsnoms cumulées et2lieux438/479 séparés. Principal6957sélections/6948textes/9structures,combat597qualifiés/2préparés/5opaques/4structures inchangés. Relecture principale exhaustive0. Aucun audit hérité clôturé.

## Recette finale

Depuis la racine,avec sources privées vérifiées DQ6_JP,DQ6_DS,DQ6_IPS etsortie DQ6_OUT horsGit :

```sh
python restore_sources.py
python dq6-fr/v0.72/prepare.py --jp "$DQ6_JP" --ds "$DQ6_DS" --ips "$DQ6_IPS"
python dq6-fr/v0.72/build.py --jp "$DQ6_JP" --out "$DQ6_OUT"
python dq6-fr/v0.72/verify.py --jp "$DQ6_JP" --out "$DQ6_OUT"
python dq6-fr/v0.72/inventory_names.py --jp "$DQ6_JP" --rom "$DQ6_OUT/result.sfc"
python dq6-fr/v0.72/audit_blockages.py
```

Le générateur souspreparations conserve le point préparatoire etrefuse d’écraser une version finale publiée ;utiliser les scripts ci-dessus.558champsDS et848positionsIPS vérifiés,avec empreintes des trois sources. BPS/IPS réappliqués àJPintacte,sources erronées rejetées,zones protégées identiques.8Mio ;tableactive7AF000 de14260octets,capacitéjusqu’à7B8703 réservée,pluscombat etmoteur. Ancienne table etmiroir,tail2050octets intacts ;moteur,polices et dictionnaire inchangés. Lecteur common.py::names/LogicalTable v068+ obligatoire.

## Tests et limites

Lecteur2477SIDs statiques (35dynamiques exclus),mutationSID16 détectée,terrainC3763A etB2C6FDF0 avant/après21libellés,42dialogues diagnostiques relus visuellement,busROM etJournal àfroid.2491autres chaînes brutes et464alias identiques. Les derniers emplacements font l’objet d’un audit structurel,pas de nouveaux dialogues rendus. Les diagnostics au camp ne valident pas les menus naturels,genres/pluriels,combat ou toutes les compositions. Les audits322/323,1836,4095,610/1135/2404/5341/5351 du script principal,lescommandes rares,alphabet,recherche exhaustive d’oublis et relecture complète restent ouverts. Ne pas désactiver le suivi comme si la traduction était finalisée.

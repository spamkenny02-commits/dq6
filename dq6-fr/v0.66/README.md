# DQVI FR v0.66 — huit noms de lieux DS

Huit préparations antérieures sont intégrées :Puidebourg417,Pierrebrute418,Milmarin423,Sorcéria425,Aridéa426,Mélankolia430,Zénithia443,Fort-Terreur450. Le registre ne les compte pas comme huit nouvelles préparations.17lieux restent PREPARE_NON_INSERE,avec motifs individuels dans lieux-prepares-non-inseres.json.

## Sources et sens

Chaque nom japonais est relu depuis les octets de la JP SFC intacte et correspond exactement au nom de la liste DS. Les seize champs JA/FR sont revérifiés directement dans les fichiers MPT de la ROM DS vérifiée,avec leurID. L'ancienIPS headered est réappliqué en privé à la JP intacte ; ses huit libellés secondaires sont contrôlés,et ne remplacent pas les noms officiels DS. Références,empreintes et décisions de sens parID dans revue-lieux-v066.json etqa-sources.json. Milmarin/ペスカニ est distingué de Militia/アークボルト ; Mélankolia/ぜつぼうのまち de Kupidia/よくぼうのまち. Fort-Terreur conserve son tiret et remplace l'inexact Ile des Cavernes hérité. Aucun rapprochement flou seul validé.

## Insertion et conservation

Les huit noms sont encodés avec les glyphes et les paires DTE déjà présents. Leur variation de stockage totale est exactement0 :+3,+0,+1,+0,−1,−1,+0,−2octets. Recompaction des2048entrées physiques,157groupes de pointeurs dans deux copies. Les464classes d'alias sont conservées ; chaque nom modifié a un seulSID.2504autres chaînes de noms sont identiques octet pour octet. Les2050octets de fin de table restaurés env065 restent strictement identiques dans les deux copies. Aucun espace libre déduit de cette réserve.

870groupes du principal,6957sélections,608emplacements combat,moteurv061,polices,dictionnaire et autres octets protégés inchangés. Seuls le pool atteignable des noms,ses pointeurs et les sommesSNES changent.8Mio conservés. Delta lisible dans delta-lieux-v066.json. Les17autres lieux ne sont pas forcés pour un quota :croissance du stockage,22glyphes de438 etcommande98 de479 restent à résoudre. Aucun de ces noms en attente n'est déclaré intégré.

## Recette reproductible

```
python restore_sources.py
python dq6-fr/v0.66/prepare.py --jp /source/JP.sfc --ds /source/DS.nds --ips /source/ancien.ips
python dq6-fr/v0.66/build.py --jp /source/JP.sfc --out /sortie/privee
python dq6-fr/v0.66/verify.py --jp /source/JP.sfc --out /sortie/privee
python dq6-fr/v0.66/inventory_names.py --jp /source/JP.sfc --rom /sortie/privee/result.sfc
```

Recette idempotente depuisv065 vérifié. BPSautonome publié,IPS généré localement et réappliqué. Sources JP/DS/IPS vérifiées parSHA256 avant le lot ; aucun original modifié. Rejette JP altérée et source avec en-tête ajouté.

## Tests réels et limites

Redécodage des huit noms,2504autres chaînes identiques,alias et zones protégées,BPS/IPS réappliqués. Snes9x :2477SIDs statiques lus parC0315E/C031DB,pointeurs et tous15242octets comparés ;35SIDs dynamiques09A7..09C9 explicitement exclus. Mutation de pointeur volontaire détectée pourSID16.

C3763A contrôle le flux des glyphes dans la tilemap terrain etC6FDF0 celui du bufferB2,pour les huit noms avant et après. Tous correspondent aux octets attendus. Le seuil20 est une référence documentaire,pas une mesure de la fenêtre naturelle. Seize dialogues de camp (huit avant,huit après),troisB2parpage ; huit nouveaux libellés complets,accents et tiret relus à l'écran,sans troncature dans cette fixture.6513plages/546219octets sur le bus,Démarrage neuf versJournal1/2/3. Un seul émulateur à la fois.

Ce sont des redirections diagnostiques,pas un parcours de huit lieux ou un menu de voyage naturel. Les fenêtres compactes et autres consommateurs,35SIDs dynamiques,commandes rares,fragments et essais naturels restent ouverts. Captures,ROM,SRAM et états demeurent privés ; scripts et empreintes publiés. Le champ de rendu nom ne qualifie aucune autre scène.

## Progression réelle

Principal6957sélections :6948linguistiques,9structures,aucun ajout principal. Combat597français qualifiés,2préparés27/277 inclus dans le reliquat,5emplacements opaques603–607 hors frontière JP,4structures ; inchangé. Noms47confirmés sur2048physiques/2512SIDs/464alias,344identifiants,1548autres à revoir,25correspondancesFRDS non qualifiées,83vides à qualifier,1créditretiré. L'absence de japonais ne prouve pas une traduction.17lieux préparés,4aides grammaticales et16compositions héritées inchangées.

Relecture exhaustive du principal0 ; ce lot de huit noms ne constitue pas une relecture générale. Autres ressources,menus,objets,sorts,classes,système,fin etépilogue à inventorier/revoir. Audits322/323,1836,4095,610/1135/2404/5341/5351 etRNG naturel des16compositions toujours ouverts. Ne pas annoncer la finalisation.

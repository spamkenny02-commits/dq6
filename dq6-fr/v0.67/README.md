# DQVI FR v0.67 — dix lieux DS et stockage conservé

Dix préparations antérieures intégrées :Desmodia420,Vallonclair424,Montgivré428,Donjon de Meurtor434,Brigandia441,Poste-frontière466,Chez madame Luce470,Manoir Médaillon473,Au fond du puits491,Tour des Maléfices517. Aucune nouvelle préparation ; sept restent PREPARE_NON_INSERE dans un registre parSID. Le lot n'atteint pas400traductions et ne le prétend pas.

## Sources et décisions

Les noms japonais SFC sont relus depuis les octets de la source intacte,puis comparés exactement aux libellés DS japonais.24champsMPT JA/FR sont revérifiés directement dans la ROM DS vérifiée. L'ancienIPS est réappliqué sur une copie headered de la JP et ses dix noms secondaires contrôlés. Références textuelles,IDs et empreintes dans revue-lieux-v067.json etqa-sources.json. Les variantes de mondes deDesmodia etVallonclair ont chacune deux références DS concordantes ; cela n'invente pas deux noms physiques SFC. Chez madame Luce conserve la casse officielle,Poste-frontière le tiret/è,Manoir Médaillon le libellé complet etTour des Maléfices le pluriel/é. Le donjon appartient àMeurtor/ムドー. Aucun rapprochement flou seul validé.

## Recompression distincte

Six anciens lieux419/422/427/432/442/444 et seize libellés de sorts/actions1570/1576/1579/1581/1585/1589/1592/1604/1605/1611/1620/1627/1628/1639/1714/1716 sont recomprimés avec les paires DTE déjà présentes. Leur texte et flux de glyphes restent strictement identiques ; ces22entrées ne sont pas de nouvelles traductions ni une nouvelle relecture sémantique. Pas de changement de Gus ou des noms par défaut des personnages. Le registre revue-stockage.json donne chaque delta d'encodage.

Ces22recompressions libèrent26octets,exactement absorbés par les dix noms de lieux. Le pool atteignable garde14349octets et s'arrête à0x3BBF10 ; les2050octets protégés jusqu'à0x3BC712 restent identiques dans les deux copies.2048entrées physiques/464classes d'alias conservées ; chaque chaîne modifiée n'a qu'unSID.2480autres chaînes brutes identiques,2502autres flux développés identiques.870groupes principaux,6957sélections,608emplacements combat,moteurv061,polices,dictionnaire et autres octets protégés inchangés. Seuls le pool atteignable,ses157groupes de pointeurs dans deux copies et les sommesSNES changent.8Mio conservés.

## Recette idempotente

```
python restore_sources.py
python dq6-fr/v0.67/prepare.py --jp /source/JP.sfc --ds /source/DS.nds --ips /source/ancien.ips
python dq6-fr/v0.67/build.py --jp /source/JP.sfc --out /sortie/privee
python dq6-fr/v0.67/verify.py --jp /source/JP.sfc --out /sortie/privee
python dq6-fr/v0.67/inventory_names.py --jp /source/JP.sfc --rom /sortie/privee/result.sfc
```

Reprend le BPSv066 vérifié surJP intacte. Sources JP/DS/IPS contrôlées parSHA256 avant le lot. BPSautonome publié,IPS généré localement et réappliqué ; JP altérée et source avec en-tête ajouté rejetées. Restauration en archive Git propre et empreintes contrôlées avant/après publication. Aucune ROM,SRAM,état,capture ni archive de ROM sur Git.

## Contrôles Snes9x et limites

2477SIDs statiques entièrement lus viaC0315E/C031DB,pointeurs et15242octets comparés.35SIDs09A7..09C9 prennent la brancheWRAM C44FDF et restent explicitement exclus. Mutation de pointeur volontaire détectée surSID16. Les32noms modifiés sont contrôlés avant/après parC3763A (tilemap terrain) etC6FDF0 (bufferB2). Tous correspondent aux flux de glyphes attendus ; les22recompressions donnent des sorties identiques. Aucun code de lecteur n'est changé. Le seuil20 reste une référence documentaire,pas la preuve d'une largeur naturelle de menu.

64dialogues diagnostiques au camp,32avant/32après,troisB2parpage. Les22paires de stockage ont des pixels identiques. Dix nouveaux libellés complets sont relus à l'écran,accents,tiret,casse et pluriels conservés.6513plages/546219octets contrôlés sur le bus,Journal1/2/3 visible au démarrage neuf. Les scripts emulator_names_probe.py,emulator_consumers.py,emulator_render_names.py etbus_layout.py reproduisent ces contrôles avec cœur et état locaux ; un seul émulateur à la fois.

Ce sont des redirections privées,pas des menus naturels de voyage/sorts,un parcours de lieux ou des combats naturels. Les lecteurs connus de terrain/B2 sont testés pour tous les encodages modifiés ; autres consommateurs,fenêtres compactes,35SIDs dynamiques etaccessibilité naturelle restent à auditer. Ne pas qualifier toutes les scènes par ces fixtures.

## État et suite

Principal6957sélections :6948linguistiques et9structures,aucun ajout. Combat597qualifiés,2préparés27/277 inclus dans le reliquat,5emplacements603–607 hors frontière JP,4structures ; inchangé. Noms57confirmés sur2048physiques/2512SIDs/464alias,344identifiants,1538autres à revoir,25candidatsFRDS non qualifiés,83vides à qualifier,1créditretiré.4aides grammaticales et16compositions héritées inchangées. L'absence de japonais ne prouve pas la traduction.

Sept lieux préparés436/437/438/464/479/481/490 totalisent48octets estimés de croissance après DTE ; ce n'est pas une allocation approuvée.438compte22glyphes et479contient l'ancien saut98 à traiter sans l'aplatir arbitrairement. Registre individuel conservé. Puis autres noms,menus,objets,sorts,classes,système,fin/épilogue et recherche exhaustive des ressources. Relecture exhaustive du principal0. Audits322/323,1836,4095,610/1135/2404/5341/5351,fragments,commandes rares etRNG naturel des16compositions toujours ouverts. Ne pas annoncer de finalisation.

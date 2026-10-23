# DQVI FR v0.68 — capacité des noms et cinq lieux DS

Cinq préparations intégrées : Abbaye des Vocations436, Château de Joliroche437, Pic des Terreurs464, Cap de Somnia481, Prison du Chagrin490. Deux lieux restent PREPARE_NON_INSERE :438 pour22glyphes,479 pour la commande de mise en page98. Aucun nouveau préparé. Le nom complet,leâ deChâteau,les capitales et les pluriels DS sont conservés. Les japonais SFC/DS sont identiques ;12champs MPT JA/FR sont revérifiés directement dansDS et5libellés secondaires dans l'ancienIPS réappliqué à une JP headered privée. Décisions parSID et empreintes dans revue-lieux-v068.json etqa-sources.json.

## Relocalisation isolée

L'ancien pool atteignable était plein. Le nouveau pool actif est à0x7AF000,14383octets,jusqu'à0x7B282F. Cette plage appartient aux seules zones d'ancien script réutilisées depuisv019 :0x77175B..0x7B8703. Le préparateur contrôle l'absence de recouvrement avec les870groupes principaux actuels,le pool combat et l'allocation moteurv061. Aucun espace n'est déduit du simple contenuFF.

Le lecteur d'origine C0315E ajoute la baseCPU0xFB8703 à un décalage24bits avec retenue. Les157groupes reçoivent donc (nouvelle_adresse_CPU−0xFB8703)&0xFFFFFF,dans les deux copies. Aucun code de lecteur,moteur,police ou dictionnaire modifié. Le pool physique historique0x3B8703..0x3BC712 est préservé intégralement dans les deux copies,tail2050octets inclus.2507autres chaînes sont identiques,2048entrées physiques et464classes d'alias conservées. Principal6957sélections/870groupes et608emplacements combat inchangés.8Mio conservés.

La capacité restante dans cette réservation est24276octets ; ce n'est pas une traduction validée. Les futurs builds et fixtures doivent protéger le pool actif et idéalement toute la capacité jusqu'à7B8703,plus le moteur etle combat. Les anciennes copies peuvent être lues par des consommateurs hardcodés encore inconnus : leur conservation évite de les écraser,mais ne prouve pas qu'ils affichent les cinq nouveaux libellés. Audit exhaustif des ressources et chemins toujours ouvert.

## Lecteur des outils

Utiliser common.py::names etLogicalTable v068. Les helpers historiques v061.names et nametable.Table supposent que la table reste dans le pool historique et ne doivent pas lire cette nouvelle ROM. Le nouvel inventaire restitue les mêmes positions logiques via les adresses réellement résolues. Il ne compte pas deux copies comme deux traductions. Les35SIDs dynamiques09A7..09C9 gardent leur brancheWRAM ; aucune équivalence de pointeur statique n'est prétendue pour eux.

## Recette et contrôles

```
python restore_sources.py
python dq6-fr/v0.68/prepare.py --jp /source/JP.sfc --ds /source/DS.nds --ips /source/ancien.ips
python dq6-fr/v0.68/build.py --jp /source/JP.sfc --out /sortie/privee
python dq6-fr/v0.68/verify.py --jp /source/JP.sfc --out /sortie/privee
python dq6-fr/v0.68/inventory_names.py --jp /source/JP.sfc --rom /sortie/privee/result.sfc
```

Recette idempotente surBPSv067 contrôlé etJP intacte. Trois sources locales vérifiées parSHA256,originaux inchangés. BPSautonome publié,IPS régénéré et réappliqué,JP altérée/en-tête ajouté rejetés. Anciennes chaînes,alias,groupes,frontières et octets protégés contrôlés. Restauration en archive Git propre avant et après publication. Aucune ROM,SRAM,état,capture ou archive deROM surGit.

Snes9x :2477SIDs statiques,pointeurs ettous15276octets relus viaC0315E/C031DB. Mutation de pointeur détectée surSID16. SID676 traverse réellement0x7AFFFF/0x7B0000 : lecteur complet et diagnostics terrainC3763A/B2C6FDF0 vérifiés,libellé anglais hérité Tiger Claw non qualifié par cet essai. Dix noms terrain/B2 avant et après,cinq nouveaux etcinq régressions.20dialogues de camp,troisB2parpage,cinq traductions relues et cinq paires de pixels de régression identiques.4002plages/574057octets du bus etJournal1/2/3 au démarrage neuf. Un seul émulateur à la fois.

Ces redirections ne sont pas des parcours naturels des lieux,menus de voyage/sorts ou combats. Les fenêtres compactes,les lecteurs inconnus,les35SIDs dynamiques et les scènes naturelles restent à auditer. Le seuil20 des noms de lieu est documentaire,aucune largeur de fenêtre naturelle déduite du seul renduB2.

## Progression

Principal6948textes+9structures,combat597qualifiés/2préparés/5opaques/4structures inchangés. Noms62confirmés sur2048physiques,344identifiants,1533autresàrevoir,25candidatsFRDS non qualifiés,83videsàqualifier,1créditretiré.4aides et16compositions héritées inchangées.2lieux préparés restants ; absence de japonais ne prouve pas le français. Relecture exhaustive du principal0. Autres menus,objets,sorts,classes,système,fin/épilogue et recherche des oublis restent à traiter. Audits322/323,1836,4095,610/1135/2404/5341/5351,fragments,commandes rares etRNG naturel des16compositions ouverts. Ne pas annoncer de finalisation.

# DQVI FR v0.65 — réparation isolée du stockage des noms

Zéro nouvelle traduction ou préparation. Les comptes restent6957 sélections principales (6948 linguistiques,9structures),597entrées combat françaises qualifiées,2préparées27/277 incluses dans le reliquat,5emplacements opaques603–607 et4structures. Relecture exhaustive0. L'inventaire séparé reste2048entrées physiques,2512SIDs,464alias :39confirmées,25candidatsFRDS à vérifier,344identifiants,1556autres à revoir,83vides à qualifier,1créditretiré.25lieux préparés,4aides grammaticales et16noms composés inchangés. Absence de japonais et égalité DS ne constituent pas une validation.

## Correction

La v061 avait étendu le pool atteignable de7octets dans une fin de table à préserver. Restaurer ces octets surplace aurait corrompu les derniers noms. Cette recette recomprime cinq noms existants avec les paires du dictionnaire déjà utilisé par le jeu :Céleste(2octets),Braséria(1),Olivier(1),Francis(2),Laura(1). Aucun nom n'est modifié linguistiquement. Recompaction des2048entrées,157groupes de pointeurs en deux copies ; les464classes d'alias sont conservées. La limite revient de0x3BBF17 à0x3BBF10. Tous les2050octets jusqu'à0x3BC712 sont restaurés exactement depuis le BPSv060 appliqué à la JP intacte. On ne déclare pas ces données inutilisées ; leur sémantique reste inconnue et elles doivent rester protégées.

Aucun code moteur,police,dictionnaire,commande,sélection principale ou texte combat changé. Les2512flux de glyphes développés sont identiques. Les seuls octets modifiés sont dans le pool des noms et sa fin préservée,les157pointeurs dans deux copies et les sommesSNES.8Mio conservés. Delta lisible dans delta-stockage-v065.json.

## Recette

```
python restore_sources.py
python dq6-fr/v0.65/prepare.py --jp /source/intacte.sfc
python dq6-fr/v0.65/build.py --jp /source/intacte.sfc --out /sortie/privee
python dq6-fr/v0.65/verify.py --jp /source/intacte.sfc --out /sortie/privee
python dq6-fr/v0.65/inventory_names.py --jp /source/intacte.sfc --rom /sortie/privee/result.sfc
```

prepare/build/verify sont idempotents. BPSautonome publié ; IPS reproductible localement. Trois sources locales revérifiées parSHA256 avant le lot. Le DS et l'IPS servent de références héritées ; aucune nouvelle correspondance sémantique n'est revendiquée dans cette correction de stockage.

## Tests réalisés

BPS/IPS réappliqués à la JP intacte,deux mauvaises sources rejetées,allers-retours des cinq noms,2512flux développés et464alias comparés,608emplacements combat et870groupes principaux identiques,octets protégés contrôlés.

Sous Snes9x,2477SIDs statiques sont lus entièrement viaC0315E/C031DB,avec pointeur et chaque octet comparés. Les35SIDs09A7..09C9 prennent le cheminWRAM C44FDF : ils sont exclus de l'équivalence des pointeurs statiques. Le recensement logique2512SIDs ne prouve pas leur consommation réelle. Une mutation de pointeur volontaire est détectée surSID16.

Les cinq noms passent les lecteurs natifs de terrain C3763A et B2 C6FDF0 :tilemap etbuffer de glyphes égaux avant/après,34glyphes par lecteur contrôlés. La branche terrain des cinqSIDs utiliseC031DB ; les autres lecteursC031FA ne sont pas modifiés ni validés globalement. Dix dialogues de camp (cinq avant/cinq après),trois B2parpage,produisent des pixels identiques ; les cinq noms et lesé sont relus visuellement. Ce sont des redirections privées,aucun recrutement ou combat naturel.6513plages/546219octets contrôlés sur le bus,Journal1/2/3 visible au démarrage neuf.

Les scripts emulator_names_probe.py,emulator_consumers.py,emulator_render_names.py etbus_layout.py reproduisent ces diagnostics avec le cœur et l'état locaux. Les scripts demandent --runner,--camp,--out,et --jp pour les comparaisons avant/après. ROM,états,SRAM etcaptures restent privés.

## À poursuivre

27/277 :appelants et statut d'usage non établis.603–607 :hors frontière JP,ne pas inventer de source. Autres menus,objets,sorts,noms,lieux,classes,système,fin etépilogue à inventorier/revoir. Les autres consommateurs de noms,fenêtres compactes,parcours naturels et35SIDs dynamiques ne sont pas validés par ce lot. Audits322/323,1836,4095,610/1135/2404/5341/5351,fragments etcommandes rares toujours ouverts. Les16branches de noms composés restent testées historiquement par forçage,sans preuve RNG naturelle exhaustive. Ne pas annoncer de finalisation ; grosse relecture suivie parIDs encore à faire.

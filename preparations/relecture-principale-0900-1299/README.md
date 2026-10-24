# Relecture préparatoire900–1299 après v0.78

400 nouvelles positions principales comparées manuellement au japonais SFC,aux références françaises/japonaises DS disponibles,au contexte textuel et à l'extraction IPS secondaire. Chaque ID possède sa note et son dossier de provenance. Les 400 positions ne sont ni400 nouvelles traductions ni400 scènes jouées.

55 révisions PREPARE_NON_INSERE :42 de typographie seule,8 de sens/consigne sans nouveau glyphe,4 d'orthographe/ponctuation et1 mixte (1045,endormir+sœur).43 propositions exigent donc au moins un des glyphes À/Ç/œ absents du charset principal v056 ; ces catégories se recoupent pour1045.

- 955 précise que les gardes distribuent les rations ;961 restitue la consigne SFC «Passez par derrière pour en parler»,omise du français DS.
- 1002 propose de porter du vin au capitaine pour l'amadouer,conformément au japonais,plutôt que de boire pour son propre moral.1003 parle de confiscation,1012 exprime l'absence de choix au présent,1045 précise endormir plutôt qu'éliminer,1082 restitue l'ordre d'avaler une larve vivante.
- 1105 propose nord-ouest :SFC et DS japonais disent 北西,mais le français DS dit nord-est. Aucune carte ni direction native testée ;pas de remplacement global.1291 conserve son nord-est concordant.1131 adapte «au château» à la source SFC,distincte du «près» ajouté par le DS.
- 1018 corrige gêolier→geôlier,1151 Dites lui→Dites-lui,1181 telle quelle est→telle qu'elle est,1252 ponctue l'apposition «ma reine et moi».

Lire audit-consignes-orbe-vin.json et audit-variable-1179.json. L'audit hérité1135 est effectivement relu dans ce lot,mais reste ouvert :lancer l'orbe SFC n'est pas lever l'orbe DS ;cap,mer,action et résultat n'ont pas été testés.1179 contient U+E000 dans sa représentation lisible alors que les tokens portent C9,comme le japonais ;cela ne prouve pas un bug ROM. Ne pas réencoder ce texte lisible divergent avant un redécodage natif.

Les adaptations officielles (puits916/934–936/1032/1115,alcool/jus969–970/1038,parler stylisé de Sergueï/Svetlana,rimes d'Ondine,parler régional de Colin) sont distinguées des fautes ordinaires ;aucune réécriture de quota. Les références969 et989 sont qualifiées comparaison d'édition ou lexique,non équivalence de scène.1138 et1178 sont des silences sous commandes,non de nouveaux mots traduits.

Cumul :900 positions400–1299 en relecture préparatoire,126 révisions de textes principaux déjà intégrés noninsérées,distinctes des419 propositions noms/menus. Relecture principale exhaustive finale acceptée0. Restent0–399 et1300–6956. Principal natif inchangé :6948 textes+9 structures/6957sélections ;table2048positions déjà examinées,367FR qualifiés,2512SIDs/464alias. Combat/patch v0.78 et8Mio inchangés.

## Reproduction et limites

Depuis la racine :`python restore_sources.py`,puis `python preparations/relecture-principale-0900-1299/prepare.py`. notes.json et decisions.json sont les décisions manuelles ;le script vérifie les références exactes,les ancres de substitution,les variables textuelles préservées et les tokens source. Il reproduit registres,propositions,QA et audits,sans générer de nouvelle sélection encodée. Réexécution et restauration dans un dossier initialement vide contrôlées avant publication ;contrôle du commit publié consigné séparément.

Sources privées absentes et ancien espace fc8c8cdec832 inexistant. Verrou historique inaccessible ;verrou exclusif dans l'espace courant pour ces seules préparations,publication conditionnée à l'empreinte main initiale,sans force. Aucun build ROM,redécodage natif,réapplication de BPS/IPS,rejet de mauvaise ROM,contrôle bus ou émulation exécuté dans ce lot. Contrôler des hashes de patch conservés n'est pas réappliquer un patch. DA/DB/D4/D5/DE,variables,noms longs,pagination,choix oui/non,acquisitions et scènes naturelles restent à tester. Aucun audit hérité clôturé ni finalisation annoncée.

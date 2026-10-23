# Reprise v0.70 — lot400–799 des2048positions

Lire dq6-fr/v0.70/README.md,registre0400–0799,revue,delta etQA.28nomsmonstres intégrés,216propositionsDS PREPARE_NON_INSERE,32anciensFR conservés.800positions consignées/2048,128FRqualifiés ;pas800traductions. Prochainlot800–1199,puis1200–1599,1600–1999,2000–2047. Ne pas recycler ces28noms ni les revuesprécédentes.

Tableactive7AF000 de14329octets,capacitéprotégéejusqu’à7B8703,pluscombat etmoteur ;lecteurv068+obligatoire.251propositionsnoms cumulées (35+216) et2lieuxpréparés438/479 distincts. Principal/combat inchangés,relectureexhaustive0 ;accords/pluriels etscènesnaturellesdesmonstres nonvalidés parB2. Aucun audit hérité clôturé.

# Reprise v0.69 — lot 0000–0399 des 2048 positions

Lire dq6-fr/v0.69/README.md, registre-positions-0000-0399.json, revue et QA. 400positions examinées,25libellés modifiés,13français existants relus source,35PREPARE_NON_INSERE.100FRqualifiés/2048 ;1508autres,344identifiants,12candidatsFR,83vides et1crédit retiré. Pas400traductions ni400validations naturelles. Prochain lot400–799 puis800–1199,1200–1599,1600–1999,2000–2047 ; conserver un registre par position et revenir sur les réserves. Ne pas recycler ce lot.

Table active7AF000..7B2819 (14361octets), réserver capacitéjusqu’à7B8703, moteur etcombat. Lecteur common.py::names/LogicalTable v068 ou ultérieur obligatoire ; ancienne table et miroir préservés. Particularité byte85 : deux-points natif8x8 etB2observé, malgré métadonnéecharset0240 « point » ; pas de validation naturelle parB2. Sources privées vérifiées ànouveau ; aucune ROM ni état surGit. Principal6957,combat et2lieux préparés438/479 inchangés. Relecture exhaustive0 ; audits et scènes naturelles ouverts.

# Reprise v0.68 — table des noms relocalisée et cinq lieux intégrés

Lire dq6-fr/v0.68/README.md,audit-relocation.json,revue et QA. Reprendre BPSv068 surJP intacte.5lieux préparés intégrés :Abbaye des Vocations436,Château de Joliroche437,Pic des Terreurs464,Cap de Somnia481,Prison du Chagrin490.2lieux préparés438/479 restent pour mise en page ; capacité de stockage débloquée.

**Nouveau lecteur obligatoire :** common.py::names/LogicalTable v068 résout les pointeurs24bits avec la baseCPU FB8703. Ne pas utiliser v061.names ou nametable.Table sur la nouvelle ROM : ils supposent un emplacement physique historique. Table active7AF000..7B282F (14383octets) ; limite de capacité7B8703. Réserver au moins cette allocation dans tout futur build/fixture,ainsi que poolcombat etmoteurv061. Ancienne table0x3B8703..0x3BC712 et son miroir entièrement préservés,tail2050octets intact. Aucun code moteur modifié,157groupes de pointeurs dans deux copies.

Lecteur natif2477SIDs et15276octets,35dynamiques exclus,mutationSID16. La chaîne676 traverse7AFFFF/7B0000 ; lecteur,terrain/B2 vérifiés.10noms avant/après,20dialogues diagnostiques,5régressions pixels identiques ; cinq traductions relues. Bus4002plages etJournal à froid. Aucun parcours naturel de voyage/combat ni audit global des lecteurs hardcodés déclaré.

Principal6957sélections (6948linguistiques/9structures),combat597qualifiés/2préparés/5opaques/4structures inchangés. Noms62confirmés/2048physiques/2512SIDs/464alias ;344identifiants,1533autres,25candidatsFR,83videsàqualifier,1créditretiré. Relecture exhaustive0.438a22glyphes,479anciennecommande98. Autres tables etaudits hérités ouverts ;8Mio.

# Reprise v0.67 — dix lieux intégrés,22encodages équivalents

Lire dq6-fr/v0.67/README.md,revue-lieux-v067.json,revue-stockage.json,delta,inventaire etQA. Reprendre BPSv067 surJP intacte.10anciens lieux préparés intégrés :Desmodia420,Vallonclair424,Montgivré428,Donjon de Meurtor434,Brigandia441,Poste-frontière466,Chez madame Luce470,Manoir Médaillon473,Au fond du puits491,Tour des Maléfices517. Japonais SFC/DS exacts,24champsMPT JA/FR relus directement dansDS,ancienIPS secondaire.7lieux préparés restent ;aucune nouvelle préparation.

22anciens noms (6lieux,16sorts/actions) sont recomprimés sans changement des flux développés.26octets récupérés,26octets absorbés par les10lieux :tail0x3BBF10..0x3BC712 ettaillepool inchangés. Ne pas compter22encodagescomme22traductions.2502autres flux de glyphes et2480autres chaînes brutes identiques ;464alias préservés,2048physiques/2512SIDs. Noms57confirmés,344identifiants,1538autres,25candidatsFR,83videsàqualifier,1créditretiré. Principal6957sélections (6948linguistiques/9structures),combat597qualifiés/2préparés/5opaques/4structures inchangés. Relecture exhaustive0,4aides et16compositions inchangées.

Snes9x :2477SIDs statiques et15242octets lus,35dynamiques exclus ;mutationSID16 détectée.32noms terrain/B2 avant/après,64dialogues diagnostiques et22paires de pixels inchangées ;10nouveaux noms relus visuellement. Bus6513plages etJournal à froid. Aucun menu de voyage naturel ni autre consommateur globalement validé. Reprendre7lieux (48octets estimés,438largeur22 et479commande98),autres tables,relecture etaudits hérités. Protéger tail,moteurv061 etpoolcombat ;8Mio.

# Reprise v0.66 — huit noms de lieux intégrés

Lire dq6-fr/v0.66/README.md,revue-lieux-v066.json,delta,inventaire etQA. Reprendre le BPSv066 surJP intacte. SIDs417/418/423/425/426/430/443/450 :Puidebourg,Pierrebrute,Milmarin,Sorcéria,Aridéa,Mélankolia,Zénithia,Fort-Terreur. Références japonaises SFC etDS exactes,FRDS extrait directement de la ROM,ancienIPS secondaire.8préparations résolues ;17restent,aucune nouvelle préparation. Ne pas recycler ces8noms.

Stockage net0 :2048entrées physiques/464alias,2504autres chaînes identiques,157groupes de pointeurs actualisés en deux copies. Aucun octet du tail0x3BBF10..0x3BC712 touché. Principal6957sélections (6948textes/9structures) etcombat597qualifiés/2préparés/5opaques/4structures inchangés. Noms47confirmés/2048 ;344identifiants,1548autres,25candidatsFR,83videsàqualifier et1créditretiré restent distincts.4aides et16compositions inchangées. Relecture exhaustive0.

Snes9x :2477SIDs statiques entièrement lus,35dynamiques09A7..09C9 exclus ;mutationSID16 détectée. TerrainC3763A etB2C6FDF0 des8noms,16dialogues avant/après et8libellés relus visuellement,bus6513plages,Journal à froid. Diagnostics privés,pas de fenêtre de voyage naturelle validée. Reprendre17lieux/stockage,autres tables,ambiguïtés combat,relecture etaudits hérités. Préserver le tail,moteurv061 etpoolcombat.8Mio.

# Reprise v0.65 — chevauchement des noms corrigé, zéro nouvelle traduction

Lire dq6-fr/v0.65/README.md,qa-storage.json,delta et rapports. Reprendre le BPSv065 sur JP intacte. Cinq noms existants sont recomprimés avec le dictionnaire existant :7octets récupérés et fin de table2050octets restaurée à l’identique depuisv060 dans les deux copies.2048physiques/464alias,2512flux développés identiques ; principal et608emplacements combat inchangés. Ne pas recompter ces cinq noms comme traductions ou relecture exhaustive.

Snes9x :2477SIDs lus entièrement avec pointeurs ;35SIDs09A7..09C9 détournés versWRAM parC44FDF,donc exclus du test de table. MutationSID16 détectée. Lecteurs terrain etB2 des cinq noms identiques avant/après ;10dialogues diagnostiques,5comparaisons pixels et noms relus. Bus6513plages etJournal à froid. Aucun parcours naturel ou menu compact validé. La sémantique du tail reste inconnue : conserver intégralement0x3BBF10..0x3BC712.

Principal6957sélections (6948linguistiques,9structures),combat597qualifiés/2préparés27/277/5opaques603–607/4structures ; noms39confirmés/25candidatsFRàrelire/344identifiants/1556autres/83videsàqualifier/1créditretiré.25lieuxpréparés,4aides,16compositions inchangés. Relecture exhaustive0. Reprendre tables,ambiguïtés et audits hérités,naturels inclus.8Mio. Protéger pool combat et moteurv061 dans toute allocation.

# Reprise v0.64 — 11 compositions/contrôles combat et réserve héritée des noms

597 entrées combat qualifiées ;2libellés techniques27/277 préparés non insérés inclus dans le reliquat,5emplacements VF603–607 hors frontière JP,4structures.11entrées intégrées :5anglais traduits,6français corrigés,dont9fragments. Lire dq6-fr/v0.64/README.md,revue,delta,bindings et QA. Tester les fragments en composition,conserver+0C et les AC source restaurés de61/63/64.36scénarios positifs,1négatifC6,lecteurs,bus,démarrage et patchs vérifiés ; aucun parcours naturel déclaré.

**Réserve bloquante héritée v061 :** les noms atteignables ont grandi de7octets,de0x3BBF10 à0x3BBF17,dans une fin de table non auditée et nonFF.4octets ont changé ; le reste du tail est intact. v064 ne change pas cette zone. Lire audit-tail-noms-herite.json ; prouver l'absence de consommateurs ou relocaliser/recompacter proprement. Ne pas restaurer en place en corrompant les noms actifs. Restauration depuis Git ne vaut pas résolution de cette réserve.

Inventaire noms actuel2512SIDs/2048physiques/464alias :39français qualifiés,25candidatsFRàrevoir,344identifiants non traduits,1556autres textes à revoir,83vides à qualifier,1crédit retiré,0japonais détecté (pas preuve de français).25lieux préparés,4aides et16compositions inchangés. Principal6957 sélections dont9structures inchangé,relecture exhaustive0. Protéger pool natif et moteur v061. Reprendre27/277,slots603–607,tail hérité,autres tables,relecture et audits ; ne pas recycler le lot.8Mio.

# Reprise v0.63 — 191 entrées combat qualifiées, frontière JP corrigée

586 entrées françaises qualifiées en diagnostic. Ce lot comprend188 traductions anglaises,2 corrections françaises et1 fragment de composition497, pas191 nouvelles phrases autonomes.13 textes JP valides restent différés,5 emplacements VF603–607 restent opaques et4 structures restent hors traduction. Le lecteur JP historique débordait à603 dans le script principal compressé à0x37175B : lire audit-frontiere-source.json ; source_guard.py borne désormais la préparation à602. Les cinq emplacements sont conservés à l'identique, sans les appeler vides ou inutilisés. Aucun total608 de textes japonais n'est validé.

Lire dq6-fr/v0.63/README.md,inventaire,revue,delta et QA. Reprendre le BPS v0.63 sur JP intacte ; préparer avec ce nouveau lot uniquement. Principal6957 sélections dont9 structures,noms2512 SIDs/2048 physiques/464alias,39 français+4 aides,16 noms composés inchangés.25 lieux préparés. Relecture exhaustive du principal0. Protéger le pool natif déplacé ET moteur v0.61. Autres tables,audits hérités et scènes naturelles restent ouverts.8Mio conservés. Ne pas recycler les191IDs.

# Reprise v0.62 — 288 textes de combat hérités relus

395 textes natifs qualifiés,209 hérités encore non qualifiés,4 structures.190 anglais traduits et98 français corrigés dans ce lot. Lire dq6-fr/v0.62/README.md,revues,delta et inventaire.234 concordances japonaises complètes normalisées,2 compositions DS relues et52 adaptations directes SFC ; aucun rapprochement flou seul validé.21 corrections explicites de commandes héritées vers JP. Principal6957 sélections,2512 noms,16 noms composés,moteur v0.61 et police inchangés. Protéger nouveau pool natif ET allocation du moteur v0.61.18 cas différés inclus dans209 ; prochains IDs hérités continus à partir312. Relecture principale exhaustive toujours0 ; autres tables et scènes naturelles ouvertes. Ne pas recycler le lot.8Mio conservés.

# Reprise v0.61 — les trois derniers manquants du combat

107 messages combat intégrés, zéro préparation restante sur les107 anciens manquants ;497 hérités non qualifiés et4 structures restent séparés.464/465 : adaptation explicite en jeu de rimes, quatre mots variables conservés ;Céleste0369 etBraséria036A reliés aux entrées contextuelles DS349/351.498 :16 noms complets DS, petit lecteur localisé aux SIDs virtuelsFF00..FF10 et appelant497+498 ;vrai sort061F inchangé. Douze noms JA exacts, quatre variantesバキ/バギ adaptées explicitement par contexte, aucune identité JA inventée. Lire dq6-fr/v0.61/README.md, rapports et registre des réserves. Préserver aussi les nouvelles allocations moteur et le pool natif dans les futures recettes. Les tests forcés des16 branches ne prouvent pas leur accessibilité conjointe avec le RNG naturel. Principal6957 sélections et605 autres messages natifs inchangés ;2510 autres noms identiques et464 alias conservés. Autres tables,497 hérités, relecture exhaustive et audits naturels ouverts.8Mio conservés. Ne pas recycler cette revue.

# Reprise v0.60 — 64 messages natifs et sept accents

104 textes combat intégrés,3 préparés restants464/465/498 ;497 hérités non qualifiés et4 structures. Principal6957 sélections inchangé. Lire dq6-fr/v0.60/README.md, manifest.json etrapports. Extension isolée de sept slots inutilisés dans les consommateurs connus : police8x8 + correspondances principales, aucun moteur modifié.64 IDs testés,68 scénarios/236 captures ; autres544 messages natifs inchangés.397 : AD remplacé par espace, A/B et noms distincts passent en diagnostic, scène naturelle ouverte. Démarrage neuf recharge256 tuiles et menuJournal vérifié. Les états anciens conservent leur police.3 blocages dans blocages-restants.json ; noms, autres tables, relecture et audits restent ouverts. Pool natif réservé à8001024 sur16559 octets ;8Mio conservés. Ne pas recycler cette revue.

# Reprise v0.59 — quatre messages de combat intégrés

IDs337,428,454,455 intégrés :40 au total,67 préparés (dont2 réserves),497 hérités non qualifiés,4 structures. Principal6957 sélections et noms inchangés. Lire dq6-fr/v0.59/README.md et rapports ; restaurer toutes les versions puis exécuterprepare/build/verify etinventory. Ne pas recycler cette revue. B2/B4 testés en diagnostic,608 pointeurs contrôlés, neuf rendus acceptés et unB4 nul exclu ; menuJournal au démarrage vérifié. Aucun combat naturel, nom joueur ou fenêtre compacte validé.498 exclu : composition497+498 et16 noms DS toujours en préparation.64 accents,367,397, autres tables, relecture exhaustive et audits ouverts. Réserver le pool à8001024 sur12980 octets. Garder8Mio.

# Point de reprise combat-v066 — 16 noms DS préparés

Lire preparations/combat-v066/README.md et qa-preparation.json. Douze correspondances japonaises exactes, quatre réserves バキ/バギ. Aucune insertion : la composition native497+498 exige les deux choix, les noms DS ne sont pas factorisables par simple concaténation. Préserver061F partagé avec le vrai sort Flamme. Deux noms nécessitent é. Aucun nouveau test Snes9x. Version et patch restentv0.58 ;principal6957 sélections,combat36 intégrés/71 préparés inchangés. Les16 combinaisons sont un inventaire distinct et non additionnel. Relecture exhaustive et audits ouverts.

# Reprise v0.58 — 28 textes natifs de combat à noms variables intégrés

Reprendre v0.58, pas la base v0.56 seule.36 français intégrés dans le pool combat ;71 préparés non insérés (69 relus sémantiquement,2 réserves464/465),497 hérités non qualifiés,4 structures. Principal6957 sélections inchangé (6948 linguistiques,9 structures) ; noms et autres tables inchangés. Lire dq6-fr/v0.58/README.md, inventaire-combat-v058.json et les rapports. La recette applique le BPS v0.57 vérifié à la JP intacte, conserve ses huit traductions et insère les28 IDs explicites. Le BPS v0.58 est autonome sur JP intacte.

B7/B8 testés via le résolveur natif avec deux entités distinctes puis homonymes A/B, noms hérités anglais de13/15 caractères utilisés pour les rôles et largeurs seulement.543 : trois AD remplacés par des espaces, mots et autres commandes identiques ; rendu retesté.397 reste PREPARE_NON_INSERE : après AD, le profil homonyme affiche A puis A, cause native/contexte à tracer avant insertion. Lire blocage-397.json. Les71 restants comprennent64 cas avec accents,6 substitutions ASCII complexes et397. Camp diagnostique C02A29 uniquement ; pas de combat naturel, chemin des noms de personnages ni fenêtre compacte validés. Autres tables, relecture exhaustive, audits hérités ouverts ;8 Mio conservés. Réserver aussi le pool natif déplacé dans les futures allocations.

# Reprise v0.57 — huit textes natifs de combat intégrés

Reprendre v0.57 :8 textes statiques intégrés (51,427,429,494,519,520,536,538),99 préparés encore non insérés et497 hérités non validés ;4 structures hors traduction. Principal6957 sélections inchangé, tables de noms inchangées. Lire dq6-fr/v0.57/README.md, inventaire-combat-v057.json et les rapports. prepare.py/build.py/verify.py reconstruisent depuis JP intacte plus le BPS v0.56 vérifié ; les fichiers v0.57 sont suivis directement. Le BPS v0.57 s’applique à la JP intacte. Pool natif déplacé : réserver aussi ce nouveau segment dans toute allocation future du principal. Ne pas recycler les huit IDs comme nouvelle revue.

Les608 pointeurs et premiers octets natifs passent sous Snes9x ; huit textes sont relus à l’écran par l’API C02A29, aucun combat naturel déclaré. BC/BD/B1/C2/AF/AD sont conservés. Pour427/429, les appels source C02A16 confirment la grande fenêtre ; les tests petite fenêtre ne les valident pas. La correction de protocole est dans les ROM privées de diagnostic seulement, pas dans le moteur de production. Accents, noms variables, réserves464/465, autres tables, relecture exhaustive et audits hérités restent ouverts.8 Mio conservés.

# Reprise combat-v060 — Céleste préparée, aucune insertion

Un nouveau nom SID0369/Céleste préparé depuis trois références DS vérifiées, alias physique contrôlé.107 textes de combat inchangés et non insérés. Parcours depuis le camp vers le château consigné en entrées de manette ; aucun combat validé. Alphabet latin et ponctuation relus sur la police résidente de terrain, plan0 ; chargement/rendu en combat et accents toujours non approuvés. Lire tools/combat-v060/README.md. ROM/patch restent v0.56, principal6957 sélections dont9 structures ; autres tables, relecture complète et audits ouverts.

# Reprise combat-v059 — lecteur natif, aucune insertion

Lecteur natif vérifié sous Snes9x pour608 IDs, mutation de pointeur détectée.107 préparés restent non insérés. Le modèlev058 repose sur la table Huffman : ses43 allers-retours/64 caractères manquants ne prouvent pas la police native. Relever la police en combat et établir B2 de465 avant codec/insertion. Archive privée d’états sauvegardée dans cette conversation mais non récupérée après réinitialisation ; aucun état de combat validé. Puis497 hérités, autres tables, relecture et audits naturels. Lire tools/combat-v059/README.md et les rapports. Le patch restev0.56. Aucun fichier ROM, SRAM ou état ne doit être publié sur Git.

# Reprise combat-v058-codec — aucune insertion

Combat :43 candidats encodables strictement,64 bloqués par accents absents ;107 préparés toujours non insérés. Essai de rendu camp rejeté : obtenir un contexte de combat/fenêtre naturel. Alphabet byte à étendre avec preuve globale ou maintenir le blocage. Réserves464/465 et497 hérités toujours ouverts ; autres tables, relecture exhaustive et audits naturels ensuite. Lire tools/combat-v058/README.md et les deux rapports QA. Le patch reste v0.56. Ne pas convertir un aller-retour de codec ni un ID en RAM en validation visuelle. Le test camp natif échoue à afficher une fenêtre lisible et reste explicitement rejeté. Les préparationsv057 restent inchangées.

# Reprise combat-v057 — préparations non insérées

Pool combat :107 propositions préparées non insérées,105 relues et2 réserves464/465. Établir codec/largeurs/commandes et essais natifs avant insertion ;497 textes hérités encore non relus. Puis autres tables, recherche exhaustive, relecture intégrale et audits naturels. Le script reste6957 sélections (6948 linguistiques et9 structures), patchv0.56 inchangé. Lire preparations/combat-v057/README.md et qa-preparation.json. Les105 relectures ne valident pas le codec ni le rendu. Ne pas rejouer ces préparations comme nouvelles traductions.

# Reprise après inventaire du combat — v0.56

Script principal terminé : ne pas rejouer le lot16. Priorité au pool séparé de combat608 entrées (107 identifiants sans texte,497 héritées non relues,4 structurelles), avec japonais/DS/contexte. Puis compléter noms/menus/objets/sorts/classes et recherche des autres ressources, relecture exhaustive et audits naturels. Zéro français validé pour le pool combat par ce seul inventaire. La preuve verification-v056-depuis-git.json vérifie une restauration neuve et les patchs du commit c04ad91728580dfda8feb5a055fb451c298dfb2b. Les rapports du lot attestent les anciens tests Snes9x ; ne pas les prendre pour des tests nouvellement exécutés dans le contrôle de restauration. L’audit de ressources reste incomplet hors des trois pools identifiés.

# Reprise v0.56 — passer aux tables et à la relecture

16 derniers textes intégrés. Script principal6957 sélections dont6948 entrées linguistiques et9 structurelles ; zéro texte principal en attente. Trois corrections isolées de disposition équipement et réparation de frontière6956 explicites. Tests diagnostiques réussis, scènes naturelles encore ouvertes. Passer à la recherche exhaustive des ressources oubliées et aux tables séparées, puis relecture intégrale suivie par IDs. Terminer les audits naturels ; ne pas déclarer le projet finalisé. Ne pas recycler la revue v0.56. Restaurer toutes les versions, y compris replacements_file v0.56. Garder la distinction entre traduction complète du script et finalisation du projet.

# Reprise v0.55

29 traductions et9 restaurations exactes de structure. Toutes les6903 anciennes sélections inchangées. Tests de composition AE, énigme et directions ; audits naturels ouverts. 16 textes restants :12 debug ambigus et6956 préparés non insérés,3 fragments équipement différés. Tables, recherche exhaustive des oublis, relecture intégrale et audits naturels à poursuivre. Ne pas recycler cette revue. Ne pas prendre les9 structures pour9 traductions.

# Reprise v0.54

8 textes à commandes natives C7/DC/E0/E1 relus. Autorisation minimale du compilateur, moteur et anciens tokens inchangés ; branches et noms testés en diagnostic. Continuer les54 entrées dont25 préparées non insérées, fragments assemblés, tables, audits naturels et relecture exhaustive. Ne pas recycler la revue de ce lot.

# Reprise v0.53

12 textes : six C4, casino, variante technique à X littéraux, refrain et libellés. Commandes et noms natifs gardés, deux branches C4 testées en diagnostic. Continuer les62 entrées dont25 préparées non insérées, les tables et audits naturels. Recherche des oublis et relecture exhaustive encore à faire. Ne pas recycler la revue de ce lot.

# Reprise v0.52

Trois indices relus : orbe1135, salle à répétition2404, bouclier5341. Écarts SFC/DS explicitement conservés ; parcours naturels encore ouverts. Continuer les74 entrées, dont26 préparées non insérées, puis les tables, recherche des oublis et relecture complète. Ne pas recycler la revue de ce lot.

# Reprise v0.51

16 descriptions de vocations SFC relues avec lexique DS explicite. Techniques, prérequis et mécaniques SFC conservés ; ancien IPS secondaire corrigé sans servir de validation. Continuer les77 entrées, dont26 préparées non insérées, les tables et audits. Après traduction, recherche exhaustive des oublis et relecture de tous les textes par lots suivis. Ne pas recycler la revue de ce lot.

# Reprise v0.50

135 dialogues, récits, retrouvailles et conversations finales relus. Plans explicites : ordre de tous les contrôles hors mise en lignes conservé, pauses sources gardées, locuteurs et noms non consolidés. DS prioritaire pour les références explicites, écarts SFC conservés ; IPS secondaire non admis comme validation de ses décalages. Continuer les 93 messages, dont26 préparés non insérés, les tables et les audits naturels. Les commandes rares C7/DC/E0/E1, les fragments assemblés et les choix couplés exigent encore une revue spécifique. Lire native_plan.py et les plans du lot, ne pas recycler cette revue pour le prochain lot.

# Reprise v0.49

57 dialogues, narrations et répliques à commandes natives relus. Plans explicites : ordre de tous les contrôles hors mise en lignes conservé, pauses sources gardées, locuteurs et noms non consolidés. DS prioritaire pour les références explicites, écarts SFC conservés ; IPS secondaire non admis comme validation de ses décalages. Continuer les 228 messages, dont19 préparés non insérés, les tables et les audits naturels. Les commandes rares C7/DC/E0/E1, les fragments assemblés et les choix couplés exigent encore une revue spécifique. Lire native_plan.py et les plans du lot, ne pas recycler cette revue pour le prochain lot.

# Reprise v0.48

143 textes SFC relus : dialogues, panneaux, objets légendaires, commerces et quelques libellés techniques. 69 références DS de formulation, fragments ou lexique, avec écarts SFC documentés ; 74 adaptations directes sans équivalent DS validé. Pauses natives conservées. Ancien IPS secondaire relu mais ses nombreux décalages sont rejetés. Terminer les 285 entrées restantes, dont19 préparées non insérées, en traitant les dialogues couplés et commandes avant toute annonce de finalisation. Continuer aussi les tables et audits naturels.

# Reprise v0.47

142 libellés techniques, progression des quêtes et textes de démonstration SFC relus directement. Français DS utilisé comme lexique explicite pour 47 entrées ; aucun dialogue DS équivalent déclaré. Trois pauses d’avertissement natives conservées et testées. Huit brouillons ambigus restent non insérés, avec onze fragments hérités. Continuer les 428 messages restants dont 19 préparés non insérés, les tables et les audits naturels. Projet non finalisé.

# Reprise v0.46

111 ajouts : commerces, achats/reventes, banque, Journal, vocations, compagnons, noms et concours. B3/C0/C9/D3, B2, BB, B5 et D8 restent variables. 66 formulations DS relues/adaptées ; 45 adaptations directes SFC sans équivalent DS validé. Aucun rapprochement flou seul admis. Onze fragments préparés non insérés en attente de test d’assemblage ; 150 brouillons de libellés techniques/progression sauvegardés séparément, sans validation d’insertion. Continuer les 570 textes restants dont 11 fragments préparés et 150 brouillons non insérés, les tables et les audits naturels. Projet non finalisé.

# Reprise v0.45

111 ajouts : objets, déplacement, mémoire SFC, Journal, sac sauvegardé C3 et nouveau nom D8. 57 formulations DS relues/adaptées ; 54 adaptations directes SFC sans équivalent DS validé. Aucun rapprochement flou seul admis. Onze fragments préparés non insérés en attente de test d’assemblage. Continuer les 681 textes restants dont 11 fragments préparés, les tables et les audits naturels. Projet non finalisé.

# Reprise v0.44

Correction technique isolée : extension minimale Huffman C4/DF, vecteur C4 japonais rétabli, quatre aides grammaticales adaptées. Aucune sélection principale ajoutée ou modifiée. Nom du sac conservé en sauvegarde. Traduire les 792 textes restants ; conserver les réserves et les audits naturels ouverts.

# Reprise v0.44

Correction technique isolée : extension minimale Huffman C4/DF, vecteur C4 japonais rétabli, quatre aides grammaticales adaptées. Aucune sélection principale ajoutée ou modifiée. Nom du sac conservé en sauvegarde. Traduire les 792 textes restants ; conserver les réserves et les audits naturels ouverts.

# Reprise v0.43

63 ajouts : cris, répliques courtes, noms variables de sorts et de vocations, appels aux compagnons. 6414 conserve deux C0, 6416 deux C0 et B2, 6441 deux C0 puis D3 ; 5281 deux C9. Noms de locuteurs natifs conservés. Les 26 cas différés historiques v0.34 sont réconciliés : 2368 et 6265 résolus explicitement en v0.41, 24 encore différés. Le reliquat reproductible compte 792 textes non validés et sépare les propositions de mots des validations. Continuer les 792 textes et les tables. Audits hérités et scènes naturelles ouverts, pas finalisé.

# Reprise v0.42

71 ajouts : utilisation, appréciation, équipement, transfert, abandon et rachat d’objets. Noms natifs B5 et rôles C0/C1/D3 explicitement liés ; la garde d’ambiguïté du compilateur ne s’ouvre que si tous les rôles contextuels sont liés par la revue. Contrôle indépendant de chaque occurrence conservé. 5917 garde ses deux C1, comme les deux japonais, sans réduire silencieusement la répétition. Objet et prix du marchand restent variables. Les objets fixes des descriptions DS sont remplacés par le B5 SFC, sans nom figé ni effet d’objet inventé. Continuer les 855 textes et les tables. Audits hérités et scènes naturelles ouverts, pas finalisé.

# Reprise v0.41

64 ajouts relus, 5967 anciens tokens et tous les noms inchangés. Dialogues, panneaux, services et cris ; aucune extension du moteur. 71 pages de diagnostic pour les 64 textes. Continuer les 926 textes et les tables. Conserver audits hérités, 25 lieux préparés et 26 cas différés v0.34. Aucune finalisation annoncée.

# Reprise v0.40

40 ajouts relus ; 5927 anciennes sélections et 2512 noms inchangés. Rendu des 40 textes : 75 pages, plus 11 pages de stress B5 sur cinq textes. Diagnostics au camp, pas les scènes naturelles. Continuer les 990 textes, tables et réserves héritées. B5 natif maintenant lié explicitement aux noms d’objets ; réserve 24 cellules, sans ponctuation accolée. Ne pas annoncer finalisé.

# Reprise DQVI FR depuis GitHub

Dernière version : v0.39, 5927/6957 intégrés, 1030 restants. 22 ajouts nouveaux, zéro préparé principal. Tables inchangées : huit lieux, Gus et 20 noms de sorts/actions ; 37 entrées FR confirmées, 25 lieux préparés. Toujours 8 Mio.

## Lot v0.39 : noms et nombres natifs

Lire v0.39/LISEZ-MOI.md et revue-lot-v039.json. Périmètre strict de 22 nouveaux IDs ; 5905 anciennes sélections et 2512 noms inchangés. Recette pass39.py, base v0.38, helper spells.py hérité. Override de locuteur explicite seulement sur les IDs relus. Deux D2 dans 5647, huit C9 et CB/CA dans 4757 ; Tommy littéral reste littéral. Tous les 22 textes ont des bancs de rendu, 117 pages relues, pas scènes naturelles ni transactions. IMPORTANT BB : initialiser trois octets 5A2E/5A2F/5A30, pas seulement deux. Le premier banc montrait 7352377, reprise avec [39,30,00] hex : 12345. Rapport historique v0.19 conservé, correction isolée qa-protocole-BB-24bit.json. Aucun handler modifié. Audit alphabet des noms : 28 octets non observés, aucun prouvé libre ni réaffecté. Continuer 1030 textes et tables ; 26 cas différés v0.34, 25 lieux préparés, fenêtres natives, accents et scènes naturelles héritées restent ouverts. Ne pas annoncer finalisé.

## Lot v0.38 : 20 noms de sorts/actions

Lire v0.38/LISEZ-MOI.md et revue-sorts-v038.json. Périmètre strict : 20 SID sans alias, ASCII complet, une ligne, au plus neuf cellules, aucune largeur augmentée. Aucun ajout principal ; revue-lot-v038.json vide intentionnellement. 5905 sélections et 2492 autres noms inchangés. Recette pass38.py, helper spells.py, comparaison avec v0.37. Snes9x B2 : les 20 noms observés trois fois chacun, pas leurs fenêtres natives de sorts/combat ni exécution des actions. Sonde initiale manquant les noms courts conservée ; ne pas prétendre en connaître la cause exacte ni avoir corrigé le moteur. BPS/IPS, mauvaises sources, redécodage, bus et Journal vérifiés. Inventaire : audit_tables.py v0.38 puis inventaire_tables_v038.py v0.38. Continuer 1052 textes et les tables ; alphabets accentués, fenêtres natives, 25 lieux préparés, 26 cas différés v0.34 et scènes naturelles héritées ouverts. Ne pas annoncer finalisé.

## Lot v0.37 : variantes DS adaptées

Lire v0.37/LISEZ-MOI.md et revue-lot-v037.json. Périmètre strict de 51 nouveaux IDs, 5854 anciennes sélections et 2512 noms inchangés. Ne pas compter ces revues comme un futur lot. Recette pass37.py, comparaison avec v0.36. 6960 entrées redécodées, BPS/IPS et mauvaises sources, zones protégées, bus ROM, démarrage/Journal vérifiés. 45 captures sur 12 messages, pas tous les 51 et pas un parcours naturel. 6220 garde DE/D5 et un texte de deux pages, choix hôte séparé. Pierre/Pierrick relus dans les DS 0024:465–477 ; Tommy littéral reste littéral. Aucun préparé principal. Continuer les 1052 textes, tables et réserves héritées ; ne pas annoncer finalisé. Inventaire par audit_tables.py v0.37 puis inventaire_tables_v035.py v0.37. Ne pas écraser les anciens outils empreintés.

## Lot v0.36 : 4095 concis

Lire v0.36/LISEZ-MOI.md et preparations-resolues.json. Formulation fidèle de six lignes, deux pages de texte cohérentes, D5 conservé. Le choix hôte conserve ensuite le dernier écran, avant les messages hôtes. Cinq captures relues ; aucun correctif machine. Ancien essai et ancien préparé v0.34 conservés ; cause exacte du chevauchement précédent non établie. Scène naturelle de marchands non parcourue. 5853 anciens textes et 2512 noms conservés. Recette pass36.py, delta v0.36, comparaison avec v0.35 construit ; ne pas réinsérer l'ancien texte long du 4095. BPS/IPS, redécodage, zones protégées, bus et Journal vérifiés. Continuer 1103 textes et tables ; les 26 autres cas différés v0.34 et les réserves de parcours naturels restent ouverts. Ne pas annoncer la fin.

## Lot v0.35 : Gus

Rookie devient Gus, nom officiel DS de ルーキー, MENULIST6 FR b1001000.mpt:8. SID 0930, position 1888, ASCII complet plus court. Builder vérifie les anciens octets et champs JP SFC/DS JA/FR. 2511 autres noms et 5853 textes conservés. BPS/IPS, redécodage, bus script+tables, Journal et six pages de 1836 vérifiés : Gus/AM/Gus, deux B2 visibles. RAM du banc uniquement, pas scène naturelle de recrutement. Ne pas modifier les noms personnalisés des sauvegardes. Recette pass35.py, delta v0.35 ; comparaison stricte avec v0.34 construit. Audit tables reproductible par audit_tables.py v0.35 puis inventaire_tables_v035.py v0.35. Ne pas modifier les anciens outils inventaire_tables.py ou inventaire_tables_v033.py, empreintés dans les anciens lots. Continuer script et tables ; 4095 D5 et autres réserves restent ouverts.

## Lot v0.34 : 121 ajouts

Lire v0.34/LISEZ-MOI.md et revue-lot-v034.json. Noms, directions, temporalité, alcool, carte/clef, épée légendaire et équipement perdu SFC explicitement adaptés. Nom DS lame du Châtiment et clef du geôlier vérifiés dans MENULIST6. 5732 anciens textes et 2512 noms inchangés, dont correction 323, 1836 et huit lieux. Recette pass34.py, delta v0.34 ; ne pas réutiliser cette revue comme nouvelle traduction. Vérifier init/prepare/build/verify et check_body_names.py ; v0.33 construit nécessaire pour la comparaison stricte des noms. Contrôles patchs, redécodage, zones protégées et bus script+tables ; Journal et 16 textes par diagnostics au camp, pas les parcours naturels.

4095 : PREPARE_NON_INSERE. Dernière page D5 avec reprise de lignes dans le camp ; cause non établie. Conserver prepares-non-inseres.json et qa-4095-preparation.json. Ne pas supprimer D5, vérifier la scène de marchands naturelle. Les 26 autres cas différés sont documentés avec sources, fichier et IDs DS ; ne pas les insérer automatiquement. Continuer 1104 textes et tables. Garder indices 610/1135/2404/5341/5351, alphabet accentué et fenêtres naturelles des tables. Aucune finalisation annoncée.

## Lot v0.33 : huit lieux

Lire v0.33/LISEZ-MOI.md et revue-lieux-v033.json. Port Abbri, Monstria, Colombourg, Kupidia, Noirgibet, Somnia, Militia, Typhonia. FR DS complet, JP SFC/DS exacts vérifiés par builder, ASCII existant et largeur non supérieure à l'ancien libellé. Pas de troncature ni accent supprimé. 157 groupes et 464 alias conservés, 2504 autres SIDs et 5732 textes inchangés. BPS/IPS, redécodage, bus des deux pools et pointeurs, Journal et huit noms par B2 au camp vérifiés. Menus de voyage naturels non parcourus, ne pas les annoncer validés. Recette pass33.py et delta v0.33. Inventaire mis à jour : 16 entrées FR confirmées, 25 lieux encore PREPARE_NON_INSERE. Continuer script et tables, garder réserves des accents/fenêtres/indices différés.

## Lot v0.32 : 1836

Lire v0.32/LISEZ-MOI.md et blocage-rendu-1836.json. Le second B2 est visible en quatrième page du nouveau texte à pagination explicite. L'ancien banc de trois pages ne montrait pas ce nom ; la cause précise de son échec n'est pas établie. Maintenant intégré avec ordre B2/D3/B2, Rookie/AM/Rookie visibles après injection diagnostique 5A28=0930. Six pages jusqu'au choix hôte et au message hôte 101 ; moteur inchangé. Japonais SFC et DS relus, VF adaptée aux faits et noms SFC. 5731 anciennes sélections conservées, correction 323 héritée intacte. Recette pass32.py utilisant templates compilateurs v0.30 et données baseline v0.31 ; delta v0.32. Restauration complète et reconstruction à vérifier à chaque point de reprise. Les scènes naturelles 322/323 et 1836 restent à vérifier ; 5351/5341 et cas différés v0.30 ouverts. Continuer 1225 textes et tables ; aucune finalisation annoncée.

## Lot v0.31 : tapis 322/323

Lire dq6-fr/v0.31/LISEZ-MOI.md et audit-tapis-reordonne.json. 322 nouveau, 323 corrigé explicitement : les français DS 0056:584–588 étaient réordonnés, l'ancienne sélection 323 portait les faits de 322. Revue de tout le bloc JP/FR DS et JP SFC. 5729 autres anciennes sélections inchangées. Restauration étendue avec replacements_file gardé par empreinte des tokens et ancien texte ; 7 tests unitaires. Ne pas retirer ce mécanisme ni réappliquer l'ancien 323. Recette pass31.py et delta sources/lots/v0.31.json. BPS/IPS réappliqués, 6960 entrées redécodées, bus 870 groupes/467014 octets ; Journal et 8 pages 321/322/323 relues. Redirections de diagnostic au camp, pas les branches naturelles. Continuer 1226 textes et tables, audit 1836 et indices 5351 ouverts ; ne pas annoncer la fin. Les 33 lieux restent PREPARE_NON_INSERE : alphabet accentué, tailles, pointeurs et fenêtres à tester.

## Lot v0.30 : 114 ajouts

114 textes relus dont six courtes répliques ancrées dans leurs séquences DS. 47 adaptations explicites : fins SFC omises, noms restitués ou retirés, carte SFC plutôt que clef DS, action d'ouverture de commode accomplie, croix sur le bouclier de Valora (nom DS MENULIST6 b1000000:155), royaume évoqué sans expliciter les dimensions. Six propositions non intégrées documentées dans nouveaux-cas-differes.json : indice du bouclier 5341 avec 5351, répétitions 1356, orbe 1135, litanie 4880, regard sur monde/fond marin 5778/5818. Pas de score flou employé seul comme validation.

5616 anciennes sélections conservées. Toutes les occurrences des noms dans les corps des 114 textes sont comparées à SFC, y compris C0 ; labels répétés de locuteurs exclus de ce compte. BPS/IPS réappliqués, 6960 entrées redécodées, octets hors zones autorisées inchangés. Snes9x : bus 870 groupes/466984 octets, Journal au démarrage, 40 pages sur dix messages relues ; C0 en 5868 avec Olivier après RAM 3B2D=2. Bancs au camp, pas de parcours naturel. ROM SHA256 16a920616d6c86767559dea03a9ce06c1f9986bb1349da88094a62a255db73a3.

Recette idempotente dq6-fr/pass30.py, delta sources/lots/v0.30.json ; restauration par restore_sources.py et reconstruction init/prepare/build/verify sous v0.30. Lire l'inventaire v0.29 pour les tables ; ne pas insérer de noms accentués sans maîtriser l'alphabet d'octets et leur affichage. Garder les audits 322/323 et 1836. Continuer les 1227 messages et les tables sans plafond artificiel, avec sauvegarde après chaque lot.

## Lot v0.29 : 64 ajouts et inventaire des tables

64 propositions auparavant différées relues et intégrées, 61 adaptations détaillées dans revue-lot-v029.json ; 5552 anciennes sélections conservées. Les corps des nouveaux textes gardent exactement les occurrences des variables de noms SFC, hors labels de locuteurs consolidés. Tommy (nom français DS par défaut du Terry japonais) est littéral en 5673 avant son recrutement, sans nouveau CD ; Laura n'est pas nommée avant sa présentation en 2300. Exceptions de locuteurs 1111/6749/5252 et ouvertures anonymes 1203/5036/5040 contrôlées explicitement. L'indice supplémentaire DS du coffre du lac est retiré de 719 ; le titre non nommé de 4061 reste non nommé ; la vente 3046 est une carte, pas une clef. Recette idempotente pass29.py, delta sources/lots/v0.29.json.

BPS/IPS réappliqués, 6960 entrées redécodées, octets hors zones protégées inchangés, 870 groupes et 462145 octets sur le bus ; 57 pages de onze messages et démarrage Journal relus dans Snes9x. Redirections de diagnostic au camp, aucun parcours naturel complet. ROM SHA256 813ce33afb47fb0728a1d66b5097cd7a546095b180422755c922fcdfe4faf930. Captures et états locaux seulement.

Tables : audit_tables.py v0.29 puis inventaire_tables.py v0.29. Inventaire par blocs physiques, pas par numéro de SID : conserver les 464 alias et les 157 pointeurs. 906 correspondances JP exactes à une VF DS unique ne sont pas 906 validations. Les 349 identifiants et 82 vides incluent des zones à qualifier ; les 1585 AUTRE incluent aussi du français hérité, pas seulement de l'anglais. 33 lieux sont PREPARE_NON_INSERE, sans compte intégré. Encodage accentué, fenêtres, sauts de ligne et repacking à tester avant insertion ; détails et marges dans inventaire-tables.json. Audits 322/323, 1836 et indice 5351 ouverts. Continuer sans plafond de 150, en sauvegardant chaque lot ; ne pas forcer ces ambiguïtés pour finir dans la nuit.

## Lot v0.28 : 150 ajouts

150 textes relus et intégrés, 0 préparé non inséré ; 65 autres propositions examinées restent DIFFERE_NON_INSERE. 19 adaptations détaillées dans revue-lot-v028.json, notamment la réalité du récit de Méphisto et la régénération en combat plutôt qu’en marchant. Aucune ancienne sélection intégrée modifiée. Recette idempotente dq6-fr/pass28.py, delta sources/lots/v0.28.json ; seules les 150 nouvelles identités relues peuvent être intégrées. Les ouvertures mixtes de Tulipe (3256) et l’alias カルベ/カルベ夫人 (6804, déjà établi dans cette branche) sont contrôlés explicitement.

Contrôles : 5402 anciens messages inchangés, octets hors zones autorisées conservés, BPS/IPS réappliqués, 6960 entrées redécodées, mauvaises sources rejetées. Snes9x : 870 groupes, 456996 octets sur le bus, Journal au démarrage à froid, 72 pages de onze textes relues avec noms variables. Redirections de diagnostic au camp, aucun parcours naturel des 150 scènes. Audits 322/323 et 1836 ouverts. Lire l’audit des 65 candidats différés ; ne pas intégrer automatiquement leurs propositions. L’ancien IPS présente beaucoup de textes décalés ou lacunaires. Les 1405 restants sont ici marqués hors_lot_revu ; reprendre aussi les motifs détaillés de v0.27 pour les commandes bloquées.

## Lot v0.27 : 150 ajouts

5402/6957 messages intégrés, 1555 restants plus tables séparées. Les 5252 anciennes sélections et les octets hors zones autorisées sont conservés. Recette idempotente dq6-fr/pass27.py ; delta lisible sources/lots/v0.27.json. Les anciennes correspondances encore non intégrées remplacées par ce lot sont archivées dans revues-preparatoires-remplacees.json ; aucun ancien texte intégré n'est réécrit.

Huit adaptations explicites, dont bonus SFC +1 contre DS +5 et niveau inchangé au changement de vocation. Voir revue-lot-v027.json. Sept cas étudiés restent différés : ne pas reprendre automatiquement le contre-sens de 3526, le référent du démon 4061, le nom CD avant recrutement 5673, les renseignements du coffre 719 ni les locuteurs 5252/5036. Contrôles : BPS/IPS réappliqués, 6960 entrées redécodées, 870 groupes et 445461 octets vérifiés sur le bus. Snes9x : menu Journal au démarrage à froid, 39 pages de neuf dialogues et un rendu contextuel de 5988 avec Olivier (+1) après injection RAM 3B2D=2. ROM SHA256 473fc5936f2123409a7bf9936f3f04e6ac3f86023a070f858f5a04f3721a82b7. Ces bancs n'équivalent pas à un parcours naturel. Audits 322/323 et 1836 ouverts. Sources, rapports et BPS uniquement sur Git ; captures, ROM et états locaux.

## Lot v0.26 : 100 ajouts

Cent dialogues relus et regroupés depuis les segments DS. 5252/6957 sélections intégrées, 1705 restantes plus tables séparées. Les 5152 anciennes sélections et tous les octets hors zones autorisées sont conservés. Cinq adaptations explicites : habitants sauvés dans le discours final de Zénith, chambre des soldats à l'étage, duel contre le champion du Gluodrome, enquête sur l'abbaye hors du rêve, nom supplémentaire DS retiré de 4358. Voir revue-lot-v026.json.

Recette idempotente dq6-fr/pass26.py et delta lisible sources/lots/v0.26.json. La restauration sans ROM reproduit les sélections ; avec les sources, init.py puis prepare.py/build.py/verify.py sous v0.26 reconstruisent la ROM SHA256 232ec6f2e3bfbd8e3d7cf7af52d252e242dad9697c2e7d2466f02c6241cbdd46. BPS/IPS réappliqués, 6960 entrées redécodées, 870 groupes et 432620 octets vérifiés sur le bus. 44 pages de six dialogues relues par redirections dans le camp initial, noms variables et voix inclus. Démarrage, Journal, cadre du nom et arrivée au camp vérifiés dans Snes9x. Pas de parcours naturel de ces scènes ni test de tous les nouveaux messages. Audits 322/323 et blocage 1836 ouverts. Sources, rapports et BPS publiés ; les captures, ROM et états restent locaux.

## Lot v0.25 du 19 octobre 2026

12 ajouts à Montgivré : village gelé puis réveillé, avertissement et confession de Saul Ytaire, visiteur du sage et itinéraire de Kad Abra. Les 5140 anciennes sélections sont inchangées. Message 571 : DS 496 et 502 sont deux variantes il/elle ; la SFC partage une seule réplique, adaptée en « Cette personne est gelée ». Recette idempotente `dq6-fr/pass25.py`, delta lisible `sources/lots/v0.25.json`. Restaurer puis lancer init.py, prepare.py, build.py, verify.py sous v0.25. ROM SHA256 `f6169c83fd1fe8da2ee6b527a971679fcb8eea2fa7057fba092efcfb834dc266`. BPS/IPS réappliqués, 6960 entrées redécodées, 870 groupes et 420639 octets sur le bus ; 25 pages sur cinq messages (571,591,605,623,626). Aucun parcours naturel complet ni validation globale des tables. Audits 322/323 et blocage 1836 ouverts. Formule 610 différée : relire ensemble indices, mot de passe et réponses SFC avant insertion ; les jeux de mots DS ne peuvent être repris indépendamment des choix de la porte. Les boissons 598–602 restent aussi différées : alcool SFC contre thé DS et réponses modifiées. Sources et BPS publiés sans ROM ni état.

## Lot v0.24 du 19 octobre 2026

12 ajouts : récit complet de Lynx sur Charles, Éthel et Martel, habitants de Colombourg, regard fixe de Martel et refus d’entrée. 5128 anciennes sélections inchangées. La question 553 parle des reliques légendaires (armes et armures dans les deux japonais), pas seulement de l’épée comme en FR DS 734. Recette idempotente `dq6-fr/pass24.py` et delta lisible `sources/lots/v0.24.json` ; restaurer puis exécuter init.py, prepare.py, build.py, verify.py sous v0.24. ROM SHA256 `4ff2ef0d45e5f91cab6cd349fb5612fd25b934b6b7fdf39b7a9fd103c1ca25b5`. BPS/IPS réappliqués, 6960 entrées redécodées, 870 groupes et 419905 octets sur le bus ; 26 pages ciblées sur quatre messages (528,536,553,567). Aucun parcours naturel complet ni validation globale des tables. Audits 322/323 et blocage 1836 toujours différés. Le refus violent 535 n’est pas repris automatiquement depuis la DS, qui en a supprimé une partie ; la narration 541 à variable reste à adapter. Ne pas confondre les silences de Martel 414 et 504. Sources et BPS publiés sans ROM ni état.

## Lot v0.23 du 19 octobre 2026

30 ajouts relus à Colombourg et autour du défi de Lynx. Les 5098 anciennes sélections restent identiques. Accueil pluriel et deux descriptions de pièces adaptés au japonais SFC avec appui IPS ; tarifs 50000 puis 2000 conservés. ROM résultat SHA256 `3f119ae5e9a55b03dcfd09bb4d1b01bfaee94d2de3df4aab6f25503973c5c08b`. Reconstruction : `init.py`, `prepare.py`, `build.py`, `verify.py` sous `dq6-fr/v0.23/`. Le delta lisible `sources/lots/v0.23.json` et la recette idempotente `dq6-fr/pass23.py` restaurent ce lot sans ROM. BPS/IPS réappliqués, 6960 entrées redécodées, 870 groupes et 419352 octets sur le bus ; 27 pages sur sept messages (383,397,407,458,459,489,526) relues en banc de camp. Aucun parcours naturel complet ni validation globale des tables séparées. Audits 322/323 et blocage 1836 toujours ouverts. Le BPS est publié ; l’IPS et les captures restent dans la sauvegarde locale sans ROM ni état.

Après un clone, lancer `python restore_sources.py`. Ce script vérifie les empreintes des morceaux sous sources/ et patches/, restaure les sources complètes de la v0.19 et les IPS. Les fichiers déjà modifiés sont conservés. Le BPS utilisable directement est sous patches/. Le fractionnement des archives sert uniquement au transfert ; le script les reconstitue automatiquement.

Les sources comprennent les extractions FR/JA de la DS, SFC JP/VF, les sélections, adaptations et scripts. Aucun fichier ROM, SRAM ni état d'émulateur n'est publié. Le contrôle complet du 19 octobre 2026 a reconstruit exactement la ROM v0.19 : SHA256 0bc90d81f3d1d347212a9b7a5cf70f2a77659aa964aff86d0de37e0cb29976e2. Les BPS/IPS ont été réappliqués et 6960 entrées redécodées. Aucun nouvel essai en émulateur n'a été effectué lors de l'import.

Les ROM locales attendues sont dans upload/, au niveau racine du dépôt : `Dragon Quest VI - Maboroshi no Daichi (Japan).sfc` et `Dragon Quest VI - Realms of Reverie (E).nds`. Le restaurateur y place seulement Dq6f.ips. Les empreintes attendues des ROM sont dans init.py. Utiliser uniquement les pièces et espaces accessibles dans cette conversation ; ne pas chercher des ROM dans d'autres conversations. Si ces ROM manquent, continuer la relecture et préparer les nouveaux lots depuis les extractions JSON ; enregistrer PREPARE_NON_INSERE, sans augmenter la couverture intégrée ni prétendre avoir reconstruit ou testé le jeu.

Prendre un verrou local avant mutation. Identifier la dernière version réellement sauvegardée sur Git, préserver les modifications distantes et les anciennes sélections. Ne pas rejouer les générateurs pass*.py sur leurs propres sorties. Cloner la version actuelle vers une nouvelle version, actualiser ses références, relire japonais, français DS et contexte. Aucun score flou ne suffit pour valider une traduction. Conserver les commandes natives, les noms variables, Journal/Options, le retrait des crédits et le cadre élargi du nom du héros. Voir les rapports de commandes, notamment le blocage de rendu 1836, avant toute extension.

Avec les sources locales, utiliser init.py si nécessaire, prepare.py, build.py et verify.py ; comparer l'empreinte et les tokens précédents. Effectuer les essais ciblés de rendu si l'émulateur est disponible, en distinguant ces essais d'un parcours naturel complet. Ne pas faire fonctionner plusieurs émulateurs à la fois.

Après chaque lot, sauvegarder les sources/adaptations, patchs vérifiés et bilan réel, puis committer et pousser dans ce dépôt. Publier uniquement les patchs et sources, jamais les ROM, SRAM ni états. Les nouveaux lots de relecture peuvent être ajoutés comme petits fichiers distincts ; garder le paquet initial v0.19 comme point de reprise. GitHub est accessible via le connecteur si git push n'a pas d'identifiants. Ne pas pousser dans les dépôts tiers upstream.

La tâche horaire doit continuer jusqu'à finalisation réellement vérifiée du script ET des tables séparées, puis se désactiver. En cas de blocage ponctuel, sauvegarder la préparation possible et indiquer précisément ce qui manque, sans inventer d'avancement ni redemander à chaque heure les mêmes pièces.

## Lot v0.20 du 19 octobre 2026

18 nouveaux messages intégrés (Vallonclair), 5040 anciens tokens inchangés. ROM résultat SHA256 `2817bf421bc107ef9962075a697f97b83f4400e34a7f4a0c205eb1c712fd4cad`. Lire `etat-projet.json` et les rapports v0.20. `restore_sources.py` restaure désormais aussi les deltas lisibles sous `sources/lots/` via `restore_lots.py`, sans écraser les fichiers modifiés. Le paquet initial v0.19 est conservé. Les 18 nouvelles sélections sont en JSON lisible ; le restaurateur les fusionne avec les 5040 sélections v0.19 après vérification des empreintes. Les scripts et rapports v0.20 sont suivis directement. Le BPS est disponible sous patches/. L’IPS et les captures ont été vérifiés localement ; les ROM et états restent locaux.

Après restauration, les sélections de v0.20 sont présentes sans exécuter un générateur. `pass20.py` est le delta de revue, idempotent et limité aux données du lot ; ne pas rejouer les anciens pass non idempotents. Reconstruction : `python dq6-fr/v0.20/init.py`, puis `prepare.py`, `build.py`, `verify.py`. Les tests de rendu demandent un cœur local Snes9x et un état de camp compatible, non publiés. Le blocage 1836 reste différé. Pour les verrous, utiliser flock sur `.dq6-translation.lock` et libérer le verrou après sauvegarde/push ; un fichier de métadonnées restant seul ne prouve pas un passage actif.

## Lot v0.21 du 19 octobre 2026

20 messages intégrés : fin de la quête de l’insigne du courage et Calcado/Aridéa avant/après l’île des Sourires. Deux formulations de genre DS neutralisées et marqueurs de citation retirés autour de l’île pour éviter une double apostrophe. Aucun ancien token modifié. ROM résultat SHA256 `efb866259dd3190193217783df403beca15efb01559daa6036aab57cf5f083f4`.

`restore_sources.py` restaure dans l’ordre v0.19, v0.20 puis v0.21 : les deltas sont des JSON lisibles avec empreintes, sans archive opaque ajoutée. Le script idempotent `dq6-fr/pass21.py` reconstruit les entrées du lot. Les sélections intégrées sont reconstituées sans ROM en fusionnant les 20 nouvelles avec les 5058 précédentes. Reconstruction locale complète : `init.py`, `prepare.py`, `build.py`, `verify.py` sous `dq6-fr/v0.21/`. Le BPS est dans `patches/` ; l’IPS est régénéré par build.py.

Rapports : 6960 entrées redécodées, BPS/IPS réappliqués, 870 groupes et 417222 octets contrôlés sur le bus, 31 pages sur six répliques en banc de camp (220,246,248,251,255,282). Les captures et états restent locaux ; le protocole et leurs empreintes sont suivis. Aucun parcours complet ni scène naturelle complète déclaré. Conserver le blocage 1836 comme différé. Ne pas gonfler le compte principal avec les tables séparées.

## Lot v0.22 du 19 octobre 2026

20 ajouts relus à Aridéa/Sorcéria, 5098 messages intégrés, 1859 restants. Les 5078 anciennes sélections sont inchangées. Accueil DS neutralisé et Madame Soren identifiée comme dans la réplique 374 précédente. ROM résultat SHA256 `b37fb9066bd91c194ba903549d592c29977991abcb08376d7582bde96b471c06`. Reconstruction : `init.py`, `prepare.py`, `build.py`, `verify.py` sous `dq6-fr/v0.22/`. Ne pas réexécuter verify.py d’une ancienne version dans le checkout source : ses rapports historiques peuvent différer si l’ancienne ROM de comparaison manque ; utiliser un dossier de reproduction distinct pour ces anciens essais.

Le restaurateur applique les deltas lisibles jusqu’à v0.22 sans ROM. `pass22.py` est idempotent et limité aux entrées du lot. Il enregistre aussi un audit de la branche du tapis : FR DS 584–588 réordonne fabrication, vol et propriétaire par rapport au japonais. Le message 322 est différé ; la traduction ancienne de 323 doit être révisée avec cette branche. Ne pas compter ce constat comme un ajout et ne pas déclarer la validation sémantique complète des anciennes sélections. L’audit `audit-tapis-reordonne.json` garde les deux langues et l’ancien texte ; les anciens tokens restent conservés ici conformément à la consigne. Conserver aussi le blocage 1836.

Contrôles v0.22 : BPS/IPS réappliqués, 6960 entrées redécodées, 870 groupes et 418571 octets sur le bus ; 28 pages de rendu ciblé sur six messages (298,313,318,361,373,376). Aucun parcours naturel complet ni validation globale des tables séparées. Le BPS est publié directement ; l’IPS est régénéré par build.py. Les sources, adaptations et rapports sont publiés, les ROM et états restent locaux.

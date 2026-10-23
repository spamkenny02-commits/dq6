# v0.78 — 87 libellés et mise en page B5

80 noms d’objets et 7 commandes modifiés : 81 nouvelles traductions, 6 révisions de français existant. Les références japonaises SFC, les 174 champs japonais/français DS et l’IPS secondaire sont vérifiés par prepare.py. Les 87 positions/SIDs sont dans selection.json et revue-table-v078.json. 86 préparations antérieures résolues ; 405 restent PREPARE_NON_INSERE. Aucune nouvelle préparation ni nouveau lot de 400 revendiqué.

La table compte 367 positions françaises qualifiées sur 2048 déjà examinées (464 alias, 2512 SIDs). Ces nombres ne mesurent pas l’achèvement global. Script principal inchangé : 6948 textes + 9 entrées structurelles ; combat : 597 textes qualifiés, 2 préparés, 5 sources opaques et 4 structures. La relecture exhaustive principale reste à faire.

## Adaptations isolées

Noms d’objets : limites mesurées de 12 glyphes en première ligne et 11 en deuxième dans l’équipement. Aucun nombre de coupures modifié. Le menu principal utilise les libellés DS99–104, dont Divers distinct de Tactique en combat. Fenêtre8 : largeur16→20 à 0x57BCE et dans son miroir ; trois étiquettes de gauche alignées sur7 glyphes par espaces. Équiper reprend DS350. Moteur, dictionnaire et alphabet inchangés.

Audit B5 : dix messages70,71,72,73,331,366,367,433,434,435 reçoivent uniquement des sauts de ligne à la place d’espaces pour empêcher les noms longs de recouvrir la prose. Mots, variables et commandes hors AD préservés ; 598 autres messages identiques. Pool combat 0x7A5C00/23485 octets inchangé en taille. La liaison itemID→SID passe par la table0x41A3D, non par une soustraction : ID206→SID08BC. audit-item-bindings.json consigne les256 enregistrements.

## Tests exécutés et limites

prepare/build/verify, idempotence, redécodage, BPS et IPS réappliqués à la source intacte, mauvaises sources rejetées, protection des zones et anciens messages. Lecture CPU de2477 SIDs statiques ; contrôles négatifs pointeur et métadonnée de coupure ; 174 dialogues B2 avant/après ; 87 noms après relus. Inventaire/équipement :160 vues pour80 objets, avec liaison diagnostique à l’item courant. Menu principal testé par entrées ordinaires ; ancienne largeur négative détectée. Démarrage froid, bus8Mio, Journal et alphabet natif contrôlés. Prologue rejoué depuis l’état de camp privé :1285 actions/50674frames, sans injection WRAM/ROM/VRAM ; ce n’est pas une nouvelle partie depuis zéro.

Combat C02A29 :80 vrais itemIDs et les10 messages révisés avec le pendentif de Colombourg et noms variables/ordinal A/B ;32 captures de ces10 messages relues,80 noms comparés pixel à pixel à la police ROM. Redirection diagnostique depuis le camp, pas80 acquisitions ni combats naturels. L’état ancien nécessite le rafraîchissement de police décrit par le script ; le chargement naturel est contrôlé séparément à froid.

**Réserve ouverte : C02A4F**, l’API de petite fenêtre, rend du texte incomplet sur plusieurs des10 messages dans ce diagnostic. qa-native-B5-compact.json est un test non accepté ; déterminer les appels naturels et la pagination avant clôture. Le succès de la grande fenêtre ne valide pas cette API. Aucun audit hérité322/323,1836,4095,fragments/commandes rares ou contexte naturel n’est clôturé ici. Le premier candidat B5 rejeté est conservé dans diagnostics-rejetes avec son empreinte distincte.

## Reconstruction

Depuis la racine : python restore_sources.py, puis python dq6-fr/v0.78/prepare.py --jp SOURCE_SFC --ds SOURCE_DS --ips SOURCE_IPS ; python dq6-fr/v0.78/build.py --jp SOURCE_SFC --out SORTIE ; python dq6-fr/v0.78/verify.py --jp SOURCE_SFC --out SORTIE ; python dq6-fr/v0.78/inventory_names.py --rom SORTIE/result.sfc --jp SOURCE_SFC. Les trois SHA256 sources sont vérifiés, aucun fichier privé n’est publié.

Protéger le pool noms0x7AF000/14221octets jusqu’à0x7B8703, le moteur0x7A5800/1024 et le pool combat. Utiliser common.py::names/LogicalTable ; ne pas restaurer l’ancien lecteur contigu. Scripts emulator_*.py et rapports QA distinguent diagnostic, parcours ordinaire et réserves. Le projet reste partiel ; blocages-restants.json contient les405 propositions, sans les compter comme nouvelles revues.

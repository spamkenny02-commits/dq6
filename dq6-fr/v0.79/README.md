# v0.79 — cinq révisions principales intégrées

493 costaude,556 pourrai,1018 geôlier,1151 Dites-lui,1181 telle qu'elle. Ce sont cinq révisions de français déjà traduit,issues des préparations publiées ;ni nouvelles traductions ni nouvelles positions de relecture exhaustive.121 révisions principales restent préparées,distinctes des419 propositions noms/menus. Les6948 textes+9 structures/6957sélections,367libellés FR qualifiés/2048positions et le combat sont inchangés en couverture.

Les cinq substitutions touchent chacune une ligne existante qui reste au plus à24colonnes de caractères. Chaque commande,variable,retour ligne AD,pause AF et terminaison est conservé dans son ordre exact. Aucun nouveau glyphe :ô de geôlier existait déjà. Aucun changement de police,moteur,noms,combat,Journal/Options,crédits ou cadre du nom.8Mio.

Cinq groupes Huffman réencodés sur place avec l'arbre existant,un groupe raccourci d'un octet ;aucun groupe relocalisé. Les865autres groupes sont identiques octet par octet. Les6960slots sont redécodés,6955inchangés en tokens,les trois slots au-delà du visible restent distincts des6957sélections. La capacité des noms jusqu'à7B8703 et les allocations du moteur/combat restent protégées.

## Preuves et tests

prepare vérifie les SHA256 JP/DS/IPS et40champs JA/FR directement dans la ROM DS,puis compare les anciens tokens à la ROM v078 reconstruite. Les fautes de français DS gêolier et Dites lui sont corrigées explicitement,non maquillées en traduction nouvelle. selection.json conserve JP,références DS,motif et tokens avant/après ;delta-lisible.json montre chaque ligne modifiée.

build/verify,idempotence,redécodage complet,BPS et IPS réappliqués à la source intacte,mauvaises sources avec octet modifié ou en-tête rejetées,protection de tous les autres octets. Démarrage froid :4016plages/573868octets sur le mappage ROM,chargement naturel en VRAM des256glyphes de la police native,écran Journal. Le hook Snes9x de lecture ROM ne change ni mémoire ni cycles CPU ;ce n'est pas une trace d'exécution de toutes les adresses.

Rendu camp diagnostique des cinq dialogues en entier :25pages après et25avant. Toutes les25pages après ont été relues visuellement,ainsi que les cinq pages corrigées avant/après. Seules493p2,556p5,1018p1,1151p2,1181p10 diffèrent ;les20autres captures sont identiques octet par octet. Nom variable C9 de8lettres AAAAAAAA dans le dialogue1181 de13pages,glyphe ô visible dans geôlier,aucun débordement observé. Les planches jointes conservent ces vues ;les captures complètes privées sont indexées par empreinte dans les rapports.

Ces rendus redirigent le message100 depuis le camp privé créé par une nouvelle partie. Ils ne constituent pas les scènes naturelles des cinq PNJ ;le choix Oui/Non visible dans la scène hôte n'est pas une sélection de ces dialogues. Aucune injection WRAM/VRAM ;les fixtures ROM privées et états ne sont pas publiés. Aucun audit322/323,1836,4095,610/1135/2404/5341/5351 ou1179 clôturé. La relecture principale finale exhaustive reste0 ;les900positions400–1299 restent une passe préparatoire suivie,avec5corrections désormais rendues en diagnostic.

## Reproduction et reprise

Depuis la racine :python restore_sources.py ;python dq6-fr/v0.79/prepare.py --jp SOURCE_SFC --ds SOURCE_DS --ips SOURCE_IPS ;python dq6-fr/v0.79/build.py --jp SOURCE_SFC --out SORTIE_PRIVEE ;python dq6-fr/v0.79/verify.py --jp SOURCE_SFC --out SORTIE_PRIVEE. Conserver les sorties ROM/IPS hors du dépôt. Le BPS public complet est patches/DQVI-FR-DS-v0.79-BASE-JP-PARTIEL.bps.

La lecture actuelle des6957sélections se reconstruit par common.py::current_main_selection :base lisiblev056+les5remplacements selection.json. Ne pas relire le seul v056 comme s'il contenait déjà ces corrections. Préparations anciennes conservées historiquement ;preparations-resolues.json trace leur insertion sans les recompter.

emulator_boot.py --out SORTIE_PRIVEE --runner RUNNER_PRIVE ;emulator_render.py --out SORTIE_PRIVEE --runner RUNNER_PRIVE --camp CAMP_PRIVE. Pour comparaison --before ROM_V078_INTACTE reconstruite. Le cœur,runner et camp sont ceux documentés dans checks/source-return-v078 ;si perdus,reconstruire depuis le dépôt officiel et une nouvelle partie. Le nom AAAAAAAA appartient à la partie de test,non à la ROM livrée.

Verrou historique absent avec l'ancien espace :verrou exclusif de l'espace actuel tenu pour ce lot,publication main avec empreinte de départ et sans force. Sources(3) revérifiées avant le lot. Aucun fichier privé ROM,SRAM,état ou archive n'est publié. Reprendre les121révisions et419noms/menus,les glyphes manquants et les réserves,puis poursuivre la passe à1300 et0–399 non encore relus.

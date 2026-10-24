# Relecture préparatoire600–699 et audit textuel610

100 nouvelles positions examinées individuellement, après400–599. Le registre compare japonais SFC extrait, français courant, champs japonais/français DS disponibles, IPS secondaire renseigné et contexte des répliques.18 révisions restent PREPARE_NON_INSERE :16 sous réserve de glyphes,2 d'harmonisation ou de simplification. Les23 révisions principales antérieures ne sont pas recomptées ; cumul41 révisions principales, distinctes des419 propositions de noms/menus. Aucun nouveau texte intégré ou essai natif.

## Réserve610 : indices et choix doivent être relus ensemble

La sélection610 contient bien dix références DS explicites53–62. Leurs champs sont contrôlés exactement contre les extractions, après décodage des seuls échappements littéraux de lignes,tabulations et espaces japonais présents dans les références historiques ; aucun rapprochement flou. Les formes japonaises de la série DS et les dix propos SFC sont comparés dans le registre.

Le problème est l'adaptation des indices aux choix raccourcis de la SFC. Le premier indice dit « détenir la vérité » comme le texte DS, mais le premier choix visible1312 est « J'ai le coeur pur ». Le deuxième dit « lame et galets », jeu de mots rattaché au choix DS long, tandis que1317 affiche « Lame à force cachée ». Propositions : « Il y est question d'avoir le coeur pur, je crois... » et « Une lame qui cache sa force, peut-être ? Enfin, vous voyez. » Les hésitations du sage,Frizzam et toutes les autres parties restent conservés. Les deux indices proposés reprennent les libellés SFC existants sans imposer de nouveaux choix trop longs ou de glyphe œ non établi.

L'audit audit-610-indices-selections.json consigne les menus1312/1317/1322, leurs neuf échos, la question d'activation,Frizzam1308/1309 et les textes de succès/échec. Le mot Frizzam a la même graphie dans610/1308/1309. Les échos conservent leur D5. Le premier choix du deuxième groupe (« Beauté d'antan... ») et son écho (« Belle princesse d'antan ») sont de longueur différente ; cette différence est consignée sans la déclarer corruption ou la corriger aveuglément.

Le rapprochement sémantique suggère les positions affichées1,3,2 ; **ce n'est pas une séquence native validée**. Aucun code d'événement,ordre de branche,flag,passage de porte ou chemin naturel n'est inspecté sans ROM. Les23 IDs supplémentaires1307–1329 sont un corpus de comparaison de l'audit, pas23 nouvelles positions de la passe exhaustive. La réserve610 reste OUVERTE. Rejouer naturellement Frizzam,les dix propos,chaque mauvais choix,les reprises et la réussite effective avant de la clôturer. Un succès par redirection diagnostique ne suffira pas.

## Autres propositions et réserves

677 : le texte courant empile une phrase DS sur l'achat d'information avec une adaptation SFC disant encore que Friquet reçoit des renseignements pour s'enrichir. Proposer deux phrases claires : le pot-de-vin aux soldats de Noirgibet, puis l'échange de renseignements pour s'enrichir. Les personnages,lieu et modalité de rumeur sont conservés ; aucun dialogue natif ou paiement modifié.

Les16 autres propositions concernent Ça/À et œuvre/œil/cœur. Ce sont des réserves de fidélité graphique et de casse :le charset principal actuel ne contient pas Ç,À,œ. Aucun glyphage ou nouvel encodage n'est déclaré disponible. Pour694,la révision porte à la fois sur cœur et À moins. Les ça et à à l'intérieur des phrases restent inchangés. Les données JSON gardent l'intégralité des tokens de référence avec leurs empreintes ; aucun new_selection ni nouveau token n'est produit.

649 : l'accord de conduit dépend du référent de vous. Le contexte d'admission638 peut viser un client individuel masculin, mais cette portée n'est pas démontrée par le texte seul :pas de correction inconditionnelle en conduits/conduite. Le même contexte explique les adresses monsieur,étalon et tout cru, sans prétendre couvrir toutes les configurations de groupe.

Les lectures distinguent alcool SFC/thé DS600,changements de style D9/DA618/619,variables de conteneur C3 en663,Frizzam et règles des formules,lieux Montgivré/Colombourg/Kupidia/Noirgibet,Pascal et Mortamor. Les tarifs sont textuellement distincts :50 d'extorsion,200 d'admission,1000 de service et1200 total,80 par herbe,5000 pour l'information de Friquet. L'égalité200+1000=1200 n'est pas un test du débit réel ou du cumul des événements. Rien n'est écrit en SRAM.

## Reproduction et progression

Après `python restore_sources.py`, lancer `python preparations/relecture-principale-0600-0699/prepare.py`. La recette reproduit les100 notes de lecture,18 révisions,références exactes et audit610 ; elle ne remplace pas la lecture du sens et ne joue aucune scène. Les fichiers sont identiques après une deuxième exécution. La source textuelle principale reste la sélection v056 restaurée avec tous les lots ; le principal est déclaré inchangé par les versions suivantes publiées, sans nouvelle vérification native possible ici.

Cumul de cette passe préparatoire :300 positions400–699,en attente des réserves techniques. Relecture exhaustive finale validée0. Les plages0–399 et700–6956 restent à parcourir. Aucun message vide n'est compté comme nouvelle traduction et aucune réserve héritée n'est clôturée. Les419 propositions de noms/menus,la couverture intégrée,les autres audits et le patch v078 sont inchangés.

Les ROM privées et l'ancien workspace sont toujours absents. Aucun build,redécodage ROM,réapplication de patch,Snes9x ou scène naturelle n'est exécuté. Un flock exclusif est tenu dans le workspace courant pour les fichiers préparatoires ;le verrou historique disparu n'est pas prétendu acquis. Le projet reste partiel et ses sources privées ne sont pas demandées à nouveau par ce lot.

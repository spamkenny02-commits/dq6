# Relecture préparatoire des dialogues400–499

100 positions principales examinées individuellement, dont la composition de silence avec variable430 ; aucune nouvelle traduction ou insertion. Cette passe comparative est consignée par ID, avec japonais SFC extrait, français courant, référence DS japonaise/française et notes de contexte. Elle est distincte de la traduction initiale et du lot de43 menus. Ce n'est pas une relecture exhaustive du jeu ni une validation de100 scènes naturelles.

11 révisions restent PREPARE_NON_INSERE :

- Accord féminin493 : « elle est plutôt costaud » → « elle est plutôt costaude ». Le français DS contient lui aussi la forme non accordée ; 娘, Martel et elle établissent le sujet féminin, sans variable de genre.
- Capitales410,416,424,429,433,440,458,460,471,499 : reprendre Ça/À de la source française DS. Les autres ça et à à l'intérieur des phrases ne changent pas. L'ancien encodeur rabat explicitement Ç→ç et À→à ; ces dix cas sont donc une réserve d'alphabet héritée, pas onze fautes isolées à remplacer automatiquement dans les tokens. Le charset principal ne contient pas les deux capitales. Aucun glyphe de ROM n'a été inspecté ou ajouté ici.

Les préparations conservent séparément le texte proposé et l'intégralité des tokens d'origine avec empreinte. Elles ne produisent pas de new_selection ni de nouveau token. Commandes, variables, styles, terminaisonsAC/AE et pauses restent ceux du point publié jusqu'à une insertion testée. Le total de419 propositions de noms/menus est inchangé ; les11 révisions du script existant sont comptées à part et ne sont pas11 messages principaux manquants.

## Sens et variantes de plateforme

Les différences de contenu sont consignées :407 pièce du dessous SFC contre terrain derrière DS ;417 invitation SFC plus explicite que la danse DS ;452 linge SFC contre murs DS ;472/473 alcool SFC contre nourriture DS. Le français DS reste la référence principale, mais recopier la géographie ou la scène DS différente serait un contresens. Les variations de localisation (sourire/baiser420, casino souterrain467) sont explicites dans les notes, sans validation naturelle inventée.

Les branches425/426, la séance445 et le bisou498 conservent leurs commandes natives B0/D4/D9/DA. Les références DS658/659,733–736,970/971 sont ajoutées comme comparaisons ; la comptine DS736 ajoute une variable absente de la composition SFC, donc aucun collage automatique. La DS759 de452 ne prouve pas l'identité du texte SFC. Pour478, DS910 a été retrouvé comme début comparable ; les deux fragments911/912 n'étaient pas la totalité de la réplique SFC. Les répliques441 et473 restent sans référence DS exacte établie, avec traduction SFC directe documentée.

Noms et nombres contrôlés dans la scène : Lynx/ホック, Séductra/ラビアン, Martel/サリイ, Colombourg et Brigandia ;100 d'entrée,50 d'information,50000 puis2000 pour trois déguisements, gain de style5. Les états de présence/absence de Lynx sont des variantes de quête, pas des contradictions à supprimer. Le premier et le deuxième déguisement ne sont pas fusionnés. Le jeu de mots boutons/moutons489 et le dialecte quequ'chose402 sont intentionnels dans le français DS.

## Reproduction et limites

Après `python restore_sources.py`, lancer `python preparations/relecture-principale-0400-0499/prepare.py`. La recette contrôle la présence des100 notes individualisées, les champs DS exacts, les hashes d'extractions, les11 remplacements décidés et l'absence de nouvelle sélection encodée. Une deuxième exécution produit les mêmes fichiers. Le script reproduit la trace d'une lecture déjà effectuée ; il ne remplace pas la lecture du sens et ne déclare pas de scène validée.

La sélection principale lisible v0.56 restaurée avec tous ses lots sert de source textuelle ; les versions suivantes déclarent le principal inchangé dans leurs rapports publiés. L'identité de la ROM de distribution n'est pas revérifiée ici, faute de sources privées. Le principal reste6948 textes +9 entrées structurelles intégrées dans v078 ; aucun compteur intégré ou patch n'est modifié.

Les sources ROM et l'ancien workspace sont toujours absents. Aucun build ROM, redécodage natif, réapplication de patch ou émulateur n'a été lancé. Un flock exclusif est tenu dans le workspace courant pour ces fichiers préparatoires ; le verrou historique n'est pas prétendu acquis. Les100 positions sont enregistrées comme relecture sémantique préparatoire en attente des réserves techniques ; le compteur de relecture exhaustive finale validée reste0. Les autres positions0–399 et500–6956 restent à parcourir dans cette passe. Les audits hérités322/323,1836,4095 et les autres ressources ne sont pas clôturés.

# Relecture préparatoire700–799

100 nouvelles positions relues individuellement, dont le silence755, après400–699. Le registre compare japonais SFC extrait, français courant, champs DS japonais/français disponibles, IPS secondaire renseigné et contexte des séquences.12 propositions PREPARE_NON_INSERE :10 typographiques sous réserve de glyphes et2 de précision du sujet ou de composition variable. Aucune insertion, nouvelle sélection encodée ou émulation.

La passe préparatoire couvre désormais400 positions400–799. Ce total ne signifie pas400 nouveaux textes traduits,400 corrections intégrées ou400 scènes testées. Cumul53 révisions principales préparées, séparées des419 propositions de noms/menus. Le compteur de relecture exhaustive finale validée reste0 ;0–399 et800–6956 restent à parcourir.

## Deux propositions de contexte

701 : la première phrase dit que le père reprend un travail honnête. Le japonais SFC et DSJA précise ensuite que l'enfant n'a plus à gagner de l'argent. Le français DS et hérité généralise à « il n'y a pas que l'argent dans la vie ». Préparer « Il dit que je n'ai plus besoin de gagner de l'argent. » pour restituer ce sujet enfant. C'est une précision de sens adaptée contre la formulation française DS, isolée et non validée dans la scène.

784 : la description impose « un splendide [B2] » au nom variable de la récompense. Sans liste des valeurs réelles, l'accord ne peut pas être considéré correct pour tout objet. Proposition : « Près du lit repose le chef-d'oeuvre de Clume ([B2]). Son éclat éblouit le regard. » Le chef-d'oeuvre est le nom commun stable ;le libellé variable reste entre parenthèses. La comparaison DS0084/522 dit bien « le chef-d'œuvre de Clume » sans nom variable dans le corps français. La proposition conserve B2 et le reste de la composition SFC au lieu de supprimer une variable pour recopier la DS. La ligature est transcrite oe dans cette proposition compatible avec la réserve d'alphabet actuelle, sans déclarer son encodage testé.

La séquence visible de784 garde deux D3,un B2 et un B5,dans le même ordre. audit-composition-recompense-clume.json regroupe les demandes,confirmation,refus,fabrication,obtention et rappel de Clume. Les choix réels,leurs IDs,le couplage B2/B5,les accords de toute valeur,la pagination et la possession n'ont pas été testés. Aucune liste de récompenses ni correspondance d'ID n'est inventée à partir du contexte. Contrôler chaque choix et chaque chemin naturellement avant insertion. La présence d'une variable et sa bonne conservation ne prouvent pas un rendu correct.

## Comparaisons et réserves

Les dix autres propositions restaurent Ça ou cœur dans702,703,735,751,753,759,763,765,783,799. Ç et œ sont absents du charset principal actuel. Aucun glyphe nouveau n'est supposé disponible, aucun replacement global de tous les ça ou coeur n'est appliqué.

752 : les huit champs DS0082/49–56 sont retrouvés en comparaison,au-delà du seul fragment55 déjà enregistré. La première phrase SFC porte DF après Vous,alors que la DS dit explicitementあなたがた. Le DF est présent une seule fois dans les tokens et dans le texte de référence ;il n'est pas supprimé ou interprété comme une simple décoration. La portée réelle du nombre/genre,les voix et les huit propos restent à vérifier au rendu ;pas de correction inconditionnelle de venus.

Pour784,les champs japonais/français521 et522 sont comparés. Le champ japonais0084/523 est présent mais aucun enregistrement français pair n'est trouvé dans l'extraction publiée. Cela ne prouve pas que la ROM DS est dépourvue de traduction :un partage,alias ou autre chemin ne peut pas être résolu sans les sources. Le constat est limité à cette extraction et n'est pas compté comme un texte manquant du projet.

Autres points relus :coffre vide et passage de Pascal719/720,états Mélankolia/Espérance706/707/735/791,origine de Kupidia et séquences du manteau,Monde de Mortamor,famille à Morneville et chien Airain,pipe puis outils puis équipement de Clume. Le détail Monstria au nord-ouest ajouté par la DS est absent de l'indication SFC768/772 et n'est pas greffé automatiquement. DS741 remplace le monstre battu à mains nues par un arbre déraciné :variante de localisation conservée,aucune fausse correspondance de bestiaire. Recouvré700/725,le ne explétif704,les conditionnels et les accords des PNJ sont consignés sans correction automatique abusive.

Les reprises de dialogue sont des états de quête légitimes,non des doublons à supprimer. Les contreparties de quête et les variables D3/B2/B5,le D4 de narration769,le DF752 et les terminaisons natives restent dans les tokens d'origine avec empreintes. Les propositions sont du texte séparé ;aucun nouveau token n'est généré.

## Reproduction

Après `python restore_sources.py`,lancer `python preparations/relecture-principale-0700-0799/prepare.py`. La recette reproduit les décisions déjà relues,vérifie les100 IDs,références exactes et empreintes,12 remplacements limités,conservation des marqueurs visibles,DF et comptes de784. Les références historiques à échappements littéraux sont normalisées seulement pour les lignes,tabulations et espaces japonais avant comparaison exacte. Ce contrôle n'est pas un rapprochement flou ni une relecture automatique du sens. Une seconde exécution reproduit les mêmes fichiers.

Source textuelle principale :sélection v056 restaurée avec tous ses lots,principal déclaré inchangé par les versions suivantes publiées. L'identité native actuelle n'est pas vérifiée de nouveau faute de ROM. Les trois sources privées et l'ancien workspace sont toujours absents. Aucun build,redécodage ROM,réapplication de patch,Snes9x,parcours naturel,transaction d'or ou écriture SRAM n'est exécuté. Un flock exclusif est tenu dans le workspace courant ;le verrou historique disparu n'est pas prétendu acquis. Le patch v078,la couverture intégrée,les tables et tous les audits hérités restent inchangés ou ouverts. Réserve610 toujours ouverte ;ce lot n'en teste pas la porte.

Reprendre hors400–799 déjà consignés. Conserver les53 révisions principales et419 propositions de tables séparées comme noninsérées jusqu'aux contrôles nécessaires. Ne pas annoncer de finalisation générale.

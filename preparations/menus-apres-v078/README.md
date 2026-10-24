# Préparation après v0.78 — 43 positions de menus relues

14 nouvelles corrections préparées, aucune insérée : positions157,159,160,168,173,174,182,186,187,191,215,216,217,218. Les27 propositions existantes référencées ici ne sont pas de nouvelles traductions ni préparations. Les positions235 et249 restent sans référence DS exacte établie par ce contrôle. Le total des propositions de noms/menus préparées passe de405 à419 ; le nombre intégré/qualifié reste367. La relecture exhaustive du script principal n'a pas avancé par ce lot de menus.

Exemples de corrections de sens :160 Un→Changer tous (そうがえ),215 Pouvoir→Force (ちから),218 Agilite→Vitalité (みのまもり). Le couple216/217 est bien Agilité (すばやさ). Tactique352 correspond au sous-menu de stratégie, alors que Divers104 est le menu principal déjà corrigé dans v078. Transférer161 est l'action d'inventaire, DONNER861 la distribution de cartes. Les articles grammaticaux DS sont consignés mais pas recopiés dans les noms isolés des statistiques ; les deux-points SFC sont préservés.

Les choix ambigus restent ouverts :とくぎ a Magie DS5 dans un menu et Aptitudes665 dans un autre ;やめる a Quitter165 ou Rien604/621/684 selon le service. La proposition Sur Meurtor321 a une référence DS exacte mais le personnage réellement visé dans le chemin SFC reste à établir. Les noms de candidats sont des localisations officielles exactes, pas des rapprochements phonétiques. Aucun de ces exemples ne valide une fenêtre SFC.

## Ce qui a été vérifié

Lecture comparée du japonais SFC extrait, du français hérité de l'IPS et des champs japonais/français DS avec les deux voisins de chaque côté lorsqu'ils existent. Registre individuel dans registre-relecture.json ; décisions manuelles dans decisions.json ; champs exacts, empreintes des enregistrements et voisinages dans les préparations et références. prepare.py reproduit les43 positions, contrôle les41 correspondances japonaises (deux positions restent sans référence), les14 libellés français et leurs adaptations explicites de ponctuation. Il ne sélectionne aucune correspondance floue. Les extractions ont été restaurées par restore_sources.py et tous ses lots ; elles n'ont pas été réextraites depuis une ROM absente.

Relancer `python preparations/menus-apres-v078/prepare.py` depuis la racine reproduit les résultats. Les fichiers générés sont identiques après une deuxième exécution. Les contrôles portent sur les extractions et la recette, pas sur le rendu.

## Limites et reprise

Les trois sources privées, l'archive et l'ancien espace /workspace/scratch/fc8c8cdec832 sont absents de cet environnement. Aucun build, patch, redécodage ROM, test Snes9x, rendu ou parcours naturel n'est revendiqué. Le verrou historique ne peut pas être acquis sur un chemin disparu : un flock exclusif de même nom est tenu dans l'espace courant pour ce travail préparatoire. La publication utilise une mise à jour de main avec ancien SHA attendu et sans force. Aucune insertion n'est autorisée par cette préparation seule ; les compteurs intégrés et le patch v078 sont inchangés.

Avant insertion : sources privées intactes et hashes, encodage/glyphes, alias, blancs techniques, largeur de toutes les fenêtres, pagination, commandes et tests complets demandés. Ne pas supprimer le blanc initial de218 sans mesure. Confession (Sauveg.) est long et n'est pas abrégé automatiquement. Les réserves natives331/367 du complément v078 et tous les audits hérités restent ouverts. Ne pas refaire le lot43 comme de nouvelles traductions à la prochaine reprise ; reprendre ses blocages ou d'autres ressources non relues.

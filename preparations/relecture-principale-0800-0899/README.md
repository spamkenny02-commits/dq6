# Relecture préparatoire800–899 après v0.78

100 nouvelles positions comparées au japonais SFC,au français/japonais DS disponibles et à l'ancienne extraction IPS. Lecture manuelle par ID dans notes.json puis registre-relecture.json. Les références lexicales seules et les divergences officielles ne prouvent pas une équivalence intégrale de scène.

18 révisions PREPARE_NON_INSERE :14 de typographie sous réserve de glyphes,4 de sens/neutralité (852,875,876,888). Aucun texte nouvellement traduit ou inséré.

- 852 : «vous laisser capturer» → «faire semblant d'être en captivité», suivant とらえられたフリ et DS0088.p110. Trois DB anciens conservés ; aucune capture,clé ou infiltration exécutée.
- 875/876 : remplacer l'accord «prudents» par une formule de prudence sans genre/nombre imposé.
- 888 : «augmenter le rationnement» → «augmenter les rations» pour préciser une quantité de nourriture accrue.
- 828 : la référence DS héritée0082.p138 décrit recevoir la pipe ; le SFC décrit la présenter. Référence requalifiée lexique seulement dans le registre,texte principal «présente» conservé ; sélection héritée non modifiée.
- 814/825/826 : différences entre japonais et localisation officielle française consignées,ni faux alignement conclu ni réécriture forcée.
- 897 : silence sous D9,ne pas compter comme une traduction de mots.

Les glyphes À,Ç,Â,œ n'existent pas dans le charset principal v056 publié. Ils exigent un audit et des essais natifs avant encodage ; aucun nouvel octet ni nouvelle sélection généré. Les commandes/variables visibles et les tokens hérités sont conservés,mais la conservation textuelle ne valide pas leur fonctionnement en scène.

Cumul de cette passe :500 positions400–899 en relecture préparatoire,71 révisions de textes principaux déjà intégrés noninsérées,distinctes des419 propositions noms/menus. Relecture principale exhaustive finale acceptée0. Restent0–399 et900–6956. Couverture native inchangée :6948 textes+9 structures dans6957sélections ; table2048 positions déjà examinées,367FR qualifiés,2512SIDs/464alias. Combat et patch v0.78 inchangés.

## Reproduction et limites

Depuis la racine :`python restore_sources.py`,puis `python preparations/relecture-principale-0800-0899/prepare.py`. Le script contrôle les références exactes publiées,les anciens tokens et les substitutions,et reproduit le registre,les propositions,l'audit et la QA. Exécuter deux fois et comparer les empreintes.

Les sources privées et l'ancien espace fc8c8cdec832 sont absents. Le verrou historique est inaccessible ; verrou exclusif de remplacement dans l'espace courant utilisé pour ces seules préparations,avec publication main conditionnée à son empreinte de départ. Aucune ROM reconstruite,réapplication BPS/IPS,mauvaise source testée,zone ROM redécodée ni émulation exécutée dans ce lot. Aucun audit hérité clôturé ;v0.78,8Mio et patches inchangés. Les tests de restauration Git et de recette ne sont pas des tests de jeu.

# Version actuelle : v0.58

28 textes natifs de combat ajoutés ;36 intégrés,71 préparés encore non insérés. Script principal6957 sélections inchangé. Voir [la recette v0.58](dq6-fr/v0.58/README.md). Le BPS v0.58 s’applique à la JP intacte vérifiée. Projet non finalisé : autres tables, relecture exhaustive et audits naturels ouverts.

Les versions ci-dessous sont historiques.

# Mise à jour v0.57

Le patch courant est patches/DQVI-FR-DS-v0.57-BASE-JP-PARTIEL.bps, pour la JP intacte SHA25690ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e.8 textes statiques de combat sont intégrés et testés en diagnostic ;99 préparés restent en attente. Principal6957 sélections inchangé. Lire dq6-fr/v0.57/README.md pour les tests, limites et reconstruction. Le projet reste partiel. Les indications de versions antérieures ci-dessous sont historiques.

## Inventaire complémentaire après v0.56

Le pool séparé de combat compte608 entrées physiques, sans alias :107 affichent leur propre identifiant,497 contiennent du texte hérité non relu en contexte et4 sont vides ou composées de commandes seules. Aucune de ces608 entrées n’est comptée dans les6957 du script principal. Aucune nouvelle traduction de combat n’est validée par cet audit. Lire audits/ressources-v056.json ; la langue des497 héritées reste à qualifier.

# DQVI FR v0.56 — script principal traduit, projet partiel

Les16 derniers textes sont intégrés :6957/6957 sélections, dont6948 entrées linguistiques et9 structurelles sans texte à traduire. Zéro texte principal préparé non inséré ou différé. Trois corrections d’anciennes sélections sont isolées :5698/5699/5700. Ce jalon ne signifie pas que les tables, la relecture exhaustive ou les scènes naturelles sont finalisées. ROM8 Mio conservée.

5701–5703 : fragments d’équipement relus contre l’appel natif C3C5BE–C3C652, avec la distinction listes1–5 et6–8, conjonction après le cinquième nom et suffixes distincts. Le préfixe5698 devient Compatible avec, les suffixes gardent semble-t-il sans accord imposé aux noms.5699/5700 gardent C1/D5 et AE ; des AF/AD typographiques sont ajoutés entre les noms pour permettre des pauses et maîtriser les lignes. Le moteur peut conserver plusieurs noms courts sur une ligne dans certaines séquences ; les noms forcés à14 cellules ont été testés. Les changements des trois anciennes sélections sont consignés avec leur empreinte exacte, leur motif et leur nouvelle sélection.6938 autres anciens tokens inchangés.

6040–6042 : marche avec Annuler, bit0002 à7E3D00, lecture de l’entrée5840 masque0020 dans C5907D ; aucune touche physique ni traversée des murs inventée.6046–6048 : étage de départ truqué/standard, bit0004, branche de démarrage identifiée ; pas un nom de lieu DS.6184–6186 : poème à double lecture replacé dans ses branches oui/non ; drapeau et gouttes restent volontairement ambigus, sans objet de quête ajouté.6193–6195 : fusion, goutte, faire tourner ça ; appels, drapeaux et destinations techniques établis, sans remplacer les objets omis par des suppositions. Les équivalents DS absents ne sont pas inventés, l’IPS décalé ne sert pas de validation.

6956 : préfixe japonais utile jusqu’au premier AF (44 tokens), puis extraction erronée dans la table des noms au-delà de0x3B8703. Réparation explicite : C9 et AF valides conservés, ajout d’un AC sûr après le AF. Aucun AC original prétendu, aucun faux dialogue traduit depuis les octets de noms. Tulipe et la phrase DS0816:12 relus avec la différence C9/CC et obligation/souhait ; variable C9 SFC conservée. L’extracteur source historique n’est pas modifié silencieusement. La réparation est isolée dans bounded_source.py et ses rapports.

prepare.py/build.py/verify.py réussis :6960 entrées redécodées,16 nouvelles sélections et trois corrections contrôlées ; BPS/IPS réappliqués à la source intacte, mauvaises sources rejetées, zones protégées vérifiées. Noms, pointeurs de noms, handlers, arbre natif, fontes, cadre du nom, Journal/Options et crédits retirés inchangés.

Snes9x :14 pages des13 textes autonomes ;47 captures d’équipement avec le résolveur C1 réel et47 avec SID privé forcé à14 cellules, pour0/1/2/3/5/6/8 porteurs. Chaque série inclut quatre tests à trois fragments avec les vrais retours AE. Les listes longues sont des diagnostics aplatis suivant l’ordre de l’appel natif, pas une opération d’inventaire naturelle complète. Trois étapes6956 : C9 forcé à14 cellules, retour après AF/AC au choix du camp, continuation101. Ces111 captures de texte ont été relues, ainsi que le menu Nouveau jeu/Journal. Six tests unitaires privés exécutent C92E50/C92E93/C5907D : bits2/4 positionnés/effacés, autres bits conservés, indicateur6E51 conforme au drapeau et à l’entrée forcée. Bus922 plages/529887 octets. Aucun émulateur concurrent.

Limites : redirections au camp et hooks privés clairement distingués des parcours naturels. Aucun mouvement réel avec Annuler, changement naturel d’étage, fusion, scène de goutte/tour, opération d’équipement complète ni scène naturelle de Tulipe validé. Les audits322/323/1836/4095, routes1135/2404/5341/5351, énigme610, alphabet/fenêtres et commandes rares restent à achever. Une première tentative de nom14 via WRAM n’avait pas changé C1 (Olivier restait affiché) : rejetée et remplacée par le test SID14 explicite, sans faux compte.

Tables réinventoriées et inchangées :2512 SID,2048 entrées physiques,464 alias ;37 libellés FR confirmés et4 aides grammaticales,25 lieux préparés.1558 autres textes à revoir,346 identifiants,83 vides à qualifier,23 identités DS à vérifier,1 crédit retiré. Zéro japonais détecté ne prouve pas leur traduction. Recherche exhaustive des ressources/fin/épilogue et grosse relecture complète encore à faire. La tâche de finalisation reste ouverte.

SHA256 résultat :e14ebc5611642b229edd3e7becae27813c823ef8182e2d06058953d593f2375d. BPS pour JP sans en-tête SHA25690ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e. Recette et delta idempotents, restauration neuve vérifiée avant publication, contrôle depuis Git publié après récupération. Sources/revues/rapports/patch uniquement : aucune ROM, SRAM ou état d’émulation.

# DQVI FR v0.62 — attaques, états et techniques du combat

288 textes hérités relus et insérés :190 traductions de l'anglais,98 corrections du français hérité. Le pool natif compte désormais395 entrées françaises qualifiées,209 entrées héritées encore non qualifiées et4 structures. Les107 anciens identifiants manquants de v0.61 restent inchangés. Zéro nouvelle préparation non insérée. Les18 réserves examinées sont incluses dans les209, pas ajoutées à ce chiffre.

Le principal reste à6957 sélections, dont6948 linguistiques et9 structures. Les2512 SIDs de noms (2048 entrées physiques,464 alias),39 entrées françaises,4 aides grammaticales et16 noms composés restent inchangés.25 lieux demeurent en préparation. Aucune relecture exhaustive du principal enregistrée ; autres ressources et audits naturels ouverts.

## Revue

plans.py porte288 formulations explicites. insertion-combat.json garde pour chaque ID le plan français, l'ancien hash, les empreintes JP, les références DS avec empreintes et portée, le contexte voisin et les corrections de commandes.234 concordances utilisent la phrase japonaise complète normalisée : espaces, largeur Unicode et balises remplacées par leurs places variables, sans score flou ni sélection de sous-chaîne. Le français DS correspondant a été relu, puis adapté aux variables et détails SFC. Deux autres cas71/157 sont les compositions explicites de deux répliques DS.52 cas restent des adaptations directes SFC sans équivalence complète établie. Une concordance n'est pas une preuve de parcours naturel ou d'identité des macros DS.

Le lot corrige notamment les attaques rapides transformées en rayons oculaires, le corps d'acier devenu de pierre, les PM inversés avec leur cible, le personnage à terre traduit comme s'il se relevait, l'estocade devenue un coup de poing, la foudre devenue une tornade et des messages encore anglais. Les différences DS sont documentées : zéro de défense SFC conservé, pas de variable de cible ajoutée depuis le français DS, ni doublement d'attaque ajouté dans le message216.

Les variables natives restent explicites. Les accords de genre sont évités lorsque le nom peut désigner plusieurs personnages ou espèces. Le nom DS Mégabanga et la danse des soins ont des références précises. Les noms hérités anglais vus dans les tests sont des données de fixture ; ils ne sont pas comptés comme noms traduits.

## Corrections de commandes héritées isolées

21 IDs24/28/29/33/34/71/91/98/99/122/157/162/202/210/234/253/258/259/267/284/293 différaient de la séquence japonaise. Le delta décrit chaque ancienne et nouvelle séquence. Les B9/BA anglais ajoutés par la VF sont retirés pour ces seules formulations françaises, les noms perdus sont rétablis, les ordres B8 puis BB ou B8 puis B2 sont restaurés.157 retrouve ses deux B7,284 son BD,258 perd les noms absents du japonais. Les AD de disposition deviennent des espaces ; les autres commandes et pauses suivent le JP. Aucune réécriture silencieuse d'un ancien audit.

35/36 et leurs commandes C6, les fragments54/55,60–64,76/77, les B4 de4/5/69, les libellés techniques27/277,222 et265 restent réservés avec raisons concrètes dans blocages-restants.json. Ce sont18 entrées parmi209, aucune entrée vide présentée comme une traduction.

## Recette et zones

```
python restore_sources.py
python dq6-fr/v0.62/prepare.py --jp /chemin/source-intacte.sfc
python dq6-fr/v0.62/build.py --jp /chemin/source-intacte.sfc --out /chemin/prive
python dq6-fr/v0.62/verify.py --jp /chemin/source-intacte.sfc --out /chemin/prive
python dq6-fr/v0.62/inventory.py --rom /chemin/prive/result.sfc
```

Le BPS v0.61 contrôlé est appliqué à la JP intacte, puis seul le nouveau pool natif et ses76 pointeurs sont écrits. build-report.json donne la nouvelle allocation. La recherche de place exclut les870 groupes du principal ET l'allocation moteur v0.61, qui doit aussi être protégée par toutes les futures recettes. Le moteur, la police, les dictionnaires et tous les noms sont inchangés.8Mio conservés.

verify redécode les288 textes, compare les320 autres messages dont les107 traductions précédentes, réapplique BPS et IPS, rejette deux mauvaises sources, contrôle l'idempotence, la somme SNES et toutes les zones protégées. Le delta et les sources de ce lot sont lisibles et restaurables sans rejouer les générateurs antérieurs.

## Essais Snes9x

288 rendus au camp, noms homonymes A/B longs, B3=AM,B5=Cypress Stick,B2=Blaze et BB=999 lorsque présents ;34 autres rendus avec acteur/cible distincts, B3=Olivier,B5=Bamboo Spear et B2=Lightning.322 scénarios acceptés, retours API vérifiés et captures finales relues. Les trois textes71/260/297 à pauses internes montrent les deux phrases. Les21 corrections de commandes ont aussi un profil distinct. Pas de deuxième émulateur simultané.

Un premier second-profil utilisait le SID2309 à la place du sélecteur B3=2 et affichait un nom invalide. Ses34 scénarios sont exclus du compte accepté, consignés sous diagnostics-rejetes ; les34 ont été rejoués correctement. Aucun patch de moteur n'est introduit pour masquer un défaut de fixture.

608 pointeurs et premiers octets natifs, mutation attendue de l'ID8, bus des groupes vivants et du moteur, démarrage neuf jusqu'au menu Journal sont contrôlés. Les diagnostics de rendu utilisent une redirection privée et rafraîchissent sept tuiles que l'ancien état de camp conserve. Les noms de joueur et les fenêtres naturelles ne sont pas exhaustivement validés. La preuve de chargement neuf des accents de v0.61 reste applicable à des octets de police identiques ; elle ne remplace pas les tests naturels du combat.

Les captures, ROM et états restent privés. Les322 scénarios ne prouvent ni tous les appelants, ni tous les noms possibles, ni les scènes naturelles. Les réserves héritées322/323,1836,4095,610/1135/2404/5341/5351 et celles du moteur v0.61 restent ouvertes. Le projet n'est pas finalisé.

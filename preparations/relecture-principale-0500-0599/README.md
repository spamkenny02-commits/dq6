# Relecture préparatoire500–599

100 nouvelles positions relues après400–499, dont la composition de silence532. Le registre conserve pour chacune le japonais SFC extrait, le français courant, l'IPS secondaire lorsqu'il est renseigné, les champs japonais/français DS disponibles et une note individuelle de sens/contexte. Aucun nouveau texte inséré ou nouvel essai natif. Les200 positions400–599 sont maintenant consignées en relecture préparatoire ; elles ne sont pas200 scènes testées ni une passe exhaustive validée.

## Douze révisions non insérées

Quatre propositions de contexte, grammaire ou formulation :

- 546 : le patron « prend un poste à temps partiel » dans le français hérité et DS. Le japonais parle de compter sur un employé à temps partiel ;501 et530 montrent qu'il l'a embauché. Préparer « C'est la dernière fois que j'embauche quelqu'un à temps partiel. » Seconde phrase inchangée. Correction de rôle isolée, scène naturelle à confirmer.
- 547 : le japonais rapporte une paix déjà revenue (平和になった). Préparer « la paix est revenue » au lieu de « va revenir », en conservant les rumeurs et le doute du locuteur. Le français DS a lui aussi le futur ; cette correction temporelle n'est pas un copier-coller DS validé.
- 556 : projet situé dans dix ans après « Quand elle sera » ; proposer « je pourrai » au lieu de « je pourrais ». Révision de projection future, gardée sous réserve de contexte avant insertion.
- 574 : reprendre la formulation DS du tarif : « Le tarif est de [BB] pièces d'or la nuit, je crois. » La proposition garde exactement l'unique variable BB déjà présente. [BB] est ici une notation documentaire ; le JSON conserve le marqueur natif existant.

Huit propositions graphiques sous réserve de glyphes : Ça/À aux positions501,507,521,531,570 et œil aux positions560,561,565. Le charset principal v056 ne contient pas Ç,À,œ. L'ancien rabattement Ç→ç,À→à et œ→oe est explicite dans la recette de traduction ; aucun nouveau glyphe n'est déclaré disponible sur la seule base de ces propositions. Les autres prépositions à et les ça internes restent inchangés.

Le fichier revisions-preparees-non-inserees.json contient les12 textes proposés, les raisons, remplacements limités et tokens d'origine avec empreinte. Aucune nouvelle sélection ou nouveau token n'est généré. Les11 révisions du lot précédent ne sont pas recomptées :23 révisions principales préparées cumulées. Les419 propositions de noms/menus sont un ensemble distinct et restent inchangées. Ces23 corrections ne sont pas23 messages principaux manquants.

## Variantes et compositions préservées

Styles D4/DA de Lynx en danseuse500, D4/D9 de Martel, silence532, chants545/562, remise de l'épée541/564, réveil collectif576 et sauvegarde581/582 gardent leurs commandes. La SFC remet une épée légendaire en541 quand la DS parle d'épée rouillée : ne pas renommer l'objet à partir de cette différence de plateforme. En535, l'avertissement SFC inclut tuer des gens, absent de la version DS adoucie ; le texte propre à la SFC est conservé. La phrase519 passe d'un verre dans le japonais à dix dans le français DS : hyperbole de dialogue documentée, aucune quantité d'objet ou de transaction modifiée.

Le récit528 a été relu dans ses douze parties : Charles,Éthel,Martel,50 ans environ,10 ans de disparition, maison au nord du bar et sanctuaire nord. Ces directions sont distinctes du sanctuaire nord-est du village gelé586. Prix et conditions vérifiés textuellement :50000→2000 pour trois déguisements ; variable du prix de nuit574 ; nom du journal B2 et niveau BB séparés en581. Journal/Options et tous les tokens existants restent inchangés. Aucun débit d'or, sauvegarde SRAM ou résultat d'événement n'a été exécuté.

## Diagnostic de provenance séparé

diagnostic-provenance-selection.json recense315 enregistrements de la sélection v056 portant references_DS_explicites dans leur méthode, mais sans ds_file exploitable et sans ds_references renseigné. Dans ce lot,554,598,599 montrent ce décalage entre l'étiquette générique et les champs effectifs. Ce scan est mécanique :315 n'est ni un nombre de nouveaux textes relus, ni de traductions manquantes, ni une preuve que les autres registres historiques ne contiennent aucune référence. Rechercher ces liens et qualifier les adaptations SFC avant d'utiliser ce nom de méthode comme preuve autonome. Aucun texte ou compteur intégré n'est invalidé ou changé par ce diagnostic.

## Reproduction et limites

Après `python restore_sources.py`, lancer `python preparations/relecture-principale-0500-0599/prepare.py`. La recette reproduit les décisions déjà relues, vérifie les100 IDs, champs DS et empreintes, remplacements exacts et conservation des marqueurs visibles. Pour521, l'ancrage contient la phrase entière afin de ne pas capitaliser aussi le deuxième à boire. Le montant BB de574 apparaît une seule fois avant et après. Une deuxième exécution reproduit les mêmes fichiers. Ces contrôles ne remplacent pas une lecture du sens ni une validation de ROM.

Les sources ROM et l'ancien workspace sont toujours absents ; aucune reconstruction, réapplication de patch ou émulation n'est revendiquée. Les extractions publiées ont été restaurées avec tous les lots. La source textuelle principale est la sélection v056, le principal ayant été déclaré inchangé dans les versions ultérieures publiées ; cette identité native n'est pas revérifiée sans ROM. Un flock exclusif est tenu dans le workspace courant pour les préparations, sans prétendre avoir acquis le verrou historique disparu. Aucun fichier privé n'est publié et le patch v078 reste inchangé.

Reprise :0–399 et600–6956 restent à parcourir dans cette passe ; ne pas rejouer400–599 comme nouvelle revue. Les réserves techniques et contextuelles des23 propositions principales restent à lever avant insertion. Les tables,331/367 et audits hérités322/323,1836,4095,fragments,commandes rares et alphabet restent ouverts. Pas de finalisation du projet annoncée.

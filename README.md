# Dragon Quest VI Super Famicom — état actuel v0.76

[Patch BPS v0.76](patches/DQVI-FR-DS-v0.76-BASE-JP-PARTIEL.bps) · [Recette et limites](dq6-fr/v0.76/README.md) · [Reprise](REPRISE-AUTOMATIQUE.md)

14 libellés supplémentaires intégrés avec leur mise en page native ; les 110 propositions restantes du cycle ont été relues. La table compte **275 entrées françaises qualifiées sur 2048 positions examinées ; 496 propositions restent non insérées**. Le cycle des 510 relectures commencé en v075 est complet, pas leur insertion. Le script principal et les messages de combat sont inchangés. Les tests naturels, la recherche exhaustive d’oublis, la relecture principale et les audits restent ouverts.

Les sections suivantes sont historiques ; l’état courant figure dans les liens ci-dessus et etat-projet.json. Aucune ROM, SRAM, sauvegarde d’émulateur ou archive de ROM publiée.

---

# Dragon Quest VI Super Famicom — état actuel v0.75

[Patch BPS v0.75](patches/DQVI-FR-DS-v0.75-BASE-JP-PARTIEL.bps) · [Recette, tests et limites](dq6-fr/v0.75/README.md) · [Reprise](REPRISE-AUTOMATIQUE.md)

50 libellés préparés intégrés (49 traductions et une correction de casse), puis 400 autres propositions relues avec leurs blocages conservés. Table des noms : **261 entrées françaises qualifiées sur 2048 positions examinées ; 510 propositions encore non insérées**. Ces 400 relectures ne sont pas 400 nouvelles traductions. Le script principal compte 6957 sélections, dont 6948 linguistiques et neuf structures. La relecture exhaustive du script principal et les tests naturels restent à faire ; le projet n’est pas finalisé.

Les sources privées doivent avoir les empreintes vérifiées dans la recette. ROM conservée à 8 Mio ; aucune ROM, SRAM, sauvegarde d’émulateur ni archive de ROM publiée. Les sections suivantes sont des points de reprise historiques ; l’état courant est dans les liens ci-dessus et etat-projet.json.

---

# Reprise v0.60 — 64 messages natifs et sept accents

104 textes combat intégrés,3 préparés restants464/465/498 ;497 hérités non qualifiés et4 structures. Principal6957 sélections inchangé. Lire dq6-fr/v0.60/README.md, manifest.json etrapports. Extension isolée de sept slots inutilisés dans les consommateurs connus : police8x8 + correspondances principales, aucun moteur modifié.64 IDs testés,68 scénarios/236 captures ; autres544 messages natifs inchangés.397 : AD remplacé par espace, A/B et noms distincts passent en diagnostic, scène naturelle ouverte. Démarrage neuf recharge256 tuiles et menuJournal vérifié. Les états anciens conservent leur police.3 blocages dans blocages-restants.json ; noms, autres tables, relecture et audits restent ouverts. Pool natif réservé à8001024 sur16559 octets ;8Mio conservés. Ne pas recycler cette revue.

# Reprise v0.59 — quatre messages de combat intégrés

IDs337,428,454,455 intégrés :40 au total,67 préparés (dont2 réserves),497 hérités non qualifiés,4 structures. Principal6957 sélections et noms inchangés. Lire dq6-fr/v0.59/README.md et rapports ; restaurer toutes les versions puis exécuterprepare/build/verify etinventory. Ne pas recycler cette revue. B2/B4 testés en diagnostic,608 pointeurs contrôlés, neuf rendus acceptés et unB4 nul exclu ; menuJournal au démarrage vérifié. Aucun combat naturel, nom joueur ou fenêtre compacte validé.498 exclu : composition497+498 et16 noms DS toujours en préparation.64 accents,367,397, autres tables, relecture exhaustive et audits ouverts. Réserver le pool à8001024 sur12980 octets. Garder8Mio.

# Point de reprise combat-v066 — 16 noms DS préparés

Lire preparations/combat-v066/README.md et qa-preparation.json. Douze correspondances japonaises exactes, quatre réserves バキ/バギ. Aucune insertion : la composition native497+498 exige les deux choix, les noms DS ne sont pas factorisables par simple concaténation. Préserver061F partagé avec le vrai sort Flamme. Deux noms nécessitent é. Aucun nouveau test Snes9x. Version et patch restentv0.58 ;principal6957 sélections,combat36 intégrés/71 préparés inchangés. Les16 combinaisons sont un inventaire distinct et non additionnel. Relecture exhaustive et audits ouverts.

# Dragon Quest VI — traduction française Super Famicom

**v0.58 : 28 textes de combat à noms variables ajoutés, 36 intégrés au total.** Rendus diagnostiques Snes9x avec acteurs/cibles distincts et homonymes A/B.71 préparations restent en attente ;497 textes hérités restent à qualifier et relire,4 entrées sont structurelles. Aucun combat naturel complet déclaré.

Principal inchangé :6957 sélections, dont6948 linguistiques et9 structures. Autres tables, recherche des oublis, relecture exhaustive et audits restent ouverts.

[Patch BPS v0.58](patches/DQVI-FR-DS-v0.58-BASE-JP-PARTIEL.bps), pour la JP intacte vérifiée. [Recette, tests et limites](dq6-fr/v0.58/README.md). Lire REPRISE-AUTOMATIQUE.md et etat-projet.json ; restaurer par python restore_sources.py. Aucune ROM, SRAM ou sauvegarde d’émulateur publiée.

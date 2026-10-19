# Dragon Quest VI — traduction française Super Famicom

Projet partiel fondé sur le script français DS fourni par l'utilisateur, avec le patch VF IPS comme seconde source.

Base vérifiée : **v0.19 — 5 040 / 6 957 messages du script principal**, 1 917 restants. Les menus, noms, objets, sorts et combats restent des tables distinctes. ROM cible : ExHiROM 8 Mio. Aucun parcours complet du jeu déclaré.

Les scripts de la v0.19 sont disponibles dans `dq6-fr/`. Les données de traduction, patchs et archives de reprise ne sont pas encore publiés. Aucune ROM, SRAM ni sauvegarde d'état ne doit être publiée ici. Les trois sources utilisateur sont requises en local dans `upload/` ; voir le LISEZ-MOI et REPRISE-AUTOMATIQUE inclus dans l'archive.

## Reprise

Consulter `REPRISE-AUTOMATIQUE.md`. La reprise complète depuis Git attend la publication autorisée des données v0.19 ; le code seul ne suffit pas. Avec les sources et données en local, utiliser les scripts `init.py`, `prepare.py`, `build.py`, `verify.py` de la version. Les générateurs `pass*.py` ne sont pas idempotents : ne pas les rejouer sur leurs sorties finales.

Le statut PARTIEL est conservé jusqu'à vérification des comptes et essais de toutes les tables.

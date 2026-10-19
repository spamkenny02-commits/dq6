# Dragon Quest VI — traduction française Super Famicom

Base **v0.23 partielle : 5 128 / 6 957 messages intégrés** du script principal. Les menus, noms, objets, sorts et combats restent des tables distinctes. Le français DS est la source principale ; l'ancien IPS VF sert de seconde source. Version actuelle : 8 Mio.

Les scripts sont dans `dq6-fr/`, le patch BPS directement utilisable dans `patches/`. Appliquer ce BPS à la ROM japonaise intacte sans en-tête (CRC32 `33304519`), sans autre patch préalable.

Pour restaurer toutes les sources de traduction et le patch IPS depuis les fichiers compressés du dépôt :

```sh
python restore_sources.py
```

Consulter ensuite `REPRISE-AUTOMATIQUE.md`. Le restaurateur contrôle les empreintes et préserve les fichiers déjà modifiés. Les ROM doivent être fournies uniquement en local sous `upload/` ; aucune ROM, SRAM ou sauvegarde d'état n'est publiée.

La reconstruction et la réapplication des patchs ont été vérifiées le 19 octobre 2026 ; voir `verification-import-v019.json`. L’import v0.19 ne comprenait pas de nouvel essai en émulateur. Le lot v0.20 comprend 21 captures ciblées et un contrôle de 870 groupes sur le bus ; ces bancs ne valident pas un parcours naturel complet. La traduction reste partielle.

Dernier lot intégré : **v0.23**, 30 messages supplémentaires à Colombourg et autour du défi de Lynx ; état détaillé dans `etat-projet.json`. Patch BPS dans `patches/`. Les sources complètes sont restaurées par `python restore_sources.py` ; l’IPS v0.23 est régénéré localement par build.py. Il reste 1 829 messages du script principal, plus les tables séparées. BPS/IPS réappliqués, anciens tokens comparés, 870 groupes sur le bus et 27 pages de rendu ciblé sur sept messages. Aucun parcours naturel complet déclaré.

Audit ouvert : la DS française réordonne les renseignements sur le tapis volant entre plusieurs répliques. Le message 322 reste différé et le message déjà intégré 323 doit être revu dans ce contexte. Les anciens tokens sont conservés dans ce lot. Le nombre intégré ne garantit donc pas une relecture sémantique complète des anciennes sélections ; voir `dq6-fr/v0.23/audit-tapis-reordonne.json`.

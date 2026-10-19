# Dragon Quest VI — traduction française Super Famicom

Base **v0.20 partielle : 5 058 / 6 957 messages** du script principal. Les menus, noms, objets, sorts et combats restent des tables distinctes. Le français DS est la source principale ; l'ancien IPS VF sert de seconde source. Version actuelle : 8 Mio.

Les scripts sont dans `dq6-fr/`, le patch BPS directement utilisable dans `patches/`. Appliquer ce BPS à la ROM japonaise intacte sans en-tête (CRC32 `33304519`), sans autre patch préalable.

Pour restaurer toutes les sources de traduction et le patch IPS depuis les fichiers compressés du dépôt :

```sh
python restore_sources.py
```

Consulter ensuite `REPRISE-AUTOMATIQUE.md`. Le restaurateur contrôle les empreintes et préserve les fichiers déjà modifiés. Les ROM doivent être fournies uniquement en local sous `upload/` ; aucune ROM, SRAM ou sauvegarde d'état n'est publiée.

La reconstruction et la réapplication des patchs ont été vérifiées le 19 octobre 2026 ; voir `verification-import-v019.json`. L’import v0.19 ne comprenait pas de nouvel essai en émulateur. Le lot v0.20 comprend 21 captures ciblées et un contrôle de 870 groupes sur le bus ; ces bancs ne valident pas un parcours naturel complet. La traduction reste partielle.

Dernier lot intégré : **v0.20**, 18 messages supplémentaires ; état détaillé dans `etat-projet.json`. Patch BPS dans `patches/`. Les sources complètes sont restaurées par `python restore_sources.py` ; l’IPS v0.20 est régénéré localement par build.py.

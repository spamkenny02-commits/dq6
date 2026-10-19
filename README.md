# Dragon Quest VI — traduction française Super Famicom

Base **v0.19 partielle : 5 040 / 6 957 messages** du script principal. Les menus, noms, objets, sorts et combats restent des tables distinctes. Le français DS est la source principale ; l'ancien IPS VF sert de seconde source. Version actuelle : 8 Mio.

Les scripts sont dans `dq6-fr/`, le patch BPS directement utilisable dans `patches/`. Appliquer ce BPS à la ROM japonaise intacte sans en-tête (CRC32 `33304519`), sans autre patch préalable.

Pour restaurer toutes les sources de traduction et le patch IPS depuis les fichiers compressés du dépôt :

```sh
python restore_sources.py
```

Consulter ensuite `REPRISE-AUTOMATIQUE.md`. Le restaurateur contrôle les empreintes et préserve les fichiers déjà modifiés. Les ROM doivent être fournies uniquement en local sous `upload/` ; aucune ROM, SRAM ou sauvegarde d'état n'est publiée.

La reconstruction et la réapplication des patchs ont été vérifiées le 19 octobre 2026 ; voir `verification-import-v019.json`. Aucun nouvel essai en émulateur n'a été effectué lors de l'import. La traduction reste partielle.

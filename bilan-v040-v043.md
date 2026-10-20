# Bilan v0.40–v0.43

238 nouveaux textes relus, intégrés et poussés : 5927 → 6165/6957, 792 restants. Aucun préparé principal nouveau. Tables inchangées : 37 entrées françaises confirmées, 25 lieux préparés ; hors compte principal. Les sources locales ont été contrôlées contre les trois empreintes attendues avant les lots. Les ROM, états et captures restent privés.

| Version | Nouveaux | Pages cibles relues | Pages de stress supplémentaires |
|---|---:|---:|---:|
| v0.40 | 40 | 75 | 11 |
| v0.41 | 64 | 71 | 0 |
| v0.42 | 71 | 99 | 14 |
| v0.43 | 63 | 68 | 0 |

Chaque lot a une recette idempotente, une revue et un delta lisibles, les contrôles prepare/build/verify, réapplication BPS/IPS et rejet de mauvaises sources, redécodage des 6960 entrées, conservation des sélections et noms antérieurs, comparaison des zones protégées. Les quatre reconstructions dans un dossier neuf ont reproduit exactement les ROM testées. Les restaurations depuis chaque commit public ont reproduit les sources et sélections attendues. Les preuves précédentes sont conservées ; la dernière est verification-v043-depuis-git.json.

Snes9x : 313 pages cibles au total, plus 25 pages de stress avec un nom d’objet de 24 cellules. Bus des 870 groupes plus quatre zones de noms/pointeurs et démarrage Journal contrôlés à chaque lot. Valeurs C0/C1/D3 distinctes pour les transferts, B2 de vocation/sort, BB sur trois octets. Ce sont des diagnostics, pas les scènes naturelles, calculs d’effets ou transactions réelles. Les 21 captures initiales hors cible de v0.43 ont été remplacées par des captures avant confirmation du choix du camp ; elles ne gonflent ni les comptes de textes ni les 68 pages finales. Aucun changement machine dans ce passage.

Le registre reproductible v0.43/qa-reliquat.json sépare les 792 textes non validés des 38 simples propositions de mots. Aucun score ni égalité de mots seule ne vaut validation. Sur les 26 cas historiques v0.34, 2368 et 6265 sont résolus explicitement dans la revue v0.41 ; 24 restent différés. Scènes naturelles 322/323,1836,4095, indices, alphabet accentué et fenêtres natives des tables restent ouverts. Le projet n’est pas finalisé. Conserver 8 Mio et reprendre la dernière main publiée.

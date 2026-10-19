# Dragon Quest VI — VF DS — v0.21 PARTIELLE

5078 messages sur 6 957 du script principal validés sur les textes DS fournis, dont 20 nouveaux. Les sélections v0.20 sont conservées avec leurs tokens identiques. Il reste 1879 messages du script principal, plus les tables séparées de menus, noms, objets, sorts et combat. Ces comptes ne sont pas un pourcentage global du jeu.

20 dialogues supplémentaires relus : fin de la quête de l’insigne du courage et Calcado/Aridéa avant et après l’île des Sourires. 5078/6957 messages du script principal ; 1879 restants, plus les tables séparées. Les 5058 sélections précédentes restent identiques. Deux variantes de genre DS neutralisées et une double apostrophe corrigée. BPS/IPS relus, 6960 entrées redécodées, 870 groupes contrôlés sur le bus. 31 pages de rendu ciblé sur six messages, sans parcours naturel complet.

## Appliquer

Appliquer DQVI-FR-DS-v0.21-BASE-JP-PARTIEL.bps directement sur la ROM japonaise intacte sans en-tête de copieur :

- Dragon Quest VI - Maboroshi no Daichi (Japan).sfc
- Taille 4 194 304 octets ; CRC32 33304519
- SHA256 90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e

Ne pas préappliquer un ancien patch. Ne pas utiliser dquest6.smc. L'IPS alternatif attend la même source mais ne contrôle pas son empreinte. Le résultat reste à 8 388 608 octets (ExHiROM), en attendant l'étude des 4 Mo après les textes.

SHA256 du résultat : efb866259dd3190193217783df403beca15efb01559daa6036aab57cf5f083f4

## Vérifications et limites

Les 6 960 entrées techniques sont redécodées et comparées aux tokens attendus. Les patchs BPS/IPS sont relus indépendamment. Les anciennes sélections sont comparées au JSON de référence inclus ; la comparaison supplémentaire des octets hors script nécessite la ROM précédente locale. Les commandes natives protégées sont conservées. Les rapports qa-*.json et validation.json précisent les essais effectués.

Les captures d'émulation proviennent de l'ouverture ou de bancs temporaires qui redirigent un message vers un texte choisi. Elles contrôlent le rendu, pas la progression naturelle jusqu'à chaque scène. Le parcours complet, les achats, les combats et la sauvegarde en église ne sont pas déclarés validés.

## Reproduire

Placer les trois sources fournies dans upload/ à côté de dq6-fr/ (ROM japonaise intacte, ROM DS et Dq6f.ips), puis :

```bash
python dq6-fr/v0.21/init.py
python dq6-fr/v0.21/prepare.py
python dq6-fr/v0.21/build.py
python dq6-fr/v0.21/verify.py
```

Ces quatre étapes utilisent Python standard. Les essais d'émulation demandent numpy, Pillow et un cœur Snes9x libretro compilé. Les noms personnalisés de sauvegarde ne sont pas réécrits. Aucune ROM, SRAM ni sauvegarde d'état n'est incluse.

Sources techniques : https://github.com/ButThouMust/dq6-sfc et https://github.com/RadMageIRL/DQVI_SCRIPT_REFILL. Source française principale : ROM DS fournie ; source secondaire : IPS fourni. Les adaptations explicites conservent le corps DS d'origine ; les propositions de rapprochement ne sont pas automatiquement validées.

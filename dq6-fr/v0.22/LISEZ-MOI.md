# Dragon Quest VI — VF DS — v0.22 PARTIELLE

5098 messages sur 6 957 du script principal validés sur les textes DS fournis, dont 20 nouveaux. Les sélections v0.21 sont conservées avec leurs tokens identiques. Il reste 1859 messages du script principal, plus les tables séparées de menus, noms, objets, sorts et combat. Ces comptes ne sont pas un pourcentage global du jeu.

20 dialogues supplémentaires relus à Aridéa/Sorcéria, soit 5098/6957 messages intégrés du script principal ; 1859 restants, plus les tables séparées. Les 5078 anciennes sélections restent identiques. Accueil DS neutralisé et identité de Madame Soren alignée sur la réplique voisine 374. BPS/IPS relus, 6960 entrées redécodées, 870 groupes contrôlés sur le bus et 28 pages sur six messages relues. Audit ouvert : la localisation DS a réordonné les informations sur le tapis ; insertion 322 différée et ancien message 323 à revoir ensemble, sans modifier les anciens tokens ici. Le compte intégré ne vaut pas validation sémantique complète de toutes les anciennes sélections. Aucun parcours naturel complet déclaré.

## Appliquer

Appliquer DQVI-FR-DS-v0.22-BASE-JP-PARTIEL.bps directement sur la ROM japonaise intacte sans en-tête de copieur :

- Dragon Quest VI - Maboroshi no Daichi (Japan).sfc
- Taille 4 194 304 octets ; CRC32 33304519
- SHA256 90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e

Ne pas préappliquer un ancien patch. Ne pas utiliser dquest6.smc. L'IPS alternatif attend la même source mais ne contrôle pas son empreinte. Le résultat reste à 8 388 608 octets (ExHiROM), en attendant l'étude des 4 Mo après les textes.

SHA256 du résultat : b37fb9066bd91c194ba903549d592c29977991abcb08376d7582bde96b471c06

## Vérifications et limites

Les 6 960 entrées techniques sont redécodées et comparées aux tokens attendus. Les patchs BPS/IPS sont relus indépendamment. Les anciennes sélections sont comparées au JSON de référence inclus ; la comparaison supplémentaire des octets hors script nécessite la ROM précédente locale. Les commandes natives protégées sont conservées. Les rapports qa-*.json et validation.json précisent les essais effectués.

Les captures d'émulation proviennent de l'ouverture ou de bancs temporaires qui redirigent un message vers un texte choisi. Elles contrôlent le rendu, pas la progression naturelle jusqu'à chaque scène. Le parcours complet, les achats, les combats et la sauvegarde en église ne sont pas déclarés validés.

## Reproduire

Placer les trois sources fournies dans upload/ à côté de dq6-fr/ (ROM japonaise intacte, ROM DS et Dq6f.ips), puis :

```bash
python dq6-fr/v0.22/init.py
python dq6-fr/v0.22/prepare.py
python dq6-fr/v0.22/build.py
python dq6-fr/v0.22/verify.py
```

Ces quatre étapes utilisent Python standard. Les essais d'émulation demandent numpy, Pillow et un cœur Snes9x libretro compilé. Les noms personnalisés de sauvegarde ne sont pas réécrits. Aucune ROM, SRAM ni sauvegarde d'état n'est incluse.

Sources techniques : https://github.com/ButThouMust/dq6-sfc et https://github.com/RadMageIRL/DQVI_SCRIPT_REFILL. Source française principale : ROM DS fournie ; source secondaire : IPS fourni. Les adaptations explicites conservent le corps DS d'origine ; les propositions de rapprochement ne sont pas automatiquement validées.

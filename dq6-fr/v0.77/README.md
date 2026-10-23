# v0.77 — ô, ç, É et cinq libellés insérés

Le blocage de police est levé pour trois caractères natifs supplémentaires. Le codec utilise les slots3F/40/41 et les glyphes principaux existants025A/025F/0260. Seuls les plans0 de trois tuiles8x8 et trois mots de correspondance changent dans chaque copie. Aucun moteur ni glyphe de la police principale ne change. L’audit isolé rejette12collisions provoquées (combat,noms,dictionnaire,mapping), contrôle les pools connus et conserve les253autres tuiles/mappings. Les consommateurs hardcodés non inventoriés restent une réserve explicite.

Cinq anciennes propositions DS deviennent insérables sans allonger les libellés :fantôkane (625),geôlier (673),Érudit (1016),Évac’ (1242,SID1706,apostrophe ASCII dans la ROM),caleçon (1694,SID2158). Les champs JA/FR sont relus directement dans la ROM DS, le japonais SFC etl’ancienIPS contrôlés. Aucune nouvelle position ni préparation n’est comptée.280positions françaises qualifiées sur2048,491propositions noninsérées ;principal etcombat inchangés. La relecture principale exhaustive reste à0.

Les cinq grilles terrain512cases etbuffersB2 sont vérifiés avant/après.10dialogues diagnostiques,5rendus après lus visuellement ;2477SIDs statiques lus par le CPU etmutation pointeur détectée. Le démarrage àfroid charge les256glyphes natifs depuis la ROM enVRAM sans injection ;l’atlas des trois nouveaux dessins est relu. Le bus etle menu Journal sont contrôlés. Il ne s’agit pas d’une validation naturelle de toutes les fenêtres d’inventaire,de vocation ou de combat ;genres/pluriels etlargeurs restent ouverts.

## Recette

Depuis la racine,après `python restore_sources.py`,avec les sources privées vérifiéesJP/DS/IPS etune sortieOUT horsGit :

```sh
python dq6-fr/v0.77/prepare.py --jp "$JP" --ds "$DS" --ips "$IPS"
python dq6-fr/v0.77/build.py --jp "$JP" --out "$OUT"
python dq6-fr/v0.77/verify.py --jp "$JP" --out "$OUT"
python dq6-fr/v0.77/verify_font.py --jp "$JP" --out "$OUT"
python dq6-fr/v0.77/inventory_names.py --jp "$JP" --rom "$OUT/result.sfc"
```

`emulator_consumers.py` et`emulator_render_names.py` prennent `--jp --out --runner --camp` ;`emulator_names_probe.py` prend `--out --runner --camp`,àlancer aussi avec `--mutate-pointer`. `emulator_boot.py --out --runner` vérifie le bus etlechargement naturel dela police àfroid. Utiliser le protocole Snes9x local,séquentiellement ;aucune ROM,SRAM,image niétat d’émulation n’est publié.

ROM8Mio,table active7AF000 de14124octets,capacitéréservéejusqu’à7B8703 ;2050octets defin historique etdeuxcopies de l’ancienpool intacts. Les2507autres chaînes de noms,464alias,608slots de combat et6957sélections principales sont préservés. BPS/IPS réappliqués àJPintacte,mauvaises sourcesBPS rejetées. La restauration depuis Git est contrôlée séparément. Aucun audit hérité clôturé ;largeurs naturelles,œ,compositions,recherche d’oublis,relecture exhaustive ettests finaux restent àfaire.

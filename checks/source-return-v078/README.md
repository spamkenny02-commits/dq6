# Sources revenues et reconstruction v0.78

Les trois nouveaux fichiers(3) ont les SHA256 attendus. Les sources ont été restaurées depuis main7e4c0d2,tous lots pris en compte. prepare/build/verify v078 exécutés :ROM8Mio identique à l’empreinte publiée,BPS/IPS réappliqués,mauvaises sources rejetées,anciens messages et zones protégées inchangés. Les rapports historiques v078 ont été reproduits sans modification.

Cœur recompilé depuis le dépôt officiel snes9xgit/snes9x au commit de qa-recovery.json. core-rom-map-readonly.patch expose seulement une lecture de Memory.Map pour les blocs ROM,selon le lecteur natif ;aucun ajout de cycle CPU,aucune écriture ni redirection de scène. Ce contrôle du mappage ne constitue pas une trace d’exécution de toutes les adresses CPU.

Démarrage à froid :4016plages/573869octets concordants,256glyphes de police native chargés naturellement en VRAM,Journal relu. Une nouvelle partie a été créée par entrées ordinaires,nom observé AAAAAAAA,réglages confirmés,camp du prologue atteint et relu. new-game-inputs.json conserve les actions ;des snapshots privés assurent la continuation entre processus. Aucune injection WRAM/ROM/VRAM. Le camp est local et privé,son empreinte seule est conservée. Ce n’est pas un parcours de combat ou une relecture de toutes les scènes.

Les126 révisions principales et419 propositions noms/menus restent préparées,noninsérées. Aucun nouveau texte traduit ou relu dans ce contrôle. Reprendre les corrections sûres à glyphes existants puis les extensions de glyphes,audits et scènes ;ne pas compter ce redémarrage comme validation des propositions. L’audit1179 reste à redécoder sur la ROM et à rendre ;1135 et autres réserves restent ouverts.

## Reproduire

Depuis la racine du dépôt :python restore_sources.py,puis les commandes prepare.py/build.py/verify.py de dq6-fr/v0.78/README.md avec les trois sources(3) et un dossier de sortie PRIVÉ extérieur au dépôt. Pour le cœur :cloner le dépôt officiel,vérifier le commit enregistré,appliquer le patch de diagnostic,make -C libretro -j2. Le runner publié dq6-fr/emulator-tests/run_core.py doit être copié dans un dossier privé dont P.parents[1] contient emulator-snes9x ;lancer emulator_boot.py avec le dossier ROM privé et ce runner. Rediriger sa sortie qa-bus-boot.json vers le dossier privé pour ne pas écraser une preuve historique. Les rapports de ce contrôle sont conservés ici,mais aucune ROM,SRAM,archive ou état d’émulateur n’est publié.

Sources et camp disponibles au contrôle uniquement :leur survie à une réinitialisation de l’espace n’est pas garantie. L’ancien espace et son verrou sont absents ;verrou exclusif de l’espace actuel utilisé pour chaque mutation et chaque émulation. main publié sans force avec contrôle de son empreinte initiale.

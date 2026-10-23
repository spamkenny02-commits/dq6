# DQVI FR v0.64 — compositions natives et contrôles différés

11 entrées de combat qualifiées et intégrées :5 traductions de l'anglais et6 corrections du français hérité. Neuf de ces entrées sont des fragments, pas neuf nouvelles phrases autonomes. Le registre atteint597 entrées françaises qualifiées en diagnostic. Deux libellés techniques27/277 sont préparés sans insertion et restent inclus dans les2textes JP différés ; cinq emplacements VF603–607 hors frontière JP et4structures sont séparés.

Le principal reste6957 sélections (6948 linguistiques,9structures),sans nouvelle relecture exhaustive. Noms et alias sont inchangés ; inventaire-noms-v064.json recompte2512SIDs,2048entrées physiques,464alias :39 françaises confirmées par le projet,25 correspondances françaises DS à revoir en contexte,344 identifiants non traduits,1556 autres textes à revoir,83 vides à qualifier,1crédit retiré,0caractère japonais détecté. L'absence de japonais ne prouve pas du français. Les vides ne sont pas automatiquement des manquants. Les candidats exacts ne sont pas validés automatiquement.25lieux préparés,4aides grammaticales et16noms composés restent inchangés. Autres ressources et chemins toujours à inventorier exhaustivement.

## Sens et composition

35/36 conservent B8 puis BB et C6. Le français nominal « Dégâts subis par … ! … ! » évite un pluriel incorrect avec1 et garde la quantité. DS0801:144/152 est la source française relue ; les rôles SFC restent prioritaires. C6 pointe vers C691DC et exécute STA5A1C,1 puis RTL : il n'imprime pas un caractère et n'inflige pas les dégâts lui-même. Ce code de production est inchangé.

54/55 : le code02AF21 compare le nombre de bénéficiaires à2 et saute54 en dessous ;55 doit aussi fonctionner seul. « Par membre de l'équipe » est l'en-tête facultatif, « Gain de … EXP ! » le message autonome. EXP est une abréviation invariable, évitant point/points pour0/1/pluriel. Le sens est relu avec DS0801:83 et le japonais SFC. Le cas0 est forcé en diagnostic après la garde naturelle : le code original retourne sans message si le gain est nul.

60–64 : Force/Agilité puis Sagesse/Vitalité puis Style, dans l'ordre SFC, selon le lexique DS0801:94. Le signe+ existant est la tuile0C, glyphe0208 ; son dessin et son rendu sont contrôlés sans modification graphique. Les AE de60/62 sont conservés ; les AC source de61/63/64 sont rétablis à la place des AE de la vieille VF, avec delta et tests distincts. Une espace sépare les deux colonnes françaises. Aucun ajout de commande de saut.

76/77 : « B3, de la vocation B2, » suivi de « atteint le rang B2 ! ». Le premier B2 est la vocation, le second le rang écrit dans4877. Les deux appelants02B2DC/02FA56 sont identifiés et leurs deux appels natifs sont gardés. DS0801:103 confirme la distinction vocation/rang. Les noms hérités de vocations et de rangs ne sont pas traduits ou validés par ce lot.

27/277 : traductions littérales avec leur numéro technique, dans prepares-non-inseres.json. Aucun appelant établi. Le hiding anglais de277 ne correspond pas au japonais aucune-action6. Les deux ne sont ni insérés ni comptés comme qualifiés en ROM. La recherche statique limitée en banqueC2 ne prouve pas leur inaccessibilité et ne résout pas les cinq emplacements opaques.

## Nouvelle réserve bloquante héritée

**audit-tail-noms-herite.json :** la v0.61 a allongé de7octets la partie des noms atteinte par les2512SIDs. La limite passe de0x3BBF10 à0x3BBF17. Ces7octets appartenaient à la fin de table que l'inventaire précédent demandait de conserver et d'auditer ; ils n'étaient pas tousFF,et4octets diffèrent. Le reste jusqu'à0x3BC712 est inchangé. Les anciennes données sont reproductibles depuis le BPSv0.60.

Cette réserve était déjà présente avant ce lot. La v0.64 ne modifie aucun nom ni cet intervalle. Aucun correctif n'est prétendu : il faut identifier les consommateurs de cette fin de table,puis prouver ces octets inutilisés ou déplacer/recompacter les noms en préservant les données et tester les lecteurs. Restaurer les7octets en place corromprait la fin des noms actifs. Une restauration identique depuis Git reproduit le risque ; elle ne le résout pas. Ne pas annoncer de finalisation tant que cette réserve et les audits ouverts subsistent.

## Recette

```
python restore_sources.py
python dq6-fr/v0.64/prepare.py --jp /chemin/source-intacte.sfc
python dq6-fr/v0.64/build.py --jp /chemin/source-intacte.sfc --out /chemin/prive
python dq6-fr/v0.64/verify.py --jp /chemin/source-intacte.sfc --out /chemin/prive
python dq6-fr/v0.64/audit_bindings.py --jp /chemin/source-intacte.sfc
python dq6-fr/v0.64/audit_name_tail.py --jp /chemin/source-intacte.sfc --rom /chemin/prive/result.sfc
python dq6-fr/v0.64/inventory_names.py --jp /chemin/source-intacte.sfc --rom /chemin/prive/result.sfc
python dq6-fr/v0.64/inventory.py --rom /chemin/prive/result.sfc
```

La recette applique le BPSv0.63 contrôlé à la JP intacte,puis reconstruit le pool VF608 en ne changeant que les11IDs. Les597autres emplacements,dont586qualifiés et cinq opaques,sont identiques. Les870groupes du principal,tous les noms/alias,moteur v0.61,police,dictionnaires,cadres et autres octets protégés restent identiques. Seul le nouveau pool,ses76pointeurs en deux copies et les sommes SNES changent.8Mio conservés. L'encodage strict autorise désormais le+ existant0C ; aucune nouvelle tuile n'est créée.

## Essais réellement effectués

36scénarios positifs sous Snes9x :12rendus de dégâts (0/1/999,noms longs homonymes et distincts),12compositions EXP (0/1/2/999/65536/16777215,seul ou par membre),8affichages des cinq statistiques (1..5,9..13,95..99,251..255,AM/Olivier),4paires vocation/rang avec libellés courts et longs.124captures stables ; finales relues. Les paires utilisent les instructions originales de l'appelant,avec une terminaison RTL privée pour revenir au harnais. Ce sont des redirections du camp, pas des niveaux gagnés ou combats naturels.

C6 vaut1 dans les12cas positifs. Un contrôle négatif distinct désactive seulement C6 dans la fixture privée et observe0 ; il est exclu des36scénarios acceptés. Lecteur608pointeurs et premiers octets,mutation volontaireID8,bus1485plages,démarrage neuf menuJournal,BPS/IPS réappliqués,rejet de deux mauvaises sources,redécodage des11,idempotence et zones protégées contrôlés. Un seul émulateur à la fois. L'ancien état de camp reçoit un rafraîchissement privé des sept tuiles d'accents ; la police de production est inchangée.

Les tests ne prouvent pas tous les nombres et appelants,les fenêtres compactes,les noms joueur ou les parcours naturels. Les audits322/323,1836,4095,610/1135/2404/5341/5351,le RNG naturel des16compositions,les autres tables,la recherche d'oublis et la relecture exhaustive restent ouverts. Aucune ROM,SRAM,état,capture ou archive de ROM sur Git.

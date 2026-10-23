# Complément après publication de v0.78

Le commit36b98e3681aedfe3b8f231900743e57f40d5d749 a été cloné puis restauré avec tous les lots. build.py et verify.py reconstruisent la ROM0a69826c5139f75e8f78db7bdfa6ab5867180c866d09f26a548fdd2050c71a97 ; les54 fichiers du manifeste sont identiques. Les tests d’émulateur antérieurs portent sur ce même SHA ; ils n’ont pas été rejoués après cette restauration.

## Précision sur la réserve C02A4F

Le test forcé de petite fenêtre reste non accepté et ses captures restent négatives. L’audit complémentaire établit cependant des appels natifs de grande fenêtre pour huit IDs :70,71,72,73,366,433,434,435. Les formes inlineC02A16 et accumulateurC02A29 convergent vers2A62 ; les formes compactes3C/4F vers2A92. Le chemin de trésor sélectionne73 ou72 dans2593 puis appelle2A29. Les adresses et octets sont vérifiés dans la JP et les deux copies ROM par audit_native_callers.py.

Cela prouve ces sites d’appel précis, pas l’absence de tout autre appel. Les liaisons de331 et367 restent à établir ; leur présence possible dans une table d’actions ne valide aucun message. Ne pas modifier le moteur pour faire réussir artificiellement un mode compact qui ne serait pas utilisé par ces scènes. Reprendre ces deux liaisons et les chemins dynamiques, puis les405 propositions restantes. Aucun nouveau texte intégré ni relecture exhaustive ajouté par cet audit.

Les87 libellés,10 modifications de mise en page,comptes et autres limites de README.md restent applicables. La recherche globale des oublis,relecture exhaustive,audits hérités et scènes naturelles ne sont pas terminés. Aucune finalisation générale annoncée.

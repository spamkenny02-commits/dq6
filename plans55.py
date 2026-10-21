"""Reviewed riddle and composed travel fragments. Debug ambiguities stay deferred."""
PLANS={
610:"{D4}Kad Abra. La formule qui brise le sceau comprend un mot de passe et trois phrases.{AF}{D4}Kad Abra. Le mot de passe est Frizzam ! Cela devrait réveiller la porte scellée.{AF}{D4}Kad Abra. Et maintenant, le plus important. Retenez bien ce qui suit.{AF}{D4}Kad Abra. La première phrase... Hmm... Il y est question de détenir la vérité, je crois...{AF}{D4}Kad Abra. La deuxième... Euh... Ça parle de lame et de galets, je crois ? Enfin, vous voyez.{AF}{D4}Kad Abra. Et la troisième... Un type qui sort de la glace... Oui, c'est ça ! Ou pas...{AF}{D4}Kad Abra. Bon ! Avec tout cela, le sceau est pour ainsi dire brisé !{AF}{D4}Kad Abra. L'épée dort dans une grotte couverte de glace, au nord de ce village. Soyez prudents !{AF}{D4}Kad Abra. Ah, j'oubliais... si vous obtenez l'épée, revenez me le dire.{AF}{D4}Kad Abra. C'est la moindre des politesses. Hmm.",
1312:"1 J'ai le coeur pur{AD}2 L'heure est venue !{AD}3 Tout selon la légende",
1313:"J'ai le coeur pur{D5}{AD}",1314:"L'heure est venue !{D5}{AD}",1315:"Tout selon la légende{D5}{AD}",
1317:"1 Beauté d'antan...{AD}2 Combattons ensemble{AD}3 Lame à force cachée",
1318:"Belle princesse d'antan{D5}{AD}",1319:"Combattons ensemble{D5}{AD}",1320:"Lame à force cachée{D5}{AD}",
1322:"1 Révèle-toi ici !{AD}2 Sors de la glace !{AD}3 Éclaire nos vies.",
1323:"Révèle-toi ici !{D5}",1324:"Sors de la glace !{D5}",1325:"Éclaire nos vies.{D5}",
4952:"{D4}Roi Louis. (Paroles indéchiffrables...)",
5351:"Sur l'ordre du roi, j'étudie la légende du bouclier légendaire.{AF}Allez tout droit vers le sud depuis la statue Goyle. Au bout du chemin, posez la main gauche sur le mur et longez-le...{AF}Examinez le premier buisson ! ...Mais de quel endroit s'agit-il ? Hmm...",
5820:"Est - {BB} pas{D5}",5821:"Ouest - {BB} pas{D5}",
5822:"{AD}Nord - {BB} pas.{AD}Quelque chose en vue.",5823:"{AD}Sud - {BB} pas.{AD}Quelque chose en vue.",
5832:"Surprise !{D5}",
5833:"{AD}Une auberge ambulante{AD}apparaît.",5834:"{AD}Un prêtre ambulant{AD}apparaît.",
5835:"{AD}Un vendeur d'armes{AD}ambulant apparaît.",5836:"{AD}Un vendeur d'armures{AD}ambulant apparaît.",
5837:"{AD}Un bazar ambulant{AD}apparaît.",5838:"{AD}Un vendeur d'objets{AD}ambulant apparaît.",5839:"{AD}Un monstre errant{AD}apparaît !",
6019:"{DE}C'est bien cela !",6157:"Château de Mortamor après la chute",
}
FIXED=set(range(1312,1316))|set(range(1317,1321))|set(range(1322,1326))|{5820,5821,5822,5823,5832,5833,5834,5835,5836,5837,5838,5839}
STRUCTURAL=[1,2,3,2358,5699,5700,5775,6213,6214]

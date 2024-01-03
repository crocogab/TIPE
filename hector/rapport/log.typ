#import "template.typ": *

// Take a look at the file `template.typ` in the file panel
// to customize this template and discover how it works.
#show: project.with(
  title: "Tipe",
  authors: (
    "Hector Nussbaumer",
  ),
  date: "November 14, 2023",
)

#import "@preview/cetz:0.1.2": canvas, draw, tree

= Règles
On fait un choix arbitraire parmis les nombreuses variantes des règles du blackjack. Ces règles seront choisies pour leur simplicité et leur clarté.

== But du jeu
Le but du jeu est d'obtenir un score supérieur à celui du croupier sans dépasser 21. Si le score du joueur dépasse 21, il perd la partie.

== Déroulement d'une partie
Le croupier distribue 2 cartes au joueur et a lui même. Le joueur a ensuite le choix entre tirer une carte ou rester. Si le joueur tire une carte et que son score dépasse 21, il perd la partie. Si le joueur reste, le croupier tire des cartes jusqu'à ce que son score soit supérieur à 17. Si le score du croupier dépasse 21, le joueur gagne la partie. Sinon, le joueur gagne si son score est supérieur à celui du croupier.
 
== Valeur des cartes
Les cartes numérotées valent leur valeur numérique. Les figures valent 10. L'as vaut 1 ou 11 selon ce qui est le plus avantageux pour le joueur. (En réalité dans notre implémentation, on choisira toujours 1, sauf en cas de victoire).

== Cas d'égalité
En cas d'égalité, le joueur ne gagne ni ne perd rien. (Dans l'implémentation, pour le calcul du taux de victoire, on relancera la partie).

== Variante 
On n'implémentera pas la variante où le joueur peut doubler sa mise après avoir vu ses deux premières cartes ou encore la variante où le joueur peut séparer ses deux premières cartes si elles ont la même valeur. Enfin, l'assurance ne sera pas implémentée non plus. On utilisera de même un jeu de carte

=== Mélange de cartes parfait
“On dira alors qu'un paquet de cartes est "parfaitement mélangé" si tous les ordres possibles ont la même probabilité.”
On va alors aléatoirement choisir une carte pour chaque postion (indéxée par $n in [|1,52|]$)



= Résumé du progres

== Première implémentation
Nous avions besoin de pouvoir rapidement simuler des parties, de sorte a pouvoir se concentrer sur l'implémentation et l'étude des systèmes décisionels. L'implémentation devra être facilement adaptables aux besoins futurs du projets inconnus a ce point. Nous devons également pouvoir automatiser la simulation de partie en fournissant un choix à cahque étape de la partie. Nous avons donc opté pour la programation orientée objet, qui, selon nous répondait a tous nos besoins.

== Arbre de jeu


== Problèmes recontrés
=== Problème de performance
La taille de l'arbre dépend de la profondeur de la partie (ie. le nombre de la carte dans la main d'un joueur avant la fin de la partie). Pour determiner une profondeur maximale, j'ai généré un grand nombre de partie, en adoptant une stratégie naïve (tirer des cartes jusqu'a perdre). J'ai simulé 200 000 000 de parties et obtenu les résultats suivants :
#figure(
  image("depth.png", width: 70%),
  caption: [
    Distribution du nombre de cartes nécéssaires à la fin d'une partie
  ],
)
J'ai donc choisi une profondeur maximale de 8. Il reste tout de même $52^8  = $ #calc.pow(52, 8) nœuds dans l'arbre. On regrouppe donc les cartes par valeur et on donne un poids a l'arrête qui sera décrémenté a chaque fois qu'on tire une carte de cette valeur. On obtient alors un arbre de taille #calc.pow(10,8), ce qui est beaucoup plus raisonnable. On a réduit la taille de l'arbre de 5 ordres de grandeur. On peut alors générer l'arbre en quelques secondes.
=== Problème de conception
La première version ne prenait pas en compte la première carte du croupier. On génère donc 10 arbres différents, un pour chaque valeur de la première carte du croupier. Cependant, avec l'implémentation actuelle, la première carte n'a pas d'influence sur le comportement idéal déterminé par le programme car la première carte du croupier n'agit pas sur la valeur seuil de la probabilité de dépasser 21 à la prochaine carte tirée. Il faut donc que je trouve un moyen de faire influer la première carte du croupier sur la valeur seuil. On m'a suggérer de faire une exploration exhaustive du graphe de jeu. Je pense qu'il est possible de trouver une fonction mathématique prenant en compte la première carte du croupier pour la valeur seuil. Je vais donc essayer de trouver cette fonction.
Ou alors la probabilité de perdre du croupier doit etre calculée en fonction de la première carte du croupier. (pour la prendre en compte pour le choix du joueur)
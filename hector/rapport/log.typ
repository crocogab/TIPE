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

#bibliography("biblio.bib")
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

#let data = (
  [A], ([B], [C], [D]), ([E], [F])
)

#canvas(length: 1cm, {
  import draw: *

  set-style(content: (padding: .2),
    fill: gray.lighten(70%),
    stroke: blue.lighten(70%))

  tree.tree(data, spread: 2.5, grow: 1.5, draw-node: (node, _) => {
    circle((), radius: .45, stroke: none)
    content((), node.content)
  }, draw-edge: (from, to, _) => {
    line((a: from, number: .6, abs: true, b: to),
         (a: to, number: .6, abs: true, b: from), mark: (end: ">"))
  }, name: "tree")

  // Draw a "custom" connection between two nodes
  let (a, b) = ("tree.0-0-1", "tree.0-1-0",)
  line((a: a, number: .6, abs: true, b: b), (a: b, number: .6, abs: true, b: a), mark: (end: ">", start: ">"))
})
Ci dessus, on représente une partie de l'arbre de jeu.
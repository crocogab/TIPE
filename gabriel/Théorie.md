# __Principe général__

## Fonctionnement général

Les algorithmes génétiques ont pour but d'obtenir la solution approchée à un problème d'optimisation dont on ne connait pas la solution en un temps raisonnable.



Dans notre cas un algorithme génétique serait particulierement adapté à notre problème.

Les algorithmes génétiques se décomposent tous en plusieurs étapes clés

1. Codage du problème / modélisation mathématique
2. Génération d'une population initiale
3. Définition de la fonction à optimiser
4. Choix des individus / diversification de la population 
5. Arret selon certaines conditions 

Le schéma ci-dessus représente bien le fonctionnement général de l'algorithme :

<p align="center">
    <img src="https://upload.wikimedia.org/wikipedia/commons/4/42/Schema_simple_algorithme_genetique.png">


## Comparaison avec notre problème

Le but de l'algorithme est simple : il doit, à partir de nos 2 cartes et de celle du croupier déterminer si il faut prendre une carte ou pas.

Sachant que le blackjack est partiellement un jeu de hasard il n'est pas possible de prédire toujours l'issue du tirage. Le but de notre algortihme sera donc de déterminer la solution optimale pour chaque situation.

# __Principe détaillé__

## Codage du problème

Le but de cette partie est de réfléchir à comment nous allons encoder notre problème de manière à pouvoir traiter efficacement chaque situation auquel nous pouvons avoir affaire.
Le codage du problème est essentiel et une grande partie de la réussite de notre algorithme dépendra du codage de nos données.

Nous utiliserons dans cet étude le codage suivant :
* Une carte sera encodée par un entier naturel de la manière suivante :
  * Toute carte entre $2$ et $10$ sera encodée par sa valeur respective ( exemple : $3$ de carreaux est représenté par $3$)
  * Le valet,le roi ainsi que la dame seront représentés par l'entier $10$
  * L'as par l'entier $11$
  * L'absence de carte sera encodée par l'entier $0$ 

* La main d'un joueur sera représentée par $\{c_1,c_2,c_r\}$ avec $c_1$ la première carte du joueur , $c_2$ la seconde carte du joueur (valant 0 si le joueur n'a qu'une seule carte) et $c_r$ la carte visible du croupier.

__Exemple__ : Si un joueur a dans sa main un 7 de trèfle ,ainsi qu'une dame de carreaux et que la carte du croupier est un as de trèfle alors la situation sera encodée par $\{7,10,11\}$









## Autres trucs

Scaling : $1-({d \over {\gamma}})^\alpha$


Si on considère l'application :

$\begin{array}{ccccc}
f & : & \mathbb{N}*\mathbb{N} & \to & \llbracket 0;1\rrbracket \\
 & & x & \mapsto & f(x) \\
\end{array}$

Qui prends en entrée le tuple composé de la valeur de la 

import random as rd
suits = ['club', 'diamond', 'heart', 'spade']


class Card:
    """
    Card class
    value [1,2,3,4,5,6,7,8,9,10,11,12,13] avec 11 = V , 12 = D , R = 13
    suit [c,d,h,s] club,diamond,heart,spade (trefle, carreau,coeur,pique)
    """

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return f"Card : {self.value} of {self.suit}"


class hand:
    """Classe de la main"""

    def __init__(self, nb_cards: int, l_cards: list):
        self.nb_cards = nb_cards
        self.l_cards = l_cards

    def __str__(self):
        return f"Nombre de cartes [MAIN] : {self.nb_cards} , cartes = {self.l_cards}"

    def as_value(self) -> int:
        # TODO: faire une fonction qui calcule la valeur de l'as et l'utiliser dans get_value
        pass

    def get_value(self) -> int:
        total = 0
        for card in self.l_cards:
            total += card.value if card.value < 10 else 10


class Deck:
    def __init__(self, nb_cards: int, l_cards: list):
        self.nb_cards = nb_cards
        self.l_cards = l_cards

    def __str__(self):
        return f"Nombre de cartes [PILE] : {self.nb_cards} , cartes = {self.l_cards}"

    def swap(self, i: int, j: int):
        temp = self.l_cards[j]
        self.l_cards[j] = self.l_cards[i]
        self.l_cards[i] = temp

    def shuffle(self):
        for i in range(self.nb_cards):
            self.swap(i, rd.randint(0, self.nb_cards-1))


class Player:
    def __init__(self, hand: hand, id: int):
        self.id = id
        self.hand = hand
        self.is_out = False

    def check(self):
        if self.hand.get_value() > 21:
            self.is_out = True


def make_deck(n: int) -> Deck:
    """
    returns a deck of n*52 cards
    """
    deck = Deck(n*52, [])
    for i in range(n):
        for i in range(4):
            for j in range(1, 14):
                deck.l_cards.append(Card(j, suits[i]))
    for cards in deck.l_cards:
        print(cards)
    return deck


def tick():
    """
    Fonction qui gere les tours de jeu (distribution, verification, etc.)
    """

    pass


def simulation(p: int, n: int):
    """
    Fonction qui simule n parties de blackjack avec p joueurs
    """
    pass

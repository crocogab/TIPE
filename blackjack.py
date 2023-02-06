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
        print("Valeur: ", self.value, "\r")
        print("Suit: ", self.suit, "\r")
        print("--------------------------")
        return ""


class hand:
    """Classe de la main"""

    def __init__(self, nb_cards: int, l_cards: list):
        self.nb_cards = nb_cards
        self.l_cards = l_cards

    def __str__(self):
        return f"Nombre de cartes [MAIN] : {self.nb_cards} , cartes = {self.l_cards}"

    def add_card(self, card: Card) -> list:
        """ Prends une carte en argument et ajoute a la main"""
        self.l_cards.append(card)

    def get_value(self) -> int:
        total = 0
        for card in self.l_cards:
            total += card.value
        return total


class Deck:
    def __init__(self, nb_cards: int, l_cards: list):
        self.nb_cards = nb_cards
        self.l_cards = l_cards

    def __str__(self):
        return f"Nombre de cartes [PILE] : {self.nb_cards} , cartes = {self.l_cards}"

    def swap(self, i, j):
        temp = self.l_cards[j]
        self.l_cards[j] = self.l_cards[i]
        self.l_cards[i] = temp

    def shuffle(self):
        for i in range(self.nb_cards):
            self.swap(i, rd.randint(0, self.nb_cards-1))


def make_deck():
    deck = Deck(52, [])
    for i in range(4):
        for j in range(1, 14):
            deck.l_cards.append(Card(j, suits[i]))
    deck.shuffle()
    for i in range(deck.nb_cards):
        print(deck.l_cards[i])


make_deck()

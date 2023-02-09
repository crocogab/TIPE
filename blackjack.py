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
        """
        Fonction qui retourne la valeur de la main
        """
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
        """
        Fonction qui permute deux cartes dans le deck
        """
        temp = self.l_cards[j]
        self.l_cards[j] = self.l_cards[i]
        self.l_cards[i] = temp

    def shuffle(self, n: int):
        """
        Mélange un deck n fois
        TODO: implementer un algo de mélangage plus réaliste
        """
        for i in range(n):
            for j in range(self.nb_cards):
                self.swap(j, rd.randint(0, self.nb_cards-1))

    def draw(self) -> Card:
        """
        Retourne la carte du dessus du deck et la supprime du deck
        """
        card = self.l_cards[0]
        self.l_cards.pop(0)
        self.nb_cards -= 1
        return card


class Player:
    """
    Classe du joueur
    choix: true = prend une carte, false = rester
    is_out: true = le joueur est out(+21), false = le joueur est en jeu
    stopped: true = le joueur a arreté de tirer des cartes, false = le joueur peut encore tirer des cartes
    """
    def __init__(self, hand: hand, id: int):
        self.id = id
        self.hand = hand
        self.is_out = False
        self.stopped = False

    def check(self):
        """
        Fonction qui verifie si le joueur est out
        """
        if self.hand.get_value() > 21:
            self.is_out = True

    def play(self):
        """
        Fonction qui permet au joueur de jouer
        """
        # TODO: implémenter le choix
        choice = True
        if choice and not self.stopped:
            Game.give_card(self)
        else:
            self.stopped = True


class Game:
    def __init__(self, players: list, deck: Deck):
        self.players = players
        self.deck = deck

    def give_card(self, player: Player):
        """
        Fonction qui donne une carte au joueur
        """
        player.hand.l_cards.append(self.deck.draw())
        player.hand.nb_cards += 1


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

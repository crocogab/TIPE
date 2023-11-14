import random as rd

suits = ["club", "diamond", "heart", "spade"]

class Card:  # pylint: disable=too-few-public-methods
    """
    Card class
    value [1,2,3,4,5,6,7,8,9,10,11,12,13] avec 11 = V , 12 = D , R = 13
    suit [c,d,h,s] club,diamond,heart,spade (trefle, carreau,coeur,pique)
    """

    def __init__(self, value: int, suit: str):
        self.value = value
        self.suit = suit

    def real_value(self):
        """retourne la valeur réelle de la carte"""
        if self.value > 10:
            return 10
        return self.value

    def __str__(self):  # pylint: disable=inconsistent-return-statements
        if self.value > 10:
            if self.value == 11:
                return f"Jake of {self.suit}"
            if self.value == 12:
                return f"Queen of {self.suit}"
            if self.value == 13:
                return f"King of {self.suit}"
        else:
            return f"{self.value} of {self.suit}"


class Hand:
    """Classe de la main"""

    def __init__(self, nb_cards: int, l_cards: list):
        self.nb_cards = nb_cards
        self.l_cards = l_cards

    def __str__(self):
        # l'ancienne version ne marchait pas (cards.l_cards) ça affichait l'adresse mémoire
        string = (
            f"Nombre de cartes : {self.nb_cards} ,total = {self.get_value()} ,cartes = "
        )
        if self.nb_cards == 0:
            return string + "None"
        for card in self.l_cards:
            string += str(card) + " "
        return string

    def get_string(self):
        """Fonction permettant d'obtenir la liste des cartes sous forme de string"""
        string = ""
        for card in self.l_cards:
            string += str(card.real_value()) + ","
        return string[:-1]

    def get_bot_hand(self):
        """Fonction permettant au bot d'obtenir la liste des cartes justes en int"""
        return [card.value for card in self.l_cards]

    def get_value(self):
        """
        Calcul de la valeur de la main si> 21, et si on a un as, on le transforme en 1
        """
        value = 0
        for card in self.l_cards:
            if card.value == 1:
                value += 11
            elif card.value > 10:
                value += 10
            else:
                value += card.value
        for card in self.l_cards:
            if value > 21 and card.value == 1:
                value -= 10
        return value


class Deck:
    """
    Classe du deck
    self.nb_cards: nombre de cartes dans le deck
    self.l_cards: liste des cartes dans le deck
    """

    def __init__(self, nb_cards: int, l_cards: list):
        self.nb_cards = nb_cards
        self.l_cards = l_cards

    def __str__(self):
        return f"Nombre de cartes [PILE] : {self.nb_cards} , cartes = {self.l_cards}"

    def shuffle(self, shuffles: int):
        """
        Mélange un deck shuffles fois
        """
        lcard = []
        for _ in range(shuffles):
            for _ in range(self.nb_cards):
                lcard.append(self.l_cards.pop(rd.randint(0, self.nb_cards - 1)))
                self.nb_cards -= 1
        self.l_cards = lcard

    def draw(self) -> Card:
        """
        Retourne la carte du dessus du deck et la supprime du deck
        """
        card = self.l_cards[0]
        self.l_cards.pop(0)
        self.nb_cards -= 1
        return card


class Croupier:
    """
    Classe de la croupier
    """

    def __init__(self, hand: Hand, croupier_id: int):
        self.id = croupier_id  # pylint: disable=invalid-name
        self.hand = hand
        self.is_out = False
        self.stopped = False
        self.is_croupier = True

    def check(self, current_game: "Game"):
        """
        Fonction qui verifie si le croupier est out et si il blackjack gagne
        """
        if self.hand.get_value() > 21:
            self.is_out = True

        elif self.hand.get_value() == 21:
            self.stopped = True
            for player in current_game.players:
                player.is_out = True
            self.is_out = False

    def play(self, current_game: "Game"):
        """
        Fonction qui permet au croupier de jouer
        """
        self.check(current_game)
        if not self.is_out and not self.stopped:
            if self.hand.get_value() < 17:
                current_game.give_card(self)
            else:
                self.stopped = True
        self.check(current_game)


class Player:
    """
    Classe du joueur
    choix: true = prend une carte, false = rester
    is_out: true = le joueur est out(+21), false = le joueur est en jeu
    stopped: false si le joueur peut encore jouer
    """

    def __init__(self, hand, player_id: int):
        self.id = player_id  # pylint: disable=invalid-name
        self.hand = hand
        self.is_out = False
        self.stopped = False
        self.is_croupier = False

    def check(self):
        # current_game est nécéssaire pour le check du croupier
        """
        Fonction qui verifie si le joueur est out
        """
        if self.hand.get_value() > 21:
            self.is_out = True
        elif self.hand.get_value() == 21:
            self.stopped = True

class Game:
    """
    Classe du jeu
    contient les joueurs et le deck
    """

    def __init__(self, players: list, deck: Deck):
        self.players = players
        self.deck = deck

    def get_deck(self):
        """
        Fonction qui retourne le deck
        """
        return self.deck

    def give_card(self, player):
        """
        Fonction qui donne une carte au joueur
        """
        player.hand.l_cards.append(self.deck.draw())
        player.hand.nb_cards += 1


def make_deck(deck_nbr: int) -> Deck:
    """
    returns a deck of deck_nbr*52 cards
    """
    deck = Deck(deck_nbr * 52, [])
    for i in range(deck_nbr):
        for i in range(4):
            for j in range(1, 14):
                deck.l_cards.append(Card(j, suits[i]))
    return deck
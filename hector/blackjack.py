import random as rd


class Card:  # pylint: disable=too-few-public-methods
    """
    Card class
    value [1,2,3,4,5,6,7,8,9,10,11,12,13] 11 = J , 12 = Q , 13 = K
    suit [c,d,h,s] club,diamond,heart,spade
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
    """
    Hand class
    attributes:
        nb_cards: the number of cards in the hand
        l_cards: the list of cards in the hand
    """

    def __init__(self, nb_cards: int, l_cards: list):
        self.nb_cards = nb_cards
        self.l_cards = l_cards

    def __str__(self):
        string = (
            f"Nombre de cartes : {self.nb_cards} ,total = {self.get_value()} ,cartes = "
        )
        if self.nb_cards == 0:
            return string + "None"
        for card in self.l_cards:
            string += str(card) + " "
        return string

    def get_string(self):
        """Get a string representation of the hand"""
        string = ""
        for card in self.l_cards:
            string += str(card.real_value()) + ","
        return string[:-1]

    def get_bot_hand(self):
        """Returns the values of the cards in the bot's hand"""
        return [card.value for card in self.l_cards]

    def get_value(self):
        """Computes the value of the hand, if the hands bursts, it will try to remove aces"""
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
    Deck class
    attributes:
        nb_cards: the number of cards in the deck
        l_cards: the list of cards in the deck
    """

    def __init__(self, nb_cards: int, l_cards: list):
        self.nb_cards = nb_cards
        self.l_cards = l_cards

    def __str__(self):
        return f"Nombre de cartes [PILE] : {self.nb_cards} , cartes = {self.l_cards}"

    def shuffle(self, nb_shuffle: int):
        """Shuffles the deck nb_shuffle times"""
        lcard = []
        for _ in range(nb_shuffle):
            for _ in range(self.nb_cards):
                lcard.append(self.l_cards.pop(rd.randint(0, self.nb_cards - 1)))
                self.nb_cards -= 1
        self.l_cards = lcard
        self.nb_cards = len(lcard)

    def draw(self) -> Card:
        """Returns the first card of the deck and removes it from the deck"""
        card = self.l_cards[0]
        self.l_cards.pop(0)
        self.nb_cards -= 1
        return card

    def remove(self, card: Card):
        """
        Removes a given card from the deck
        input:
            card: Card, the card to remove
        output:
            -1 if the card is not in the deck, 0 otherwise
        """
        for i in range(self.nb_cards):
            if (
                self.l_cards[i].value == card.value
                and self.l_cards[i].suit == card.suit
            ):
                self.l_cards.pop(i)
                self.nb_cards -= 1
                return 0
        return -1


class Croupier:
    """
    Croupier class
    attributes:
        id: the id of the croupier
        hand: the hand of the croupier
        is_out: True if the croupier is out, False otherwise
        stopped: True if the croupier stopped, False otherwise
        is_croupier: True if the player is the croupier, False otherwise
    """

    def __init__(self, hand: Hand, croupier_id: int):
        self.id = croupier_id  # pylint: disable=invalid-name
        self.hand = hand
        self.is_out = False
        self.stopped = False
        self.is_croupier = True

    def check(self, current_game: "Game"):
        """
        Function that checks if the croupier is out
        input:
            current_game: Game, the game the croupier is playing
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
        Function that makes the croupier play
        input:
            current_game: Game, the game the croupier is playing
        """
        self.check(current_game)
        if not self.is_out and not self.stopped:
            if self.hand.get_value() < 17:
                current_game.give_card(self)
            else:
                self.stopped = True
        self.check(current_game)


class Player:  # pylint: disable=too-few-public-methods
    """
    Player class
    attributes:
        id: the id of the player
        hand: the hand of the player
        is_out: True if the player is out, False otherwise
        stopped: True if the player stopped, False otherwise
        is_croupier: True if the player is the croupier, False otherwise
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
    Game class
    attributes:
        players: the list of players
        deck: the deck of the game
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
    suits = ["club", "diamond", "heart", "spade"]
    deck = Deck(deck_nbr * 52, [])
    for i in range(deck_nbr):
        for i in range(4):
            for j in range(1, 14):
                deck.l_cards.append(Card(j, suits[i]))
    return deck

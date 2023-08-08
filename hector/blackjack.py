import random as rd
import sys
import colorama as col
suits = ["club", "diamond", "heart", "spade"]
color_list = [col.Fore.RED, col.Fore.BLUE, ]
INFO = col.Fore.CYAN
col.init()
HEADLESS = True


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
        string = f"Nombre de cartes : {self.nb_cards} ,total = {self.get_value()} ,cartes = "
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
        return string

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
        lcard=[]
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
            if not HEADLESS:
                print(f"{self.hand}\n")
                print("Croupier est out")
            self.is_out = True

        elif self.hand.get_value() == 21:
            if not HEADLESS:
                print("Blackjack du croupier ! La banque récupère la mise \n")
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
                if not HEADLESS:
                    print(INFO, "Croupier pioche.", col.Style.RESET_ALL)
                current_game.give_card(self)
                if self.hand.l_cards != [] and len(sys.argv) != 0 and not HEADLESS:
                    print(INFO, f"La premiere carte du jeu du croupier est {self.hand.l_cards[0]}",\
                          col.Style.RESET_ALL)
            elif not HEADLESS:
                print("Le croupier s'arrete")
            self.stopped = True
        if not HEADLESS:
            print("\n", end="")
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
        self.color = color_list[rd.randint(0, len(color_list)-1)] if not HEADLESS else ""
        if color_list.__contains__(self.color):
            color_list.remove(self.color)

    def check(self):
        # current_game est nécéssaire pour le check du croupier
        """
        Fonction qui verifie si le joueur est out
        """
        if self.hand.get_value() > 21:
            if not HEADLESS:
                print(self.color+f"{self.hand}\n")
                print(f"Joueur {self.id} est out")
            self.is_out = True
        elif self.hand.get_value() == 21:
            if not HEADLESS:
                print(self.color, "BLACKJACK !", col.Style.RESET_ALL)
            self.stopped = True

    def play(self, current_game):
        """
        Fonction qui permet au joueur de jouer
        """
        if not self.is_out and not self.stopped:
            print(self.color, "Voulez vous prendre une carte (o/n)",
                  col.Style.RESET_ALL, end="")
            choice = input()
            if choice in ["o", "O"]:
                current_game.give_card(self)
            elif choice in ["n", "N"]:
                self.stopped = True
            else:
                print(self.color, "Choix invalide", col.Style.RESET_ALL)
                self.play(game)
        print("\n", end="")

    def rand_play(self, current_game: "Game"):
        """Permet au bot de jouer (aléatoirement)"""
        if not self.is_out and not self.stopped:
            random = rd.randint(0, 2)
            # print(r)
            if random > 0 or self.hand.l_cards == []:
                # 66% de chance de tirer ou tire forcement si premier choix
                current_game.give_card(self)
                self.check()
            else:
                self.stopped = True

    def bot_play(self, current_game: "Game", choice: bool):
        """Permet au bot de jouer (sans input)
        choice: true = prend une carte, false = rester

        """
        if not self.is_out and not self.stopped:
            if choice:
                current_game.give_card(self)
                self.check()
            else:
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
    deck = Deck(deck_nbr*52, [])
    for i in range(deck_nbr):
        for i in range(4):
            for j in range(1, 14):
                deck.l_cards.append(Card(j, suits[i]))
    return deck


def game(players: list):
    """
    Fonction principale de la partie
    """
    deck = make_deck(1)
    deck.shuffle(100)
    my_game = Game(players, deck)
    while len([player for player in players if (not player.stopped and not player.is_out)]) >= 1:
        for player in players:
            if not player.stopped and not player.is_out and not player.is_croupier:
                print(
                    player.color, f"Joueur {player.id} : {player.hand}", col.Style.RESET_ALL)
                player.play(my_game)
                player.check()
            else:
                player.play(my_game)
                player.check(my_game)
    print("Fin de la partie, Résultats :")
    if len([player for player in players if (not player.is_out and not player.is_croupier)]) == 0:
        print("Tous les joueurs sont out, la banque gagne")
    else:
        my_croupier = [player for player in players if player.is_croupier][0]
        croupier_hand_value = my_croupier.hand.get_value()
        print("Gagnant(s) :")
        for player in players:
            if not player.is_out and not player.is_croupier:
                if player.hand.get_value() > croupier_hand_value:
                    print(
                        f"Joueur {player.id} a gagné avec le jeu \
                        {player.hand} total = {player.hand.get_value()}")
                elif player.hand.get_value() == croupier_hand_value:
                    print(
                        f"Joueur {player.id} a fait égalité avec le croupier avec le jeu\
                             {player.hand} total = {player.hand.get_value()}")
                elif not croupier.is_out:
                    print(
                        f"Joueur {player.id} a perdu contre le croupier avec le jeu\
                             {player.hand} total = {player.hand.get_value()}")
            elif player.is_out:
                print(
                    f"Joueur {player.id} a perdu (+21)\
                        {player.hand} total = {player.hand.get_value()}")
        print(
            f"Croupier avec le jeu : {croupier.hand} total = {croupier.hand.get_value()}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "game":
        HEADLESS = False
        hector = Player(Hand(0, []), 0)
        gabriel = Player(Hand(0, []), 1)
        croupier = Croupier(Hand(0, []), 2)
        game([hector, gabriel, croupier])

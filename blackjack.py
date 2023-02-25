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
        for card in self.l_cards:
            string += str(card) + " "
        return string
    
    def get_bot_hand(self):
        """Fonction permettant au bot d'obtenir la liste des cartes justes en int"""
        return [card.value for card in self.l_cards]


    def get_value(self):
        """
        calcul de la valeur de la main: si elle est > 21, alors on regarde si on a un as, si oui on le transforme en 1
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
        if self.nb_cards>=1: 
            """Evite de pop un deck vide"""
            card = self.l_cards[0]
            self.l_cards.pop(0)
            self.nb_cards -= 1
            return card
        else:
            raise Exception("Deck is empty")

class Croupier:
    """
    Classe de la croupier
    """
    def __init__(self, hand,id:int):
        self.id = id
        self.hand = hand
        self.is_out = False
        self.stopped = False
        self.is_croupier= True
    
    def check(self,game):
        """
        Fonction qui verifie si le croupier est out et si il blackjack gagne
        """
        if self.hand.get_value() > 21:
            print(f"{self.hand}\n")
            print(f"Croupier est out")
            self.is_out = True
        
        elif self.hand.get_value() == 21:
            print("Blackjack du croupier ! La banque récupère la mise \n")
            self.stopped = True
            for player in game.players:
                player.is_out = True
            self.is_out = False
    
    def play(self, game):
        if not self.is_out and not self.stopped:
            if self.hand.get_value() < 17:
                print(f"Croupier pioche.")
                game.give_card(self)
                self.check(game)
                if self.hand.l_cards != []:
                    print(f"La premiere carte du jeu du croupier est {self.hand.l_cards[0]}")

            else :
                print("Le croupier s'arrete")
                self.stopped = True
            




        


class Player:
    """
    Classe du joueur
    choix: true = prend une carte, false = rester
    is_out: true = le joueur est out(+21), false = le joueur est en jeu
    stopped: true = le joueur a arreté de tirer des cartes, false = le joueur peut encore tirer des cartes
    """

    def __init__(self, hand, id: int):
        self.id = id
        self.hand = hand
        self.is_out = False
        self.stopped = False
        self.is_croupier= False

    def check(self,game):
        """
        Fonction qui verifie si le joueur est out
        """
        if self.hand.get_value() > 21:
            print(f"{self.hand}\n")
            print(f"Joueur {self.id} est out")
            self.is_out = True
        elif self.hand.get_value() == 21:
            print("BLACKJACK !")
            self.stopped = True

    def play(self, game):
        """
        Fonction qui permet au joueur de jouer
        """
        if not self.is_out and not self.stopped:
            print("Voulez vous prendre une carte (o/n)")
            choice = input()
            if choice == "o" or choice == "O":
                game.give_card(self)
                self.check(game)
            elif choice == "n" or choice == "N":
                self.stopped = True
            else:
                print("Choix invalide")
                self.play(game)
    
    
    def rand_play(self, game):
        """Permet au bot de jouer (aléatoirement)"""
        if not self.is_out and not self.stopped:
            r=rd.randint(0,2)
            #print(r)
            if r > 0 or self.hand.l_cards==[]:
                """66% de chance de tirer ou tire forcement si premier choix"""
                game.give_card(self)
                self.check(game)
            else:
                self.stopped = True
                
        
    
    def bot_play(self, game,choice:bool):
        """Permet au bot de jouer (sans input)
        choice: true = prend une carte, false = rester

        """
        if not self.is_out and not self.stopped:
            if choice :
                game.give_card(self)
                self.check(game)
            else:
                self.stopped = True


            




class Game:
    def __init__(self, players: list, deck: Deck):
        self.players = players
        self.deck = deck
    

        

    def get_deck(self):
        return self.deck

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
    return deck


def game(players: list):
    deck = make_deck(1)
    deck.shuffle(100)
    game = Game(players, deck)
    while len([player for player in players if (not player.stopped and not player.is_out)]) > 1:
        for player in players:
            if not player.stopped and not player.is_out:
                print(f"Joueur {player.id} : {player.hand}")
                player.play(game)
                player.check(game)
    print("Fin de la partie, gagnant(s) :")
    
    croupier_is_out=True
    
    for player in players :
        if not player.is_out:
            if player.is_croupier :
                croupier_is_out=False
                croupier_hand_value=player.hand.get_value()
    
    if croupier_is_out:
        for player in players:
            if not player.is_out:
                print(f"Joueur {player.id} : {player.hand} ")
    else:
        for player in players :
            
            if not player.is_out and player.is_croupier:
                print(f"Croupier avec le jeu : {player.hand} total = {player.hand.get_value()}")



            if not player.is_out and player.hand.get_value() > croupier_hand_value and not player.is_croupier:
                print(f"Joueur {player.id} : {player.hand} ")
            if not player.is_out and player.hand.get_value() == croupier_hand_value and not player.is_croupier:

                print(f"Joueur {player.id} est à égalité avec le croupier. Il récupère sa mise ")


        
            




# hector = Player(Hand(0, []), 0)
# gabriel = Player(Hand(0, []), 1)
# croupier = Croupier(Hand(0, []), 2)

# game([hector, gabriel,croupier])

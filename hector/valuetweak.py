# Find the best SAFENESS value to use in hector/tree.py to get the best winrate.
# Théorie: Tirer une valeur de SAFENESS aléatoire entre 0 et 1, et
#enregistrer sous le format suivant : victoire(0/1),SAFENESS\n
import logging
import sys
import tree
from blackjack import Player, Croupier, Game, Hand, make_deck
logging.basicConfig(level=logging.INFO)


def simple(safeness:float)->bool:
    """
    Play a game with a given safeness and return True if the player lost
    """
    deck = make_deck(1)
    deck.shuffle(100)
    player = Player(Hand(0, []), 0)
    croup = Croupier(Hand(0, []), 1)
    my_game = Game([player, croup], deck)
    # Here, we take two cards for each player as it is the minimum to start the game
    mytree = tree.create_game_tree(tree.Tree(0,0), 0)
    logging.info("\033[32m"+"--------------------"+"\033[0m")
    for _ in range(2):
        my_game.give_card(player)
        mytree.navigate(player.hand.l_cards[-1].real_value())
        my_game.give_card(croup)
    logging.debug("player hand: %s",player.hand)
    while ((not player.is_out and not player.stopped) or (not croup.is_out and (not croup.stopped))):
        if not player.is_out and not player.stopped:
            cards_string = player.hand.get_string()
            cards_string = cards_string[:-1]
            logging.debug("cards_string = %s",cards_string)
            if (automate(cards_string,safeness,mytree)[0] or player.hand.get_value() == 0):
                logging.info("HIT! %s cards with a value of %s", \
                             len(player.hand.l_cards),player.hand.get_value())
                my_game.give_card(player)
                player.check()
            else:
                player.stopped = True
                logging.info("STOP! %s cards with a value of %s. Surival rate: %s",\
                             len(player.hand.l_cards),player.hand.get_value(),\
                                automate(cards_string,safeness,mytree)[1]) #TODO change this
        if not croup.is_out and not croup.stopped:
            croup.play(my_game)
    logging.info("\033[31m"+"--------------------")
    lost = False
    if player.is_out or (player.hand.get_value() < croup.hand.get_value() and not croup.is_out):
        lost = True
        logging.info("Player lost because he has %s and croupier has %s"+"\033[0m",\
                     player.hand.get_value(),croup.hand.get_value())
    else:
        logging.info("Player won because he has %s and croupier has %s"+"\033[0m",\
                     player.hand.get_value(),croup.hand.get_value())
    return lost


def automate(card_string:str,safeness:float,mytree:tree.Tree) -> tuple:
    """
    take a list of cards as argument and return true if the player should take a card
    """
    card_string = card_string.split(",")
    logging.debug("card_tab: %s",card_string)
    mytree.survival_meth() #TODO  pas besoin de calculer la survie pour tout l'arbre
    for card in card_string:
        mytree = mytree.navigate(card)
    return mytree.shouldtake(safeness),mytree.survival

def wrapper():
    """
    Wrapper for the simple function
    """
    n = int(sys.argv[1]) #pylint: disable=invalid-name
    step = 0.1
    safeness = 0.5
    while safeness < 1:
        for _ in range(n):
            if simple(safeness):
                with open("data.csv", "a", encoding="utf-8") as file:
                    file.write(f"0,{safeness}\n")
            else:
                with open("data.csv", "a", encoding="utf-8") as file:
                    file.write(f"1,{safeness}\n")
        safeness += step

if __name__ == "__main__":
    wrapper()

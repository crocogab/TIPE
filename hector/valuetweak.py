# Find the best SAFENESS value to use in hector/tree.py to get the best winrate.
# Théorie: Tirer une valeur de SAFENESS aléatoire entre 0 et 1, et enregistrer sous le format suivant : victoire(0/1),SAFENESS\n

import random
import tree
from blackjack import *
import logging
logging.basicConfig(level=logging.DEBUG)
import sys
import random



def simple(safeness:float)->bool:
    deck = make_deck(1)
    deck.shuffle(100)
    player = Player(Hand(0, []), 0)
    croup = Croupier(Hand(0, []), 1)
    my_game = Game([player, croup], deck)
    # Here, we take two cards for each player as it is the minimum to start the game
    for i in range(2):
        my_game.give_card(player)
        my_game.give_card(croup)
    logging.debug("player hand: %s",player.hand)
    while not( player.is_out or player.stopped):
        cards_string = player.hand.get_string()
        cards_string = cards_string[:-1]
        logging.debug("cards_string = %s",cards_string)
        if (tree.automate(cards_string,safeness)[0] or player.hand.get_value() == 0):
            logging.debug("HIT! %s cards with a value of %s",len(player.hand.l_cards),player.hand.get_value())
            my_game.give_card(player)
        else:
            player.stopped = True
            logging.debug("STOP! %s cards with a value of %s. Surival rate: %s",len(player.hand.l_cards),player.hand.get_value(),tree.automate(cards_string,safeness)[1])
        my_game.give_card(croup)
    lost = False
    if player.is_out or (player.hand.get_value() < croup.hand.get_value() and not croup.is_out):
        lost = True
    return lost


def wrapper():
    n = int(sys.argv[1])
    step = 0.1
    safeness = 0
    while safeness < 1:
        for _ in range(n):
            if simple(safeness):
                with open("data.csv", "a") as file:
                    file.write(f"0,{safeness}\n")
            else:
                with open("data.csv", "a") as file:
                    file.write(f"1,{safeness}\n")
        safeness += step

if __name__ == "__main__":
    wrapper()
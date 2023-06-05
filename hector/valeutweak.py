# Find the best SAFENESS value to use in hector/tree.py to get the best winrate.
# Théorie: Tirer une valeur de SAFENESS aléatoire entre 0 et 1, et enregistrer sous le format suivant : victoire(0/1),SAFENESS\n

import random
import tree
from blackjack import *
def main():
    print(tree.automate("10,5"))

def simple():
    deck = make_deck(1)
    deck.shuffle(100)
    player = Player(Hand(0, []), 0)
    croupier = Croupier(Hand(0, []), 1)
    players = [player, croupier]
    my_game = Game([player, croupier], deck)
    while not( player.is_out or player.stopped):
        cards_string = ""
        for card in player.hand.l_cards:
            cards_string += str(card.value) + ","
        cards_string = cards_string[:-1]
        if (tree.automate(cards_string) or player.hand.get_value() == 0):
            print("DEBUG: taking card because" ,tree.automate(cards_string) , "or", player.hand.get_value() == 0)
            my_game.give_card(player)
            print("DEBUG: HIT",player.hand)
        else:
            player.stopped = True
        my_game.give_card(croupier)
    lost = False
    if player.is_out or (player.hand.get_value() < croupier.hand.get_value() and not croupier.is_out):
        lost = True
    return lost

if __name__ == "__main__":
    simple()
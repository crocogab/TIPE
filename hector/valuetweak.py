# Find the best SAFENESS value to use in hector/tree.py to get the best winrate.
# Théorie: Tirer une valeur de SAFENESS aléatoire entre 0 et 1, et
# enregistrer sous le format suivant : victoire(0/1),SAFENESS\n
import logging
import tqdm
import tree
from blackjack import Player, Croupier, Game, Hand, make_deck

logging.basicConfig(level=logging.INFO)


def simple(safeness: float, mytree: tree.Tree) -> bool:
    """
    Play a game with a given safeness and return True if the player lost
    """
    deck = make_deck(1)
    deck.shuffle(100)
    player = Player(Hand(0, []), 0)
    croup = Croupier(Hand(0, []), 1)
    my_game = Game([player, croup], deck)
    # Here, we take two cards for each player as it is the minimum to start the game
    logging.debug("\033[33m" + "----------GAME START----------" + "\033[0m")
    for _ in range(2):
        my_game.give_card(player)
        my_game.give_card(croup)
    logging.debug("player hand: %s", player.hand)
    while (not player.is_out and not player.stopped) or (
        not croup.is_out and not croup.stopped
    ):
        if not player.is_out and not player.stopped:
            cards_string = player.hand.get_string()
            cards_string = cards_string[:-1]
            logging.debug("cards_string = %s", cards_string)
            if (
                automate(cards_string, safeness, mytree)[0]
                or player.hand.get_value() == 0
            ):
                logging.debug(
                    "HIT! %s cards with a value of %s",
                    len(player.hand.l_cards),
                    player.hand.get_value(),
                )
                my_game.give_card(player)
                player.check()
            else:
                player.stopped = True
                logging.debug(
                    "STOP! %s cards with a value of %s. Surival rate: %s",
                    len(player.hand.l_cards),
                    player.hand.get_value(),
                    automate(cards_string, safeness, mytree)[1],
                )
                logging.debug([child.val for child in mytree.children])
        if not croup.is_out and not croup.stopped:
            croup.play(my_game)
    logging.debug("\033[31m" + "--------------------")
    lost = False
    if player.is_out or (
        player.hand.get_value() < croup.hand.get_value() and not croup.is_out
    ):
        lost = True
        logging.debug(
            "\033[31m"
            + "Player lost because he has %s and croupier has %s"
            + "\033[0m",
            player.hand.get_value(),
            croup.hand.get_value(),
        )
    else:
        logging.debug(
            "\033[32m" + "Player won because he has %s and croupier has %s" + "\033[0m",
            player.hand.get_value(),
            croup.hand.get_value(),
        )
    logging.debug("\033[33m" + "---------GAME END-----------" + " \033[0m")
    return lost


def automate(card_string: str, safeness: float, my_tree: tree.Tree) -> tuple:
    """
    take a list of cards as argument and return true if the player should take a card
    """
    card_list = card_string.split(",")
    for card in card_list:
        my_tree = my_tree.navigate(card)
    return my_tree.shouldtake(safeness), my_tree.survival


def print_surivals(mytree: tree.Tree):
    """
    print the survivals of the tree
    """
    with open("survivals.csv", "a", encoding="utf-8") as file:
        for child in mytree.children:
            val = str(child.val) + " " + str(child.survival)
            file.write(val)
            file.write("\n")
            print_surivals(child)


def wrapper():
    """
    Wrapper for the simpyle function
    """
    n = 10000  # int(sys.argv[1])  # pylint: disable=invalid-name
    step = 0.0625
    safeness = 0.45
    mydeck = tree.make_my_deck()
    mytree = tree.create_game_tree(tree.Tree(0, 0), 0, mydeck)
    mytree.survival_meth()
    # print_surivals(mytree)
    while safeness < 1:
        for _ in range(n):
            if simple(safeness, mytree):
                with open("data.csv", "a", encoding="utf-8") as file:
                    file.write(f"0,{safeness}\n")
            else:
                with open("data.csv", "a", encoding="utf-8") as file:
                    file.write(f"1,{safeness}\n")
            mytree = mytree.root
        safeness += step


def contest(number: int):
    "plays number games and print the winrate (use a loading bar)"
    mydeck = tree.make_my_deck()
    mytree = tree.create_game_tree(tree.Tree(0, 0), 0, mydeck)
    mytree.survival_meth()
    lost = 0
    for _ in tqdm.tqdm(range(number)):
        if simple(0.45, mytree):
            lost += 1
    mytree = mytree.root
    print(f"Winrate: {(1 - lost/number)*100}")


if __name__ == "__main__":
    contest(1000000)

# Find the best SAFENESS value to use in hector/tree.py to get the best winrate.
import logging
import time
import multiprocessing
import tqdm
import tree
from blackjack import Player, Croupier, Game, Hand, make_deck

logging.basicConfig(level=logging.INFO)


def simple(safeness: float, trees:dict) -> bool:
    """
    simple plays a game of blackjack following survival >= safeness
    inputs:
        safeness: float between 0 and 1, won't take a card if the survival rate is below safeness
        mytree: tree.Tree, the tree to decide the player's actions
    output:
        lost: bool, True if the player lost, False otherwise
    """
    # create a deck and shuffle it
    deck = make_deck(1)
    deck.shuffle(100)
    # instantiate the player, the croupier and the game
    player = Player(Hand(0, []), 0)
    croupier = Croupier(Hand(0, []), 1)
    my_game = Game([player, croupier], deck)
    logging.debug("\033[33m" + "----------GAME START----------" + "\033[0m")
    # take two cards for player and the croupier
    for _ in range(2):
        my_game.give_card(player)
        my_game.give_card(croupier)
    croup_fst = croupier.hand.l_cards[0].real_value()
    # copy trees so we can modify them without modifying the original
    mytree = trees[croup_fst]
    logging.debug("player hand: %s", player.hand)
    # while one of the player is neither out nor stopped, play
    while (not player.is_out and not player.stopped) or (
        not croupier.is_out and not croupier.stopped
    ):
        if not player.is_out and not player.stopped:
            cards_string = player.hand.get_string()
            logging.debug("cards_string = %s", cards_string)
            # if the player should take a card
            if automate(cards_string, safeness, mytree)[0]:
                logging.debug(
                    "HIT! %s cards with a value of %s",
                    len(player.hand.l_cards),
                    player.hand.get_value(),
                )
                my_game.give_card(player)
                player.check()
            else:
                # if the player shouldn't take a card, stop
                player.stopped = True
                logging.debug(
                    "STOP! %s cards with a value of %s. Surival rate: %s",
                    len(player.hand.l_cards),
                    player.hand.get_value(),
                    automate(cards_string, safeness, mytree)[1],
                )
                logging.debug([child.val for child in mytree.children])
        if not croupier.is_out and not croupier.stopped:
            croupier.play(my_game)
    logging.debug("\033[31m" + "--------------------")
    lost = False
    trees[croup_fst] = mytree.root
    if player.is_out or (
        player.hand.get_value() < croupier.hand.get_value() and not croupier.is_out
    ):
        lost = True
        logging.debug(
            "\033[31m"
            + "Player lost because he has %s and croupier has %s"
            + "\033[0m",
            player.hand.get_value(),
            croupier.hand.get_value(),
        )
    elif player.hand.get_value() == croupier.hand.get_value():
    # if the player and the croupier have the same value, we replay
        lost = simple(safeness, trees)
    else:
        logging.debug(
            "\033[32m" + "Player won because he has %s and croupier has %s" + "\033[0m",
            player.hand.get_value(),
            croupier.hand.get_value(),
        )
    logging.debug("\033[33m" + "---------GAME END-----------" + " \033[0m")
    return lost


def automate(card_string: str, safeness: float, my_tree: tree.Tree) -> tuple:
    """
    returns true if a player should take a card and the survival rate of the node
    inputs:
        card_string: str, the cards the player has
        safeness: float, the safeness value to use
        my_tree: tree.Tree, the tree to use
    outputs:
        should_take: bool, True if the player should take a card, False otherwise
        survival: float, the survival rate of the node
    """
    # separate the cards
    card_list = card_string.split(",")
    # navigate the tree to the last card
    for card in card_list:
        my_tree = my_tree.navigate(card)
    # return the decision
    return my_tree.shouldtake(safeness), my_tree.survival


def print_surivals(mytree: tree.Tree):
    """
    print the survivals of the tree for debug purposes
    input:
        mytree: tree.Tree, the tree of which we want to print the survivals
    """
    with open("survivals.csv", "a", encoding="utf-8") as file:
        for child in mytree.children:
            val = str(child.val) + " " + str(child.survival)
            file.write(val)
            file.write("\n")
            print_surivals(child)


def safeness_iterate(
    iterations: int = 10000, step: float = 0.0625, safeness: float = 0, stop = 1
):
    """
    repeat simple with different safeness values to find the best one. Write the results in data.csv
    inputs:
        iterations: int, the number of games to play for each safeness value
        step: float, the step between each safeness value
        safeness: float, the starting safeness value
    """
    # create a tree
    mydeck = tree.make_my_deck()
    mytree = tree.create_game_tree(tree.Tree(0, 0), 0, mydeck)
    mytree.survival_meth()
    while safeness < stop:
        for _ in range(iterations):
            if simple(safeness, mytree):
                with open("data2.csv", "a", encoding="utf-8") as file:
                    file.write(f"0,{safeness}\n")
            else:
                with open("data.csv", "a", encoding="utf-8") as file:
                    file.write(f"1,{safeness}\n")
            # navigate back to the root to avoid creating a new tree
            mytree = mytree.root
        safeness += step


def contest(iterations: int):
    """plays number games and print the winrate
    inputs:
        iterations: int, the number of games to play
    """
    # create a deeck and a tree
    # mydeck = tree.make_my_deck()
    # mytree = tree.create_game_tree(tree.Tree(0, 0), 0, mydeck)
    # mytree.survival_meth()
    timestamp = time.time()
    trees = {}
    for i in range(1,11):
        mydeck = tree.make_my_deck()
        mydeck.remove(i)
        trees[i] = tree.create_game_tree(tree.Tree(0, 0), 0, mydeck)
        trees[i].survival_meth()
    lost = 0
    print("pre-iteration time:", time.time() - timestamp)
    # tqdm is used for the progress bar it's like a for loop but with a progress bar
    timestamp2 = time.time()
    for _ in tqdm.tqdm(range(iterations)):
        if simple(0.4921875, trees):
            lost += 1
    print("iteration time:", time.time() - timestamp2)
    print("time per iteration:", (time.time() - timestamp2)/iterations)
    print("total time:", time.time() - timestamp)
    print(f"Winrate: {((iterations - lost)/iterations)*100}")
    with open("winrate", "a", encoding="utf-8") as file:
        file.write(f"Winrate: {(1 - lost/iterations)*100}\n")
    return (1 - lost/iterations)*100

if __name__ == "__main__":
    # compute a total winrate from multiple contests run in parallel with multiprocessing
    ITERATION_PER_THREADS = 1000000000
    threads = multiprocessing.cpu_count()
    with multiprocessing.Pool(threads) as p:
        WINRATE = sum(p.map(contest, [ITERATION_PER_THREADS]*threads))/threads
    print(f"Total winrate: {WINRATE}")

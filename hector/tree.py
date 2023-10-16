import time
import sys
import logging

# SAFENESS = 0.5
# SAFENESS represents the minimum survival rate of a node's children to be considered a good node
# the rate is calculated by dividing the number of children
#  with a value < 21 by the total number of children


class Tree:
    """
    A tree is a node with a value and a list of children
    """

    def __init__(self, value: int, total: int, children=None, root=None):
        self.val = value
        self.children = children or []
        self.total = self.val + total
        self.virtualchildrenscount = 0
        self.survival = -1
        self.root = root or self
        self.weight = 1
        # virtual childrens are childrens that represents losing hands
        # ( needed to calculate the survival rate but  faster to count instead of creating)

    def survival_meth(self):
        """calculates the survival rate of the tree"""
        try:
            total_weight = sum(
                child.weight for child in self.children if child.total <= 21
            )
            self.survival = total_weight / (total_weight + self.virtualchildrenscount)
        except ZeroDivisionError:
            self.survival = 0
        for child in self.children:
            child.survival_meth()

    def is_empty(self):
        """returns True if the node is empty"""
        return self.val == -1

    def navigate(self, next_node: int):
        """returns the child with the value next_node if it exists, else returns -1"""
        try:
            for child in self.children:
                if child.val == int(next_node):
                    return child
        except (IndexError, ValueError):
            logging.warning(
                f"Invalid child value {next_node}, childs are %s",
                [child.val for child in self.children],
            )
            return Tree(-1, -1)
        return -1

    def shouldtake(self, safeness: float):
        """returns True if the node is safe enough to be considered a good node"""
        if self.children == []:
            return False
        return self.survival > safeness


def create_game_tree(current: Tree, depth: int, deck: list):
    """
    create_game_tree creates recursively a tree with each node being a card.
    current: the current node
    depth: the number of iterations we've been through
    deck: list of ints representing cards.
    """
    maxdepth = 6  # arbitrary value
    if depth == maxdepth:
        return current
    for card in deck:
        if current.total + card <= 21:
            # if a child with the same value does not exist, create it
            if current.navigate(card) == -1:
                current.children.append(Tree(card, current.total, root=current.root))
            else:  # else, increment the weight of the existing child
                current.navigate(card).weight += 1
        else:
            # if total + card > 21 the game is lost so we don't create a child we just count it
            current.virtualchildrenscount += 1
    for child in current.children:
        # for each child, remove the card from the deck and create the tree
        try:
            deck.remove(child.val)
        except ValueError:
            logging.warning(
                "card %s already removed (this should never happen wtf)", child.val
            )
        create_game_tree(child, depth + 1, deck)
        deck.append(child.val)
    return current


def make_my_deck():
    """
    returns a list of cards
    """
    cards = []
    for i in range(13):
        for _ in range(4):
            if i >= 10:
                cards.append(10)
            else:
                cards.append(i + 1)
    return cards


def main():
    """main function"""
    carte_croupier = input("Entrer la carte du croupier : ")
    while not carte_croupier.isdigit() or int(carte_croupier) not in range(1, 11):
        carte_croupier = input("Entrée incorrecte : ")
    timestamp = time.time()
    mydeck = make_my_deck()
    mydeck.remove(int(carte_croupier))
    mytree = create_game_tree(Tree(0, 0), 0, mydeck)
    mytree.survival_meth()
    print(time.time() - timestamp)
    while True:
        next_card = input("Entrer la carte recue : ")
        while not next_card.isdigit() or int(next_card) not in range(1, 11):
            next_card = input("Entrée incorrecte : ")
        mytree = mytree.navigate(int(next_card))  # not sure how it worked before
        mytree = mytree.navigate(int(next_card))  # not sure how it worked before
        print(
            [child.val for child in mytree.children],
            mytree.virtualchildrenscount,
            " virtual childs",
        )
        if mytree.shouldtake(0.45):
            print(mytree.total)
            print("Je prends")
            print(mytree.survival)
        else:
            print(mytree.total)
            print("Je ne prends pas")
            print(mytree.survival)


def automate(card_string: str, safeness: float) -> tuple:
    """
    take a list of cards as argument and return true if the player should take a card
    """
    card_string = card_string.split(",")
    logging.debug("card_tab: %s", card_string)
    mytree = create_game_tree(Tree(0, 0), 0, make_my_deck())
    mytree.survival_meth()
    for card in card_string:
        mytree = mytree.navigate(card)
    return mytree.shouldtake(safeness), mytree.survival


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "game":
        main()
    elif len(sys.argv) > 1:
        automate(sys.argv[1].split(","), float(sys.argv[2]))
        logging.debug("sys.argv[1]: %s", sys.argv[1])
    else:
        automate([10], 0.5)

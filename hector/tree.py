import time
import logging
import sys

# SAFENESS represents the minimum survival rate of a node's children to be considered a good node
# the rate is calculated by dividing the number of children
#  with a value < 21 by the total number of children


class Tree:
    """
    Tree class
    A tree is a node with a value and a list of children
    attributes:
        val: the value of the node
        children: the list of children
        total: the total value of the node and all its parents
        virtualchildrenscount: the number of children with a value > 21 (for the survival rate)
        survival: the survival rate of the node
        root: the root of the tree
    """

    def __init__(self, value: int, total: int, children=None, root=None):
        self.val = value
        self.children = children or []
        self.total = self.val + total
        self.virtualchildrenscount = 0
        self.survival = -1
        self.root = root or self
        self.weight = 1

    def survival_meth(self):
        """calculates the survival rate of the while tree recursively"""
        try:
            total_weight = sum(
                child.weight for child in self.children if child.total <= 21
            )
            self.survival = total_weight / (total_weight + self.virtualchildrenscount)
        except ZeroDivisionError:
            self.survival = 0
        for child in self.children:
            child.survival_meth()

    def navigate(self, next_node: int):
        """navigate to the next node
            input:
                next_node: the value of the next node
            output:
                the next node if it exists, -1 otherwise
        """
        try:
            for child in self.children:
                if child.val == int(next_node):
                    return child
        except (IndexError, ValueError):
            logging.warning(
                f"Invalid child value {next_node}, childs are %s",
                [child.val for child in self.children],
            )
            # quit the program if the child does not exist (this should theoretically never happen)
            sys.exit(-1)
        return -1

    def shouldtake(self, safeness: float):
        """returns True if the node is a good node (survival rate > safeness)"""
        if self.children == []:
            return False
        return self.survival > safeness


def create_game_tree(current: Tree, depth: int, deck: list):
    """
    create_game_tree creates recursively a tree with each node being a card.
    inputs:
        current: the current node
        depth: the depth of the current node
        deck: the deck of cards
    output:
        the root of the tree
    """
    maxdepth = 8
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
            logging.error(
                "card %s already removed (this should never happen)", child.val
            )
        create_game_tree(child, depth + 1, deck)
        deck.append(child.val)
    return current


def make_my_deck() -> list[int]:
    """returns a list of 52 cards"""
    cards = []
    for i in range(13):
        for _ in range(5):
            if i >= 10:
                cards.append(10)
            else:
                cards.append(i + 1)
    return cards


def main():
    """
    main function
    asks for the croupier's card and then asks for the player's cards, used for interactive mode
    (deprecated)
    """
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
        mytree = mytree.navigate(int(next_card))
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


if __name__ == "__main__":
    main()

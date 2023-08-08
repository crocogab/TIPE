import time
import sys
import logging
# TODO: Only generate the tree after the first two cards are drawn
# TODO: check if lost before navigating

#SAFENESS = 0.5
# SAFENESS represents the minimum survival rate of a node's children to be considered a good node
# the rate is calculated by dividing the number of children
#  with a value < 21 by the total number of children

class Tree:
    """
    A tree is a node with a value and a list of children
    """

    def __init__(self, value: int, total: int, children=None):
        self.val = value
        self.children = children or []
        self.total = self.val + total
        self.virtualchildrenscount = 0
        self.survival = 0
        # virtual childrens are childrens that represents losing hands
        # ( needed to calculate the survival rate but  faster to count instead of creating)

    def survival_meth(self):
        """calculates the survival rate of a node"""
        try:
            self.survival = len(
                [child for child in self.children if child.total <= 21]
            ) / (len(self.children) + self.virtualchildrenscount)
        except ZeroDivisionError:
            self.survival = 0
        for child in self.children:
            child.survival_meth()

    def is_empty(self):
        """returns True if the node is empty"""
        return self.val == -1

    def navigate(self, next_node: int):
        """returns the child with the value next if it exists, else returns an empty tree"""
        try:
            return [child for child in self.children if child.val == int(next_node)][0]
        except (IndexError,ValueError):
            logging.warning(f"Invalid child value {next_node}, childs are %s", \
                            [child.val for child in self.children])
            return Tree(-1, -1)

    def shouldtake(self,safeness:float):
        """returns True if the node is safe enough to be considered a good node"""
        if self.children == []:
            return False
        return self.survival > safeness


def create_game_tree(current: Tree, depth: int):
    """creates a game tree with a maximum depth of 6"""
    cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    maxdepth = 6
    if depth == maxdepth:
        return current
    for card in cards:
        if current.total + card <= 21:
            current.children.append(Tree(card, current.total))
            # here, we pass current.total as the constructor handle the card's value
        else:
            current.virtualchildrenscount += 1
    for child in current.children:
        create_game_tree(child, depth + 1)
    return current


def main():
    """main function"""
    timestamp = time.time()
    mytree = create_game_tree(Tree(0,0), 0)
    mytree.survival_meth()
    print(time.time() - timestamp)
    while True:
        next_card = input("Entrer la carte recue : ")
        while not next_card.isdigit() or int(next_card) not in range(1, 11):
            next_card = input("Entrée incorrecte : ")
        mytree = mytree.navigate(int(next_card)) # not sure how it worked before
        print(
            [child.val for child in mytree.children],
            mytree.virtualchildrenscount,
            " virtual childs",
        )
        if mytree.shouldtake():
            print(mytree.total)
            print("Je prends")
            print(mytree.survival)
        else:
            print(mytree.total)
            print("Je ne prends pas")
            print(mytree.survival)

def automate(card_string:str,safeness:float) -> tuple:
    """
    take a list of cards as argument and return true if the player should take a card
    """
    card_string = card_string.split(",")
    logging.debug("card_tab: %s",card_string)
    mytree = create_game_tree(Tree(0,0), 0)
    mytree.survival_meth()
    for card in card_string:
        mytree = mytree.navigate(card)
    return mytree.shouldtake(safeness),mytree.survival



if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "game":
        main()
    elif len(sys.argv) > 1:
        automate(sys.argv[1].split(","),float(sys.argv[2]))
        logging.debug("sys.argv[1]: %s",sys.argv[1])
    else:
        automate([10],0.5)

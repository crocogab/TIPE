import time

SAFENESS = 0.5
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
                [child for child in self.children if child.total < 21]
            ) / (len(self.children) + self.virtualchildrenscount)
        except ZeroDivisionError:
            self.survival = 0
        for child in self.children:
            child.survival_meth()

    def is_empty(self):
        """returns True if the node is empty"""
        return self.val == -1

    def navigate(self, next: int):
        """returns the child with the value next if it exists, else returns an empty tree"""
        try:
            return [child for child in self.children if child.val == next][0]
        except IndexError:
            return Tree(-1, 0)

    def shouldtake(self):
        """returns True if the node is safe enough to be considered a good node"""
        if self.children == []:
            return False
        return self.survival > SAFENESS


def create_game_tree(current: Tree, depth: int):
    """creates a game tree with a maximum depth of 6"""
    cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    maxdepth = 6
    if depth == maxdepth:
        return current
    else:
        for card in cards:
            if current.total + card < 21:
                current.children.append(Tree(card, current.total))
            else:
                current.virtualchildrenscount += 1
    for child in current.children:
        create_game_tree(child, depth + 1)
    return current

    # MAINTREE est un arbre vide, il sera rempli par game_tree


MAINTREE = Tree(-1, 0)


def main():
    timestamp = time.time()
    mytree = create_game_tree(MAINTREE, 0)
    mytree.survival_meth()
    print(time.time() - timestamp)
    while True:
        next = input("Entrer la carte recue : ")
        while not next.isdigit() or int(next) not in range(1, 11):
            next = input("Entrée incorrecte : ")
        mytree = mytree.navigate(int(next))
        print(
            [child.val for child in mytree.children],
            mytree.virtualchildrenscount,
            " virtual childs",
        )
        if mytree.shouldtake():
            print("Je prends")
            print(mytree.survival)
        else:
            print("Je ne prends pas")
            print(mytree.survival)


if __name__ == "__main__":
    main()

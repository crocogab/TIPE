import time

SAFENESS = 0.5
# SAFENESS represents the minimum survival rate of a node's children to be considered a good node
# the rate is calculated by dividing the number of children with a value < 21 by the total number of children


class Tree():
    def __init__(self, value: int, total: int, children=None):
        self.val = value
        self.children = children or []
        self.total = self.val + total
        # self.parent = None            parents should not be needed
        # for child in self.children:
        #     child.parent = self

    def survival_meth(self):
        try:
            self.survival = len(
                [child for child in self.children if child.total < 21]) / len(self.children)  # there is a bug here. Children val will always be less than 21
        except ZeroDivisionError:
            self.survival = 0
        for child in self.children:
            child.survival_meth()

    def is_empty(self):
        return self.val == -1

    def navigate(self, next: int):
        """renvoie le noeud enfant correspondant à next, ou l'arbre vide si il n'existe pas (défaite)"""
        try:
            return [child for child in self.children if child.val == next][0]
        except IndexError:
            return Tree(-1)

    def shouldtake(self):
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
            current.children.append(Tree(card, current.total))
            # si la main dépasse 21, on n'a pas besoin de créer les enfants car ils sont tous perdants
    for child in current.children:
        create_game_tree(child, depth + 1)
    return current


    # MAINTREE est un arbre vide, il sera rempli par game_tree
MAINTREE = Tree(-1, 0)


def main():
    global MAINTREE
    timestamp = time.time()
    mytree = create_game_tree(MAINTREE, 0)
    mytree.survival_meth()
    print(time.time() - timestamp)
    while True:
        next = input("Entrer la carte recue : ")
        while not next.isdigit() or int(next) not in range(1, 11):
            next = input("Entrée incorrecte : ")
        mytree = mytree.navigate(int(next))
        print([child.val for child in mytree.children])
        if mytree.shouldtake():
            print("Je prends")
            print(mytree.survival)
        else:
            print("Je ne prends pas")
            print(mytree.survival)


main()

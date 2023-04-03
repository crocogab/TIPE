SAFENESS = 0.5
# SAFENESS represents the minimum survival rate of a node's children to be considered a good node


class Tree():
    def __init__(self, value: int, children=None):
        self.val = value
        self.children = children or []
        self.parent = None
        for child in self.children:
            child.parent = self
        try:
            self.survival = len(
                [child for child in self.children if child.val < 21]) / len(self.children)
        except ZeroDivisionError:
            self.survival = 0

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


def list_to_tree(l: list):
    """transforme une liste de liste en arbre
    [0[1[2]][2][3][4][5][6]] cette liste renverra
    Tree(0, [Tree(1, [Tree(2)]), Tree(2), Tree(3), Tree(4), Tree(5), Tree(6)])"""
    if len(l) == 0:
        return Tree(-1)
    if len(l) == 1:
        return Tree(l[0])
    return Tree(l[0], [list_to_tree(l[1:])])


MAINTREE = Tree(-1)


def main():
    next = input("Enteer la carte recue : ")
    MAINTREE.navigate(int(next))
    print("Voici ce que vous devez faire :", +
          "prendre" if MAINTREE.shouldtake()else "ne pas prendre")


main()

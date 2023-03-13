class Tree():
    def __init__(self, cardslist: list, value: int, parent, childrens: list, winprobability: int):
        self.cards_list = cardslist
        self.value = value
        self.parent = parent
        self.total = sum(cardslist)
        self.children = childrens
        self.winprobability = winprobability


tree = Tree([], 0, None, [], 0.5)

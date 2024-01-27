#TODO: refactor this file
from valuetweak import automate, tree_dict
from tkinter import Tk, Label
import math

elts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
SAFENESS = 0.412


def glouton(elts, target):
    """
        returns a string of the elements of elts that sum to target
        inputs:
            elts: list, the list of elements to use
            target: int, the target sum
        outputs:
            res: str, the string of the elements that sum to target
    """
    res = ""
    ind = len(elts) - 1
    while target > 0:
        if target < elts[ind]:
            ind -= 1
        else:
            target -= elts[ind]
            res += str(elts[ind]) + ","
    return res

def fix_list(l):
    for i in range(len(l)):
        l[i] = l[i][:-1]
    return l


def get_all_strings():
    res = []
    for i in range(1, 21):
        res.append(glouton(elts, i))
    return res


def str_sum(string):
    res = 0
    for elt in string.split(","):
        res += int(elt)
    return res


def get_all_choices(elts):
    trees = tree_dict()
    res = {}
    for i in range(1, 11):
        safeness_table = [
            0.3125,
            0.6875,
            0.75,
            0.9375,
            0.75,
            0.6875,
            0.375,
            0.375,
            0.375,
            0.4375,
        ]
        SAFENESS = safeness_table[i - 1]
        for elt in elts:
            res[i, str_sum(elt)] = automate(elt, SAFENESS, trees[i])[0]
    return res


get_all_choices(fix_list(get_all_strings()))

# display the results in a table (with tkinter)
# rows are the player's hand sum
# columns are the croupier's first card #green if the player should take a card, red otherwise
choices = get_all_choices(fix_list(get_all_strings()))
window = Tk()
tableau = []
for i in range(20):
    ligne = []
    for j in range(11):
        if j > 0 and j <= 10 and i == 0:
            case = Label(
                window, text=j, borderwidth=1, relief="solid", width=8, height=3
            )
        elif j == 0 and i > 0:
            case = Label(
                window, text=21 - i, borderwidth=1, relief="solid", width=8, height=3
            )
        else:
            case = Label(
                window, text=" ", borderwidth=1, relief="solid", width=8, height=3
            )
        case.grid(row=i, column=j)
        ligne.append(case)
    tableau.append(ligne)

for i in range(1, 11):
    for j in range(1, 20):
        if choices[i, 21 - j]:
            tableau[j][i].configure(bg="green")
        else:
            tableau[j][i].configure(bg="red")
window.mainloop()

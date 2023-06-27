import random
import numpy as np
import string

import matplotlib.pyplot as plt


PRECISION = 10
FAV_REUSSITE = 3.5
PUNITION = 3.5


# main1=Main((7,10,0,0,0,0,0,11))
# print(main1)


class Individu():
    def __init__(self) -> None:
        # 10 premiers = n'a pas d' as  ou as = valeur # 11 à fin = as
        self.chromosomes = [0 for _ in range(20)]

    def __str__(self) -> str:
        return f"""        ---------------------------[ Croupier {self.chromosomes[19]}]--------------------------------- \n 
        Sans as : [2-11]| [12]| [13]| [14]| [15]| [16]| [17]| [18]| [19]| [20]\n 
                  [{self.chromosomes[0]}]   | [{self.chromosomes[1]}] | [{self.chromosomes[2]}] | [{self.chromosomes[3]}] | [{self.chromosomes[4]}] | [{self.chromosomes[5]}] | [{self.chromosomes[6]}] | [{self.chromosomes[7]}] | [{self.chromosomes[8]}] | [{self.chromosomes[9]}]\n
        ---------------------------------------------------------------------- 
        \n        Avec as : [10]| [11]| [12]| [13]| [14]| [15]| [16]| [17]| [18-20]
        \n                  [{self.chromosomes[10]}] | [{self.chromosomes[11]}] | [{self.chromosomes[12]}] | [{self.chromosomes[13]}] | [{self.chromosomes[14]}] | [{self.chromosomes[15]}] | [{self.chromosomes[16]}] | [{self.chromosomes[17]}] | [{self.chromosomes[18]}]
        \n        ----------------------------------------------------------------------"""

        # return f'Sans as = {self.chromosomes[:10]} | Avec as : {self.chromosomes[10:18]} | Courtier : {self.chromosomes[18]}'

    def random_init(self):
        for i in range(19):
            self.chromosomes[i] = random.randint(0, 1)

    def survival_rate(self, possede_as, valeur):
        points = 0
        if not possede_as:

            for _ in range(PRECISION):
                total = valeur + np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13]))
                total_croupier = self.chromosomes[18] + np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13]))
                if total > 21:
                    points -= (total-21)*PUNITION
                    if total_croupier > 21:
                        points += (total_croupier-21)
                    else:
                        if total_croupier > valeur:
                            points += (21-total_croupier)
                        else:
                            points -= (valeur-total_croupier)
                else:
                    if total_croupier < 21 and total_croupier > valeur:  # valorisation car choix risque mais necessaire
                        points += (21-total)*FAV_REUSSITE
                    else:
                        points += (21-total)

        else:
            for _ in range(PRECISION):
                total = valeur + np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13]))
                total_croupier = self.chromosomes[18] + np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13]))
                if total > 21:
                    total -= 9
                if valeur > total_croupier:
                    if total > total_croupier:
                        points += (total-total_croupier)
                    else:
                        points -= (total_croupier-total)*PUNITION
                else:
                    if total > total_croupier:
                        points += (total-total_croupier)*FAV_REUSSITE
                    else:
                        points -= (total_croupier-total)

        return points/PRECISION

    def fitness(self):
        fitness_c = 0
        for i in range(20):
            if self.chromosomes[i] == 1:
                if i == 0:
                    avg = (sum([self.survival_rate(False, c)
                           for c in range(2, 12)]))/11
                    fitness_c += avg

                elif i < 10:

                    fitness_c += self.survival_rate(False, i+11)

                elif i < 18:
                    fitness_c += self.survival_rate(True, i)
                else:
                    avg = (sum([self.survival_rate(True, c)
                           for c in range(18, 20)]))/3
                    fitness_c += avg
        # print('[DEBUG] :',fitness_c)
        return (fitness_c)/20


def croisement(i1: Individu, i2: Individu):
    """Croisement de deux individus -> découpe en 2 sous-chaines pour l'instant"""
    i3 = Individu()
    i4 = Individu()
    index1 = random.randint(0, 17)
    index2 = random.randint(0, 17)
    i3.chromosomes = i1.chromosomes[:index1] + i2.chromosomes[index1:]
    i4.chromosomes = i2.chromosomes[:index2] + i1.chromosomes[index2:]
    return i3, i4


def mutation(i1: Individu):
    """Mutation d'un individu -> 1 bit aléatoire"""
    index = random.randint(0, 17)
    i1_p = i1
    i1_p.chromosomes[index] = 1-i1.chromosomes[index]
    return i1_p


i1 = Individu()
i1.chromosomes[10] = 1
i1.chromosomes[18] = 1

# print(i1)
# print(i1.chromosomes[10])


# print(i1.fitness(False,13))
# print(i1.fitness2())
# def fitness(adn):

moyenne1 = 0
moyenne2 = 0
moyenne3 = 0

i1.chromosomes[0] = 1


for i in range(18):
    i1.chromosomes[i] = 1

# for i in range(100):
#     moyenne1 += i1.fitness()


i1.chromosomes[10] = 0
i1.chromosomes[19] = 2
i1.chromosomes[9] = 0
i1.chromosomes[8] = 0

# for i in range(100):
#     moyenne2 += i1.fitness()

i1.chromosomes[17] = 0
i1.chromosomes[16] = 0

i1.chromosomes[15] = 0

#  print(i1)

# print(i1.survival_rate(False, 12))
# for i in range(100):
#     moyenne3 += i1.fitness()

# i1.show()
# print(
#     f'[COMPARAISON] moyenne_1: {moyenne1/100} | moyenne_2: {moyenne2/100} | moyenne_3: {moyenne3/100}')


# print(i1)
# print(f'score i1 : {i1.fitness()}')
# i2 = Individu()
# i2.chromosomes[18] = 2
# i2.random_init()
# print(i2)
# print(f'score i2 : {i2.fitness()}')

# i3, i4 = croisement(i1, i2)
# print(i3)
# print(f'score i3 : {i3.fitness()}')
# print(i4)
# print(f'score i3 : {i3.fitness()}')
# print(i1)


def generation():
    list_individus = []

    for _ in range(10):
        i1 = Individu()
        i1.chromosomes[19] = 7
        i1.random_init()
        list_individus.append(i1)

    fitness_list = [(list_individus[i].fitness(), i) for i in range(10)]
    fitness_list.sort()

    list_conserve = fitness_list[5:]
    print(list_conserve)

    def new_generation(liste):

        mut = mutation(list_individus[liste[0][1]])
        if mut.fitness() > list_individus[liste[0][1]].fitness():
            list_individus[liste[0][1]] = mut
        coupl_crois = croisement(
            list_individus[liste[3][1]], list_individus[liste[4][1]])
        if coupl_crois[0].fitness() > list_individus[liste[3][1]].fitness():
            list_individus[liste[3][1]] = coupl_crois[0]
        if coupl_crois[1].fitness() > list_individus[liste[4][1]].fitness():
            list_individus[liste[4][1]] = coupl_crois[1]
        for i in range(10):
            if i not in [liste[0][1], liste[1][1], liste[2][1], liste[3][1], liste[4][1]]:
                list_individus[i].random_init()
        fitness_list = [(list_individus[i].fitness(), i) for i in range(10)]
        fitness_list.sort()
        return fitness_list[5:]

    for _ in range(100):
        list_conserve = new_generation(list_conserve)
        print(list_conserve)

    for elem in list_conserve:
        print(list_individus[elem[1]])


# ce qu'il faut faire -> ameliorer generation (plus d'indivius et plus de generations)
# avoir un meilleur rendu pour l'affichage
generation()

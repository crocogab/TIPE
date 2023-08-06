import random
import numpy as np

PRECISION = 10


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

    def survival_rate(self, possede_as: bool, valeur: int, tire: bool):
        points = 0

        if not possede_as:
            for _ in range(PRECISION):
                total = valeur + np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13]))
                total_croupier = self.chromosomes[19] + np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13]))
                if total <= 21:
                    if tire:
                        # jusqu'à 22 car on doit recevoir des points meme si on fait 21
                        points += (22-total)/PRECISION
                    else:
                        points -= (22-total)/PRECISION
                else:
                    if not tire:
                        points += (total-21)/PRECISION
                        if total_croupier <= 21 and total_croupier > valeur:
                            points -= (22-total_croupier)/PRECISION
                        else:
                            if total_croupier < valeur:
                                points += (valeur-total_croupier)/PRECISION

                    else:
                        points -= (total-21)/PRECISION
                        if total_croupier <= 21 and total_croupier > valeur:
                            points += (22-total_croupier)/PRECISION
                        else:
                            if total_croupier < valeur:
                                points -= (valeur-total_croupier)/PRECISION
        else:  # peut juste etre cette partie à améliorer
            for _ in range(PRECISION):

                total = valeur + np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13]))
                total_croupier = self.chromosomes[19] + np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13]))

                if total <= 21:
                    if tire:
                        points += (22-total)/PRECISION
                    else:
                        points -= (22-total)/PRECISION
                elif valeur > total_croupier:
                    if not tire:
                        points += (valeur-total_croupier)/PRECISION
                    elif total <= 21 and tire:
                        points += (22-total)/PRECISION
                    else:
                        points -= (22-total)/PRECISION
                elif valeur < total_croupier:
                    if not tire:
                        points -= (total_croupier-valeur)/PRECISION
                    elif total <= 21:
                        points += (22-total)/PRECISION
                    elif total-10 >= total_croupier:
                        points += (22-total)/PRECISION
                    else:
                        points -= (22-total)/PRECISION

        return points

    def fitness(self):
        fitness_c = 0
        for i in range(19):

            if i == 0:
                if self.chromosomes[i] == 1:
                    avg = (sum([self.survival_rate(False, c, True)
                           for c in range(2, 12)]))/11
                    fitness_c += avg
                else:
                    avg = (sum([self.survival_rate(False, c, False)
                           for c in range(2, 12)]))/11
                    fitness_c += avg

            elif i < 10:
                if self.chromosomes[i] == 1:
                    fitness_c += self.survival_rate(False, i+11, True)
                else:
                    fitness_c += self.survival_rate(False, i+11, False)

            elif i < 18:
                if self.chromosomes[i] == 1:
                    fitness_c += self.survival_rate(True, i, True)
                else:
                    fitness_c += self.survival_rate(True, i, False)

            else:
                if self.chromosomes[i] == 1:
                    avg = (sum([self.survival_rate(True, c, True)
                           for c in range(18, 20)]))/3
                    fitness_c += avg
                else:
                    avg = (sum([self.survival_rate(True, c, False)
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


def generation(list_individus, nb_individus, iterations_demande):
    """ nb d'invidus doit être pair"""
    if iterations_demande == 0:
        for elem in list_individus:
            print(f'fitness : {elem.fitness()}\n{elem}\n')

    else:

        fitness_list = [(list_individus[i].fitness(), i)
                        for i in range(nb_individus)]
        fitness_list.sort()
        print(fitness_list)

        list_conserv = []

        # garde la moitié des meilleurs individus
        for i in range(nb_individus//2):
            if fitness_list[i][0] > fitness_list[i+nb_individus//2][0]:
                list_conserv.append(
                    list_individus[fitness_list[i][1]])

            else:
                list_conserv.append(
                    list_individus[fitness_list[i+nb_individus//2][1]])

        for i in range(nb_individus//4):
            i1, i2 = croisement(
                list_conserv[i], list_conserv[i+1])
            list_conserv.append(i1)
            list_conserv.append(i2)

        for i in range(nb_individus//2):
            list_conserv.append(mutation(list_conserv[i]))
        list_conserv.sort(key=lambda x: x.fitness(), reverse=True)

        generation(list_conserv[:len(list_individus) -
                                len(list_conserv)], nb_individus, iterations_demande-1)


list_individus = []

for _ in range(20):
    i1 = Individu()
    i1.chromosomes[19] = 6
    i1.random_init()
    list_individus.append(i1)

generation(list_individus, 20, 60)


# ce qu'il faut faire -> ameliorer generation / fonction fitness pour avoir meilleurs resultats

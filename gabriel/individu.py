import random
import numpy as np

PRECISION = 10
FAV_REUSSITE = 1.3


class Main():
    def __init__(self, cards) -> None:
        self.cards = cards
        self.possede_as = 11 in self.cards[:7]
        self.total = sum(cards[:7])

    def __str__(self) -> str:
        return f'Cartes = {self.cards} | As ? ={self.possede_as} | Total ={self.total}'


# main1=Main((7,10,0,0,0,0,0,11))
# print(main1)


class Individu():
    def __init__(self) -> None:
        # 10 premiers = n'a pas d' as  ou as = valeur # 11 à fin = as
        self.chromosomes = [0 for _ in range(19)]

    def __str__(self) -> str:
        return f'Sans as = {self.chromosomes[:10]} | Avec as : {self.chromosomes[10:18]} | Courtier : {self.chromosomes[19]}'

    # pour chaque situation tire 10 * une carte et compare le resultat en moyenne au resultat mis -> evalue la difference
    def survival_rate(self, possede_as: bool, valeur: int):
        """ renvoie un taux entre 0 et 1 avec 1= best / max et 0 le pire + si il a depasse """
        taux = 0
        if possede_as:
            for _ in range(PRECISION):
                total = valeur + np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13]))  # valeur + carte aléatoire (pondérée comme dans le jeu)
                if total > 21:
                    taux -= (total-21)
                else:
                    taux += (21-total)*FAV_REUSSITE

            # return (1, taux > (PRECISION/1.5)
            print(f"[DEBUG TAUX] : {taux/PRECISION} valeur : {valeur}")
            return (taux/PRECISION)
        else:
            for _ in range(PRECISION):
                total = valeur + np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13]))
                if total > 21:
                    taux -= (total-21)
                else:
                    taux += (21-total)*FAV_REUSSITE
            print('[DEBUG ACTU]', taux/PRECISION)
            return (taux/PRECISION)

    def fitness(self, possede_as, valeur):
        surv = self.survival_rate(possede_as, valeur)

        return surv/2.1

    def fitness2(self):
        fitness_c = 0
        for i in range(19):
            if self.chromosomes[i] == 1:
                if i == 0:
                    avg = (sum([self.fitness(False, c)
                           for c in range(2, 12)]))/10
                    fitness_c += avg

                elif i < 10:

                    fitness_c += self.fitness(False, i+11)
                elif i == 10:
                    fitness_c += self.fitness(False, 20)
                elif i < 17:
                    fitness_c += self.fitness(True, i)
                else:
                    avg = (sum([self.fitness(True, c)
                           for c in range(18, 21)]))/3
                    fitness_c += avg
        #print('[DEBUG] :',fitness_c)
        return (fitness_c)/19


i1 = Individu()
i1.chromosomes[10] = 1


# print(i1)
# print(i1.chromosomes[10])


# print(i1.fitness(False,13))
# print(i1.fitness2())
# def fitness(adn):

moyenne1 = 0
moyenne2 = 0
moyenne3 = 0

i1.chromosomes[0] = 1
i1.chromosomes[18] = 1


for i in range(18):
    i1.chromosomes[i] = 1

for i in range(100):
    moyenne1 += i1.fitness2()


i1.chromosomes[10] = 0
i1.chromosomes[18] = 10
i1.chromosomes[9] = 0
i1.chromosomes[8] = 0

for i in range(100):
    moyenne2 += i1.fitness2()

i1.chromosomes[17] = 0
i1.chromosomes[16] = 0

i1.chromosomes[15] = 0


for i in range(100):
    moyenne3 += i1.fitness2()


print(
    f'[COMPARAISON] moyenne_1: {moyenne1/100} | moyenne_2: {moyenne2/100} | moyenne_3: {moyenne3/100}')

# Probleme dans survival rate je pense

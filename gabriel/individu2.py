import random
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt



PRECISION = 10
FAV_REUSSITE = 1.5
PUNITION=1.2


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
        return f'Sans as = {self.chromosomes[:10]} | Avec as : {self.chromosomes[10:18]} | Courtier : {self.chromosomes[18]}'

    def survival_rate(self,possede_as,valeur):
        points=0
        if not possede_as:
            
            for _ in range(PRECISION):
                total= valeur + np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13])) 
                total_croupier= self.chromosomes[18] + np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13])) 
                if total>21:
                    points-=(total-21)*PUNITION
                    if total_croupier>21:
                        points+=(total_croupier-21)
                    else:
                        if total_croupier>valeur:
                            points+=(21-total_croupier)
                        else:
                            points-=(valeur-total_croupier)
                else:
                    if total_croupier<21 and total_croupier>valeur :#valorisation car choix risque mais necessaire
                        points+=(21-total)*FAV_REUSSITE
                    else:
                        points+=(21-total)
        
        else:
            for _ in range(PRECISION):
                total= valeur + np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13])) 
                total_croupier= self.chromosomes[18] + np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13])) 
                if total>21:
                    total-=9
                if valeur>total_croupier:
                    if total>total_croupier:
                        points+=(total-total_croupier)
                    else:
                        points-=(total_croupier-total)*PUNITION
                else:
                    if total>total_croupier:
                        points+=(total-total_croupier)*FAV_REUSSITE
                    else:
                        points-=(total_croupier-total)
                
        return points/PRECISION
    

    def fitness(self):
        fitness_c = 0
        for i in range(19):
            if self.chromosomes[i] == 1:
                if i == 0:
                    avg = (sum([self.survival_rate(False, c)
                           for c in range(2, 12)]))/10
                    fitness_c += avg

                elif i < 10:

                    fitness_c += self.survival_rate(False, i+11)
                elif i == 10:
                    fitness_c += self.survival_rate(False, 20)
                elif i < 17:
                    fitness_c += self.survival_rate(True, i)
                else:
                    avg = (sum([self.survival_rate(True, c)
                           for c in range(18, 21)]))/3
                    fitness_c += avg
        #print('[DEBUG] :',fitness_c)
        return (fitness_c)/19
    

                    


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



# for i in range(18):
#     i1.chromosomes[i] = 1

# for i in range(100):
#     moyenne1 += i1.fitness()


# i1.chromosomes[10] = 0
# i1.chromosomes[18] = 2
# i1.chromosomes[9] = 0
# i1.chromosomes[8] = 0

# for i in range(100):
#     moyenne2 += i1.fitness()

# i1.chromosomes[17] = 0
# i1.chromosomes[16] = 0

# i1.chromosomes[15] = 0

#  print(i1)

#  print(i1.survival_rate(False,12))
# for i in range(100):
#     moyenne3 += i1.fitness()

i1.show()
# print(
#     f'[COMPARAISON] moyenne_1: {moyenne1/100} | moyenne_2: {moyenne2/100} | moyenne_3: {moyenne3/100}')

# Probleme dans survival rate je pense

import random
import numpy as np
import matplotlib.pyplot as plt

PRECISION = 100
NB_ITERATIONS=50

class Individu():
    def __init__(self) -> None:
        # 10 premiers = n'a pas d' as  ou as = valeur # 11 à fin = as (cf affichage)
        self.chromosomes = [0 for _ in range(20)]

    def __str__(self) -> str:
        """Affichage un peu esthétique"""

        return f"""        ---------------------------[ Croupier {self.chromosomes[19]}]--------------------------------- \n
        Sans as : [2-11]| [12]| [13]| [14]| [15]| [16]| [17]| [18]| [19]| [20]\n
                  [{self.chromosomes[0]}]   | [{self.chromosomes[1]}] | [{self.chromosomes[2]}] | [{self.chromosomes[3]}] | [{self.chromosomes[4]}] | [{self.chromosomes[5]}] | [{self.chromosomes[6]}] | [{self.chromosomes[7]}] | [{self.chromosomes[8]}] | [{self.chromosomes[9]}]\n
        ----------------------------------------------------------------------
        \n        Avec as : [10]| [11]| [12]| [13]| [14]| [15]| [16]| [17]| [18-20]
        \n                  [{self.chromosomes[10]}] | [{self.chromosomes[11]}] | [{self.chromosomes[12]}] | [{self.chromosomes[13]}] | [{self.chromosomes[14]}] | [{self.chromosomes[15]}] | [{self.chromosomes[16]}] | [{self.chromosomes[17]}] | [{self.chromosomes[18]}]
        \n        ----------------------------------------------------------------------"""



    def random_init(self):
        for i in range(19):
            self.chromosomes[i] = random.randint(0, 1)

    def convert(self,valeur:int,h_as:bool):
        """ Renvoie l'indice du chromosome associé à une valeur"""
        if h_as:
            if valeur >=10 and valeur<18:
                return valeur
            else:
                return 18
        else:
            if valeur>=2 and valeur<12:
                return 0
            else:
                return valeur-11
    
    def calculate_val(self,tab:list):
        total=0
        for card in tab:
            if card==1:
                total+=10
            else:
                total+=card
        return total
    
    def play(self):
        """Joue un 1v1 contre le croupier en fonction de ses chromosomes et voit si il gagne"""

        winner=False
        is_playing=True
        player_list=[np.random.choice(np.arange(1, 11), p=( #renvoie une valeur de 1/10 pondérée
                    [1/13 for _ in range(9)]+[4/13]))]
        croupier_list=[np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13]))]
        
        self.chromosomes[19]=croupier_list[0] #initialisation du chromosome associé au croupier
        
        p_val=self.calculate_val(player_list)
        c_val=self.calculate_val(croupier_list)

        #print(f"Player list: {player_list}, Player value: {p_val}")
        #print(f"Croupier list: {croupier_list}, Croupier value: {c_val}")
        while is_playing:
            
            
            if self.chromosomes[self.convert(p_val, (1 in player_list))] == 1 or ((self.chromosomes[19]-p_val)>6.5): # prends en compte la main du croupier
                player_list.append(np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13])))
            else:
                is_playing = False

            if c_val<16:
                croupier_list.append(np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13])))
            
            p_val = self.calculate_val(player_list)
            c_val = self.calculate_val(croupier_list)
            
            if p_val>21:
                is_playing  = False
            
            if c_val>21:
                is_playing  = False
                
                if p_val<=21:
                    winner=True
            #print(f"Player list: {player_list}, Player value: {p_val}")
            #print(f"Croupier list: {croupier_list}, Croupier value: {c_val}")
        
        if p_val<=21 and c_val<=21:
            if p_val>=c_val:
                winner=True

        return winner
    
    def evaluate(self):
        """evalue le chromosome et retourne une valeur numerique"""
        count=0
        for _ in range(PRECISION):
            if self.play():
                count+=1
        return count/PRECISION
    

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


test_graph_x=[]
test_graph_y=[]

def generation(list_individus: list, nb_individus: int, nb_generations: int,croupier_hand:int):
    """nb individus multiple de 8 et plus grand que 16"""
    assert nb_individus % 8 == 0 and nb_individus > 16 , "nombre de individus doit etre un multiple de 8 et plus grand que 16"

    if nb_generations==0:
        list_individus.sort(key=lambda x: x.evaluate())
        for individu in list_individus:
            print(f'evaluate : {individu.evaluate()}\n{individu}\n') #plus forcement le meme evaluate qu'avant (random) donc le meme sens
        
    else:
        list_conserv=[]
        list_individus.sort(key=lambda x: x.evaluate()) #trie la liste 1er = plus nul -> dernier = meilleur
        for i in range(nb_individus//2):
        
            list_individus.pop(0)
        
        for i in range(nb_individus//8):
            list_conserv.append(mutation(list_individus.pop(0)))
        
        for i in range(nb_individus//8):
            list_conserv.append(list_individus.pop(0))
        
        
        
        for i in range(nb_individus//8):
            i1,i2=croisement(list_individus[i], list_individus[i+1])
            if i1.evaluate()>i2.evaluate():
                list_conserv.append(i1)
            else:
                list_conserv.append(i2)
            
            list_individus.pop(0)
            
        for i in range(nb_individus//2):
                i1 = Individu()
                i1.random_init()
                i1.chromosomes[19] = croupier_hand

                list_conserv.append(i1) 
        
        
        for i in range(nb_individus//8):
            list_conserv.append(list_individus[i])

        score=0
        for elem in list_conserv[nb_individus-4:]:
            score+=elem.evaluate()
            
        test_graph_x.append(NB_ITERATIONS-nb_generations)
        test_graph_y.append(score/4)
        
       
        
        
        
    
        print(f'Generations restantes : {nb_generations} | Meilleur score : {list_conserv[-1].evaluate()} \n')
        
        generation(list_conserv, nb_individus, nb_generations-1,croupier_hand)
            

        
        



    

# def generation(list_individus, nb_individus, iterations_demande):
#     """ nb d'invidus doit être pair"""
#     if iterations_demande == 0:
#         for elem in list_individus:
#             print(f'evaluate : {elem.evaluate()}\n{elem}\n')

#     else:

#         evaluate_list = [(list_individus[i].evaluate(), i)
#                         for i in range(nb_individus)]
#         evaluate_list.sort()
#         print(evaluate_list)

#         list_conserv = []

#         # garde la moitié des meilleurs individus
#         for i in range(nb_individus//2):
#             if evaluate_list[i][0] > evaluate_list[i+nb_individus//2][0]:
#                 list_conserv.append(
#                     list_individus[evaluate_list[i][1]])

#             else:
#                 list_conserv.append(
#                     list_individus[evaluate_list[i+nb_individus//2][1]])

#         for i in range(nb_individus//4):
#             i1, i2 = croisement(
#                 list_conserv[i], list_conserv[i+1])
#             list_conserv.append(i1)
#             list_conserv.append(i2)

#         for i in range(nb_individus//2):
#             list_conserv.append(mutation(list_conserv[i+(nb_individus//2)]))
#         list_conserv.sort(key=lambda x: x.evaluate(), reverse=True)

#         generation(list_conserv[:len(list_individus) -
#                                 len(list_conserv)], nb_individus, iterations_demande-1)

list_individus = []

for _ in range(32):
    i1 = Individu()
    i1.random_init()
    i1.chromosomes[19] = 6
    
    list_individus.append(i1)

generation(list_individus, 32, NB_ITERATIONS,6)

plt.plot(test_graph_x, test_graph_y)
plt.xlabel('iterations')
plt.ylabel('average_score best')
plt.show()
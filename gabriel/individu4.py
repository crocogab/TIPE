import random 
import numpy as np
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(100000) #pour éviter les erreurs de récursion


PRECISION = 40
NB_ITERATIONS=2000
NB_INDIVIDUS=32 #multiple de 32
MAIN_CROUPIER=6 #valeur de la main du croupier


test_graph_x=[]
test_graph_y=[]


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
                if total+10<=21:
                    total+=10
                else:
                    total+=1
            else:
                if 1 not in tab:
                    total+=card
                else:
                    if total+card>21:
                        total+=(card-9)
        return total
    
    def play(self):
        """Joue un 1v1 contre le croupier en fonction de ses chromosomes et voit si il gagne"""

        winner=False
        
        player_list=[np.random.choice(np.arange(1, 11), p=( #renvoie une valeur de 1/10 pondérée
                    [1/13 for _ in range(9)]+[4/13]))]
        croupier_list=[np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13]))]
        
         #initialisation du chromosome associé au croupier
        croupier_list.append(self.chromosomes[19])

        p_val=self.calculate_val(player_list)
        c_val=self.calculate_val(croupier_list)

        if self.convert(p_val,(1 in player_list))==1:
            player_list.append(np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13])))
        if c_val<17:
            croupier_list.append(np.random.choice(np.arange(1, 11), p=(
                    [1/13 for _ in range(9)]+[4/13])))
        
        p_val=self.calculate_val(player_list)
        c_val=self.calculate_val(croupier_list)

        if p_val==21:
            winner=True

        if p_val>=c_val and p_val<=21:
            winner=True
        
        if c_val>21 and p_val<=21:
            winner=True


        return winner

    def play2(self):
        score=0
        if self.chromosomes[0]==1:

            score+=1
         
        if self.chromosomes[10]==1:
            score+=1
        
        if self.chromosomes[11]==1:
            score+=1
        if self.chromosomes[12]==1:
            score+=1
        if self.chromosomes[13]==1:
            score+=1
        
        if self.chromosomes[14]==1:
            score+=1
        if self.chromosomes[15]==1:
            score+=1
        if self.chromosomes[16]==1:
            score+=1
        if self.chromosomes[17]==1:
            score+=1
        if self.chromosomes[18]==1:
            score-=1
        for i in range(1,10):
            if self.chromosomes[i]==1:
                score=max(score-1,0)   
        return score

            
    
    def evaluate(self):
        """evalue le chromosome et retourne une valeur numerique"""
        count=0
        for _ in range(PRECISION):
            if self.play():
                count+=1
            
        return count/PRECISION

def mutation(i1: Individu):
    """Mutation d'un individu -> 1 bit aléatoire"""
    index1 = random.randint(0, 18)
    i1_p = i1
    i1_p.chromosomes[index1] = 1-i1.chromosomes[index1]
    
    if i1_p.evaluate()<i1.evaluate(): #garde le meilleur
        i1_p=i1
    return i1_p    

def croisement(i1: Individu, i2: Individu):
    """Croisement de deux individus -> découpe en 2 sous-chaines pour l'instant"""
    i3 = Individu()
    i4=Individu()
    
    index1 = random.randint(0, 17)
    index2 = random.randint(0, 17)
    
    i3.chromosomes = i1.chromosomes[:index1] + i2.chromosomes[index1:]
    i4.chromosomes = i1.chromosomes[:index2] + i2.chromosomes[index2:]
    if i3.evaluate()<i1.evaluate(): #garde le meilleur
        i3=i1
    if i4.evaluate()<i2.evaluate():
        i4=i2
    return i3,i4

def generation(list_individus,gen_nb):
    
    if gen_nb==NB_ITERATIONS:
        list_individus.sort(key=lambda x: x.evaluate())
        for individu in list_individus:
            print(f'evaluate : {individu.evaluate()}\n{individu}\n') #plus forcement le meme evaluate qu'avant (random) donc le meme sens
    else:
        list_conserv=[]
        for _ in range(NB_INDIVIDUS//2):
            """ moitié est conservée"""
            list_conserv.append(list_individus[0])
            list_individus.pop(0) 

        for _ in range(NB_INDIVIDUS//4):
            """ un quart est muté"""
            list_conserv.append(mutation(list_individus[0]))
            list_individus.pop(0)
        
        for _ in range(NB_INDIVIDUS//8):
            i1,i2=croisement(list_individus[0],list_individus[NB_INDIVIDUS//8])
            list_conserv.append(i1)
            list_conserv.append(i2)
            list_conserv.pop(0)
            list_conserv.pop(NB_INDIVIDUS//8)
        
        score=0
        association=[]

        for id in list_conserv:
            debut=score
            score+=id.evaluate()
            fin=score
            association.append((id,debut,fin))
        
        liste_finale=[]

        for _ in range(NB_INDIVIDUS):
            a=random.uniform(0,1)
            liste_finale.append(find(association,a*score))
        
        if gen_nb%10==0:
            test_graph_x.append(gen_nb)
            test_graph_y.append(score)
        
        print(f'Generation : {gen_nb} | score : {score}')
        generation(liste_finale,gen_nb+1)
            


        
def find(liste,val):
    for elem in liste:
        if elem[2]>=val and elem[1]<=val:
            return elem[0]



    
def generate():
    list_individus=[]
    for _ in range(NB_INDIVIDUS):
        i1=Individu()
        i1.random_init()
        i1.chromosomes[19]=MAIN_CROUPIER
        list_individus.append(i1)
    generation(list_individus,2)

generate()


plt.plot(test_graph_x, test_graph_y)
plt.xlabel('iterations')
plt.ylabel('average_score best')
plt.show()

# i1=Individu()
# i1.chromosomes[19]=6
# i1.chromosomes[0]=1
# i1.chromosomes[10]=1
# i1.chromosomes[11]=1
# i1.chromosomes[12]=1
# i1.chromosomes[13]=1
# i1.chromosomes[14]=1
# i1.chromosomes[15]=1
# i1.chromosomes[16]=1
# i1.chromosomes[17]=1



# print(i1.evaluate())


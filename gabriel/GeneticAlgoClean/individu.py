import random 
import json

with open('C:/Users/croco/Documents/GitHub/TIPE/gabriel/config.json') as config_file:
    data = json.load(config_file)

############ Paramètres ############
PROBA_ARRAY=[1,2,3,4,5,6,7,8,9,10,10,10,10]
CROUPIER_MAIN=data['main_a_regarder'] #valeur de la main du croupier à observer
PRECISION = data['precision']

class Individu():
    def __init__(self) -> None:
        self.chromosomes = [0 for _ in range(190)]
        self.fitness=0
        
    
    
    
    def __str__(self) -> str:
        """Affichage un peu esthétique"""
        i=self.croupier_converter(CROUPIER_MAIN)

        return f"""        ---------------------------[ Croupier {CROUPIER_MAIN}--------------------------------- \n
        Sans as : [2-11]| [12]| [13]| [14]| [15]| [16]| [17]| [18]| [19]| [20]\n
                  [{self.chromosomes[i*19]}]   | [{self.chromosomes[i*19+1]}] | [{self.chromosomes[i*19+2]}] | [{self.chromosomes[i*19+3]}] | [{self.chromosomes[i*19+4]}] | [{self.chromosomes[i*19+5]}] | [{self.chromosomes[i*19+6]}] | [{self.chromosomes[i*19+7]}] | [{self.chromosomes[i*19+8]}] | [{self.chromosomes[i*19+9]}]\n
        ----------------------------------------------------------------------
        \n        Avec as : [10]| [11]| [12]| [13]| [14]| [15]| [16]| [17]| [18-20]
        \n                  [{self.chromosomes[i*19+10]}] | [{self.chromosomes[i*19+11]}] | [{self.chromosomes[i*19+12]}] | [{self.chromosomes[i*19+13]}] | [{self.chromosomes[i*19+14]}] | [{self.chromosomes[i*19+15]}] | [{self.chromosomes[i*19+16]}] | [{self.chromosomes[i*19+17]}] | [{self.chromosomes[i*19+18]}]
        \n        ----------------------------------------------------------------------"""

    def croupier_converter(self,valeur:int):
        if valeur==1:
            return 9
        else:
            return valeur-2
    
    def random_init(self):
        for i in range(190):
            self.chromosomes[i] = random.randint(0, 1)
    
    def convert(self,valeur:int,h_as:bool,valeur_croupier:int):
        """ Renvoie l'indice du chromosome associé à une valeur"""
        i=self.croupier_converter(valeur_croupier) # 2-> 0 | 3->1 | 1->9 
        if h_as :
            if valeur >=10 and valeur<18:
                return i*19+valeur
            else:
                return i*19+18
        
            
            
        else:
            if valeur>=2 and valeur<12:
                return i*19
            else:
                return i*19+valeur-11
    
    def calculate_val(self,tab:list):
        total=0
        for card in tab:
            if card==1:
                if total+10<=21:
                    total+=10
                else:
                    total+=1
                    tab.remove(1)
                    #retirer l'as pour qu'il ne soit plus compté
                    tab.append(2)
                    tab.append(-1)
            else:
                total+=card
        return total
    
    def play(self):
        """Joue un 1v1 contre le croupier en fonction de ses chromosomes et voit si il gagne"""
        
        in_game=True
        p_in_game=True
        c_in_game=True
        winner=False
        player_list=[random.choice(PROBA_ARRAY)]
        croupier_list=[random.choice(PROBA_ARRAY)]
        while in_game:
            
    

            choice=self.convert(self.calculate_val(player_list),(1 in player_list),croupier_list[0])
           
            
            if self.chromosomes[choice]==1 and p_in_game:
                   player_list.append(random.choice(PROBA_ARRAY))
            else:
                p_in_game=False
            
            if self.calculate_val(croupier_list)<17 and c_in_game:
                croupier_list.append(random.choice(PROBA_ARRAY))
                
            else:
                c_in_game=False
            
            if not p_in_game and not c_in_game:
                in_game=False
                if self.calculate_val(player_list)<21 and self.calculate_val(player_list)>self.calculate_val(croupier_list):
                    winner=True
            elif self.calculate_val(croupier_list)>21:
                winner=True
                in_game=False
            elif self.calculate_val(player_list)>21:
                winner=False
                in_game=False
            elif self.calculate_val(player_list)==21:
                winner=True
                in_game=False
        
        
        return winner
    

    def evaluate(self):
        """evalue le chromosome et retourne une valeur numerique"""
        count=0
        for _ in range(PRECISION):
            if self.play():
                count+=1
            
        self.fitness= count/PRECISION
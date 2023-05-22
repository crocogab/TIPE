import random
import numpy as np


class Main():
    def __init__(self,cards) -> None:
        self.cards=cards
        self.possede_as=11 in self.cards[:7]
        self.total=sum(cards[:7])
    
    def __str__(self) -> str:
        return f'Cartes = {self.cards} | As ? ={self.possede_as} | Total ={self.total}'


# main1=Main((7,10,0,0,0,0,0,11))
# print(main1)




class Individu():
    def __init__(self) -> None:
        self.chromosomes=[0 for _ in range(19)] #10 premiers as = sans as # 11 à fin = as
    
    def __str__(self) -> str:
        return f'Sans as = {self.chromosomes[:10]} | Avec as : {self.chromosomes[10:]}'
    
    def value(self,possede_as:bool,valeur:int)->int:
        """ renvoie si l'on doit prendre ou non suivant l'ADN
        valeur = (n ou p)
        si as -> p = valeur de la main avec l'as
        si !as -> n= valeur de la main
        
        """
        if possede_as:
            if valeur>=0 and valeur<=7:
                return self.chromosomes[11+valeur]
            else:
                return self.chromosomes[10]
        else:
            if valeur>=2 and valeur <=11:
                return self.chromosomes[0]
            else:
                return self.chromosomes[0+(21-valeur)]
    # pour chaque situation tire 10 * une carte et compare le resultat en moyenne au resultat mis -> evalue la difference
    def survival_rate(self,possede_as:bool,valeur:int):
        """ renvoie un taux entre 0 et 1 avec 1= best / max et 0 le pire """
        taux=0
        if possede_as:
            tire=np.random.choice(np.arange(1, 11), p=([1/13 for _ in range(9)]+[4/13]))
            if valeur+tire>21:
                return (1.0,tire+valeur-9)

            else: 
                return (1.0,tire+valeur)
        else:
            for _ in range(5):
                if valeur + np.random.choice(np.arange(1, 11), p=([1/13 for _ in range(9)]+[4/13]))>21:
                    taux+=1
            tire=random.randint(0,21-valeur)
            return ((5-taux)/5,tire)
    
    def fitness(self,possede_as,valeur):
        surv=self.survival_rate(possede_as,valeur)
        return (surv[0] *(surv[1]))/21



i1=Individu()
i1.chromosomes[10]=1

print(i1)
print(i1.value(True,0))

print(i1.fitness(False,13))

# def fitness(adn):

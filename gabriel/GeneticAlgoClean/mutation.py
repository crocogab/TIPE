import random
from individu import Individu 


def mutation(i1: Individu):
    """Mutation d'un individu par bit-flip."""
    mutation_rate = 0.02
    i1_p = Individu()
    i1_p.chromosomes = i1.chromosomes[:]  
    for i in range(len(i1.chromosomes)):
        if random.random() <= mutation_rate:  # si nombre aléatoire est inférieur au taux de mutation
            i1_p.chromosomes[i] = 1 - i1.chromosomes[i]  # inverse le bit
    return i1_p
    
              

def croisement(i1: Individu, i2: Individu):
    """Croisement de deux individus -> découpe en 3 sous-chaines et échange de la sous-chaine du milieu"""
    i3 = Individu()
    i4  =   Individu()
    
    
    index1 = random.randint(1, len(i1.chromosomes) - 2)
    index2 = random.randint(index1 + 1, len(i1.chromosomes) - 1)
    

    
    i3.chromosomes = i1.chromosomes[:index1] + i2.chromosomes[index1:index2] + i1.chromosomes[index2:]
    i4.chromosomes = i2.chromosomes[:index1] + i1.chromosomes[index1:index2] + i2.chromosomes[index2:] #revoir avec schema

    
    return i3,i4

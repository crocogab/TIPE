import random
from individuPortable import Individu 

def mutation(i1: Individu):
    """Mutation d'un individu -> 1 bit aléatoire"""
    index1 = random.randint(0, 189)
    index2 = random.randint(0, 189)
    i1_p = i1
    i1_p.chromosomes[index1] = 1-i1.chromosomes[index1]
    i1_p.chromosomes[index2] = 1-i1.chromosomes[index2]
    return i1_p    
                                  

def croisement(i1: Individu, i2: Individu):
    """Croisement de deux individus -> découpe en 2 sous-chaines pour l'instant"""
    i3 = Individu()
    i4  =   Individu()
    
    
    index1 = random.randint(2, 189)
    index2 = random.randint(2, 189)
    
    index3 = random.randint(0, index1-1)
    index4 = random.randint(0, index2-1)
    
    i3.chromosomes = i1.chromosomes[:index3] + i2.chromosomes[index3:index1] + i1.chromosomes[index1:]
    i4.chromosomes = i2.chromosomes[:index4] + i1.chromosomes[index4:index2] + i2.chromosomes[index2:] #revoir avec schema

    
    return i3,i4

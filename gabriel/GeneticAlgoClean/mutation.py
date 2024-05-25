import random
from individu import Individu 

# def mutation(i1: Individu):
#     """Mutation d'un individu -> 2 bit aléatoire"""
#     index1 = random.randint(0, 189)
#     index2 = random.randint(0, 189)
#     i1_p = i1
#     i1_p.chromosomes[index1] = 1-i1.chromosomes[index1]
#     i1_p.chromosomes[index2] = 1-i1.chromosomes[index2]
#     return i1_p    

def mutation(i1: Individu):
    """Mutation d'un individu par bit-flip."""
    mutation_rate = 0.01
    i1_p = Individu()
    i1_p.chromosomes = i1.chromosomes[:]  
    for i in range(len(i1.chromosomes)):
        if random.random() <= mutation_rate:  # si nombre aléatoire est inférieur au taux de mutation
            i1_p.chromosomes[i] = 1 - i1.chromosomes[i]  # inverse le bit
    return i1_p
    
              

def croisement(i1: Individu, i2: Individu):
    """Croisement de deux individus -> découpe en 2 sous-chaines pour l'instant"""
    i3 = Individu()
    i4  =   Individu()
    
    
    index1 = random.randint(2, 188)
    index2 = random.randint(2, 188)
    
    index3 = random.randint(0, index1-1)
    index4 = random.randint(0, index2-1)
    
    i3.chromosomes = i1.chromosomes[:index3] + i2.chromosomes[index3:index1] + i1.chromosomes[index1:]
    i4.chromosomes = i1.chromosomes[:index4] + i2.chromosomes[index4:index2] + i1.chromosomes[index2:] #revoir avec schema

    
    return i3,i4

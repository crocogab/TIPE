from individu import Individu
from math import sqrt

#inutile pour les petites populations

d_min=0.1
d_max=0.5
alpha=0.8

class cluster:
    def __init__(self) -> None:
        self.individus = []
        self.centre = None


def distance(i1: Individu, i2: Individu):
    """Distance entre deux individus"""
    return sqrt(sum([(i1.chromosomes[i] - i2.chromosomes[i])**2 for i in range(190)]))


    
def init_clusters(individus: list):
    """Initialise les clusters avec un individu chacun"""
    clusters = []
    indiviu_zero=Individu()
    for i in individus:
        clusters.append(cluster())
        clusters[-1].individus.append(i)
        clusters[-1].centre = distance(i, indiviu_zero)
    return clusters    

def update_clusters(clusters: list):
    """Met à jour les centres des clusters"""
    for c in clusters:
        c_clusters = clusters[:]
        c_clusters.remove(c)
        for o in c_clusters:
            if abs(c.centre - o.centre) < d_min:
                c.individus.extend(o.individus)
                c.centre = (c.centre + o.centre)/2
        if len(c.individus) ==1:
            min=abs(c.centre-c_clusters[0].centre)
            temp_c=c_clusters[0]
            for o in c_clusters:
                if abs(c.centre - o.centre) < min:
                    min=abs(c.centre-o.centre)
                    temp_c=o
            if min < d_max:
                temp_c.individus.append(c.individus[0])
                temp_c.centre = ((temp_c.centre)*len(temp_c.individus) + c.centre)/len(temp_c.individus)

def individu_clusters(i1: Individu, clusters: list):
    """Nombre d'individus dans le cluster de i1"""
    for c in clusters:
        if i1 in c.individus:
            return (len(c.individus),c)
    print( "Error individu not found") # cochon -> debug
    


def sharing(individu_list):
    sharing_val= []
    clusters=init_clusters(individu_list)
    update_clusters(clusters)
    indiviu_zero=Individu()
    for individu in individu_list:
        nb_individu,cluster=individu_clusters(individu,clusters)
        d_ic=abs(distance(individu,indiviu_zero)-cluster.centre)
        mi= nb_individu * (1-(d_ic/2*d_max)**alpha)
        sharing_val.append(mi)

    return sharing_val

                
                

    
                

        


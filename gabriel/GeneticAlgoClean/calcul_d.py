from sharing import distance_liste


def calcul_dmoy(liste_cluster,liste_individus):
    """Va calculer dmoy"""
    n = len(liste_individus)
    Nc= len(liste_cluster)
    somme=0
    for i in range(n):
        for j in range(Nc):
            somme+=distance_liste(liste_individus[i].chromosomes,liste_cluster[j].centre)

    return somme/(n*Nc)

def calcul_nopt(sharing_value,liste_cluster):
    """calcul Nopt (sharing value = sharing du meilleur individu de l'itération)"""
    Nc= len(liste_cluster)
    somme=0
    for i in range(Nc):
        if liste_cluster[i].best_individu.fitness>sharing_value:
            somme+=1
    return somme

def calcul_delta(Nopt,Nc,delta):
    """Calcul delta pour une nouvelle itération
    Nopt: valeur de nopt
    Nc : nombre de clusters
    delta : valeur delta pour la précédente itération 
    """
    new_delta=delta
    S1=0.85
    S2=0.75
    if (Nopt/Nc)>S1 and (100 > delta):
        new_delta=delta*1.05
    if S2> (Nopt/Nc) and (delta>1):
        new_delta=delta*0.95
    return new_delta


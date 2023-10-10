from re import I
from individu import Individu
from math import sqrt

#inutile pour les petites populations

d_min=4
d_max=2
alpha=0.8

class cluster:
    def __init__(self) -> None:
        self.individus = []
        self.centre = []


def distance_individus(i1: Individu, i2: Individu):
  """Distance entre deux individus"""
  return sqrt(sum([(i1.chromosomes[i] - i2.chromosomes[i])**2 for i in range(190)]))

def distance_liste(l1:list,l2:list):
  """Distance entre deux listes (de chromosomes)"""
  return sqrt(sum([(l1[i] - l2[i])**2 for i in range(190)]))


def init_clusters(individus: list):
  """Initialise les clusters avec un individu chacun"""
  clusters = []
  for i in individus:
      clusters.append(cluster())
      clusters[-1].individus.append(i)
      clusters[-1].centre = i.chromosomes
  print("[DEBUG] initialisation terminee")
  return clusters    

def fusion_clusters(clusters: list):
  """Met à jour les centres des clusters 
  ATTENTION -> ne conserve pas forcement la taille de la liste clusters
  """

  for c1 in clusters:
    for c2 in clusters:
      if c1!=c2:
        if distance_liste(c1.centre,c2.centre)<d_min:
          #print(f"[DEBUG] fusion entre {c1} {c2}")
          c1.centre=[(c1.centre[l]+c2.centre[l])/2 for l in range(190)]
          c1.individus.extend(c2.individus)

 
  

def add_individu(i1:Individu,clusters:list):
  """Ajoute l'individu à la liste des clusters -> crée les nouveaux clusters
  Ou modifie barycentre
  """
  
  etat=0
  indice=-1
  for indice_c in range(len(clusters)):
    if distance_liste(i1.chromosomes,clusters[indice_c].centre)<d_max:
      etat=1
      indice=indice_c
  if etat==1:
    
    a=len(clusters[indice].individus)+1
    clusters[indice].centre=[(clusters[indice].centre[l]+i1.chromosomes[l])/a for l in range(190)]
    clusters[indice].individus.append(i1)
  else:
    c=cluster()
    c.individus=[i1]
    c.centre=i1.chromosomes
    clusters.append(c)



def remove_individu(i1:Individu,clusters:list):
  for c in clusters:

    if i1 in c.individus:
        return c.individus.pop(c.individus.index(i1))
          




def individu_clusters(i1: Individu, clusters: list):
    """Nombre d'individus dans le cluster de i1"""
    for c in clusters:
        
        if i1 in c.individus:

            return (len(c.individus),c)
  
    print( f"Error individu not found {type(c)} {i1}") # cochon -> debug
    


def sharing(i1:Individu,clusters:list):
  """ Renvoie la valeur du sharing pour un individu """
  
  nc,c=individu_clusters(i1,clusters)
  return nc*(1-((distance_liste(i1.chromosomes,c.centre))/(2*d_max))**alpha)

    

                
                

    
                

        


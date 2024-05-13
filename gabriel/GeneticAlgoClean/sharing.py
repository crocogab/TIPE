from individu import Individu
from math import sqrt
import json


alpha=0.8


class cluster:
    def __init__(self) -> None:
        self.individus = []
        self.best_individu=None
        self.individus_name=[]
        self.centre = []

def update_d(initial):
  if initial :
    return (0,0)
  else:
    with open(r'training.json') as training_file:
      data = json.load(training_file)
    delta=data['delta']
    dmoy=data['dmoy']
    dmax=dmoy/delta
    return (dmax,dmax/3)

def distance_individus(i1: Individu, i2: Individu):
  """Distance entre deux individus"""
  return sqrt(sum([(i1.chromosomes[i] - i2.chromosomes[i])**2 for i in range(190)])) #pas distance euclidienne

def distance_liste(l1:list,l2:list):
  """Distance entre deux listes (de chromosomes)"""
  return sqrt(sum([(l1[i] - l2[i])**2 for i in range(190)]))


def init_clusters(individus: list):
  """Initialise les clusters avec un individu chacun"""
  clusters = []
  for i in individus:
      clusters.append(cluster())
      clusters[-1].individus.append(i)
      clusters[-1].individus_name.append(i.name)
      clusters[-1].centre = i.chromosomes
      clusters[-1].best_individu=i
  print("[DEBUG] initialisation terminee")
  return clusters    

def fusion_clusters(clusters: list,initial):
  """Met à jour les centres des clusters 
  ATTENTION -> ne conserve pas forcement la taille de la liste clusters
  """
  d_min=update_d(initial)[1]
  liste_traitee=[]
  for i in range(len(clusters)):
    for j in range(len(clusters)):
      if i!=j and (j not in liste_traitee) and (i not in liste_traitee):
        if distance_liste(clusters[i].centre,clusters[j].centre)<=d_min: #distance inferieure au seuil -> on garde le cluster 1
          #print(f"[DEBUG] fusion entre {c1} {c2}")
          
          clusters[i].individus.extend(clusters[j].individus)
          clusters[i].individus_name.extend(clusters[j].individus_name)
          if clusters[i].best_individu.fitness<clusters[j].best_individu.fitness: 
            clusters[i].best_individu=clusters[j].best_individu #on peut faire comme ca -> car python pas de pb de pointeur
          taille=len(clusters[i].individus) #different de 0
          
          for l in range(taille):
            for m in range(190):
              clusters[i].centre[m]+=(clusters[i].individus[l].chromosomes[m])/taille
          
          del clusters[j]
          liste_traitee.append(j)
          liste_traitee.append(i)
  

def add_individu(i1:Individu,clusters:list,initial):
  """Ajoute l'individu à la liste des clusters -> crée les nouveaux clusters
  Ou modifie barycentre
  """
  d_max=update_d(initial)[0]
  etat=0
  indice=-1
  for indice_c in range(len(clusters)): # len(clusters) calcul de distance (<nb individu) -> negligeable
    if distance_liste(i1.chromosomes,clusters[indice_c].centre)<d_max:
      etat=1
      indice=indice_c
  
  if etat==1:
    clusters[indice].individus.append(i1)
    clusters[indice].individus_name.append(i1.name)
    if clusters[indice].best_individu.fitness<i1.fitness:
      clusters[indice].best_individu=i1
    
    a=len(clusters[indice].individus)
    for i in range(a): #recalcul du centre du cluster
      for l in range(190):
        clusters[indice].centre[l]+=(clusters[indice].individus[i].chromosomes[l])/a
    
    
  
  else:
    c=cluster()
    c.individus=[i1]
    c.individus_name=[i1.name]
    c.centre=i1.chromosomes
    c.best_individu=i1
    clusters.append(c)


    

def remove_individu(i1:Individu,clusters:list):
  for i in range(len(clusters)): # a checker si marche bien
    if i1.name in clusters[i].individus_name:
      if len(clusters[i].individus)!=1:
        j=clusters[i].individus_name.index(i1.name)
        clusters[i].individus_name.remove(i1.name)
        clusters[i].individus.pop(j) 
        a=len(clusters[i].individus) #different de 0 car taille >1
        for j in range(a): #recalcul du centre du cluster
          for l in range(190):
            clusters[i].centre[l]+=(clusters[i].individus[j].chromosomes[l])/a
        return None

      else:
        #on supprime clusters de taille 
        clusters.pop(i)
        return None



def individu_clusters(i1: Individu, clusters: list):
    """Nombre d'individus dans le cluster de i1"""
    for i in range(len(clusters)):
      if i1.name in clusters[i].individus_name:
        return (len(clusters[i].individus),clusters[i])
    #for i in range(len(clusters)):
    #   print(clusters[i].individus_name)
    #print( f"Error individu not found {type(clusters[i])} {i1.name}") 
    


def sharing(i1:Individu,clusters:list,initial):
  """ Renvoie la valeur du sharing pour un individu """
  d_max=update_d(initial)[0]
  try:
    nc,c=individu_clusters(i1,clusters)
    return nc*(1-((distance_liste(i1.chromosomes,c.centre))/(2*d_max))**alpha)
  except: #permet d'eviter crash total si bug -> plus erreur normalement
    return 1

import random
import json
from mutationPortable import *
from scaling import *
from sharingPortable import *
from calcul_dPortable import *
from math import floor
import uuid
import matplotlib.pyplot as plt
import threading

############ Paramètres #############

lock = threading.Lock() #permet threading dans trainer
with open(r'config.json') as config_file:
    data = json.load(config_file)

NB_ITERATIONS=data['nb_iterations']
NB_INDIVIDUS=data['nb_individus']

####### Fonctions auxiliaires #######

def find(liste,val):
    for elem in liste:
        if elem[2]>=val and elem[1]<=val:
            return elem[0]

#####################################

def generation(list_individus,gen_nb,cluster_list):
  X_SCORE=[]
  Y_GEN=[]
  clusters=cluster_list
  list_individus_n=list_individus
  for actual_gen in range(gen_nb):
    
    
    list_conserv=[]
        
    # for _ in range(NB_INDIVIDUS//4):
    #   """ quart est conservée"""
    #   list_conserv.append(list_individus_n[0])
    #   list_individus_n.pop(0)
    
    for _ in range(NB_INDIVIDUS//2): 
      """ moitié est nouveau"""
      i1=Individu()
      i1.random_init()
      i1.name=uuid.uuid4()
      i1.evaluate()
      list_conserv.append(i1)
      list_individus_n.pop(0) 
    
    for _ in range(NB_INDIVIDUS//4):
      """ un quart est muté"""
      i1=mutation(list_individus_n[0])
      i1.name=uuid.uuid4() #ordre des instructions est important ici pour ne pas retirer mauvais elements
      remove_individu(list_individus_n[0],clusters)
      add_individu(i1,clusters,gen_nb==0)
      list_conserv.append(i1)
      list_individus_n.pop(0)       
      i1.evaluate()
    
    

    
    for i in range(NB_INDIVIDUS//8):
      """ un quart est croisé"""
      
      i1,i2=croisement(list_individus_n[0],list_individus_n[NB_INDIVIDUS-len(list_conserv)-1])
      i1.name=uuid.uuid4()
      i2.name=uuid.uuid4()
      remove_individu(list_individus_n[0],clusters)
      add_individu(i1,clusters,gen_nb==0)
      remove_individu((list_individus_n[NB_INDIVIDUS-len(list_conserv)-1]),clusters)
      add_individu(i2,clusters,gen_nb==0)
      i1.evaluate()
      i2.evaluate()
      list_conserv.append(i1)
      list_conserv.append(i2)
      list_individus_n.pop(0)
      list_individus_n.pop(NB_INDIVIDUS-len(list_conserv)-1)
      

    
    ### Stochastic remainder without replacement selection + sharing -> pb
    liste_finale=[]
    score=0
    k_exp=exp_scaling(actual_gen+1)
    total=0
    mi_value=[sharing(i1,clusters,gen_nb==0) for i1 in list_conserv]
    #print(f"[DEBUG]: tableau cree -> val max = {max(mi_value)}")
    
    
    for i in range(len(list_conserv)):
      total+=(((list_conserv[i].fitness)**k_exp)/mi_value[i])
    
    moy_fitness=total/NB_INDIVIDUS




    for i in range(len(list_conserv)): #pb ici
      r_i=((((list_conserv[i].fitness)**k_exp))/mi_value[i])/moy_fitness
      
      a=floor(r_i)
      
      for _ in range(a):  
        liste_finale.append(list_conserv[i])
    
    
    
    association=[]
    for i in range(len(list_conserv)):
      debut=score
      score+=((((list_conserv[i].fitness)**k_exp))/mi_value[i])/moy_fitness-floor(((((list_conserv[i].fitness)**k_exp))/mi_value[i])/moy_fitness)
      fin=score
      association.append((list_conserv[i],debut,fin))
    for _ in range(NB_INDIVIDUS-len(liste_finale)):
      a=random.uniform(0,1)
      liste_finale.append(find(association,a*score))
    #############[CALCUL DE DMOY + DELTA]########
    
    with open(r'training.json') as training_file:
      data2 = json.load(training_file)

    delta_old=data2['delta']
    dmoy=calcul_dmoy(clusters,liste_finale)
    nopt=calcul_nopt(max(mi_value),clusters)
    delta=calcul_delta(nopt,len(clusters),delta_old)
   

    ##################
    
      
    individu_json={
      'nb_generation':actual_gen,
      'fitness_moyenne':moy_fitness,
      'delta':delta,
      'dmoy':dmoy,
      'chromosomes':[''.join(map(str,individu.chromosomes)) for individu in liste_finale]
    }
    with open(r"training.json", "w") as f:
      f.write(json.dumps(individu_json, indent=4))
    
    X_SCORE.append(moy_fitness)
    Y_GEN.append(actual_gen)


    if actual_gen%10==0:
      """ On enregistre le graphique de progression"""
      plt.xlabel="Fitness moyenne (comptée avec le scaling)"
      plt.ylabel="Génération"
      plt.plot(Y_GEN, X_SCORE)
      plt.savefig('progression.png')
    

    list_individus_n=liste_finale
    clean_clusters(clusters, [i.name for i in liste_finale])
    print(f'Generation : {actual_gen} | score (avec scaling): {moy_fitness} | scaling_exp:{k_exp} | delta:{delta} | dmoy:{dmoy} |Nombre clusters : {len(clusters)} | Nombre individus : {len(liste_finale)}')

def initialise_one_cpu(list_individus):
  list_temp=[]
  for _ in range(NB_INDIVIDUS//4):
      i1=Individu()
      i1.random_init()
      i1.name=uuid.uuid4()
      i1.evaluate()
      # on peut avoir un pb de nb quand on initialise les individus - doit stocker liste temporaire et ajouter
      list_temp.append(i1)
  #print(f"Processus {threading.current_thread().ident} va ajouter les individus a la liste")
  with lock:
    list_individus.extend(list_temp)
  del list_temp


def generate():
  
  list_individus=[]
  t1 = threading.Thread(target=initialise_one_cpu, args=[list_individus])
  t2 = threading.Thread(target=initialise_one_cpu, args=[list_individus])
  t3 = threading.Thread(target=initialise_one_cpu, args=[list_individus])
  t4 = threading.Thread(target=initialise_one_cpu, args=[list_individus])


  t1.start()
  t2.start()
  t3.start()
  t4.start()

  t1.join()
  t2.join()
  t3.join()
  t4.join()
  
  

  clusters=init_clusters(list_individus)
  print("[DEBUG] Clusters ont ete init")
  fusion_clusters(clusters,True)
  print("[DEBUG] Clusters ont ete fusionnes")
  print("[DEBUG] Nombre de clusters : ",len(clusters))
  print("[DEBUG] Dmoy + Delta initialization")
  
  individu_json={
        'nb_generation':0,
        'fitness_moyenne':0,
        'delta':2.0,
        'dmoy':0,
        'chromosomes':[]
      }
  with open(r"training.json", "w") as f:
    f.write(json.dumps(individu_json, indent=4))
  
  generation(list_individus,NB_ITERATIONS,clusters)
        
if __name__=='__main__':
  generate()
  
   
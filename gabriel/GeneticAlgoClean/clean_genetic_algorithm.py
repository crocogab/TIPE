import random
import json
from mutation import *
from scaling import *
from sharing import *
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
    
    #plus forcement le meme evaluate qu'avant (random) donc le meme sens
    list_conserv=[]
        
    for _ in range(NB_INDIVIDUS//2):
      """ moitié est conservée"""
      list_conserv.append(list_individus_n[0])
      list_individus_n.pop(0) 
    
    def mutation_multi():
      for _ in range(NB_INDIVIDUS//16):
        """ un quart est muté"""
        
        with lock:
          i1=mutation(list_individus_n[0])
          i1.name=uuid.uuid4() #ordre des instructions est important ici pour ne pas retirer mauvais elements
          remove_individu(list_individus_n[0],clusters)
          add_individu(i1,clusters)
          list_conserv.append(i1)
          list_individus_n.pop(0)       
        i1.evaluate() #evaluation n'est plus dans la mutation
        
    t1 = threading.Thread(target=mutation_multi, args=[])
    t2 = threading.Thread(target=mutation_multi, args=[])
    t3 = threading.Thread(target=mutation_multi, args=[])
    t4 = threading.Thread(target=mutation_multi, args=[])
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()

    #print('[DEBUG] TAILLE : ',len(list_conserv))
    def croisement_multi():
      for i in range(NB_INDIVIDUS//16):
        """ un quart est croisé"""
        
        with lock:
          i1,i2=croisement(list_individus_n[0],list_individus_n[NB_INDIVIDUS-len(list_conserv)-1])
          i1.name=uuid.uuid4()
          i2.name=uuid.uuid4()
          remove_individu(list_individus_n[0],clusters)
          add_individu(i1,clusters)
          remove_individu((list_individus_n[NB_INDIVIDUS-len(list_conserv)-1]),clusters)
          add_individu(i2,clusters)
          list_conserv.append(i1)
          list_conserv.append(i2)
          list_individus_n.pop(0)
          list_individus_n.pop(NB_INDIVIDUS-len(list_conserv)-1)
        i1.evaluate()
        i2.evaluate()
        
        
    
    t1 = threading.Thread(target=croisement_multi, args=[])
    t2 = threading.Thread(target=croisement_multi, args=[])
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    ### Stochastic remainder without replacement selection + sharing
    liste_finale=[]
    score=0
    k_exp=exp_scaling(actual_gen+1)
    total=0
    mi_value=[sharing(i1,clusters) for i1 in list_conserv]
    #print(f"[DEBUG]: tableau cree -> val max = {max(mi_value)}")
    for i in range(len(list_conserv)):
      total+=(((list_conserv[i].fitness)**k_exp)/mi_value[i])
    moy_fitness=total/NB_INDIVIDUS
      
    for i in range(len(list_conserv)):
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
    #############
    if (actual_gen+1)%5==0:
      """On enregistre sur fichier json pour save le training"""
      individu_json={
        'nb_generation':actual_gen,
        'fitness_moyenne':moy_fitness,
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
    print(f'Generation : {actual_gen} | score (avec scaling): {moy_fitness} | scaling_exp:{k_exp}')

def initialise_one_cpu(list_individus):
  list_temp=[]
  for _ in range(NB_INDIVIDUS//4):
      i1=Individu()
      i1.random_init()
      i1.name=uuid.uuid4()
      i1.evaluate()
      # on peut avoir un pb de nb quand on initialise les individus - doit stocker liste temporaire et ajouter
      list_temp.append(i1)
  print(f"Processus {threading.current_thread().ident} va ajouter les individus a la liste")
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
  
  print(len(list_individus))

  clusters=init_clusters(list_individus)
  print("[DEBUG] Clusters ont ete init")
  fusion_clusters(clusters)
  print("[DEBUG] Clusters ont ete fusionnes")
  
  generation(list_individus,NB_ITERATIONS,clusters)
        
if __name__=='__main__':
  generate()
  
   

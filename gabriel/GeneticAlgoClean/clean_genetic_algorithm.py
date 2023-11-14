import random
import json
import sys
from mutation import *
from scaling import *
from sharing import *
from math import floor
import uuid

############ Paramètres #############

sys.setrecursionlimit(1000000)

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

    
    if gen_nb==NB_ITERATIONS:
        
        for individu in list_individus:
            individu.evaluate()
        
        list_individus.sort(key=lambda x: x.fitness)
        for individu in list_individus:
            print(f'evaluate : {individu.fitness}\n{individu}\n') #plus forcement le meme evaluate qu'avant (random) donc le meme sens
    else:
        list_conserv=[]
        clusters=cluster_list


        for _ in range(NB_INDIVIDUS//2):
            """ moitié est conservée"""
            list_conserv.append(list_individus[0])
            list_individus.pop(0) 
        
        for i in range(NB_INDIVIDUS//4):
            """ un quart est muté"""
            i1=mutation(list_individus[0])
            i1.name=uuid.uuid4() #ordre des instructions est important ici pour ne pas retirer mauvais elements

            remove_individu(list_individus[0],clusters)
            add_individu(i1,clusters)

            list_conserv.append(i1)
            list_individus.pop(0)
    
        for i in range(NB_INDIVIDUS//8):
            """ un quart est croisé"""
            i1,i2=croisement(list_individus[0],list_individus[NB_INDIVIDUS-len(list_conserv)-1])
            
            i1.name=uuid.uuid4()
            i2.name=uuid.uuid4()

            remove_individu(list_individus[0],clusters)
            add_individu(i1,clusters)

            
            remove_individu((list_individus[NB_INDIVIDUS-len(list_conserv)-1]),clusters)
            add_individu(i2,clusters)

            

            list_conserv.append(i1)
            list_conserv.append(i2)
            list_individus.pop(0)
            list_individus.pop(NB_INDIVIDUS-len(list_conserv)-1)
        
  
        ### Stochastic remainder without replacement selection + sharing
        


        liste_finale=[]
        score=0
        k_exp=exp_scaling(gen_nb)
        total=0
        

        mi_value=[sharing(i1,clusters) for i1 in list_conserv]

        print(f"[DEBUG]: tableau cree -> val max = {max(mi_value)}")



        

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
    
        if gen_nb%5==0:
            """On enregistre sur fichier json pour save le training"""
            
            individu_json={
                'nb_generation':gen_nb,
                'fitness_moyenne':moy_fitness,
                'chromosomes':[''.join(map(str,individu.chromosomes)) for individu in liste_finale]
              
            }
            with open(r"training.json", "w") as f:
                f.write(json.dumps(individu_json, indent=4))



    
           
        print(f'Generation : {gen_nb} | score (avec scaling): {moy_fitness} | scaling_exp:{k_exp}')
        
        generation(liste_finale,gen_nb+1,clusters)

def generate():
    list_individus=[]
    for s in range(NB_INDIVIDUS):
        i1=Individu()
        i1.random_init()
        i1.name=uuid.uuid4()
        i1.evaluate()
        list_individus.append(i1)
    clusters=init_clusters(list_individus)
    fusion_clusters(clusters)
    print("[DEBUG] Clusters ont ete init")
    generation(list_individus,1,clusters)
        
if __name__=='__main__':
    generate()




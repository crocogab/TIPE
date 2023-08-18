import random
import json
import sys
from mutation import *
from scaling import *
from math import floor


############ Paramètres #############

sys.setrecursionlimit(1000000)

with open('C:/Users/croco/Documents/GitHub/TIPE/gabriel/config.json') as config_file:
    data = json.load(config_file)

NB_ITERATIONS=data['nb_iterations']
NB_INDIVIDUS=data['nb_individus']

####### Fonctions auxiliaires #######

def find(liste,val):
    for elem in liste:
        if elem[2]>=val and elem[1]<=val:
            return elem[0]

#####################################

def generation(list_individus,gen_nb):
    
    if gen_nb==NB_ITERATIONS:
        
        for individu in list_individus:
            individu.evaluate()
        
        list_individus.sort(key=lambda x: x.fitness)
        for individu in list_individus:
            print(f'evaluate : {individu.fitness}\n{individu}\n') #plus forcement le meme evaluate qu'avant (random) donc le meme sens
    else:
        list_conserv=[]
        for _ in range(NB_INDIVIDUS//2):
            """ moitié est conservée"""
            list_conserv.append(list_individus[0])
            list_individus.pop(0) 
        
        for _ in range(NB_INDIVIDUS//4):
            """ un quart est muté"""
            list_conserv.append(mutation(list_individus[0]))
            list_individus.pop(0)
        
        for _ in range(NB_INDIVIDUS//8):
            """ un quart est croisé"""
            i1,i2=croisement(list_individus[0],list_individus[NB_INDIVIDUS-len(list_conserv)-1])
            list_conserv.append(i1)
            list_conserv.append(i2)
            list_individus.pop(0)
            list_individus.pop(NB_INDIVIDUS-len(list_conserv))
        
        
        ### Stochastic remainder without replacement selection + sharing
        
        liste_finale=[]
        score=0
        k_exp=exp_scaling(gen_nb)
        total=0

        

        for individus in list_conserv:
            total+=((individus.fitness)**k_exp)


        moy_fitness=total/NB_INDIVIDUS

        for id in list_conserv:
            
            r_i=(((id.fitness)**k_exp))/moy_fitness
            a=floor(r_i)
            for _ in range(a):  
                liste_finale.append(id)
            
        
        association=[]
        for id in list_conserv:
            debut=score
            
            
            score+=(((id.fitness)**k_exp))/moy_fitness-floor((((id.fitness)**k_exp))/moy_fitness)
            fin=score
            association.append((id,debut,fin))
        
        for _ in range(NB_INDIVIDUS-len(liste_finale)):
            a=random.uniform(0,1)
            liste_finale.append(find(association,a*score))

    
        #############
    
        if gen_nb%100==0:
            """On enregistre sur fichier json pour save le training"""
            
            individu_json={
                'nb_generation':gen_nb,
                'fitness_moyenne':moy_fitness,
                'chromosomes':[''.join(map(str,individu.chromosomes)) for individu in liste_finale]
            }
            with open(r"C:\Users\croco\Documents\GitHub\TIPE\gabriel\training.json", "w") as f:
                f.write(json.dumps(individu_json, indent=4))



        if gen_nb%100==0:
           
            print(f'Generation : {gen_nb} | score (avec scaling): {moy_fitness} | scaling_exp:{k_exp}')
        generation(liste_finale,gen_nb+1)

def generate():
    list_individus=[]
    for s in range(NB_INDIVIDUS):
        i1=Individu()
        i1.random_init()
        i1.evaluate()
        list_individus.append(i1)
    generation(list_individus,1)
        
if __name__=='__main__':
    generate()




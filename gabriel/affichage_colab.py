from pickle import NONE
import sys
sys.path.insert(1, 'GeneticAlgoClean')
from individu import *
import json
import threading
import uuid


with open(r'training.json') as training_file:
    data = json.load(training_file)


list_chromosomes = []
liste_finale=[]

for chromosome in data['chromosomes']:
    chromo_actu=[]
    for i in range(190):
        
        chromo_actu.append(int(chromosome[i]))
    list_chromosomes.append(chromo_actu)

index_b=0

threads=[]
for elem in list_chromosomes:
    i1=Individu()
    i1.chromosomes=elem
    i1.name=uuid.uuid4()
    t = threading.Thread(target=i1.evaluate,)
    t.start()
    threads.append(t)
    liste_finale.append(i1)
    
for thread in threads:
        thread.join()
uiid_max=None

lf2=liste_finale.copy()
lf2.sort(key=lambda x: x.fitness,reverse=True)

# for i1 in liste_finale:
#   if i1.fitness>maxi:
#         maxi=i1.fitness
#         uiid_max=i1.name

# for i in range(len(liste_finale)):
#   if liste_finale[i].name==uiid_max:
#     index_b=i      

a=[liste_finale.index(elem) for elem in lf2]

   
for i in range(10):
  print(f'Classement {i+1} : {a[i]}')

print('[DEBUG]: fitness_max = ', lf2[0].fitness)



best_individu=liste_finale[index_b]

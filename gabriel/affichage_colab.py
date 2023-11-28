from pickle import NONE
import sys
sys.path.insert(1, '/content/TIPE/gabriel/GeneticAlgoClean')
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
maxi=0
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
for i1 in liste_finale:
  if i1.fitness>maxi:
        maxi=i1.fitness
        uiid_max=i1.name

for i in range(len(liste_finale)):
  if liste_finale[i].name==uiid_max:
    index_b=i      

    

print(f"[DEBUG] Le meilleur individu est l'individu numéro {index_b}")

print('[DEBUG]: fitness_max = ', maxi)



best_individu=liste_finale[index_b]
print(f'[DEBUG]: C:2  AS     19 {best_individu.chromosomes[best_individu.convert(19,True,2)]}')
print(f'[DEBUG]: C:AS PAS AS 15 {best_individu.chromosomes[best_individu.convert(15,False,1)]}')
print(f'[DEBUG]: C:6  AS     13 {best_individu.chromosomes[best_individu.convert(13,True,6)]}')
print(f'[DEBUG]: C:3  PAS AS 19 {best_individu.chromosomes[best_individu.convert(19,False,3)]}')
print(f'[DEBUG]: C:3  PAS AS 18 {best_individu.chromosomes[best_individu.convert(18,False,3)]}')
print(f'[DEBUG]: C:3  PAS AS 17 {best_individu.chromosomes[best_individu.convert(17,False,3)]}')
print(f'[DEBUG]: C:AS AS     15 {best_individu.chromosomes[best_individu.convert(15,True,1)]}')
print(f'[DEBUG]: C:AS AS     17 {best_individu.chromosomes[best_individu.convert(17,True,1)]}')


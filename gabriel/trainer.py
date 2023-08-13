from individu5 import *
import json

with open(r'C:\Users\croco\Documents\GitHub\TIPE\gabriel\training.json') as training_file:
    data = json.load(training_file)


list_chromosomes = []
liste_finale=[]

for chromosome in data['chromosomes']:
    chromo_actu=[]
    for i in range(190):
        
        chromo_actu.append(int(chromosome[i]))
    list_chromosomes.append(chromo_actu)

for elem in list_chromosomes:
    i1=Individu()
    i1.chromosomes=elem
    i1.evaluate()
    liste_finale.append(i1)

generation(liste_finale, data['nb_generation'])


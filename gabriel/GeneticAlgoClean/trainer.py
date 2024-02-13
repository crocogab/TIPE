from clean_genetic_algorithm import generation
from individu import Individu
from sharing import init_clusters,fusion_clusters
import json
import threading

with open(r'training.json') as training_file:
    data = json.load(training_file)

with open(r'config.json') as config_file:
    data2 = json.load(config_file)


list_chromosomes = []
liste_finale=[]

print(data2['nb_iterations']-data['nb_generation'])

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



clusters=init_clusters(liste_finale)
fusion_clusters(clusters)
print('Cluster fusionnes :)\n')
generation(liste_finale, data2['nb_iterations']-data['nb_generation'],clusters)



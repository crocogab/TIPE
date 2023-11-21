from clean_genetic_algorithm import generation
from individu import Individu
from sharing import init_clusters,fusion_clusters
import json
import concurrent.futures

with open(r'training.json') as training_file:
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

clusters=init_clusters(liste_finale)
fusion_clusters(clusters)
print('Cluster fusionnes :)\n')
with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
    executor.submit(generation,liste_finale, data['nb_generation'],clusters,)



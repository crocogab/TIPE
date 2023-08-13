import random
import time
import numpy as np

PROBA_ARRAY=[1/13 for _ in range(9)]+[4/13]
NP_PROBA_ARRAY=np.arange(1, 11)
liste=[1,2,3,4,5,6,7,8,9,10,10,10,10]
liste2=[]
liste3=[]
start_time = time.time()

for _ in range(100000):
    liste2.append(random.choice(liste))
end_time = time.time()

execution_time = end_time - start_time

print(f"Temps d'exécution 1 : {execution_time} secondes")

start_time = time.time()
for _ in range(100000):
    liste3.append(np.random.choice(NP_PROBA_ARRAY, p=(
                    PROBA_ARRAY)))
end_time = time.time()
execution_time = end_time - start_time

print(f"Temps d'exécution 2 : {execution_time} secondes")
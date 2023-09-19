import time
import timeit
import random
import pyfastrand

PROBA_ARRAY=[1,2,3,4,5,6,7,8,9,10,10,10,10]


def random_python():
    for _ in range(10):
        random.choice(PROBA_ARRAY)

print(timeit.timeit(random_python))

def my_random():
    for _ in range(10):
        PROBA_ARRAY[pyfastrand.pcg32bounded(13)]

print(timeit.timeit(my_random))



#print(PROBA_ARRAY[pyfastrand.pcg32bounded(13)])
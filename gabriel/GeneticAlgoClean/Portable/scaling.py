from math import tan, pi
import json

with open(r'config.json') as config_file:
    data = json.load(config_file)

P=data['p_scaling']
NB_ITERATIONS=data['nb_iterations']

def exp_scaling(iterations_actuelle:int):
    """ permet un scaling exponentiel"""
    return 1/((tan((iterations_actuelle/NB_ITERATIONS)*(pi/2)))**P)
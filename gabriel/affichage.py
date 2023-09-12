from tkinter import *
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

index_b=0
max=0
for elem in list_chromosomes:
    i1=Individu()
    i1.chromosomes=elem
    i1.evaluate()
    if i1.fitness>max:
        max=i1.fitness
        index_b=list_chromosomes.index(elem)

    liste_finale.append(i1)





print('[DEBUG]: fitness_max = ', max)

fenetre = Tk()

tableau = []
for i in range(20):
    ligne=[]
    for j in range(11):
        if j>0 and j<10 and i==0:
            case= Label(fenetre, text=j+1, borderwidth=1, relief="solid", width=8, height=3)
        elif j==10 and i==0:
            case= Label(fenetre, text="AS", borderwidth=1, relief="solid", width=8, height=3)
        elif j==0 and i>0 and i<10:
            case= Label(fenetre, text=21-i, borderwidth=1, relief="solid", width=8, height=3)
        elif j==0 and i>0 and i==10:
            case= Label(fenetre, text="2-11", borderwidth=1, relief="solid", width=8, height=3)
        elif j==0 and i==11:
            case= Label(fenetre, text="AS 18/20", borderwidth=1, relief="solid", width=8, height=3)
        elif j==0 and i>11 and i<20:
            case= Label(fenetre, text=f"AS {29-i}", borderwidth=1, relief="solid", width=8, height=3)
        else:
            case= Label(fenetre, text=" ", borderwidth=1, relief="solid", width=8, height=3)
        case.grid(row=i, column=j)
        ligne.append(case)
    tableau.append(ligne)

index=0
for i in range(1,11):
    # i -> colonnes
    for j in reversed(range(1,11)):
        # j-> lignes
        if list_chromosomes[index_b][index]==1:
            tableau[j][i].configure(bg="green")
            index+=1
        else:
            tableau[j][i].configure(bg="red")
            index+=1
    for j in range(13,22):
        
        if list_chromosomes[index_b][index]==1:
            tableau[12-j][i].configure(bg="green")
            index+=1
        else:
            tableau[12-j][i].configure(bg="red")
            index+=1
        
    


fenetre.mainloop()  
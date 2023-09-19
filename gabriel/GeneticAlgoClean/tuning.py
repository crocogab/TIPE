from individu import Individu
import json
from tkinter import *

#Ne pas oublier changer precision (*10 ou *20)

with open(r'C:\Users\croco\Documents\GitHub\TIPE\gabriel\training.json') as training_file:
    data = json.load(training_file)


list_chromosomes = []
liste_finale=[]

index_b=0


for chromosome in data['chromosomes']:
    chromo_actu=[]
    for i in range(190):
        
        chromo_actu.append(int(chromosome[i]))
    list_chromosomes.append(chromo_actu)

best_score=0
best_individu=None

for elem in list_chromosomes:
    i1=Individu()
    i1.chromosomes=elem
    i1.evaluate()
    if i1.fitness>best_score:
        best_individu=i1
        best_score=i1.fitness
        index_b=list_chromosomes.index(elem)
    liste_finale.append(i1)

# i1 est mtn le best individu

tab=[[0,0] for i in range(10)] # Vert | Rouge

for i in range(2,12):
    for j in range(15,21):
        if i1.chromosomes[i1.convert(j,False,i)]:
            tab[i-2][0]+=1
        else:
            tab[i-2][1]+=1


fenetre1 = Tk()
fenetre1.title('DEBUG 1')

tableau = []
for i in range(20):
    ligne=[]
    for j in range(11):
        if j>0 and j<10 and i==0:
            case= Label(fenetre1, text=j+1, borderwidth=1, relief="solid", width=8, height=3)
        elif j==10 and i==0:
            case= Label(fenetre1, text="AS", borderwidth=1, relief="solid", width=8, height=3)
        elif j==0 and i>0 and i<10:
            case= Label(fenetre1, text=21-i, borderwidth=1, relief="solid", width=8, height=3)
        elif j==0 and i>0 and i==10:
            case= Label(fenetre1, text="2-11", borderwidth=1, relief="solid", width=8, height=3)
        elif j==0 and i==11:
            case= Label(fenetre1, text="AS 18/20", borderwidth=1, relief="solid", width=8, height=3)
        elif j==0 and i>11 and i<20:
            case= Label(fenetre1, text=f"AS {29-i}", borderwidth=1, relief="solid", width=8, height=3)
        else:
            case= Label(fenetre1, text=" ", borderwidth=1, relief="solid", width=8, height=3)
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
        
    


  

for i in range(2,12):
    for j in range(15,21):
        if tab[i-2][0]<tab[i-2][1]:
            if i1.chromosomes[i1.convert(j,False,i)]:
    
                score_avant=i1.fitness
                i1.chromosomes[i1.convert(j,False,i)]=0
                i1.evaluate()
                if i1.fitness<score_avant:
                    
                    i1.chromosomes[i1.convert(j,False,i)]=1

for i in range(190):
    list_chromosomes[index_b][i]=i1.chromosomes[i]

fenetre2=Toplevel()
fenetre2.title('DEBUG 2')

tableau2 = []
for i in range(20):
    ligne=[]
    for j in range(11):
        if j>0 and j<10 and i==0:
            case= Label(fenetre2, text=j+1, borderwidth=1, relief="solid", width=8, height=3)
        elif j==10 and i==0:
            case= Label(fenetre2, text="AS", borderwidth=1, relief="solid", width=8, height=3)
        elif j==0 and i>0 and i<10:
            case= Label(fenetre2, text=21-i, borderwidth=1, relief="solid", width=8, height=3)
        elif j==0 and i>0 and i==10:
            case= Label(fenetre2, text="2-11", borderwidth=1, relief="solid", width=8, height=3)
        elif j==0 and i==11:
            case= Label(fenetre2, text="AS 18/20", borderwidth=1, relief="solid", width=8, height=3)
        elif j==0 and i>11 and i<20:
            case= Label(fenetre2, text=f"AS {29-i}", borderwidth=1, relief="solid", width=8, height=3)
        else:
            case= Label(fenetre2, text=" ", borderwidth=1, relief="solid", width=8, height=3)
        case.grid(row=i, column=j)
        ligne.append(case)
    tableau2.append(ligne)

index=0
for i in range(1,11):
    # i -> colonnes
    for j in reversed(range(1,11)):
        # j-> lignes
        if list_chromosomes[index_b][index]==1:
            tableau2[j][i].configure(bg="green")
            index+=1
        else:
            tableau2[j][i].configure(bg="red")
            index+=1
    for j in range(13,22):
        
        if list_chromosomes[index_b][index]==1:
            tableau2[12-j][i].configure(bg="green")
            index+=1
        else:
            tableau2[12-j][i].configure(bg="red")
            index+=1



fenetre1.mainloop()  
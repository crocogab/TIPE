from individu import Individu 
from tkinter import *





i1=Individu()

i1.chromosomes[i1.convert(12,False,2)]=1
i1.chromosomes[i1.convert(11,False,2)]=1
i1.chromosomes[i1.convert(12,False,3)]=1
i1.chromosomes[i1.convert(11,False,3)]=1
i1.chromosomes[i1.convert(11,False,4)]=1
i1.chromosomes[i1.convert(11,False,5)]=1
i1.chromosomes[i1.convert(11,False,6)]=1
i1.chromosomes[i1.convert(11,False,7)]=1
i1.chromosomes[i1.convert(11,False,8)]=1
i1.chromosomes[i1.convert(11,False,9)]=1
i1.chromosomes[i1.convert(11,False,10)]=1
i1.chromosomes[i1.convert(11,False,1)]=1
for i in range(5):
    i1.chromosomes[i1.convert(12+i,False,7)]=1
for i in range(5):
    i1.chromosomes[i1.convert(12+i,False,8)]=1
for i in range(5):
    i1.chromosomes[i1.convert(12+i,False,9)]=1


for i in range(5):
    i1.chromosomes[i1.convert(12+i,False,10)]=1

for i in range(5):
    i1.chromosomes[i1.convert(12+i,False,1)]=1


for i in range(8):
    i1.chromosomes[i1.convert(10+i,True,1)]=1

for i in range(8):
    i1.chromosomes[i1.convert(10+i,True,10)]=1

for i in range(8):
    i1.chromosomes[i1.convert(10+i,True,9)]=1

for i in range(7):
    i1.chromosomes[i1.convert(10+i,True,8)]=1

for i in range(7):
    i1.chromosomes[i1.convert(10+i,True,7)]=1

for i in range(7):
    i1.chromosomes[i1.convert(10+i,True,6)]=1
for i in range(7):
    i1.chromosomes[i1.convert(10+i,True,5)]=1
for i in range(7):
    i1.chromosomes[i1.convert(10+i,True,4)]=1
for i in range(7):
    i1.chromosomes[i1.convert(10+i,True,3)]=1
for i in range(8):
    i1.chromosomes[i1.convert(10+i,True,2)]=1
list_chromosomes=[]
chromo_actu=[]
i1.evaluate()
print(i1.fitness)
for i in range(190):
        
    chromo_actu.append(int(i1.chromosomes[i]))
    list_chromosomes.append(chromo_actu)

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
        if list_chromosomes[0][index]==1:
            tableau[j][i].configure(bg="green")
            index+=1
        else:
            tableau[j][i].configure(bg="red")
            index+=1
    for j in range(13,22):
        
        if list_chromosomes[0][index]==1:
            tableau[12-j][i].configure(bg="green")
            index+=1
        else:
            tableau[12-j][i].configure(bg="red")
            index+=1
        

fenetre.mainloop()  
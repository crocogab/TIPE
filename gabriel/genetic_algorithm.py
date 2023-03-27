import random as rd




def aux(tab,i,a):
    for n in range(10):
        value=a
        value+=rd.choices([l for l in range(1,11)],weights=[10,10,10,10,10,10,10,10,10,30],k=1)[0]
        if value>21:
            value=0
        else:
            if value < tab[i][n]:
                value=1
            else:
                value=0
        tab[i][n]=value


class Genes:
    
    
    def __init__(self,tab:list) -> None:
        self.tab = tab
    
    def build_tab(self)->None:
        self.tab = [[rd.randint(0,1) for _ in range(10)]for _ in range(15)]
    
    def build_selection_tab(self) -> None:
        self.tab = [[i for i in range(2,12)]for _ in range(15)]
        for i in range(16):
            if i==0:
                aux(self.tab,i,20)
            elif i==1:
                aux(self.tab,i,19)


        





    def show(self) -> None:
        for i in range(len(self.tab)):
            print(f"Indice {i+1} tab : {self.tab[i]}\n")
    


class Individu:
    def __init__(self,generation:int,fitness:float=0.0,genes:Genes=None)->None:
        self.generation = generation
        self.fitness = fitness
        self.genes = genes
    

gen1= Individu(1,genes=Genes([]))
# gen1.genes.build_selection_tab()
# gen1.genes.build_tab()
gen1.genes.show()


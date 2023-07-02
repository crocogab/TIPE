data = [[1,0],[2,35573],[3,8459158],[4,10007352],[5,1456682],[6,40980],[7,255],[8,0],[9,0],[10,0]]
import matplotlib.pyplot as plt
import numpy as np


# plot a bar chart
def plot_bar(data):
    x = [i[0] for i in data]
    y = [i[1] for i in data]
    title = "Nombre de cartes en main pour finir la partie"
    legendy = "Nombre de parties"
    legendx = "Nombre de cartes en main"
    nbr_total = sum(y)
    # display nbr_total in the graph
    plt.text(6, 2.5*1e6, "Nombre total de parties: " + str(nbr_total), fontsize=22)
    # make title and labels bigger
    plt.rcParams.update({'font.size': 22})
    # make x and y labels bigger
    plt.rcParams['xtick.labelsize'] = 22
    label = [str(i) for i in x]
    plt.bar(x, y)
    # set y scale to log
    plt.yscale('log')
    plt.xticks(x, label)
    plt.title(title)
    plt.xlabel(legendx, fontsize=22)
    plt.ylabel(legendy, fontsize=22)
    plt.show()
plot_bar(data)
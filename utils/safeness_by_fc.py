import numpy as np

data = np.genfromtxt("data.csv", delimiter=",",names=["croup_fst", "win", "safeness"])
croup_fst = data["croup_fst"]
win = data["win"]
safeness = data["safeness"]
import matplotlib.pyplot as plt
ITERATIONS = 100000

# for each first card of the croupier, determine the best safeness value (the one with the highest winrate)
for i in range(1,11):
    winrate = []
    for j in np.arange(0,1,0.0625):
        winrate.append(np.sum(win[np.logical_and(croup_fst == i, safeness == j)])/ITERATIONS)
    plt.plot(np.arange(0,1,0.0625), winrate, label=i)
    # label the axes
    plt.xlabel("safeness")
    plt.ylabel("winrate")
plt.legend()
plt.show()
# plot best safeness value for each first card of the croupier
best_safeness = []
for i in range(1,11):
    winrate = []
    for j in np.arange(0,1,0.0625):
        winrate.append(np.sum(win[np.logical_and(croup_fst == i, safeness == j)])/ITERATIONS)
    best_safeness.append(np.argmax(winrate)*0.0625)
plt.plot(np.arange(1,11), best_safeness, label="best safeness value")
# label the axes
plt.xlabel("first card of the croupier")
plt.ylabel("best safeness value")
plt.show()

# print a list where l[i] is the best safeness to use
l = []
for i in range(1,11):
    winrate = []
    for j in np.arange(0,1,0.0625):
        winrate.append(np.sum(win[np.logical_and(croup_fst == i, safeness == j)])/ITERATIONS)
    l.append(np.argmax(winrate)*0.0625)
print(l)
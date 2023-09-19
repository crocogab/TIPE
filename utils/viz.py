import csv
import matplotlib.pyplot as plt

GAME_NUMBER = 100

with open("../hector/data.csv", "r") as f:
    reader = csv.reader(f)
    data = list(reader)
    mydict = {}
    for row in data:
        # Data is in the form of: 0,safeness where 0 is the game lost and 1 is the game won and safeness is the safeness of the game
        # we want to store the win/loss as a value of the safeness key
        if row[1] not in mydict:
            mydict[row[1]] = [0, 0]
        if row[0] == "0":
            mydict[row[1]][0] += 1
        else:
            mydict[row[1]][1] += 1

    # plot two bars for each safeness, to visualize loss/win and offset the bars to make them side by side
    plt.bar(
        [float(x) - 0.02 for x in mydict.keys()],
        [x[0] for x in mydict.values()],
        width=0.04,
        color="red",
        align="center",
    )
    plt.bar(
        [float(x) + 0.02 for x in mydict.keys()],
        [x[1] for x in mydict.values()],
        width=0.04,
        color="green",
        align="center",
    )
    plt.xlabel("Safeness")
    plt.ylabel("Number of Games")
    plt.show()

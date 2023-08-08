import csv
import matplotlib.pyplot as plt

with open("data.csv","r") as f:
    reader = csv.reader(f)
    data = list(reader)
    # first column is the result of the game, second is the safeness
    # we want to plot a bar chart with in green a bar for the number of games won and in red the number of games lost for each safeness
    dict = {}
    for row in data:
        try:
            dict[row[1]]["won"] += int(row[0])
            dict[row[1]]["lost"] += 1 - int(row[0])
        except KeyError:
            dict[row[1]] = {"won":int(row[0]),"lost":1-int(row[0])}
    print(dict)
    plt.bar(dict.keys(),[dict[key]["won"] for key in dict.keys()],color="green")
    plt.bar(dict.keys(),[dict[key]["lost"] for key in dict.keys()],color="red")
    plt.show()

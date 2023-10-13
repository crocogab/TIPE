import csv
import matplotlib.pyplot as plt

with open("data.csv", "r") as f:
    reader = csv.reader(f)
    data = list(reader)
    mydict = {}
    for row in data:
        try:
            mydict[row[1]]["won"] += int(row[0])
            mydict[row[1]]["lost"] += 1 - int(row[0])
        except KeyError:
            mydict[row[1]] = {"won": int(row[0]), "lost": 0}
    print(mydict)
    # display the red bar and the green bar for lost and won beside each other
    plt.bar(
        [float(key) - 0.006 for key in mydict.keys()],
        [mydict[key]["won"] for key in mydict.keys()],
        color="green",
        width=0.01,
    )
    plt.bar(
        [float(key) + 0.006 for key in mydict.keys()],
        [mydict[key]["lost"] for key in mydict.keys()],
        color="red",
        width=0.01,
    )
    # y scale log
    plt.yscale("log")
    plt.show()

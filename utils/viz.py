import csv
import matplotlib.pyplot as plt

with open("data2.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    data = list(reader)
    mydict = {}
    for row in data:
        try:
            mydict[row[1]]["won"] += int(row[0])
            mydict[row[1]]["lost"] += 1 - int(row[0]) 
        except KeyError:
            mydict[row[1]] = {"won": int(row[0]), "lost": 1 - int(row[0])}

    plt.bar(
        [float(key) for key in mydict.keys()],
        [mydict[key]["won"] / (mydict[key]["won"] + mydict[key]["lost"]) * 100 for key in mydict.keys()],
        color="green",
        width=0.005,
    )
    plt.show()
    print(f"The best winrate is {max([mydict[key]['won'] / (mydict[key]['won'] + mydict[key]['lost']) for key in mydict.keys()]) * 100}% at safeness {max(mydict, key=lambda x: mydict[x]['won'] / (mydict[x]['won'] + mydict[x]['lost']))}")
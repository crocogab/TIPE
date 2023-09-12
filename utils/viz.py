import csv
import matplotlib.pyplot as plt

with open("data.csv","r") as f:
    reader = csv.reader(f)
    data = list(reader)
    mydict = {}
    for row in data:
        try:
            mydict[row[1]]["won"] += int(row[0])
            mydict[row[1]]["lost"] += 1 - int(row[0])
        except KeyError:
            mydict[row[1]] = {"won":int(row[0]),"lost":1-int(row[0])}
    print(mydict)
    plt.bar(mydict.keys(),[mydict[key]["won"] for key in mydict.keys()],color="green")
    plt.bar(mydict.keys(),[mydict[key]["lost"] for key in mydict.keys()],color="red")
    plt.show()
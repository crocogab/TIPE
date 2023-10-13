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
            mydict[row[1]] = {"won": int(row[0]), "lost": 1 - int(row[0])}

# Extract unique "safeness" values and sort them for the x-axis
safeness_values = sorted(set(float(key) for key in mydict.keys()))

# Calculate the number of wins and losses for each "safeness" value
won_counts = [mydict[str(safe)]["won"] if str(safe) in mydict else 0 for safe in safeness_values]
lost_counts = [mydict[str(safe)]["lost"] if str(safe) in mydict else 0 for safe in safeness_values]

# Create the bar chart
width = 0.4
plt.bar([safe - width/2 for safe in safeness_values], won_counts, width=width, color="green", label="Won")
plt.bar([safe + width/2 for safe in safeness_values], lost_counts, width=width, color="red", label="Lost")

plt.xlabel("Safeness")
plt.ylabel("Count")
plt.title("Wins and Losses by Safeness")
plt.xticks(safeness_values)
plt.legend()

plt.show()

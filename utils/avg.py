
def read():
    with open("blackjack.csv", "r") as f:
        # make an average of the data
        data = f.readlines()
        data = [int(i) for i in data]
        return sum(data) / len(data)


print(read())


def max10():
    # return tuples of the count of each value
    with open("blackjack.csv", "r") as f:
        data = f.readlines()
        data = [int(i) for i in data]
        return [(i, data.count(i)) for i in range(1, 11)]


print(max10())

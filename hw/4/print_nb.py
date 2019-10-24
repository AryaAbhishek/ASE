from hw4 import Table, NB, ABCD, fromString
import csv
if __name__ == "__main__":
    file = ""
    with open('weathernon.csv','r') as lines:
        reader = csv.reader(lines, delimiter=' ', quotechar='|')
        for row in reader:
            file += ','.join(row)
            file += '\n'
    tbl = Table()
    nb = NB()
    ab = ABCD()
    lines = fromString(file)
    train_count = 4
    for i, row in enumerate(lines):
        if i == 0:
            nb.NBTrain(i, row)
        else:
            if i < train_count:
                nb.NBTrain(i, row)
            else:
                classify = nb.NBClassify(i, row)
                ab.ABCD1(row[-1], classify)
                nb.NBTrain(i, row)
    file1 = open("output2.txt", 'w+')
    file1.write("#--- nbok -------------------------\n")
    file1.write("weathornon \n")
    string = ab.ABCD_report()
    for s in string:
        file1.write(s)

    file = ""
    with open('diabetes.csv', 'r') as lines:
        reader = csv.reader(lines, delimiter=' ', quotechar='|')
        for row in reader:
            file += ','.join(row)
            file += '\n'
    tbl = Table()
    nb = NB()
    ab = ABCD()
    lines = fromString(file)
    train_count = 4
    for i, row in enumerate(lines):
        if i == 0:
            nb.NBTrain(i, row)
        else:
            if i < train_count:
                nb.NBTrain(i, row)
            else:
                classify = nb.NBClassify(i, row)
                ab.ABCD1(row[-1], classify)
                nb.NBTrain(i, row)
    file1.write("\n diabetes \n")
    string = ab.ABCD_report()
    for s in string:
        file1.write(s)
    file1.close()
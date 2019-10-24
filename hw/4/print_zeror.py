from hw4 import Table, ZeroR, ABCD, fromString
import csv
if __name__ == "__main__":
    file = ""
    with open('weathernon.csv','r') as lines:
        reader = csv.reader(lines, delimiter=' ', quotechar='|')
        for row in reader:
            file += ','.join(row)
            file += '\n'
    tbl = Table()
    zr = ZeroR(1)
    ab = ABCD()
    lines = fromString(file)
    train_count = 3
    for i, row in enumerate(lines):
        if i == 0:
            zr.train(i, row)
        else:
            if i<train_count:
                zr.train(i, row)
            else:
                classify = zr.classify(i, row)
                # print(row[-1], classify)
                ab.ABCD1(row[-1],classify)
                zr.train(i, row)
    file1 = open("output1.txt", 'w+')
    file1.write("#--- Zeror -------------------------\n")
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
    zr = ZeroR(1)
    ab = ABCD()
    lines = fromString(file)
    train_count = 3
    for i, row in enumerate(lines):
        if i == 0:
            zr.train(i, row)
        else:
            if i < train_count:
                zr.train(i, row)
            else:
                classify = zr.classify(i, row)
                # print(classify, row[-1])
                ab.ABCD1(row[-1], classify)
                zr.train(i, row)
    file1.write("\n diabetes \n")
    string = ab.ABCD_report()
    for s in string:
        file1.write(s)
    file1.close()
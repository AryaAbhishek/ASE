import csv
from hw7 import *
from hw6 import *

if __name__ == '__main__':
    hw = "auto.csv"
    file = ""
    with open(hw, 'r') as lines:
        reader = csv.reader(lines, delimiter=' ', quotechar='|')
        for row in reader:
            file += ','.join(row)
            file += '\n'
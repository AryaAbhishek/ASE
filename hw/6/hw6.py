# from thing import *
from Div1 import *
from hw4 import *
import csv


def leaf_result(val, n):
    if val == 'p':
        return {'val': "tested_positive", 'n': n}
    if val == 'n':
        return {'val': "tested_negetive", 'n': n}
    return {'val': val, 'n': n}


def tree_result(l, h, n, text, childs):
    return {"low": l, "high": h, "n": n, "text": text, "childs": childs}


def split(rows, cut, column):
    left, low = rows[:cut], rows[cut][column.pos]
    right, high = rows[cut:], rows[cut + 1][column.pos]
    return [(-float('inf'), low, left), (high, float('inf'), right)]


def tree():
    index = table.goals[0]-1
    type = "sym" if index+1 in table.syms else "num"
    data = list(map(lambda row: row.cells, table.rows))
    if type == "sym":
        for row in data:
            row[index] = 'p' if row[index] == "tested_positive" else 'n'
    return get_tree(data, index, type, 0)


def get_tree(rows, index, type, level):
    if len(rows) >= 4:
        low, cut, column = 10 ** 32, None, None
        col_types = []
        for col in table.cols:
            if isinstance(col, Num):
                col_types.append("num")
            else:
                col_types.append("sym")
        for col in table.cols:
            if col.pos == index:
                continue
            temp = []
            for row in rows:
                temp.append([row[col.pos], row[index]])
            x = Div(temp, col_types[index])
            cut1, low1 = x.cut, x.best
            if cut1 and low1:
                if low1 < low:
                    cut, low, column = cut1, low1, col
        if cut and cut >= 5: # limit for auto.csv
            return [tree_result(low, high, len(childs), column.col_name, get_tree(childs, index, type, level + 1))
                    for low, high, childs in split(rows, cut, column)]
    return leaf_result(rows[len(rows) // 2][index], len(rows))


def show(tree, level=0):
    if isinstance(tree, list):
        for each in tree:
            show(each, level)
    else:
        for _ in range(level):
            print("| ", end=" ")
        # print(tree)
        print("{0} = {1}...{2}".format(tree['text'], tree['low'], tree['high']), end=" ")
        if not isinstance(tree['childs'], list):
            print("{0} ({1})".format(tree['childs']['val'], tree['childs']['n']))
        else:
            for each in tree['childs']:
                print("")
                show(each, level + 1)


def parse_lines(lines):
    for i, row in enumerate(lines):
        row = [x for x in row if x != ""]
        table.read_lines(i, row)


if __name__ == '__main__':
    hw = 'auto.csv'
    # hw = 'diabetes.csv'
    file = ""
    with open(hw, 'r') as lines:
        reader = csv.reader(lines, delimiter=' ', quotechar='|')
        for row in reader:
            file += ','.join(row)
            file += '\n'
    table = Table()
    lines = fromString(file)
    parse_lines(lines)
    result = tree()
    for res in result:
        show(res)
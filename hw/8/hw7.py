import random, math
from hw4 import Num, Table, cells, rows, file, fromString
seed = random.seed
import csv

# Build a distance function that reports the distance between two rows:


def distance(i, j, cols):
    d = n = 0
    p = 2
    # print(cols)
    for col in cols:
        n += 1
        d0 = col.dist(i.cells[col.pos], j.cells[col.pos])
        d += (d0 ** p)
        # normalize distance
    # print(p, n)
    return d ** (1 / p) / n ** (1 / p)


# Divide the data


def cosine_distance(x, y, z, cols, dist):
    return (distance(x, z, cols) ** 2 + dist ** 2 - distance(y, z, cols) ** 2) / (2 * dist)


class random_projection_tree:
    def __init__(self):
        self.leaves = []
        self.children = []
        self.level = 0
        self.split_count = 0
        self.is_root = False


def print_tree(root):
    temp = ""
    if not root.is_root:
        for i in range(root.level):
            temp += "|. "
    print(temp + str(root.split_count))
    temp = ""
    if len(root.children) == 0:
        for j in range(root.level - 1):
            temp += "|. "
        for col in root.leaves:
            temp += col.col_name + " = "
            if isinstance(col, Num):
                temp += "{0} {1}".format(col.mu, col.sd)
            else:
                temp += "{0} {1}".format(col.mode, col.sym_ent())
        print(temp)
    else:
        for each in root.children:
            print_tree(each)
    temp = ""
    if root.is_root:
        for col in root.leaves:
            temp += col.col_name + " = "
            if isinstance(col, Num):
                temp += "{0} {1}".format(col.mu, col.sd)
            else:
                temp += "{0} {1}".format(col.mode, col.sym_ent())
        print(temp)


class hw7:
    def __init__(self, lines):
        seed(1)
        self.table = Table()
        self.lines = lines
        self.parse_lines()
        self.tree = self.split_point(self.table, 0)
        print_tree(self.tree)

    def parse_lines(self):
        # print("hello")
        for i, row in enumerate(self.lines):
            row = [x for x in row if x != ""]
            self.table.read_lines(i, row)

    def split_point(self, table, level):
        # print("hello split")
        node = random_projection_tree()
        if len(table.rows) < 2 * pow(len(self.table.rows), 1 / 2):
            for each in table.goals:
                node.leaves.append(table.cols[each-1])
            node.split_count = len(table.rows)
            node.level = level
            return node
        else:
            _, best_points = self.best_pivot_points(table)
            left_table, right_table = Table(), Table()
            left_table.read_lines(0, [col.col_name for col in table.cols])
            right_table.read_lines(0, [col.col_name for col in table.cols])
            for i, each in enumerate(table.rows):
                if i in best_points:
                    right_table.read_lines(i+1, each.cells)
                else:
                    left_table.read_lines(i+1, each.cells)
            split_count = len(left_table.rows) + len(right_table.rows)
            node.children.append(self.split_point(left_table, level + 1))
            node.children.append(self.split_point(right_table, level + 1))
            node.split_count = split_count
            node.level = level
            return node

    def fast_map(self, table):
        # print("fast_map")
        cols = [table.cols[col] for col in table.xs]
        # print(table.rows)
        # print(len(table.cols))
        # print(len(table.rows))
        random_point = random.randint(0, len(table.rows)-1)
        pivot1, pivot2 = [], []
        for row in range(0, len(table.rows)):
            dist = distance(table.rows[random_point], table.rows[row], cols)
            pivot1.append((row, dist))
        pivot1.sort(key=lambda x: x[1])
        pivot1_index = pivot1[math.floor(len(pivot1) * 0.9)][0]

        for row in range(0, len(table.rows)):
            dist = distance(table.rows[pivot1_index], table.rows[row], cols)
            pivot2.append((row, dist))

        pivot2.sort(key=lambda x: x[1])
        dist = pivot2[math.floor(len(pivot2) * 0.9)][1]
        pivot2_Index = pivot2[math.floor(len(pivot2) * 0.9)][0]
        return pivot1_index, pivot2_Index, dist

    def best_pivot_points(self, table):
        # print("best_pivot")
        count = 10
        start = len(table.rows)
        # left_split, right_split = 0, 0
        best_tuple, best_point = None, None
        while count > 0:
            final_list = []
            count -= 1
            pivot_tuple = self.fast_map(table)
            # print(table.xs)
            cols = [table.cols[col] for col in table.xs]
            for row in range(0, len(table.rows)):
                dist = cosine_distance(table.rows[pivot_tuple[0]], table.rows[pivot_tuple[1]], table.rows[row], cols, pivot_tuple[2])
                final_list.append((row, dist))
            final_list.sort(key=lambda x: x[1])

            list_length = len(final_list)
            index = (list_length - 1) // 2
            if list_length % 2 !=0:
                mid_dist = (final_list[index + 1][1] + final_list[index][1] ) / 2.0
            else:
                mid_dist = final_list[index][1]

            point1 = set()
            for point in final_list:
                if  mid_dist < point[1]:
                    point1.add(point[0])

            right = abs((list_length - len(point1))- len(point1))

            if start > right:
                start = right
                best_tuple = pivot_tuple
                best_point = point1

        return best_tuple, best_point


if __name__ == '__main__':
    # hw = 'pom310000.csv'
    hw = 'xomo10000.csv'
    file = ""
    with open(hw, 'r') as lines:
        reader = csv.reader(lines, delimiter=' ', quotechar='|')
        for row in reader:
            file += ','.join(row)
            file += '\n'
    lines = fromString(file)
    hw7(lines)
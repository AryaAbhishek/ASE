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


class RandomProjectionTree:
    def __init__(self):
        self.leaves = []
        self.children = []
        self.level = 0
        self.splitCnt = 0
        self.isItRoot = False


def printTree(root):
    temp = ""
    if not root.isItRoot:
        for i in range(root.level):
            temp += "|. "
    print(temp + str(root.splitCnt))
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
            printTree(each)
    temp = ""
    if root.isItRoot:
        for col in root.leaves:
            temp += col.column_name + " = "
            if isinstance(col, Num):
                temp += "{0} {1}".format(col.mu, col.sd)
            else:
                temp += "{0} {1}".format(col.mode, col.sym_ent())
        print(temp)


class hw7:
    def __init__(self, lines):
        seed(1)
        self.table = Table()
        self.content = lines
        self.parse()
        self.tree = self.splitPoint(self.table, 0)
        printTree(self.tree)

    def parse(self):
        for i, row in enumerate(self.content):
            row = [x for x in row if x != ""]
            self.table.read_lines(i, row)

    def splitPoint(self, table, level):
        treeNode = RandomProjectionTree()
        if len(table.rows) < 2 * pow(len(self.table.rows), 1 / 2):
            for each in table.goals:
                treeNode.leaves.append(table.cols[each-1])
            treeNode.splitCnt = len(table.rows)
            treeNode.level = level
            return treeNode
        else:
            best_tuple, best_points = self.maxPivotPoints(table)
            leftOfTable = Table()
            rightOfTable = Table()

            leftOfTable.read_lines(0, [col.col_name for col in table.cols])
            rightOfTable.read_lines(0, [col.col_name for col in table.cols])
            for i, each in enumerate(table.rows):
                if i in best_points:
                    rightOfTable.read_lines(i+1, each.cells)
                else:
                    leftOfTable.read_lines(i+1, each.cells)
            splitCount = len(leftOfTable.rows) + len(rightOfTable.rows)
            treeNode.children.append(self.splitPoint(leftOfTable, level + 1))
            treeNode.children.append(self.splitPoint(rightOfTable, level + 1))
            treeNode.splitCnt = splitCount
            treeNode.level = level
            return treeNode

    def fastMap(self, table):
        # print("table.xs", table.xs)
        cols = [table.cols[col] for col in table.xs]
        # print(table.rows)
        # print(len(table.cols))
        # print(len(table.rows))
        randPoint = random.randint(0, len(table.rows)-1)
        pivot1 = []
        pivot2 = []
        for row in range(0, len(table.rows)):
            dist = distance(table.rows[randPoint], table.rows[row], cols)
            pivot1.append((row, dist))
        pivot1.sort(key=lambda x: x[1])
        pivot1_Idx = pivot1[math.floor(len(pivot1) * 0.9)][0]

        for row in range(0, len(table.rows)):
            dist = distance(table.rows[pivot1_Idx], table.rows[row], cols)
            pivot2.append((row, dist))

        pivot2.sort(key=lambda x: x[1])
        dist = pivot2[math.floor(len(pivot2) * 0.9)][1]
        pivot2_Idx = pivot2[math.floor(len(pivot2) * 0.9)][0]
        return pivot1_Idx, pivot2_Idx, dist

    def maxPivotPoints(self, table):
        cnt = 10
        start = len(table.rows)
        # left_split, right_split = 0, 0
        maxTuple = None
        maxPoints = None
        while cnt > 0:
            completeList = []
            cnt -= 1
            PivotTuple = self.fastMap(table)
            # print(table.xs)
            cols = [table.cols[col] for col in table.xs]
            for row in range(0, len(table.rows)):
                dist = cosine_distance(table.rows[PivotTuple[0]], table.rows[PivotTuple[1]], table.rows[row], cols, PivotTuple[2])
                completeList.append((row, dist))
            completeList.sort(key=lambda x: x[1])

            listLen = len(completeList)
            idx = (listLen - 1) // 2
            if listLen % 2 !=0 :
                mDist = (completeList[idx + 1][1] + completeList[idx][1] ) / 2.0
            else:
                mDist = completeList[idx][1]

            pt1 = set()
            for pt in completeList:
                if  mDist < pt[1]:
                    pt1.add(pt[0])

            right = abs((listLen - len(pt1))- len(pt1))

            if start > right:
                start = right
                maxTuple = PivotTuple
                maxPoints = pt1

        return maxTuple, maxPoints


if __name__ == '__main__':
    hw = 'pom310000.csv'
    # hw = 'xomo10000.csv'
    file = ""
    with open(hw, 'r') as lines:
        reader = csv.reader(lines, delimiter=' ', quotechar='|')
        for row in reader:
            file += ','.join(row)
            file += '\n'
    lines = fromString(file)
    hw7(lines)
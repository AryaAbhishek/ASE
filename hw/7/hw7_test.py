import random, math
from hw4 import Num, Table, cells, rows, file
seed = random.seed

# Build a distance function that reports the distance between two rows:


def distance(i, j, cols):
    d = n = 0
    p = 2
    for col in cols:
        n = n + 1
        d0 = col.dist(i.cells[col.pos], j.cells[col.pos])
        d = d +(d0 ** p)
        # normalize distance
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
    if  root.isRoot != True:
        for i in range(root.level):
            print("|. ")

    print(root.splitCount)
    if len(root.children) == 0:
        for j in range(root.level - 1):
            print("|. ")
        for col in root.leaves:
            print(col.column_name + " = ")
            if isinstance(col, Num):
                print("{0} {1}".format(col.mu, col.sd))
            else:
                print("{0} {1}".format(col.mode, col.entropy))
        print("\n")
    else:
        for each in root.children:
            printTree(each)
    if root.isRoot:
        for col in root.leaves:
            print(col.column_name + " = ")
            if isinstance(col, Num):
                print("{0} {1}".format(col.mu, col.sd))
            else:
                print("{0} {1}".format(col.mode, col.entropy))


class hw7:
    def __init__(self, file_name):
        seed(1)
        self.table = Table()
        self.content = cells(rows(file(file_name)))
        self.tree = self.splitPoint(self.table, 0)
        self.parse()
        printTree(self.tree)

    def parse(self):
        for i, row in enumerate(self.content):
            if i != 0:
                self.table.addRow(row)
            else:
                self.table.addCol(row)

    def splitPoint(self, table, level):
        treeNode = RandomProjectionTree()
        if len(table.rows) < 2 * pow(len(self.table.rows), 1 / 2):
            for each in table.goals:
                treeNode.leaves.append(table.cols[each])
            treeNode.splitCnt = len(table.rows)
            treeNode.level = level
            return treeNode
        else:
            best_tuple, best_points = self.maxPivotPoints(table)
            leftOfTable = Table()
            rightOfTable = Table()

            leftOfTable.read([col.col_name for col in table.cols])
            rightOfTable.read([col.column_name for col in table.cols])
            for i, each in enumerate(table.rows):
                if i in best_points:
                    rightOfTable.addRow(each.cells)
                else:
                    leftOfTable.addRow(each.cells)
            splitCount = len(leftOfTable.rows) + len(rightOfTable.rows)
            treeNode.children.append(self.splitPoint(leftOfTable, level + 1))
            treeNode.children.append(self.splitPoint(rightOfTable, level + 1))
            treeNode.splitCnt = splitCount
            treeNode.level = level
            return treeNode

    def fastMap(self, table):
        cols = [table.cols[col] for col in table.xs]
        print(table.rows)
        print(len(table.cols))
        print(len(table.rows))
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

            cols = [table.cols[col] for col in table.xs]
            for row in range(0, len(table.rows)):
                dist = cosine_distance(table.rows[PivotTuple[0]], table.rows[PivotTuple[1]], table.rows[row], PivotTuple[2], cols)
                completeList.append((row, dist))
            completeList.sort(key=lambda x: x[1])

            listLen = len(completeList)
            idx = (listLen - 1) // 2
            if listLen % 2 !=0 :
                mDist = (completeList[idx + 1][1] + completeList[idx][1] ) / 2.0
            else:
                mDist = completeList[idx][1]

            pt = set()
            for pt in completeList:
                if  mDist < pt[1]:
                    pt.add(pt[0])

            right = abs((listLen - len(pt))- len(pt))

            if start > right:
                start = right
                maxTuple = PivotTuple
                maxPoints = pt

        return maxTuple, maxPoints


if __name__ == '__main__':
    hw7 = hw7('pom310000.csv')
    #hw7 = hw7('xomo10000.csv')

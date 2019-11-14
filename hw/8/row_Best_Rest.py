import csv
from hw7 import *
from hw6 import *
r = random.randint
seed = random.seed

class hw8:
    def __init__(self, lines):
        seed(1)
        self.table = Table()
        self.lines = lines
        self.parse_lines()
        self.random_rows = self.get_100_random_rows()
        self.goals = self.get_all_goals()

    def parse_lines(self):
        # print("hello")
        for i, row in enumerate(self.lines):
            row = [x for x in row if x != ""]
            self.table.read_lines(i, row)

    def dominates(self, i, j, goals): # i and j are rows.
        z = 0.00001
        s1, s2, n = z,z,z+len(goals)
        for goal in goals:
          a,b = i.cells[goal.pos], j.cells[goal.pos]
          a,b = goal.num_norm(a), goal.num_norm(b)
          s1 -= 10**(goal.weight * (a-b)/n)
          s2 -= 10**(goal.weight * (b-a)/n)
        return s1/n - s2/n # i is better if it losses least (i.e. this number under 0)

    def get_100_random_rows(self):
        l = len(self.table.rows)
        return [self.table.rows[r(0,l-1)] for _ in range(100)]

    def get_all_goals(self):
        # print(self.table.goals, len(self.table.cols))
        return [self.table.cols[idx-1] for idx in self.table.goals]

    def print_rows_best_rest(self):
        values = self.sort_rows_using_random_rows()
        cols = [each.col_name for each in self.table.cols]
        print("\t", end="\t")
        for each in cols:
            print(each, end="\t")
        print("")
        for each in values[-4:]:
            print("best", end="\t")
            for val in each[1].cells:
                print(val, end="\t")
            print("")
        print("")
        for each in values[:4]:
            print("worst", end="\t")
            for val in each[1].cells:
                print(val, end="\t")
            print("")

    def sort_rows_using_random_rows(self):
        values = []
        for row_i in self.random_rows:
            count = 0
            for row_j in self.random_rows:
                if self.dominates(row_i, row_j, self.goals) < 0:
                    count += 1
            values.append((count, row_i))
        values.sort(key=lambda x: x[0])
        return values

    def distance(self, c1, c2, goals):

        return

    def look_envy_centroid(self):

        return



if __name__ == '__main__':
    hw = "auto.csv"
    file = ""
    with open(hw, 'r') as lines:
        reader = csv.reader(lines, delimiter=' ', quotechar='|')
        for row in reader:
            file += ','.join(row)
            file += '\n'
    lines = fromString(file)
    hw = hw8(lines)
    hw.print_rows_best_rest()
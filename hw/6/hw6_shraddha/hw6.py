import re
import operator
import math
import zipfile
from collections import defaultdict
import numbers
import csv
# code provided by instructor start with some self modification
def compiler(x):
    "return something that can compile strings of type x"
    try: int(x); return  int
    except:
        try: float(x); return  float
        except ValueError: return str


def string(s):
    "read lines from a string"
    for line in s.splitlines(): yield line


def file(fname):
    "read lines from a fie"
    with open(fname) as fs:
        for line in fs: yield line


def zipped(archive, fname):
    "read lines from a zipped file"
    with zipfile.ZipFile(archive) as z:
        with z.open(fname) as f:
            for line in f: yield line


def rows(src, sep=",", doomed=r'([\n\t\r ]|#.*)'):
    "convert lines into lists, killing whitespace and comments"
    for line in src:
        line = line.strip()
        line = re.sub(doomed, '', line)
        if line:
            yield line.split(sep)


def cells(src):
    "convert strings into their right types"
    oks = None
    for n, cells in enumerate(src):
        if n == 0:
            yield cells
        else:
            oks = oks or [compiler(cell) for cell in cells]
            yield [f(cell) for f, cell in zip(oks, cells)]


def fromString(s):
    "putting it all together"
    "putting it all together"
    for lst in cells(rows(string(s))):
        yield lst


def is_number(x):
    return isinstance(x, numbers.Number)


def first_elt(l):
    return l[0]


def same_elt(x):
    return x


def last_elt(l):
    return l[-1]


def order_list(lst, key=same_elt):
    return sorted([x for x in lst if key(x) != "?"])
class Col:
    # initialize n - total numbers used to find mean and SD
    def __init__(self, col_name, pos, weight):
        self.n = 0
        self.col_name = pos
        self.pos = col_name
        self.weight = weight


class Row:
    def __init__(self, cells=[], cooked=[], dom=0):
        self.cells = cells
        self.cooked = cooked
        self.dom = dom


class Num(Col):
    # lo - lowest number, hi - highest number, mu - mean, m2 - summation of square of differences from mean
    def __init__(self, col_name, pos, weight):
        super().__init__(col_name, pos, weight)
        self.mu = self.m2 = self.sd = 0
        self.lo = 10**32
        self.hi = -1*self.lo
        self.col = []

    def add(self, a):  # get the new number and update mu, sd, lo, hi, m2
        self.col.append(a)
        self.n += 1
        if self.lo > a:
            self.lo = a
        if self.hi < a:
            self.hi = a
        d = a - self.mu
        self.mu += d/self.n
        self.m2 += d*(a-self.mu)
        self.sd = self.num_sd()
        return a

    def num_sd(self):  # return Standard Deviation of numbers
        if self.m2 < 0:
            return 0
        if self.n < 2:
            return 0
        return self.m2/(self.n-1)**0.5

    def num_mean(self):  # returns mean of numbers
        return self.mu

    def num_norm(self, c):  # not used in this assignment
        return (c-self.lo)/(self.hi-self.lo + 10**-32)

    def num_less(self, b):  # get new number and update the mu, m2 and sd by removing value the was added by the number
        if self.n < 2:
            self.sd = 0
            return b
        self.n -= 1
        d = b - self.mu
        self.mu -= d / self.n
        self.m2 -= d * (b - self.mu)
        self.sd = self.num_sd()
        return b


class ABCD:
    def __init__(self, data = "", rx = ""):
        self.known = {}
        self.a = {}
        self.b = {}
        self.c = {}
        self.d = {}
        self.rx = "rx" if rx == "" else rx
        self.data = "data" if data == "" else data
        self.yes = self.no = 0

    def ABCD1(self, want, got):
        if want not in self.known:
            self.known[want] = 1
            self.a[want] = self.yes + self.no
        else:
            self.known[want] += 1
        if got not in self.known:
            self.known[got] = 1
            self.a[want] = self.yes + self.no
        if want == got:
            self.yes += 1
        else:
            self.no += 1
        for x in self.known:
            if want == x:
                if want == got:
                    if x not in self.d:
                        self.d[x] = 0
                    self.d[x] += 1
                else:
                    if x not in self.b:
                        self.b[x] = 0
                    self.b[x] += 1
            else:
                if got == x:
                    if x not in self.c:
                        self.c[x] = 0
                    self.c[x] += 1
                else:
                    if x not in self.a:
                        self.a[x] = 0
                    self.a[x] += 1

    def ABCD_report(self):
        file = open("output3.txt", 'w+')
        file.write(str(
            "   db |    rx |   num |     a |     b |     c |     d |  acc |  pre |   pd |   pf |    f |    g | class") + '\n')
        file.write(str(
            " ---- |  ---- |  ---- |  ---- |  ---- |  ---- |  ---- | ---- | ---- | ---- | ---- | ---- | ---- |-------") + '\n')
        for x in self.known:
            pd = pf = pn = prec = g = f = acc = 0
            a = 0 if x not in self.a else self.a[x]
            b = 0 if x not in self.b else self.b[x]
            c = 0 if x not in self.c else self.c[x]
            d = 0 if x not in self.d else self.d[x]
            if (b + d > 0):
                pd = d / (b + d)
            if (a + c > 0):
                pf = c / (a + c)
                pn = (b + d) / (a + c)
            if (c + d > 0):
                prec = d / (c + d)
            if (1 - pf + pd > 0):
                g = 2 * (1 - pf) * pd / (1 - pf + pd)
            if (prec + pd > 0):
                f = 2 * prec * pd / (prec + pd)
            if (self.yes + self.no > 0):
                acc = self.yes / (self.yes + self.no)
            file.write(str(self.data + "  |   " + self.rx + "  |   " + str(self.yes + self.no) + "  |   " + str(
                a) + "  |   " + str(b) + "   |  " + str(c) + "    |   " + str(d) + "   | " + str(
                round(acc, 2)) + " | " + str(round(prec, 2)) + "  |  " + str(round(pd, 2)) + "|  " + str(
                round(pf, 2)) + " | " + str(round(f, 2)) + " |  " + str(round(g, 2)) + "| " + str(x)) + '\n')


class Sym(Col):
    def __init__(self, col_name, pos, weight):
        super().__init__(col_name, pos, weight)
        self.mode = ""
        self.most = 0
        self.cnt = defaultdict(int)

    def add(self, v):
        self.n += 1
        self.cnt[v] += 1
        tmp = self.cnt[v]
        if tmp > self.most:
            self.most = tmp
            self.mode = v
        return v

    def sym_ent(self):
        p = e = 0
        for k in self.cnt:
            p = self.cnt[k]/self.n
            e -= p*math.log10(p)/math.log10(2)
        return e

    def test_entropy(self, string):
        for str1 in string:
            self.add(str1)
        return self.sym_ent()

## Added on 24th Oct


class Div(object):
    def __init__(self, lst_len, lst, same_x=same_elt, x_is_num=Num, y_is_num=Num):

        self._lst = lst
        self.xis = x_is_num
        self.yis = y_is_num

        self.x = same_x
        self.before = self.xis(self._lst, key=same_x)
        self.step = int(lst_len ** 0.5)

        self.stp = same_x(last_elt(self._lst))
        self.strt = same_x(first_elt(self._lst))
        self.eps = self.before.sd * 0.3
        self.res = 0
        self.__divide(0, len(self._lst), self.before, 1)

    def __divide(self, lo, hi, before):
        l1 = self.xis(key=self.x)
        r1 = self.xis(self._lst[lo:hi], key=self.x)
        cut_at = None
        best = before.sd
        for j in range(lo, hi):
            r1.NumLess(self._lst[j])
            l1.Num1(self._lst[j])
            if l1.n >= self.step:
                if r1.n >= self.step:
                    now = self.x(self._lst[j-1])
                    after = self.x(self._lst[j])
                    if now == after: continue
                    if abs(l1.mu - r1.mu) >= self.eps:
                        if after - self.strt >= self.eps:
                            if self.stp - now >= self.eps:
                                expected = l1.xpect(r1)
                                if expected*1.05 < best:
                                    best, cut_at = expected, j
        self.res = [cut_at, lo]
        return cut_at, lo

#########################################


class Table:
    def __init__(self):
        self.oid = 1
        self.index = []
        self.col_len = 0
        self.rows = []
        self.cols = []
        self.goals = []
        self.xs = []
        self.nums = []
        self.syms = []

        # added on 24th Oct
        self.goalCol = 0
        self.lineCount = 0
        self.headerColumn = []
        self.dict = defaultdict(list)
        self.lst = []
        self.cnt = 0
        self.lstLength = 0
        #####################

    def read(self, lines):
        tbl_obj = fromString(lines)
        for i1, row in enumerate(tbl_obj):
            if i1 == 0:
                self.col_len = len(row)
                for j1 in range(len(row)):
                    if '?' not in row[j1]:
                        self.index.append(j1)
                        if re.search(r"[<>$]", row[j1]):
                            self.nums.append(j1+1)
                            if re.search(r"[<]", row[j1]):
                                self.cols.append([Num(row[j1], j1, -1), self.oid])
                            else:
                                self.cols.append([Num(row[j1], j1, 1), self.oid])
                        if re.search(r"[<>!]", row[j1]):
                            self.goals.append(j1+1)

                        else:
                            self.syms.append(j1+1)
                            self.xs.append(j1+1)
                            self.cols.append([Sym(row[j1], j1, 1),self.oid])
                        self.oid += 1
            else:
                if len(row) != self.col_len:
                    row = "E> skipping line"
                if "E> skipping line" not in row:
                    tmp = len(row) - 1
                    for j1 in range(tmp, -1, -1):
                        if j1 not in self.index:
                            del row[j1]
                    for j1 in range(len(self.cols)):
                        self.cols[j1][0].add(row[j1])
                self.rows.append([Row(row), self.oid])
                self.oid += 1

    def dump(self):
        file1 = open("output2.txt", "w+")
        file1.write("table_columns")
        for i2 in range(len(self.cols)):
            file1.write("\n|\t"+str(i2+1))
            file1.write("\n|\t|\tn: " + str(self.cols[i2][0].n))
            file1.write("\n|\t|\tpos: " + str(self.cols[i2][0].col_name))
            file1.write("\n|\t|\tcol_name: " + str(self.cols[i2][0].pos))
            file1.write("\n|\t|\tweight: " + str(self.cols[i2][0].weight))
            if type(self.cols[i2][0]) == Num:
                file1.write("\n|\t|\tadd: Num1")
                file1.write("\n|\t|\thi: "+str(self.cols[i2][0].hi))
                file1.write("\n|\t|\tlo: "+str(self.cols[i2][0].lo))
                file1.write("\n|\t|\tmu: "+str(self.cols[i2][0].mu))
                file1.write("\n|\t|\tm2: "+str(self.cols[i2][0].m2))
                file1.write("\n|\t|\tsd: "+str(self.cols[i2][0].sd))
                file1.write("\nt.oid: "+str(self.cols[i2][1]))
            else:
                file1.write("\n|\t|\tadd: Sym1")
                file1.write("\n|\t|\tcnt")
                for cn in self.cols[i2][0].cnt:
                    file1.write("\n|\t|\t|\t{0}: {1}".format(cn, self.cols[i2][0].cnt[cn]))
                file1.write("\n|\t|\tmode: " + self.cols[i2][0].mode)
                file1.write("\n|\t|\tmost: " + str(self.cols[i2][0].most))
        file1.write('\nt.my')
        file1.write('\n|\tnums')
        for i2 in self.nums:
            file1.write("\n|\t|\t " + str(i2))
        file1.write('\n|\tsyms')
        for i2 in self.syms:
            file1.write("\n|\t|\t " + str(i2))
        file1.write('\n|\tgoals')
        for i2 in self.goals:
            file1.write("\n|\t|\t " + str(i2))
        file1.close()

    # added for hw6 on 24th Oct

    def tree(self, lst, y, yis, lvl=0):

        if len(lst) >= 8:
            self.cut = None
            self.col = None
            self.lo = 10 ** 32;

            for col1 in range(0, len(lst[0]) - 1):
                x = sorted([val[col1] for val in lst])
                r = Div(self.lstLength, x)
                cut1 = r.res[0]
                lo1 = r.res[1]
                if cut1 and x[cut1] != '?':
                    if lo1 < self.lo:
                        self.cut, self.lo, self.col = cut1, lo1, col1
            if self.cut:
                print("Level :" + str(lvl) + " Cut : " + str(self.cut))
                lst = sorted(lst, key=lambda x1: x1[self.col])
                lst1 = lst[:self.cut]
                lst2 = lst[self.cut:]
                self.cnt += 1
                self.tree(lst1, y, yis, lvl + 1)
                self.tree(lst2, y, yis, lvl + 1)


    def readCsvFile(self, file):
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in list(csv_reader):
                if self.lineCount > 0:
                    self.lst.append([float(x) for x in row]);
                    for index, data in enumerate(row):
                        if data != '?':
                            self.dict[index].append(float(data))
                        if index not in self.dict:
                            self.dict[index] = []
                        else:
                            self.dict[index].append(0)
                else:
                    self.headerColumn = list(row)
                self.lineCount += 1
        self.lstLength = len(self.lst)
        self.tree(self.lst, 4, Num)



if __name__ == "__main__":
    s = """
    outlook, ?$temp,  <humid, wind, !play
    rainy, 68, 80, FALSE, yes # comments
    sunny, 85, 85,  FALSE, no
    sunny, 80, 90, TRUE, no
    overcast, 83, 86, FALSE, yes
    rainy, 70, 96, FALSE, yes
    rainy, 65, 70, TRUE, no
    overcast, 64, 65, TRUE, yes
    sunny, 72, 95, FALSE, no
    sunny, 69, 70, FALSE, yes
    rainy, 75, 80, FALSE, yes
    sunny, 75, 70, TRUE, yes
    overcast, 72, 90, TRUE, yes
    overcast, 81, 75, FALSE, yes
    rainy, 71, 91, TRUE, no
    """
    tbl = Table()
    tbl.read(s)
    tbl.dump()

    # test Entropy
    ent = Sym('',0,1)
    file = open("output1.txt", 'w+')
    file.write("entropy of test string is: {}".format(ent.test_entropy('aaaabbc')))
    file.close()

    report = ABCD("", "")
    for i in range(6):
        report.ABCD1('yes', 'yes')
    for i in range(2):
        report.ABCD1('no', 'no')
    for i in range(5):
        report.ABCD1('maybe', 'maybe')
    report.ABCD1("maybe", "no")
    report.ABCD_report()
    tbl.readCsvFile('diabetes.csv')
    # obj = Tree()
    # obj.readCsvFile('diabetes.csv')

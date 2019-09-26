import re
import operator
import math
from collections import defaultdict
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


def cells(src, col_len):
    "convert strings into their right types"
    oks = None
    for n, cells in enumerate(src):
        if len(cells) != col_len:
            yield "E> skipping line"
        else:
            oks = [compiler(cell) for cell in cells]
            yield [f(cell) for f,cell in zip(oks,cells)]



def fromString(s):
    "putting it all together"
    tmp = rows(string(s))
    col_name = next(tmp)
    columns = [i for i in range(len(col_name)) if '?' not in col_name[i]]
    yield(operator.itemgetter(*columns)(col_name))
    for lst in cells(tmp, len(col_name)):
        if type(lst) != list:
            yield lst
        else:
            yield list(operator.itemgetter(*columns)(lst))
# code provided by instructor end after some self modification


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

class Table:
    def __init__(self):
        self.oid = 1
        self.rows = []
        self.cols = []
        self.goals = []
        self.xs = []
        self.nums = []
        self.syms = []

    def read(self, lines):
        tbl = fromString(lines)
        for i, row in enumerate(tbl):
            if i == 0:
                for j in range(len(row)):
                    if re.search(r"[<>!]", row[j]):
                        self.goals.append(j+1)
                    if re.search(r"[<>$]", row[j]):
                        self.nums.append(j+1)
                        if re.search(r"[<]", row[j]):
                            self.cols.append([Num(row[j],j, -1), self.oid])
                        else:
                            self.cols.append([Num(row[j], j, 1), self.oid])
                    else:
                        self.syms.append(j+1)
                        self.xs.append(j+1)
                        self.cols.append([Sym(row[j], j, 1),self.oid])
                    self.oid += 1
            else:
                if "E> skipping line" not in row:
                    for j in range(len(self.cols)):
                        self.cols[j][0].add(row[j])
                self.rows.append([Row(row), self.oid])
                self.oid += 1

    def dump(self):
        file = open("output2.txt", "w+")
        file.write("table_columns")
        for i in range(len(self.cols)):
            file.write("\n|\t"+str(i+1))
            file.write("\n|\t|\tn: " + str(self.cols[i][0].n))
            file.write("\n|\t|\tpos: " + str(self.cols[i][0].col_name))
            file.write("\n|\t|\tcol_name: " + str(self.cols[i][0].pos))
            file.write("\n|\t|\tweight: " + str(self.cols[i][0].weight))
            if type(self.cols[i][0]) == Num:
                file.write("\n|\t|\tadd: Num1")
                file.write("\n|\t|\thi: "+str(self.cols[i][0].hi))
                file.write("\n|\t|\tlo: "+str(self.cols[i][0].lo))
                file.write("\n|\t|\tmu: "+str(self.cols[i][0].mu))
                file.write("\n|\t|\tm2: "+str(self.cols[i][0].m2))
                file.write("\n|\t|\tsd: "+str(self.cols[i][0].sd))
                file.write("\nt.oid: "+str(self.cols[i][1]))
            else:
                file.write("\n|\t|\tadd: Sym1")
                file.write("\n|\t|\tcnt")
                for cn in self.cols[i][0].cnt:
                    file.write("\n|\t|\t|\t{0}: {1}".format(cn, self.cols[i][0].cnt[cn]))
                file.write("\n|\t|\tmode: " + self.cols[i][0].mode)
                file.write("\n|\t|\tmost: " + str(self.cols[i][0].most))
        file.write('\nt.my')
        file.write('\n|\tnums')
        for i in self.nums:
            file.write("\n|\t|\t " + str(i))
        file.write('\n|\tsyms')
        for i in self.syms:
            file.write("\n|\t|\t " + str(i))
        file.write('\n|\tgoals')
        for i in self.goals:
            file.write("\n|\t|\t " + str(i))
        # file.write('\n|\txs')
        # for i in self.xs:
        #     file.write("\n|\t|\t " + str(i))
        file.close()


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

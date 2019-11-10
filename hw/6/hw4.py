import re
import math
from math import log
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


def cells(src):
    "convert strings into their right types"
    oks = None
    for n, cells in enumerate(src):
        if n == 0:
            yield cells
        else:
            # print(cells)
            temp = [compiler(cell) for cell in cells]
            # print("temp",temp)
            oks = temp
            # print(oks)
            yield [f(cell) for f, cell in zip(oks, cells)]



def fromString(s):
    "putting it all together"
    "putting it all together"
    for lst in cells(rows(string(s))):
        yield lst


class Col:
    # initialize n - total numbers used to find mean and SD
    def __init__(self, col_name, pos, text):
        self.n = 0
        self.col_name = col_name
        self.pos = pos
        self.text = text


class Row:
    def __init__(self, cells=[], cooked=[], dom=0):
        self.cells = cells
        self.cooked = cooked
        self.dom = dom


class Num(Col):
    # lo - lowest number, hi - highest number, mu - mean, m2 - summation of square of differences from mean
    def __init__(self, col_name, pos, text):
        super().__init__(col_name, pos, text)
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

    def num_like(self, x):
        var = self.sd**2
        denom = (3.14159*2*var)**0.5
        num = 2.71828**(-(x-self.mu)**2/(2*var+0.0001))
        return num/(denom + 10**-64)

    def dist(self, x, y):
        norm = lambda z: (z - self.lo) / (self.hi - self.lo + 10 ** -32)
        no = "?"
        if x is no:
            if y is no: return 1
            y = norm(y)
            x = 0 if y > .5 else 1
        else:
            x = norm(x)
            if y is no:
                y = 0 if x > .5 else 1
            else:
                y = norm(y)
        return abs(x - y)


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
            # print("want",want)
            self.known[want] = 1
            self.a[want] = self.yes + self.no
        else:
            self.known[want] += 1
        if got not in self.known:
            # print("got", got)
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
        string = []
        string.append(str(
            "   db |    rx |   num |     a |     b |     c |     d |  acc |  pre |   pd |   pf |    f |    g | class") + '\n')
        string.append(str(
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
            string.append(str(self.data + "  |   " + self.rx + "  |   " + str(self.yes + self.no) + "  |   " + str(
                a) + "  |   " + str(b) + "   |  " + str(c) + "    |   " + str(d) + "   | " + str(
                round(acc, 2)) + " | " + str(round(prec, 2)) + "  |  " + str(round(pd, 2)) + "|  " + str(
                round(pf, 2)) + " | " + str(round(f, 2)) + " |  " + str(round(g, 2)) + "| " + str(x)) + '\n')
        return string

class Sym(Col):
    def __init__(self, col_name, pos, text):
        super().__init__(col_name, pos, text)
        self.mode = ""
        self.most = 0
        self.cnt = defaultdict(int)

    def add(self, v):
        self.n += 1
        self.cnt[v] += 1
        tmp = self.cnt[v]
        # print(v, tmp)
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

    def sym_like(self, x, prior, m):
        f = 0 if x not in self.cnt else self.cnt[x]
        return (f + m * prior)/(self.n + m)

    def dist(self, x, y):
        no = "?"
        if x is no and y is no: return 1
        if x != y: return 1
        return 0

class Table:
    def __init__(self):
        self.index = []
        self.col_len = 0
        self.rows = []
        self.cols = []
        self.goals = []
        self.xs = []
        self.nums = []
        self.syms = []

    def read_lines(self,i, row):
        if i == 0:
            self.col_len = len(row)
            for j in range(len(row)):
                if '?' not in row[j]:
                    self.index.append(j)
                    if re.search(r"[<>!]", row[j]):
                        self.goals.append(j + 1)
                    else:
                        self.xs.append(j + 1)
                    if re.search(r"[<>$]", row[j]):
                        self.nums.append(j + 1)
                        if re.search(r"[<]", row[j]):
                            self.cols.append(Num(row[j], j, row[j]))
                        else:
                            self.cols.append(Num(row[j], j, row[j]))
                    else:
                        self.syms.append(j + 1)
                        self.cols.append(Sym(row[j], j, 1))
        else:
            if len(row) != self.col_len or "?" in row:
                row = "E> skipping line"
            if "E> skipping line" not in row:
                tmp = len(row) - 1
                for j in range(tmp, -1, -1):
                    if j not in self.index:
                        del row[j]
                for j in range(len(self.cols)):
                    self.cols[j].add(row[j])
            self.rows.append(Row(row))

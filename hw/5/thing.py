from collections import defaultdict
import math
from lib import *

class Col:
    # initialize n - total numbers used to find mean and SD
    def __init__(self, pos, weight):
        self.n = 0
        self.col_name = pos
        self.weight = weight

    def xpect(self, j):
        n = self.n + j.n
        return self.n / n * self.variety() + j.n / n * j.variety()

    def __add__(self, x):
        # y = self.key(x)
        if x != '?':
            # self.n += 1
            self.add(x)
        return x

    def __sub__(self, x):
        # y = self.key(x)
        if x != '?':
            # self.n -= 1
            self.sub(x)
        return x


class Row:
    def __init__(self, cells=[], cooked=[], dom=0):
        self.cells = cells
        self.cooked = cooked
        self.dom = dom


class Num(Col):
    # lo - lowest number, hi - highest number, mu - mean, m2 - summation of square of differences from mean
    def __init__(self, inits=[], pos=0, weight=0, key=same):
        super().__init__(pos, weight)
        self.mu = self.m2 = self.sd = 0
        self.key = key
        self.lo = 10**32
        self.hi = -1*self.lo
        self.col = []
        self.rank = 1
        [self + x for x in inits]

    def add(self, a):  # get the new number and update mu, sd, lo, hi, m2
        # a = self.key(a)
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

    def variety(self):
        return self.sd

    def num_sd(self):  # return Standard Deviation of numbers
        if self.m2 < 0:
            return 0
        if self.n < 2:
            return 0
        return self.m2/(self.n-1)**0.5

    def mean(self):  # returns mean of numbers
        return self.mu

    def num_norm(self, c):  # not used in this assignment
        return (c-self.lo)/(self.hi-self.lo + 10**-32)

    def sub(self, b):  # get new number and update the mu, m2 and sd by removing value the was added by the number
        # b = self.key(b)
        if self.n < 2:
            self.sd = 0
            return b
        self.n -= 1
        d = b - self.mu
        self.mu -= d / self.n
        self.m2 -= d * (b - self.mu)
        self.sd = self.num_sd()
        return b


class Sym(Col):
    def __init__(self, inits=[], pos=0, weight=0, key=same):
        super().__init__(pos, weight)
        self.key = key
        self.mode = ""
        self.most = 0
        self.rank = 1
        self.cnt = defaultdict(int)
        [self + x for x in inits]

    def add(self, v):
        # v = self.key(v)
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
            p = self.cnt[k]/self.n + 10**-64
            print("\nvalue of p: {0}\n".format(p))
            e -= p*math.log10(p)/math.log10(2)
        return e

    def mean(self):
        return self.mode

    def sub(self, x):
        # x = self.key(x)
        old = self.cnt.get(x, 0)
        if old > 0:
            self.cnt[x] = old - 1

    def variety(self):
        return self.sym_ent()

    def test_entropy(self, string):
        for str1 in string:
            self.add(str1)
        return self.sym_ent()
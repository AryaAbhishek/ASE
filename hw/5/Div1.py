import math
from lib import same, first, last, ordered
# from   copy  import deepcopy as kopy
from thing import Num, Sym
import random

div  = {'trivial': 1.025,
            'cohen': 0.3,
            'min': 0.5}

class Div(object):
    def __init__(self, xlst, ylst, x=same, xis = Num, yis = Num):
        self.xis = xis
        self.yis = yis
        self._lst = ordered(xlst)
        self._ylst = ordered(ylst)
        self.b4 = self.xis(self._lst)
        self.gain = 0                             # where we will be, once done
        self.x = x                             # how to get values from 'lst' items
        self.step = int(len(self._lst)**div['min']) # each split need >= 'step' items
        self.stop = x(last(self._lst))               # top list value
        self.start = x(first(self._lst))              # bottom list value
        self.ranges = []                            # the generted ranges
        self.epsilon = self.b4.variety() * div['cohen']     # bins must be seperated >= epsilon
        self.__divide(1, len(self._lst), self.b4, 1)
        self.gain /= len(self._lst)

    def __divide(self, lo, hi, b4, rank):
        "Find a split between lo and hi, then recurse on each split."
        l = self.xis()
        r = self.xis(self._lst[lo:hi])
        best = b4.variety()
        cut = None
        for j in range(lo,hi):
            l + self._lst[j]
            r - self._lst[j]
            if l.n >= self.step:
                if r.n >= self.step:
                    now = self.x( self._lst[j-1])
                    after = self.x( self._lst[j])
                    if now == after: continue
                    if abs(r.mu - l.mu) >= self.epsilon:
                        if after - self.start >= self.epsilon:
                            if self.stop - now >= self.epsilon:
                                xpect = l.xpect(r)
                                if xpect*div['trivial'] < best:
                                    best, cut = xpect, j
        if cut:
            ls, rs = self._lst[lo:cut], self._lst[cut:hi]
            if self.yis == Num:
                print(str(rank) + ' x.n    ' + str(cut - lo) + ' | x.lo ' + str(
                    round(self._lst[lo + 1], 5)) + '  x.hi ' + str(round(self._lst[cut - 1], 5))
                      + ' | y.lo ' + str(round(self.ylist[lo + 1], 5)) + ' y.hi ' + str(round(self.ylist[cut], 5)))

            if self.yis == Sym:
                symObj = self.yis(self.ylist[lo:cut])
                print(str(rank) + ' x.n    ' + str(cut - lo) + ' | x.lo ' + str(
                    round(self._lst[lo + 1], 5)) + '  x.hi ' + str(round(self._lst[cut - 1], 5))
                      + ' | y.mode ' + str(symObj.mode) + ' y.ent ' + str(symObj.entropy))
            rank = self.__divide(lo, cut, self.xis(ls,key=self.x), rank) + 1
            rank = self.__divide(cut, hi, self.xis(rs, key=self.x), rank)
        else:
            self.gain += b4.n * b4.variety()
            b4.rank = rank
            self.ranges += [b4]
        return rank


if __name__ == "__main__":
    # Part1

    r = random.random
    seed = random.seed
    n = 5
    def num(i):
        if i < 0.4: return [i, r() * 0.1]
        if i < 0.6: return [i, 0.4 + r() * 0.1]
        return [i, 0.8 + r() * 0.1]

    def x():
        seed(1)
        return [r() * 0.05 for _ in range(n)] + \
               [0.2 + r() * 0.05 for _ in range(n)] + \
               [0.4 + r() * 0.05 for _ in range(n)] + \
               [0.6 + r() * 0.05 for _ in range(n)] + \
               [0.8 + r() * 0.05 for _ in range(n)]

    def xnum():
        return [num(one) for one in x()]

    imp = xnum()
    div1 = Div(imp[0], imp[1])

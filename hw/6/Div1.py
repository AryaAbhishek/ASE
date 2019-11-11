from thing import Num, Sym
from lib import same, first, last, ordered
# import sys
# sys.setrecursionlimit(4000)

class Div(object):
    def __init__(self, lst, type="", x=first, y=last, xis=Num):
        self.xis = xis
        if type == 'num':
            self.yis = Num
        else:
            self.yis = Sym
        self.type = type
        self._lst = ordered(lst, key=x)
        self.xlist, self.ylist = [], []
        for x, y in self._lst:
            self.xlist.append(x)
            self.ylist.append(y)
        self.b4 = self.yis(self.ylist)
        self.gain = 0  # where we will be, once done
        self.x = x  # how to get values from 'lst' items
        self.y = y
        self.step = int(len(self._lst) ** 0.5)  # each split need >= 'step' items
        self.start = self.ylist[0]
        self.stop = self.ylist[-1]
        self.ranges = []  # the generted ranges
        self.epsilon = self.b4.variety() * 0.3  # bins must be seperated >= epsilon
        self.splits = ""
        self.rank, self.cut, self.best = self.__divide(1, len(self._lst), 1, self.b4)
        self.gain /= len(self._lst)

    def __divide(self, lo, hi, rank, b4):
        ly = self.yis()
        ry = self.yis(self.ylist[lo:hi])
        best = b4.variety()
        cut = None
        for j in range(lo, hi):
            ly.add(self.ylist[j])
            ry.sub(self.ylist[j])
            if ly.n >= self.step:
                if ry.n >= self.step:
                    now = self.ylist[j-1]
                    after = self.ylist[j]
                    if now == after: continue
                    if self.type == "num":
                        if abs(ry.mean() - ly.mean()) >= self.epsilon:
                            if after - self.start >= self.epsilon:
                                if self.stop - now >= self.epsilon:
                                    xpect = ly.xpect(ry)
                                    if xpect * 1.025 < best:
                                        best, cut = xpect, j
                    else:
                        if abs(ord(ry.mean()) - ord(ly.mean())) >= self.epsilon:
                            if ord(after) - ord(self.start) >= self.epsilon:
                                if ord(self.stop) - ord(now) >= self.epsilon:
                                    xpect = ly.xpect(ry)
                                    if xpect * 1.025 < best:
                                        best, cut = xpect, j
        if cut:
            ls, rs = self.ylist[lo:cut], self.ylist[cut:hi]
            if self.type == "num":
                self.splits += str(rank) + ' x.n    ' + str(cut - lo) + ' | x.lo ' + str(
                    round(self.xlist[lo + 1], 5)) + '  x.hi ' + str(round(self.xlist[cut - 1], 5))\
                               + ' | y.lo ' + str(round(self.ylist[lo + 1], 5)) + ' y.hi ' \
                               + str(round(self.ylist[cut], 5)) + '\n'

            if self.type == "sym":
                symObj = self.yis(self.ylist[lo:cut])
                self.splits += str(rank) + ' x.n    ' + str(cut - lo) + ' | x.lo ' + str(
                    round(self.xlist[lo + 1], 5)) + '  x.hi ' + str(round(self.xlist[cut - 1], 5))\
                              + ' | y.mode ' + str(symObj.mean()) + ' y.ent ' + str(symObj.variety()) + '\n'
            rank, _, _ = self.__divide(lo, cut, rank, self.yis(ls))
            rank += 1
            rank, _, _ = self.__divide(cut, hi, rank, self.yis(rs))

        else:
            self.gain = self.gain + self.b4.n * self.b4.variety()
            self.b4.rank = rank
            self.ranges = self.ranges + [self.b4]
        return rank, cut, best

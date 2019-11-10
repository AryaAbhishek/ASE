from thing import Num, Sym
from lib import same, first, last, ordered


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
        self.b4 = self.xis(self.xlist)
        self.gain = 0  # where we will be, once done
        self.x = x  # how to get values from 'lst' items
        self.y = y
        self.step = int(len(self._lst) ** 0.5)  # each split need >= 'step' items
        self.stop = self.xlist[-1]  # top list value
        self.start = self.xlist[0]  # bottom list value
        self.ranges = []  # the generted ranges
        self.epsilon = self.b4.variety() * 0.3  # bins must be seperated >= epsilon
        self.b4 = self.yis(self.ylist)
        self.splits = ""
        self.gain /= len(self._lst)
        self.rank, self.cut, self.best = self.__divide(1, len(self._lst), 1)

    def __divide(self, lo, hi, rank):
        l = self.xis()
        r = self.xis(self.xlist[lo:hi])
        ly = self.yis()
        ry = self.yis(self.ylist[lo:hi])
        best = self.b4.variety()
        cut = None
        # print(lo, hi)
        for j in range(lo, hi):
            l.add(self.xlist[j])
            ly.add(self.ylist[j])
            r.sub(self.xlist[j])
            ry.sub(self.ylist[j])
            # print("l.n",l.n,"r.n",r.n,"step",self.step)
            if l.n >= self.step:
                if r.n >= self.step:
                    now = self.xlist[j - 1]
                    after = self.xlist[j]
                    # print("check ",j, now, after, r.mu - l.mu, self.epsilon, self.stop-now, after - self.start)
                    if now == after: continue
                    if abs(r.mean() - l.mean()) >= self.epsilon:
                        # print("hello")
                        if after - self.start >= self.epsilon:
                            # print("hw")
                            if self.stop - now >= self.epsilon:
                                xpect = ly.xpect(ry)
                                # print(xpect*1.025, best)
                                if xpect * 1.025 < best:
                                    best, cut = xpect, j
            # print(cut)
        if cut:
            # print("hello")
            # ls, rs = self._lst[lo:cut], self._lst[cut:hi]
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
            rank, _, _ = self.__divide(lo, cut, rank)
            rank += 1
            rank, _, _ = self.__divide(cut, hi, rank)

        else:
            self.gain = self.gain + self.b4.n * self.b4.variety()
            self.b4.rank = rank
            self.ranges = self.ranges + [self.b4]
        return rank, cut, best

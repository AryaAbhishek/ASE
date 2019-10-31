from thing import Num, Sym
from lib import same, first, last, ordered


class Div(object):
    def __init__(self, lst, type="", x=first, y=last, xis=Num, yis=Num):
        self.xis = xis
        if type == 'num':
            self.yis = yis
        else:
            self.yis = Sym
        self.type = type
        self._lst = ordered(lst, key=x)
        self.b4 = self.xis(self._lst, key=x)
        self.gain = 0  # where we will be, once done
        self.x = x  # how to get values from 'lst' items
        self.y = y
        self.step = int(len(self._lst) ** 0.5)  # each split need >= 'step' items
        self.stop = x(y(self._lst))  # top list value
        self.start = x(x(self._lst))  # bottom list value
        self.ranges = []  # the generted ranges
        self.epsilon = self.b4.variety() * 0.3  # bins must be seperated >= epsilon
        self.splits = ""
        self.gain /= len(self._lst)
        self.__divide(0, len(self._lst), 1)

    def __divide(self, lo, hi, rank):
        l = self.xis(key=self.x)
        r = self.xis(self._lst[lo:hi], key=self.x)
        ly = self.yis(key=self.y)
        ry = self.yis(self._lst[lo:hi], key=self.y)
        b4 = self.yis(self._lst[lo:hi], key = self.y)
        self.xlist, self.ylist = [], []
        for x, y in self._lst:
            self.xlist.append(x)
            self.ylist.append(y)
        best = b4.variety()
        cut = None
        print(lo, hi)
        for j in range(lo, hi):
            l.add(self._lst[j])
            ly.add(self._lst[j])
            r.sub(self._lst[j])
            ry.sub(self._lst[j])
            if l.n >= self.step:
                if r.n >= self.step:
                    now = self.x(self._lst[j - 1])
                    after = self.x(self._lst[j])
                    print("check ",j, now, after, r.mu - l.mu, self.epsilon, self.stop-now, after - self.start)
                    if now == after: continue
                    if abs(r.mu - l.mu) >= self.epsilon:
                        if after - self.start >= self.epsilon:
                            if self.stop - now >= self.epsilon:
                                xpect = ly.xpect(ry)
                                print(xpect*1.025, best)
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
                              + ' | y.mode ' + str(symObj.mode) + ' y.ent ' + str(symObj.entropy) + '\n'
            rank = self.__divide(lo, cut, rank) + 1
            rank = self.__divide(cut, hi, rank)

        else:
            self.gain = self.gain + b4.n * b4.variety()
            b4.rank = rank
            self.ranges = self.ranges + [b4]
        return rank

    # def total_splits(self):
    #     return self.splits



# import math
# from lib import same, first, last, ordered
# # from   copy  import deepcopy as kopy
# from thing import Num, Sym
# import random
#
# div  = {'trivial': 1.025,
#             'cohen': 0.3,
#             'min': 0.5}
#
# class Div(object):
#     def __init__(self, xlst, ylst, type="", x=same, xis = Num, yis = Num):
#         self.type = type
#         self.xis = xis
#         self.yis = yis
#         self._lst = ordered(xlst)
#         self._ylst = ordered(ylst)
#         self.b4 = self.xis(self._lst)
#         self.gain = 0                             # where we will be, once done
#         self.x = x                             # how to get values from 'lst' items
#         self.step = int(len(self._lst)**div['min']) # each split need >= 'step' items
#         self.stop = x(last(self._lst))               # top list value
#         self.start = x(first(self._lst))              # bottom list value
#         self.ranges = []                            # the generted ranges
#         self.epsilon = self.b4.variety() * div['cohen']     # bins must be seperated >= epsilon
#         self.__divide(1, len(self._lst), self.b4, 1)
#         self.gain /= len(self._lst)
#
#     def __divide(self, lo, hi, b4, rank):
#         "Find a split between lo and hi, then recurse on each split."
#         l = self.xis(self._lst[lo])
#         r = self.xis(self._lst[lo:hi])
#         best = b4.variety()
#         cut = None
#         for j in range(lo,hi):
#             l + self.xis(self._lst[j])
#             r - self.xis(self._lst[j])
#             if l.n >= self.step:
#                 if r.n >= self.step:
#                     now = self.x( self._lst[j-1])
#                     after = self.x( self._lst[j])
#                     if now == after: continue
#                     if abs(r.mu - l.mu) >= self.epsilon:
#                         if after - self.start >= self.epsilon:
#                             if self.stop - now >= self.epsilon:
#                                 xpect = l.xpect(r)
#                                 if xpect*div['trivial'] < best:
#                                     best, cut = xpect, j
#         if cut:
#             print("hello")
#             ls, rs = self._lst[lo:cut], self._lst[cut:hi]
#             if self.type == "num":
#                 print(str(rank) + ' x.n    ' + str(cut - lo) + ' | x.lo ' + str(
#                     round(self._lst[lo + 1], 5)) + '  x.hi ' + str(round(self._lst[cut - 1], 5))
#                       + ' | y.lo ' + str(round(self.ylist[lo + 1], 5)) + ' y.hi ' + str(round(self.ylist[cut], 5)))
#
#             if self.type == "sym":
#                 sym_res = self.yis(self.ylist[lo:cut])
#                 print(str(rank) + ' x.n    ' + str(cut - lo) + ' | x.lo ' + str(
#                     round(self._lst[lo + 1], 5)) + '  x.hi ' + str(round(self._lst[cut - 1], 5))
#                       + ' | y.mode ' + str(sym_res.mode) + ' y.ent ' + str(sym_res.entropy))
#             rank = self.__divide(lo, cut, self.xis(ls,key=self.x), rank) + 1
#             rank = self.__divide(cut, hi, self.xis(rs, key=self.x), rank)
#         else:
#             self.gain += b4.n * b4.variety()
#             b4.rank = rank
#             self.ranges += [b4]
#         return rank

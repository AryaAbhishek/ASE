import random
from Div1 import Div
r = random.random
seed = random.seed
n = 5


def xsym():
    return [sym(one) for one in x()] * 5


def sym(i):
    if i<0.4: return [i, "a"]
    if i<0.6: return [i, "b"]
    return           [i, "c"]


def x():
    seed(1)
    return[r()*0.05 for _ in range(n)] + \
          [0.2 + r()*0.05 for _ in range(n)] +  \
          [0.4 + r()*0.05 for _ in range(n)] +   \
          [0.6 + r()*0.05 for _ in range(n)] +    \
          [0.8 + r()*0.05 for _ in range(n)]


def num(i):
    if i < 0.4: return [i, r() * 0.1]
    if i < 0.6: return [i, 0.4 + r() * 0.1]
    return [i, 0.8 + r() * 0.1]


def xnum():
    return [num(one) for one in x()]

file = open("output3.txt", 'w+')
imp = xnum()
# xlst, ylst = [], []
# for i in imp:
#     xlst.append(i[0])
#     ylst.append(i[1])
div1 = Div(imp, "num")
file.write("Div1\n")
file.write(div1.splits)
imp = xsym()
# xlst, ylst = [], []
# for i in imp:
#     xlst.append(i[0])
#     ylst.append(i[1])
div1 = Div(imp, "sym")
file.write("\nDiv2\n")
file.write(div1.splits)
file.close()

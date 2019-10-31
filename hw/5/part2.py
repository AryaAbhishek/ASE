import random
from Div1 import Div
r = random.random
seed = random.seed
n = 5

def xsym():
    return  [sym(one) for one in x()] * 5

def sym(i):
    if i<0.4: return [i, "a"]
    if i<0.6: return [i, "b"]
    return           [i, "c"]

def x():
    seed(1)
    return  [      r()*0.05 for _ in range(n)] + \
          [0.2 + r()*0.05 for _ in range(n)] +  \
          [0.4 + r()*0.05 for _ in range(n)] +   \
          [0.6 + r()*0.05 for _ in range(n)] +    \
          [0.8 + r()*0.05 for _ in range(n)]


file = open("output2.txt","w+")
imp = xsym()
# xlst, ylst = [], []
# for i in imp:
#     xlst.append(i[0])
#     ylst.append(i[1])
# div1 = Div(xlst, ylst, "sym")
div1 = Div(imp, "sym")
file.write(div1.splits)
file.close()

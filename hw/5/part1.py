from Div1 import Div
import random
if __name__ == "__main__":
    # Part1
    file = open("output1.txt", "w+")
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
    # xlst, ylst = [], []
    # for i in imp:
    #     xlst.append(i[0])
    #     ylst.append(i[1])
    # div1 = Div(xlst, ylst, "num")
    div1 = Div(imp, "num")
    file.write(div1.splits)
    file.close()

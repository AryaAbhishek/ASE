import random
import math


class Col:
    def __init__(self):
        self.n = 0


class Num(Col):
    def __init__(self):
        super().__init__()
        self.mu = self.m2 = self.sd = 0
        self.lo = 10**32
        self.hi = -1*self.lo

    def add(self, a):
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

    def num_sd(self):
        if self.m2 < 0:
            return 0
        if self.n < 2:
            return 0
        return self.m2/math.sqrt(self.n-1)

    def num_mean(self):
        return self.mu

    def num_norm(self, c):
        return (c-self.lo)/(self.hi-self.lo + 10**-32)

    def num_less(self, b):
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
    pass


class Some(Col):
    pass


if __name__ == "__main__":
    col = Num()
    list1 = [random.randint(1, 100) for i in range(100)]
    sd_add = []
    mean_add = []
    sd_less = []
    mean_less = []

    for a in range(100):
        col.add(list1[a])
        if (a+1) % 10 == 0:
            sd_add.append(col.num_sd())
            mean_add.append(col.num_mean())

    for a in range(99, 8, -1):
        if (a+1) % 10 == 0:
            sd_less.append(col.num_sd())
            mean_less.append(col.num_mean())
        col.num_less(list1[a])
    file = open("out.txt", "w+")
    file.write("list of 100 random numbers: \n"+str(list1))
    sd_less = sd_less[::-1]
    mean_less = mean_less[::-1]
    for i in range(len(sd_add)):
        file.write("\n")
        file.write("\n Sd while adding number: " + str(sd_add[i]))
        file.write("\n Sd while deleting number: " + str(sd_less[i]))
        file.write("\n mean while adding number: " + str(mean_add[i]))
        file.write("\n mean while deleting number: " + str(mean_less[i]))
    file.close()

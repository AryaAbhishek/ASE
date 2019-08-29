import random


class Col:
    # initialize n - total numbers used to find mean and SD
    def __init__(self):
        self.n = 0


class Num(Col):
    # lo - lowest number, hi - highest number, mu - mean, m2 - summation of square of differences from mean
    def __init__(self):
        super().__init__()
        self.mu = self.m2 = self.sd = 0
        self.lo = 10**32
        self.hi = -1*self.lo

    def add(self, a):  # get the new number and update mu, sd, lo, hi, m2
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


class Sym(Col):  # not used in this assignment
    pass


class Some(Col):  # not used in this assignment
    pass


if __name__ == "__main__":  # generates a list of 100 random numbers and then first call add method and then calls
    # less method to compare the sd and mean cached during both operations
    col = Num()
    list1 = [random.randint(1, 100) for i in range(100)]
    sd_add = []  # store standard deviation at every 10th index of random number list while calling add method
    mean_add = []  # store mean at every 10th index of random number list while calling add method
    sd_less = []  # store standard deviation at every 10th index of random number list while calling less method
    mean_less = []  # store mean at every 10th index of random number list while calling less method

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
    file = open("output.txt", "w+")
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

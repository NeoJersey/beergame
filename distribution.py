from scipy.stats import norm,poisson

class distribution:
    def __init__(self):
        # self.data = norm.rvs(loc=0, scale=1,size=1000)
        self.data = poisson.rvs(loc=0, mu=50, size=500)
        self.count = 0

    def getNext(self):
        next = self.data[self.count]
        self.count +=1
        if self.count == 500:
            self.count = 0
            self.data = poisson.rvs(loc=0, mu=50, size=500)
        return next

    def getCount(self):
        return self.count
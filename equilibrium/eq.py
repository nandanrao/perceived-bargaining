import numpy as np

def match_fn(unemployed, vacancies, aH):
    B = aH/3
    if vacancies/unemployed <= 1/(aH - B):
        return unemployed*vacancies/(unemployed + B*vacancies)
    else:
        return unemployed/aH


class Foo:
    def __init__(self, aH, aL, y, c, b, delta, sigma, r, match_fn, precision = .1):
        self.aH = aH
        self.aL = aL
        self.c = c
        self.match_fn = match_fn
        self.y = y # ??? is a random variable??
        self.delta = delta
        self.sigma = sigma
        self.r = r
        self.b = b

        self.A = (self.r + self.sigma)/(1 - self.sigma) + self.delta
        self.B = aH/3
        # Note: we are not including 0!!
        self.X = np.round(np.arange(0, 1/aH, precision), 4)[1:]
        self._vacancies = np.ones(len(self.X))
        self._unemployed = np.ones(len(self.X))
        self._values = np.zeros(len(self.X))

    def get_x(self, x):
        """Gets the index in self.X of a given market x"""
        try:
            return np.flatnonzero(self.X == x)[0]
        except IndexError:
            raise Exception('Trying to get an x that does not exist!')

    def vacancies(self, x):
        return float(self._vacancies[self.get_x(x)])

    def unemployed(self, x):
        return float(self._unemployed[self.get_x(x)])

    def tightness(self, x):
        # try:
        #     return self.vacancies(x)/self.unemployed(x)
        # except ZeroDivisionError:
        #     print("WHY DIS BE ZERO??")
            # return 10 # RETURN SOMETHING ELSE?
        return x/(1 - self.B*x)

    def wage(self, x):
        # One annoying part of this model is how wages go down
        # as vacancies go up... to "induce" firms into a tighter market.
        # but logically, that should make it tighter still...
        # if no vacancies, this might not hold???
        x = float(x)
        try:
            return self.y - self.c*self.A*self.tightness(x)/x
        except ZeroDivisionError:
            return


    def pos_win(self, m):
        aH, aL = self.aH, self.aL
        return aH + aL - aH*aL/m

    def pos_lose(self, x, m):
        aH, aL = self.aH, self.aL
        return aH - (aH - m)*(1 - x*aL)/(1 - x*m)

    def pick_market(self):
        # max over value_of_market...
        # his is dynamic programming - use maret values, stored?
        i = np.argmax(self._values)
        return self.X[i]

    def unemployed_value(self, m):
        x = self.pick_market()
        R = self._values[self.get_x(x)]
        return (self.b + (1-self.sigma)*R)/(1 + self.r)

    def employed_value(self, m, w):
        A = (self.r + self.sigma)/(1 - self.sigma) + self.delta
        V = self.unemployed_value(m)
        return 1/A * (w/(1-self.sigma) + self.delta * V)

    def value_of_market(self, x, m):
        J = self.employed_value(self.pos_win(m), self.wage(x))
        V = self.unemployed_value(m)
        return x*m*J + (1 - x*m)*V

    def it(self, m):
        for i in range(10):
            for x in self.X:
                self._values[self.get_x(x)] = self.value_of_market(x, m)
        return self._values

    def foo(self, m):
        (1 - sigma)(1 - aH * pick_market(m))

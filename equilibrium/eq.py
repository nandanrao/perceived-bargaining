import numpy as np

class Foo:
    def __init__(self, aH, aL, y, c, delta, sigma, match_fn, precision = .1):
        self.aH = aH
        self.aL = aL
        self.c = c
        self.match_fn = match_fn
        self.y = y # ??? is a random variable??
        self.delta = delta
        self.sigma = sigma

        self.A = (self.r + self.sigma)/(1 - self.sigma) + self.delta
        self.X = np.arange(0, 1/aH, precision)
        self._vacancies = np.zeros(len(self.X))
        self._unemployed = np.zeros(len(self.X))

    def get_x(x):
        return np.flatnonzero(self.X == x)[0]

    def vacancies(self, x):
        return self._vacancies[self.get_x(x)]

    def unemployed(self, x):
        return self._unemployed[self.get_x(x)]

    def tightness(self, x):
        try:
            return self.vacancies(x)/self.unemployed(x)
        except ZeroDivisionError:
            return 0 # RETURN SOMETHING ELSE?

    def wage(self, x):
        # One annoying part of this model is how wages go down
        # as vacancies go up... to "induce" firms into a tighter market.
        # but logically, that should make it tighter still...
        # if no vacancies, this might not hold???
        return self.y - self.c*self.A*self.tightness(x)/x

    def pos_win(self, m):
        aH, aL = self.aH, self.aL
        return aH + aL - aH*aL/m

    def pos_lose(self, x, m):
        aH, aL = self.aH, self.aL
        return aH - (aH - m)*(1 - x*aL)/(1 - x*m)


    def value_of_market(x, m):
        x*m*J(post_win(x,m), wage(x))

    def pick_market(m):
        # max over value_of_market...
        return 5

    def value(self, m):
        return (self.b + (1-self.sigma)*self.pick_market(m))/(1 + self.r)

    def employed_value(self, m, w):
        # bellman with
        return 'foo'

    def foo(m):
        (1 - sigma)(1 - aH * pick_market(m))

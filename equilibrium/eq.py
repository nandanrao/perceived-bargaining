import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sympy import Symbol, Eq, solveset

class InequilibriumError(BaseException):
    pass

class AssumptionError(BaseException):
    pass

def match_fn(unemployed, vacancies, aH):
    B = aH/3
    if vacancies/unemployed <= 1/(aH - B):
        return unemployed*vacancies/(unemployed + B*vacancies)
    else:
        return unemployed/aH

def flatten(l):
    return (flatten(l[0]) +
            (flatten(l[1:]) if len(l) > 1 else [])
            if type(l) is list else [l])

class BeliefTree:
    def __init__(self, m, unemployed, employed = [0.,0.]):
        self.m = m
        self.unemployed = np.array(unemployed)
        self.employed = np.array(employed)
        self.x = None
        self.children = []

    def add_market(self, x):
        self.x = x

    def add_children(self, low, high):
        self.children = [low, high]

    def __str__(self, level=1):
        uL, uH = self.unemployed
        eL, eH = self.employed
        ret = "   " * (level-1) + "|--" + \
              'm: {0:.2f}, u: {1:.2f}, e: {2:.2f} \n'.format(self.m, uL, eL)
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def get_amounts(self, v):
        e = getattr(self, v)
        for c in self.children:
            e += c.get_amounts(v)
        return e

    def __repr__(self):
        return str(self)

    def __len__(self):
        if self.children:
            return 1 + len(self.children[0])
        return 1


class Equilibrium:
    def __init__(self, aH, aL, y, c, b, delta, sigma, r, B, precision = .1, distortion = 0.0):
        self.aH = aH
        self.aL = aL
        self.c = c
        self.match_fn = match_fn
        self.y = y # ??? is a random variable??
        self.delta = delta
        self.sigma = sigma
        self.r = r
        self.b = b
        self.B = B
        self.distortion = distortion

        self.A = (self.r + self.sigma)/(1 - self.sigma) + self.delta


        # Note: we are not including 0!
        self.X = np.around(np.arange(0, 1/aH, precision), 4)[1:]
        self._values = np.zeros(len(self.X))

        self.pH = .5
        self.pL = 1 - self.pH
        self.m0 = self.aH * self.pH + self.aL * self.pL
        self._unemployed = { self.m0 : [self.pL * self.sigma, self.pH * self.sigma ]}
        self._employed = { self.m0 : [0,0 ]}
        self._wages = {}

        self.belief_tree = BeliefTree(self.m0, [self.pL*self.sigma, self.pH*self.sigma])

        # Check Assumption #2 regarding labor productivity, which ensures
        # workers will always accept matches
        self.assumption_2()

        # Check that delta is small enough for Assumption #3
        self.assumption_3()

        if self.aH <= self.aL:
            raise AssumptionError('High skill must be higher than low skill!')

        if self.B >= aH or self.B <= 0:
            raise AssumptionError('B must be between 0 and aH!. B: {}. aH: {}'.format(self.B, self.aH))

        # self._employed = { str(self.pos_win(0.5)) : self.currently_employed}
        # self._vacancies = np.zeroes(len(self.X))
        # self._unemployed = np.zeroes(len(self.X))

    def tightness(self, x):
        # try:
        #     return self.vacancies(x)/self.unemployed(x)
        # except ZeroDivisionError:
        #     print("WHY DIS BE ZERO??")
            # return 10 # RETURN SOMETHING ELSE?
        return x/(1 - self.B*x)

    def tightness_prime(self, y):
        x = Symbol('x')
        return self.tightness(x).diff().subs(x, y)

    def x_star(self):
        x = Symbol('x')
        e = Eq(self.tightness(x).diff() - self.aH * self.tightness(1/self.aH))
        l = list(solveset(e))
        return [i for i in l if (i > 0) and (i < 1/self.aH)][0]

    def Omega(self):
        d = Symbol('d')
        r,s = self.r, self.sigma
        aL,aH = self.aL, self.aH
        c = (r + s)/(1 - s)
        b = (1 + aL/aH) * (c + d) + aL/aH
        e = Eq( c * (c + d)**2 - d*b )
        l = [x for x in list(solveset(e)) if x > 0]
        return l[0]

    def assumption_2(self):
        left = (self.y - self.b)/self.c
        x_star = self.x_star()
        right = ((self.A + self.aH*x_star)*self.tightness_prime(x_star)
                 - self.aH*self.tightness(x_star))
        if left <= right:
            raise AssumptionError('Assumption 2 not satisfied. {} is not greater than {}'.format(left, right))

    def assumption_3(self):
        d_bar = self.Omega()
        if self.delta > d_bar:
            raise AssumptionError('Assumption 3 is not satisfied. {} is greater than d_bar: {}'.format(self.delta, d_bar))

    def get_x(self, x):
        """Gets the index in self.X of a given market x"""
        try:
            return np.flatnonzero(self.X == x)[0]
        except IndexError:
            raise Exception('Trying to get an x that does not exist!')

    # def vacancies(self, x):
    #     return float(self._vacancies[self.get_x(x)])

    # def unemployed(self, x):
    #     return float(self._unemployed[self.get_x(x)])



    def wage(self, x):
        # One annoying part of this model is how wages go down
        # as vacancies go up... to "induce" firms into a tighter market.
        # but logically, that should make it tighter still...
        # if no vacancies, this might not hold???
        x = float(x)
        try:
            return self.y - self.c*self.A*self.tightness(x)/x
        except ZeroDivisionError:
            pass

    def pos_win(self, m):
        aH, aL = self.aH, self.aL
        bayesian = aH + aL - aH*aL/m
        return np.round(bayesian, 6)

    def pos_lose(self, x, m):
        aH, aL = self.aH, self.aL
        bayesian = aH - (aH - m)*(1 - x*aL)/(1 - x*m)
        behavioral = bayesian - (m - aL)*self.distortion
        # update = bayesian - m
        # behavioral = max(aL + eps, m + update * (1 + self.distortion))
        return np.round(behavioral, 6)

    def pick_market(self):
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
        e = 1
        while e > 1e-06:
            prev = np.copy(self._values)
            for x in self.X:
                self._values[self.get_x(x)] = self.value_of_market(x, m)
            e = np.max(np.abs((prev - self._values)))
        return self._values

    def unemployed(self, m):
        return self._unemployed[m]

    def update_stats(self, d, key, val):
        try:
            d[key] += np.array(val)
        except KeyError:
            d[key] = np.array(val)

    def employed_with_belief(self, x, mn, uL, uH):
        eq = lambda a,u: ((1 - self.sigma) * a * x * u) / (self.sigma + (1 - self.sigma)*self.delta)
        return [eq(a,u) for a,u in [(self.aL, uL), (self.aH, uH)]]

    def unemployed_rejects(self, x, mn, uL, uH):
        eq = lambda a,u: (1 - self.sigma)*(1 - a * x)*u
        return [eq(a,u) for a,u in [(self.aL, uL), (self.aH, uH)]]

    def fired_employees(self, employed):
        eq = lambda e: (1 - self.sigma) * self.delta * e
        return [eq(e) for e in employed]

    def equilibrium_tree(self, max_depth = 4, tree = None, it = 1):
        if not tree:
            tree = self.belief_tree

        # Base case
        if it >= max_depth:
            self._equilibrium = True
            return tree

        # Unemployed with current beliefs
        # your double updating!!! Get from tree...
        curr_uL, curr_uH = tree.unemployed

        # this feels really mutable and ugly
        m = tree.m
        self.it(m)

        # Given these beliefs, x is the optimum market
        x = self.pick_market()

        # Next beliefs in the tree
        mL = self.pos_lose(x, m)
        mH = self.pos_win(m)

        # Determine employed and unemployed amounts
        uL = self.unemployed_rejects(x, mL, curr_uL, curr_uH)
        eH = self.employed_with_belief(x, mH, curr_uL, curr_uH)
        uH = self.fired_employees(eH)

        # # update state
        # if mL != m:
        #     self.update_stats(self._unemployed, mL, uL)
        if mH != m:
            self.update_stats(self._wages, x, eH)
        #     self.update_stats(self._unemployed, mH, uH)
        #     self.update_stats(self._employed, mH, eH)
        low = BeliefTree(mL, uL)
        high = BeliefTree(mH, uH, eH)

        # Recurse
        tree.add_children(self.equilibrium_tree(max_depth, low, it+1),
                          self.equilibrium_tree(max_depth, high, it+1))
        return tree

    def equilibrium(self, max_depth = 4):
        self._belief_tree = self.equilibrium_tree(None, 0, max_depth)

    def _flatten(self, z):
        return [ x for y in z for x in y ]

    def get_unemployment(self):
        if not self._belief_tree:
            raise InequilibriumError('You must first find equilibrium before getting unemployment')

        u = sum(self._flatten(self._unemployed.values()))
        e = sum(self._flatten(self._employed.values()))
        return u/(u+e)

    def plot_wages(self, skill = 'H'):
        if not self._belief_tree:
            raise InequilibriumError('You must first find equilibrium before getting unemployment')

        i = 0 if skill == 'L' else 1
        amts = [w[i] for w in self._wages.values()]
        arr = sorted(list(zip(self._wages.keys(), amts)),
                     key = lambda x: -x[0])
        return pd.DataFrame(arr).plot.bar(x = 0, y = 1)


## INTERACTIVE
# def show_one(self):
#     fig = self.get_figure()
#     fig.savefig("/tmp/chart.png", dpi=90)
#     fig.clear()

# import matplotlib
# matplotlib.artist.Artist.show_one = show_one

# def test_values(**kwargs):
#     foo = Equilibrium(**kwargs)
#     foo.equilibrium()
#     return foo.get_unemployment()

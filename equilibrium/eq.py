import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sympy import Symbol, Eq, solveset

class InequilibriumError(BaseException):
    pass

class AssumptionError(BaseException):
    pass

def match_fn(unemployed, vacancies, aH):
    """ Not actually used... """
    B = aH/3
    if vacancies/unemployed <= 1/(aH - B):
        return unemployed*vacancies/(unemployed + B*vacancies)
    else:
        return unemployed/aH


class BeliefTree:
    """ Class that represents the equilibrium tree of beliefs """
    def __init__(self, m, unemployed, employed = [0.,0.]):
        self.m = m
        self.unemployed = np.array(unemployed)
        self.employed = np.array(employed)
        self.x = None
        self.children = []

    def add_market(self, x):
        self.x = x

    def add_child(self, child):
        if child:
            self.children.append(child)
        return self

    def get_amounts(self, v):
        e = np.copy(getattr(self, v))
        for c in self.children:
            e += c.get_amounts(v)
        return e

    def __str__(self, level=1):
        uL, uH = self.unemployed
        eL, eH = self.employed
        ret = "   " * (level-1) + "|--" + \
              'm: {0:.2f}, u: {1:.4f}, e: {2:.4f} \n'.format(self.m, uL + uH, eL + eH)
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return str(self)

    def __len__(self):
        if self.children:
            return 1 + max([len(c) for c in self.children])
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
        self.B = B*aH # B \in {0, aH}, so just let it be a percentage of aH
        self.distortion = distortion

        self.A = (self.r + self.sigma)/(1 - self.sigma) + self.delta

        # Note: we are notf including 0!
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

        # Check other basic assumptions of the params
        if self.aH <= self.aL:
            raise AssumptionError('High skill must be higher than low skill!')

        if self.B >= aH or self.B <= 0:
            raise AssumptionError('B must be between 0 and 1!. B: {}'.format(self.B, self.aH))


    def tightness(self, x):
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
        """ Posterior belief after a win. """
        aH, aL = self.aH, self.aL
        bayesian = aH + aL - aH*aL/m
        return np.round(bayesian, 6)

    def pos_lose(self, x, m):
        """ Posterior belief after a loss. """
        aH, aL = self.aH, self.aL
        bayesian = aH - (aH - m)*(1 - x*aL)/(1 - x*m)
        behavioral = bayesian - (m - aL)*self.distortion
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
        """ Performs value function iteration with a given belief m """
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

    def equilibrium(self, max_depth = 4, tree = None, it = 1):
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

        trim = lambda a: np.max(np.abs(np.array([0,0]) - a)) < 1e-06

        # Update the amounts with a given level of wage
        if mH != m:
            self.update_stats(self._wages, x, eH)

        # Recurse!
        low,high = None, None
        if not trim(uL):
            low = self.equilibrium(max_depth, BeliefTree(mL, uL), it+1)
        if not trim(uH) and not trim(eH):
            high = self.equilibrium(max_depth, BeliefTree(mH, uH, eH), it+1)
        return tree.add_child(low).add_child(high)


    def plot_wages(self, skill = 'H'):
        if not self.belief_tree:
            raise InequilibriumError('You must first find equilibrium before getting unemployment')

        i = 0 if skill == 'L' else 1
        amts = [w[i] for w in self._wages.values()]
        arr = sorted(list(zip(self._wages.keys(), amts)),
                     key = lambda x: -x[0])
        return pd.DataFrame(arr).plot.bar(x = 0, y = 1)

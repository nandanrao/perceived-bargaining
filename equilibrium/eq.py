import numpy as np

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
        self.X = np.around(np.arange(0, 1/aH, precision), 4)[1:]
        self._values = np.zeros(len(self.X))

        self.pH = .5
        self.pL = 1 - self.pH
        self._unemployed = { '0.5': [self.pL * self.sigma, self.pH * self.sigma ]}
        # self._employed = { str(self.pos_win(0.5)) : self.currently_employed}
        # self._vacancies = np.zeroes(len(self.X))
        # self._unemployed = np.zeroes(len(self.X))


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
            e = np.max(prev - self._values)
        return self._values

    def equilibrium_tree(self, m, it = 0, max_depth = 4):
        self.it(m) # this feels really mutable and ugly
        x = self.pick_market()
        mL, mH = self.pos_lose(x,m), self.pos_win(m)
        if it >= max_depth:
            return [mL, mH]
        return [m, self.equilibrium_tree(mL, it+1), self.equilibrium_tree(mH, it+1)]

    def unemployed(self, m):
        return self._unemployed[str(m)]

    def employed_from(self, m):
        self.it(m)
        pos = self.pos_win(m)
        x = self.pick_market()
        uL, uH = self.unemployed(m)
        eq = lambda a,u: ((1 - self.sigma) * a * x * u) / (self.sigma + (1 - self.sigma)*self.delta)
        L,H = [eq(a,u) for a,u in [(self.aL, uL), (self.aH, uH)]]
        return (pos, [L,H])

    def unemployed_rejects(self, m):
        # for any m
        self.it(m)
        x = self.pick_market()
        mn = self.pos_lose(x, m)
        # traverse tree and generate all unemployed...
        uL, uH = self.unemployed(m)
        L,H = [(1 - self.sigma)*(1 - a * x)*u for a,u in [(self.aL, uL), (self.aH, uH)]]
        return (mn, [L,H])

    def fired_employees(self, m):
        # for any m
        self.it(m)
        eq = lambda e: (1 - self.sigma) * self.delta * e
        return [eq(e) for e in self.employed_from(m)[1]]

    def build_distributions(self, tree):
        m0 = tree[0]
        m1, amts = self.unemployed(m0)
        self._unemployed[m1] = amts

        rejects = get_type(tree, rejects=True)
        for m in rejects:
            self._unemployed[str(m)] = self.unemployed_rejects(m)[1]


def get_type(tree, rejects=True):
    try:
        L,H = tree[1], tree[2]
        target = L if rejects else H
        if len(target) > 2:
            return [target[0]] + get_type(L, rejects) + get_type(H, rejects)
        else: # target is a leaf
            return get_type(L, rejects) + get_type(H, rejects)
    except IndexError: # tree is leaf
        return [tree[0]] if rejects else [tree[1]]

# employed workers with type pos_win(m)

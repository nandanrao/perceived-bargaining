import numpy as np
from scipy.stats import beta

from sympy import symbols, plot_implicit, Eq, solve, S, solveset
n,p = symbols('n p')


eq = Eq(n*p*(1-p)**(n-1) - 0.05)
plt = plot_implicit(eq, x_var =(n, 1, 30), y_var=(p, 0.0001, .9999))


ns = range(15,17)
eps = .01
sols = [solve(Eq(n*p*(1-p)**(n-1) - eps), p) for n in ns]
ps = [s[1] if len(s) > 1 else s[0] for s in sols]
[p*n for p,n in zip(ps, ns)]


beta,n,j,k = symbols('beta n j k')

eq = beta**(j-n)/(2 + j) * Product(1 - 1/{1+k}, (k, n+1, j))
s = Sum(eq, (j, n+1, oo))
p = 1/(1 + n) + s


def u(rho):
    if rho == 1:
        return lambda c: np.log(c + 1)
    else:
        return lambda c: ((c + 1)**(1 - rho) - 1)/(1 - rho)

def vq(out, beta):
    return out/(1 - beta)

def p(n = 1, beta = .98, eps = 1e-6, max_iter = 10000):
    p = 0
    prev = 1
    for i in range(max_iter):
        add = beta*prev*post(n)
        if add < eps:
            break
        p += add
        n += 1
        prev = (1 - post(n))*prev
    return p


def stopping(out, n = 20, beta = .999, rho = 2, W = 4.1):
    o = out/(1 - beta)
    return np.abs(u(rho)(W + o)*p(n) - u(rho)(o))

from scipy.optimize import minimize

minimize(stopping, [5.])


################################
# S/F GAME ANALYSIS
################################

from sympy.solvers.inequalities import solve_univariate_inequality
from sympy import *
import numpy as np

x, n, W = symbols('x n W')

post = lambda n: 1 / (1 + 1 + n)

## Log Utility
c = exp( post(n) * log(W))
e = post(x*n) * log(W) - log(c/x)

a = np.ones((20, 20, 20))
for i,n_inner in enumerate(np.arange(1, 200, 10)):
    for j,W_inner in enumerate(np.arange(1, 200, 10)):
        f = lambdify(x, e.subs(W, W_inner).subs(n, n_inner), 'numpy')
        a[i, j, :] = f(np.linspace(1.2, 10, 20))

assert(len(a[a<0]) == 0)

## LOG PROOF

e = x*W**(1 / (x*n)) - W**(1/n)

for i,n_inner in enumerate(np.arange(1, 200, 10)):
    for j,W_inner in enumerate(np.arange(1, 200, 10)):
        f = lambdify(x, e.subs(W, W_inner).subs(n, n_inner), 'numpy')
        a[i, j, :] = f(np.linspace(1.2, 10, 20))

# FAILS: n = 1 no longer works!!!
assert(len(a[a<0]) == 0)


## CRRA UTILITY
rho = Symbol('rho')
c = Symbol('c')
u = lambda c: (c**(1 - rho) - 1)/(1 - rho)
# post = lambda n: 1 / (1 + 1 + n)
post = lambda n: 1/n

cost_fn = solve(post(n)*u(W) + (1 - post(n))*u(0) - u(c), c)[0]

e = post(x*n) * u(W) > u(cost_fn/x)

# c = (post(n) * u(W) * (1 - rho) + 1)**(1/(1 - rho))

e = post(n*x) * u(W) - u(c/x)

a = np.ones((20, 20, 20))
for i,n_inner in enumerate(np.arange(1, 200, 10)):
    for j,x_inner in enumerate(np.arange(2, 200, 10)):
        f = lambdify(rho, e.subs(x, x_inner).subs(n, n_inner), 'numpy')
        a[i, j, :] = f(np.linspace(-3, 30, 20))

assert(len(a[a < 0]) == 0)


# CRRA PROOF
e = x**rho * (1/n)**(1/(1 - rho)) - (1/n)**(1/(1-rho))

e = x*post(x*n)**(1/(1 - rho)) - post(n)**(1/(1-rho))
e = x**(1-rho)*post(x*n) - post(n)

e = e.subs(W, 500)
a = np.ones((20, 20, 20))
for i,n_inner in enumerate(np.arange(20, 220, 10)):
    for j,x_inner in enumerate(np.arange(2, 200, 10)):
        f = lambdify(rho, e.subs(x, x_inner).subs(n, n_inner), 'numpy')
        a[i, j, :] = f(np.linspace(-3, 3, 20))

# should be 0!
(np.linspace(-3,3,20)[np.argwhere(a < 0)[:, 2]] < 0).sum()
(np.linspace(-3,3,20)[np.argwhere(a < 0)[:, 2]] > 1).sum()



## THIS IS WITH INTEGRATING BETA PDF
rho = Symbol('rho')
u = lambda c: (c**(1 - rho) - 1)/(1 - rho)
post = lambda n: 1 / (1 + 1 + n)
c = (post(n) * u(W) * (1 - rho) + 1)**(1/(1 - rho))

e = (post(n*x) * u(W) - u(c/x)).subs(W, 500)

a = np.ones((20, 20, 20))
for i,n_inner in enumerate(np.arange(1, 200, 10)):
    for j,x_inner in enumerate(np.arange(2, 200, 10)):
        f = lambdify(rho, e.subs(x, x_inner).subs(n, n_inner), 'numpy')
        a[i, j, :] = f(np.linspace(-3, 30, 20))

assert(len(a[a < 0]) == 0)




# good sign...
e = (post(n*x) * u(W) - u(c/x)).subs(W, 500).subs(n, 1)
f = lambdify(x, e, 'numpy')
g = lambdify(rho, f(np.linspace(1.01, 20, 10)), 'numpy')

m = g(np.linspace(1.2, 20, 20))


domain = Interval.Lopen(1, 4)

e = (post(n*x) * u(W) > u(c/x)).subs(x, 5).subs(n, 6).subs(W, 50)

solve_univariate_inequality(e, rho, domain = domain)



c = exp(post(n) * log(W))




from sympy import Interval
rho = Symbol('rho')
x, n, W = symbols('x n W')

e = (n/((2 + n*x)**2)) * (1/(rho - 1)) <= 1/(x**rho)
from sympy import Union

domain = Union(Interval.Ropen(-50, 1), Interval.Lopen(1, 4))

solve_univariate_inequality(e.subs(n, 6).subs(x, 50), rho, domain = domain)
solveset(e, rho, domain = domain)


c = np.exp(post(n) * np.log(W))
np.log(c/x)
post(n*x)*np.log(W)


##################################
# implicit H/L game solution -- WRONG
##################################
t,N,n = symbols('t N n')

def p_hat(n, t, prior = .5):
    return prior * ((1-t)/1 - prior*t)**n


t = 2/N
eq = Eq(1 - (1-t)**(N-n) - (1 - t*p_hat(n,t)) * (1 - (1-t)**(N-n-1)) - t*p_hat(n,t)*(5/1))
plt = plot_implicit(eq, x_var = (n, 1, 30), y_var=(N, 3, 47))

4.25 / 9
24.5 / 45

##################################
# simulating policies in H/L game
##################################
import numpy as np

def create_game(n, p, high = True, high_val = 3):
    low_outcomes = [np.random.binomial(1,p) for i in range(n)]
    if high:
        high_outcomes = [np.random.binomial(1,p)*high_val for i in range(n)]
    else:
        high_outcomes = [0 for i in range(n)]
    return zip(low_outcomes, high_outcomes)


# gametype
n = 20
p = .10
gt = np.random.binomial(1, .5) == 1
game = create_game(n, p, gt)
for i,(l,h) in enumerate(game):
    pick = policy(i, l, h)
    # what to do with pick
    # update state?
    # redo policy
    # quit at some point?
    # this is just DP

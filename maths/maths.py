from sympy import symbols, plot_implicit, Eq, solve, S, solveset
n,p = symbols('n p')


eq = Eq(n*p*(1-p)**(n-1) - 0.05)
plt = plot_implicit(eq, x_var =(n, 1, 30), y_var=(p, 0.0001, .9999))


ns = range(15,17)
eps = .01
sols = [solve(Eq(n*p*(1-p)**(n-1) - eps), p) for n in ns]
ps = [s[1] if len(s) > 1 else s[0] for s in sols]
[p*n for p,n in zip(ps, ns)]




##################################
# implicit H/L game solution
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

from eq import *
import pytest
from numpy.testing import assert_approx_equal

def test_wage_returns_lower_value_with_higher_x():
    foo = Equilibrium(1, .05, .1, .05, .05, delta = .1, sigma = .2, r = .04, B=.3, precision = .05)
    foo.it(1.5)
    assert(foo.wage(.05) > foo.wage(.15))

def test_pos_win_raises_m():
    foo = Equilibrium(1, .05, .1, .05, .05, delta = .1, sigma = .2, r = .04, B=.3, precision = .05)
    assert(foo.pos_win(.5) > .5)
    assert(foo.pos_win(.5) < 1.)

def test_pos_lose_lowers_m():
    foo = Equilibrium(1, .05, .1, .05, .05, delta = .1, sigma = .2, r = .04, B=.3, precision = .05)
    assert(foo.pos_lose(.05, .5) < .5)
    assert(foo.pos_lose(.05, .5) > .1)

def test_pick_market_different_for_beliefs():
    foo = Equilibrium(1, .05, .1, .05, .05, delta = .1, sigma = .2, r = .04, B=.3, precision = .05)
    foo.it(0.4)
    a = np.copy(foo._values)
    a_market = foo.pick_market()
    foo.it(0.6)
    b = np.copy(foo._values)
    b_market = foo.pick_market()
    foo.it(0.8)
    c = np.copy(foo._values)
    c_market = foo.pick_market()
    assert(np.max(b) > np.max(a))
    assert(np.max(c) > np.max(b))
    assert(a_market > b_market)
    assert(b_market > c_market)


def test_equilibrium_tree_respects_depth():
    foo = Equilibrium(1, .05, .1, .05, .05, delta = .1, sigma = .2, r = .04, B=.3, precision = .05)
    tree = foo.equilibrium(3)
    assert(len(tree) == 3)
    tree = foo.equilibrium(5)
    assert(len(tree) == 5)

def test_belief_tree_get_amounts():
    tree = BeliefTree(0, [1,2])
    l,r = BeliefTree(0, [1,3], [1,1]), BeliefTree(0, [3,5], [1,2])
    tree.add_child(l).add_child(r)
    assert(np.all(tree.get_amounts('employed') == [2, 3]))
    assert(np.all(tree.get_amounts('unemployed') == [5, 10]))


def test_wages_correctly_gathers_employed():
    foo = Equilibrium(1, .05, .1, .05, .05, delta = .1, sigma = .2, r = .04, B=.3, precision = .01)
    foo.equilibrium()
    wages = sum([i for x in foo._wages.values() for i in x])
    employed = sum(foo.belief_tree.get_amounts('employed'))
    assert_approx_equal(wages, employed, 6)

def test_distortion():
    foo = Equilibrium(1, .05, .1, .05, .05, delta = .007, sigma = .1, r = .04, B=.6, precision = .01, distortion = 0.05)
    bar = Equilibrium(1, .05, .1, .05, .05, delta = .007, sigma = .1, r = .04, B=.6, precision = .01, distortion = 0.5)
    m = (1 + 0.5)/2
    foo.it(m)
    bar.it(m)
    x_foo1 = foo.pick_market()
    x_bar1 = bar.pick_market()
    assert(x_foo1 == x_bar1)

    foo.it(foo.pos_lose(x_foo1, m))
    bar.it(bar.pos_lose(x_bar1, m))
    x_foo2 = foo.pick_market()
    x_bar2 = bar.pick_market()
    # This is our test ==> discretizing into 10 bins, bar switches, while foo doesn't
    assert(np.round(x_foo1, 1) == np.round(x_foo2, 1))
    assert(np.round(x_foo2, 1) < np.round(x_bar2, 1))



# def test_fired_employees():
#     foo = Equilibrium(.9, .1, .1, .1, .05, .1, .2, .04, 0.5, precision = .05)
#     foo.build_distributions(foo.equilibrium_tree(0.5))
#     print(foo._unemployed)
#     assert(False)

from eq import *

# def test_tightness_returns_max():
#     foo = Foo(.9, .1, 15, .1, .05, .1, .2, .04, match_fn, precision = .05)
#     assert(foo.tightness(.05) == 10) # max tightness 10??

def test_wage_returns_lower_value_with_higher_x():
    foo = Foo(.9, .1, 15, .1, .05, .1, .2, .04, match_fn, precision = .05)
    foo.it(1.5)
    assert(foo.wage(.05) > foo.wage(.15))

def test_pos_win_raises_m():
    foo = Foo(.9, .1, 15, .1, .05, .1, .2, .04, match_fn, precision = .05)
    assert(foo.pos_win(.5) > .5)
    assert(foo.pos_win(.5) < .9)

def test_pos_lose_lowers_m():
    foo = Foo(.9, .1, 15, .1, .05, .1, .2, .04, match_fn, precision = .05)
    assert(foo.pos_lose(.05, .5) < .5)
    assert(foo.pos_lose(.05, .5) > .1)

def test_pick_market_different_for_beliefs():
    foo = Foo(.9, .1, .1, .1, .05, .1, .2, .04, match_fn, precision = .05)
    foo.it(1.1)
    foo.it(1.1)
    a = np.copy(foo._values)
    a_market = foo.pick_market()
    foo.it(2.9)
    foo.it(2.9)
    b = np.copy(foo._values)
    b_market = foo.pick_market()
    print(a)
    print(b)
    print(foo.X)
    print(foo.wage(.05))
    print(foo.wage(.9))
    assert(np.greater(b,a).all())
    assert(a_market != b_market)

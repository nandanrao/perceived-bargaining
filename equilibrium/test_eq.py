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
    a = np.copy(foo._values)
    a_market = foo.pick_market()
    foo.it(2.9)
    b = np.copy(foo._values)
    b_market = foo.pick_market()
    assert(np.max(b) > np.max(a))
    assert(a_market != b_market)


def test_unemployment_amounts():
    foo = Foo(.9, .1, .1, .1, .05, .1, .2, .04, match_fn, precision = .05)
    print(foo.unemployed_rejects(.5))
    # assert(False)

def test_employed_from():
    foo = Foo(.9, .1, .1, .1, .05, .1, .2, .04, match_fn, precision = .05)
    print(foo.employed_from(.5))
    # assert(False)

def test_fired_employees():
    foo = Foo(.9, .1, .1, .1, .05, .1, .2, .04, match_fn, precision = .05)
    print(foo.fired_employees(.5))
    assert(False)

def test_get_rejects():
    tree = ['root',
            ['left1',
             ['left2', ['left-leaf1', 'right-leaf1'], ['left-leaf2', 'right-leaf2']],
             ['right2', ['left-leaf3', 'right-leaf3'], ['left-leaf4', 'right-leaf4']]],
            ['right1',
             ['left3', ['left-leaf5', 'right-leaf5'], ['left-leaf6', 'right-leaf6']],
             ['right3', ['left-leaf7', 'right-leaf7'], ['left-leaf8', 'right-leaf8']]]]
    rejects = get_type(tree)
    lefties = ['left1', 'left2', 'left-leaf1', 'left-leaf2', 'left-leaf3', 'left-leaf4', 'left3', 'left-leaf5', 'left-leaf6', 'left-leaf7', 'left-leaf8']
    # assert is the same without caring about order
    assert(len(rejects) == len(lefties))
    assert(set(rejects) == set(lefties))

def test_get_winners():
    tree = ['root',
            ['left1',
             ['left2', ['left-leaf1', 'right-leaf1'], ['left-leaf2', 'right-leaf2']],
             ['right2', ['left-leaf3', 'right-leaf3'], ['left-leaf4', 'right-leaf4']]],
            ['right1',
             ['left3', ['left-leaf5', 'right-leaf5'], ['left-leaf6', 'right-leaf6']],
             ['right3', ['left-leaf7', 'right-leaf7'], ['left-leaf8', 'right-leaf8']]]]
    rejects = get_type(tree, False)
    righties = ['right1', 'right2', 'right-leaf1', 'right-leaf2', 'right-leaf3', 'right-leaf4', 'right3', 'right-leaf5', 'right-leaf6', 'right-leaf7', 'right-leaf8']
    # assert is the same without caring about order
    assert(len(rejects) == len(righties))
    assert(set(rejects) == set(righties))

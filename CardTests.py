'''
Test script for Card.py.
'''

import sys, traceback

import Card as C

def wrapper(f):
    try:
        f()
        print('TEST PASSED!\n')
    except AssertionError as e:
        print('TEST FAILED DUE TO ASSERTION ERROR!')
        print('-' * 60)
        traceback.print_exc(file=sys.stdout)
        print('-' * 60)
        print('\n')
    except:
        print("Exception in user code:")
        print('-' * 60)
        traceback.print_exc(file=sys.stdout)
        print('-' * 60)
        print('\n')

def test_init_card():
    black_cards = \
            [('A', 'S'), (2, 'C'), (5, 'S'), (9, 'C'), ('J', 'S'), ('K', 'C')]
    red_cards = \
            [('A', 'H'), (3, 'D'), (4, 'H'), (8, 'D'), (10, 'H'), ('Q', 'D')]

    for (r, s) in black_cards:
        c = C.Card(r, s)
        assert c.rank == r
        assert c.suit == s
        assert c.color == 'black'

    for (r, s) in red_cards:
        c = C.Card(r, s)
        assert c.rank == r
        assert c.suit == s
        assert c.color == 'red'

    bad_ranks = [('Ace', 'S'), ('2', 'H'), ('k', 'S'), ('10', 'S'), \
                 ('T', 'C'), ('foobar', 'D')]

    for (r, s) in bad_ranks:
        try:
            c = C.Card(r, s)
            assert False, 'should never reach this point'
        except C.InvalidRank:
            pass

    bad_suits = [('A', 'Spades'), (2, 'h'), (3, 'SC'), (4, 'SD'), \
                 ('K', 'SH'), ('A', 'xxx')]

    for (r, s) in bad_suits:
        try:
            c = C.Card(r, s)
            assert False, 'should never reach this point'
        except C.InvalidSuit:
            pass

def test_goes_above():
    true_pairs = [((2, 'S'),   ('A', 'S')),
                  ((3, 'D'),   (2, 'D')),
                  ((10, 'H'),  (9, 'H')),
                  (('J', 'H'), (10, 'H')),
                  (('Q', 'S'), ('J', 'S')),
                  (('K', 'C'), ('Q', 'C'))]
    for ((r1, s1), (r2, s2)) in true_pairs:
        c1 = C.Card(r1, s1)
        c2 = C.Card(r2, s2)
        assert c1.goes_above(c2)

    false_pairs = [((2, 'S'),   (4, 'S')),
                   ((3, 'D'),   (3, 'D')),
                   ((10, 'H'),  (8, 'H')),
                   (('J', 'H'), ('A', 'H')),
                   (('Q', 'S'), ('K', 'S')),
                   (('K', 'C'), ('J', 'C'))]
    for ((r1, s1), (r2, s2)) in false_pairs:
        c1 = C.Card(r1, s1)
        c2 = C.Card(r2, s2)
        assert not c1.goes_above(c2)

    c = C.Card('A', 'S')
    bad_cards = ['2s', (2, 'S'), 'xxx', 123]
    for card in bad_cards:
        try:
            c.goes_above(card)
        except AssertionError:
            return  # OK
        assert False, 'should never reach this point'

def test_goes_below():
    true_pairs = [(('A', 'S'), (2, 'H')),   # perfectly OK
                  ((2, 'S'),   (3, 'H')),
                  ((2, 'S'),   (3, 'D')),
                  ((3, 'D'),   (4, 'S')),
                  ((3, 'D'),   (4, 'C')),
                  ((10, 'H'),  ('J', 'S')),
                  ((10, 'H'),  ('J', 'C')),
                  (('J', 'C'), ('Q', 'H')),
                  (('J', 'C'), ('Q', 'D')),
                  (('Q', 'S'), ('K', 'H')),
                  (('Q', 'S'), ('K', 'D'))]
    for ((r1, s1), (r2, s2)) in true_pairs:
        c1 = C.Card(r1, s1)
        c2 = C.Card(r2, s2)
        assert c1.goes_below(c2)

    false_pairs = [(('A', 'S'), (2, 'C')),
                   ((2, 'S'),   (3, 'S')),
                   ((2, 'S'),   (3, 'C')),
                   ((2, 'S'),   (4, 'H')),
                   ((2, 'S'),   (4, 'D')),
                   ((2, 'S'),   ('A', 'D')),
                   ((10, 'H'),  ('J', 'H')),
                   (('J', 'H'), ('A', 'S')),
                   (('K', 'S'), ('Q', 'H')),
                   (('K', 'C'), ('J', 'D'))]
    for ((r1, s1), (r2, s2)) in false_pairs:
        c1 = C.Card(r1, s1)
        c2 = C.Card(r2, s2)
        assert not c1.goes_below(c2)

    c = C.Card('A', 'S')
    bad_cards = ['2s', (2, 'S'), 'xxx', 123]
    for card in bad_cards:
        try:
            c.goes_above(card)
        except AssertionError:
            return  # OK
        assert False, 'should never reach this point'

def test_init_deck():
    for i in range(100):
        d = C.Deck()
        c = d.cards
        assert len(c) == 52
        for card in c:
            assert type(card) is C.Card
        s = set(c)  # the __hash__ method comes in handy here!
        assert len(s) == 52
        m = list(map(str, c))
        s2 = set(m)
        assert len(s2) == 52

def test_next():
    for i in range(100):
        d = C.Deck()
        lst = []
        for card in d:
            assert type(card) is C.Card
            lst.append(str(card))
        assert len(lst) == 52
        assert len(set(lst)) == 52

#
# Entry point.
#

def main():
    print('--> TEST_INIT_CARD')
    wrapper(test_init_card)

    print('--> TEST_GOES_ABOVE')
    wrapper(test_goes_above)

    print('--> TEST_GOES_BELOW')
    wrapper(test_goes_below)

    print('--> TEST_INIT_DECK')
    wrapper(test_init_deck)

    print('--> TEST_NEXT')
    wrapper(test_next)

main()


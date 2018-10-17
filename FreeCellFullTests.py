#
# CS 1 Final exam, 2017
#

'''
Test script for FreeCellFull.py.
'''

import sys, traceback

import Card as C
import FreeCell as F
import FreeCellFull as FF
import FreeCellUtils as U
from copy import deepcopy

all_ranks = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
all_suits = ['S', 'H', 'D', 'C']

def check_valid(game):
    try:
        U.validate(game)
    except U.InvalidGame as e:
        assert False, str(e)

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

def test_longest_movable_sequence():
    cascade = [C.Card(9, 'S'), C.Card(8, 'D'), C.Card(7, 'C'), C.Card(6, 'D')]
    assert FF.longest_movable_sequence(cascade) == 4
    cascade = [C.Card(9, 'S'), C.Card(8, 'D'), C.Card(7, 'C'), C.Card(6, 'S')]
    assert FF.longest_movable_sequence(cascade) == 1
    cascade = [C.Card(9, 'S'), C.Card(8, 'D'), C.Card(6, 'C'), C.Card(6, 'H')]
    assert FF.longest_movable_sequence(cascade) == 1
    cascade = [C.Card(9, 'S'), C.Card(8, 'D'), C.Card(5, 'C'), C.Card(6, 'H')]
    assert FF.longest_movable_sequence(cascade) == 1
    cascade = [C.Card(9, 'S'), C.Card(8, 'D'), C.Card('A', 'C'), C.Card(6, 'H')]
    assert FF.longest_movable_sequence(cascade) == 1
    cascade = [C.Card(9, 'S'), C.Card(8, 'C'), C.Card(7, 'C'), C.Card(6, 'H')]
    assert FF.longest_movable_sequence(cascade) == 2
    assert FF.longest_movable_sequence([C.Card('A', 'S')]) == 1
    assert FF.longest_movable_sequence([]) == 0

    # Check for bad inputs.
    try:
        cascade = ['9s', '8c', '7c', '6h']
        FF.longest_movable_sequence(cascade)
    except AssertionError:
        pass

    try:
        cascade = 'foobar'
        FF.longest_movable_sequence(cascade)
    except AssertionError:
        pass


def test_ok_to_automove():
    card = C.Card
    ok = FF.ok_to_automove
    for suit in 'SHDC':
        assert ok(card('A', suit), {})
    assert not ok(card(2, 'C'), {})  # missing Ac
    assert ok(card(2, 'C'), {'C': 'A'})
    assert not ok(card(5, 'H'), {'H': 4})  # missing 4s, 4c
    assert not ok(card(5, 'H'), {'S': 5, 'H': 4, 'C': 3}) # missing 4c
    assert ok(card(5, 'H'), {'S': 4, 'H': 4, 'C': 4})
    assert ok(card(5, 'H'), {'S': 5, 'H': 4, 'C': 10})
    assert not ok(card(5, 'H'), {'S': 4, 'C': 4})  # missing 4h
    assert not ok(card(5, 'H'), {'S': 4, 'H': 3, 'C': 4})  # missing 4h


def test_multi_move_cascade_to_cascade():
    f1 = '''
3 2 3 4
10d None None None
6c 8s Jc 4s 9s 7c Kh
Qc Jd 10c 9d 8c 7d 6s
6d 5d Qd Qh 8d Jh 3h

Kd 9h Qs Js 10h 9c
Kc 10s 8h 7s 6h 5c 4d

Ks 5h 7h 5s 4h
'''

    # Move 7 cards.
    f = U.load(FF.FreeCellFull(), f1)
    f.multi_move_cascade_to_cascade(1, 0, 7)
    cc = list(map(str, f.cascade[0]))
    assert cc == ['6c', '8s', 'Jc', '4s', '9s', '7c', \
                  'Kh', 'Qc', 'Jd', '10c', '9d', '8c', '7d', '6s']
    cc = list(map(str, f.cascade[1]))
    assert cc == []
    f.multi_move_cascade_to_cascade(0, 1, 7)
    cc = list(map(str, f.cascade[0]))
    assert cc == ['6c', '8s', 'Jc', '4s', '9s', '7c', 'Kh']
    cc = list(map(str, f.cascade[1]))
    assert cc == ['Qc', 'Jd', '10c', '9d', '8c', '7d', '6s']

    # Try moving cards from an empty cascade.
    try:
        f = U.load(FF.FreeCellFull(), f1)
        f.multi_move_cascade_to_cascade(4, 0, 1)  # nope
    except F.IllegalMove:
        check_valid(f)

    f2 = '''
3 2 3 4
10d None None None
6c 8s Jc 4s 9s 7c Kh
Qc Jd 10c 9d 8c
6d 5d Qd Qh 8d Jh
3h 7d 6s
Kd 9h Qs Js 10h 9c
Kc 10s 8h 7s 6h 5c 4d

Ks 5h 7h 5s 4h
'''

    f = U.load(FF.FreeCellFull(), f2)
    try:
        f.multi_move_cascade_to_cascade(1, 0, 7)  # FAIL: not enough cards
        assert False
    except F.IllegalMove:
        check_valid(f)

    f = U.load(FF.FreeCellFull(), f2)
    f.multi_move_cascade_to_cascade(1, 0, 5)
    cc = list(map(str, f.cascade[0]))
    assert cc == ['6c', '8s', 'Jc', '4s', '9s', '7c', \
                  'Kh', 'Qc', 'Jd', '10c', '9d', '8c']
    cc = list(map(str, f.cascade[1]))
    assert cc == []

    f3 = '''
3 2 3 4
10d None None None
6c 8s Jc 4s 9s 7c Kh
Qc Jd 10c 9d 8c 7d 6s
6d 5d Qd Qh 8d Jh
3h
Kd 9h Qs Js 10h 9c
Kc 10s 8h 7s 6h 5c 4d

Ks 5h 7h 5s 4h
'''

    f = U.load(FF.FreeCellFull(), f3)
    try:
        f.multi_move_cascade_to_cascade(1, 0, 7)
        assert False
    except F.IllegalMove:
        check_valid(f)

    f4 = '''
3 2 3 4
10d None None None
6c 8s Jc 4s 9s 7c Kh
6d Qc Jd 10c 9d 8c
5d Qd Qh 8d Jh
3h 7d 6s
Kd 9h Qs Js 10h 9c
Kc 10s 8h 7s 6h 5c 4d

Ks 5h 7h 5s 4h
'''

    f = U.load(FF.FreeCellFull(), f4)
    f.multi_move_cascade_to_cascade(1, 0, 5)
    cc = list(map(str, f.cascade[0]))
    assert cc == ['6c', '8s', 'Jc', '4s', '9s', '7c', \
                  'Kh', 'Qc', 'Jd', '10c', '9d', '8c']
    cc = list(map(str, f.cascade[1]))
    assert cc == ['6d']

    f5 = '''
3 2 3 4
10d None None None
6c 8s Jc 4s 9s 7c Kh
6d 8c Qc Jd 10c 9d
5d Qd Qh 8d Jh
3h 7d 6s
Kd 9h 9c Js 10h Qs
Kc 8h 7s 6h 5c 4d 10s

Ks 5h 7h 5s 4h
'''

    # Move 4 cards.
    f = U.load(FF.FreeCellFull(), f5)
    f.multi_move_cascade_to_cascade(1, 0, 4)
    cc = list(map(str, f.cascade[0]))
    assert cc == ['6c', '8s', 'Jc', '4s', '9s', '7c', \
                  'Kh', 'Qc', 'Jd', '10c', '9d']
    cc = list(map(str, f.cascade[1]))
    assert cc == ['6d', '8c']

    # Move 3 cards.
    f = U.load(FF.FreeCellFull(), f5)
    f.multi_move_cascade_to_cascade(1, 4, 3)
    cc = list(map(str, f.cascade[4]))
    assert cc == ['Kd', '9h', '9c', 'Js', '10h', 'Qs', 'Jd', '10c', '9d']
    cc = list(map(str, f.cascade[1]))
    assert cc == ['6d', '8c', 'Qc']

    # Move 2 cards.
    f = U.load(FF.FreeCellFull(), f5)
    f.multi_move_cascade_to_cascade(1, 2, 2)
    cc = list(map(str, f.cascade[2]))
    assert cc == ['5d', 'Qd', 'Qh', '8d', 'Jh', '10c', '9d']
    cc = list(map(str, f.cascade[1]))
    assert cc == ['6d', '8c', 'Qc', 'Jd']

    # Move 1 card.
    f = U.load(FF.FreeCellFull(), f5)
    f.multi_move_cascade_to_cascade(1, 5, 1)
    cc = list(map(str, f.cascade[5]))
    assert cc == ['Kc', '8h', '7s', '6h', '5c', '4d', '10s', '9d']
    cc = list(map(str, f.cascade[1]))
    assert cc == ['6d', '8c', 'Qc', 'Jd', '10c']

    # Move 0 cards.
    f = U.load(FF.FreeCellFull(), f5)
    f.multi_move_cascade_to_cascade(1, 5, 0)  # no change!
    cc = list(map(str, f.cascade[5]))
    assert cc == ['Kc', '8h', '7s', '6h', '5c', '4d', '10s']
    cc = list(map(str, f.cascade[1]))
    assert cc == ['6d', '8c', 'Qc', 'Jd', '10c', '9d']

    try:
        f = U.load(FF.FreeCellFull(), f5)
        f.multi_move_cascade_to_cascade(1, 5, -1)  # error!
        assert False
    except F.IllegalMove:
        check_valid(f)

    try:
        f = U.load(FF.FreeCellFull(), f5)
        f.multi_move_cascade_to_cascade(1, 5, 14)  # too many cards!
        assert False
    except F.IllegalMove:
        check_valid(f)

    try:
        f = U.load(FF.FreeCellFull(), f5)
        f.multi_move_cascade_to_cascade(1, 8, 0)  # bad index
        assert False
    except F.IllegalMove:
        check_valid(f)

    try:
        f = U.load(FF.FreeCellFull(), f5)
        f.multi_move_cascade_to_cascade(-1, 5, 0)  # bad index
        assert False
    except F.IllegalMove:
        check_valid(f)

    f6 = '''
3 2 3 4
10d None None None
6c 8s Jc 4s 9s 7c Kh
Qc Jd 10c 9d 8c 7d 6s
6d 5d Qd Qh 8d Jh 3h

Kd 9h Qs Js 10h 9c
Kc 10s 8h 7s 6h 5c 4d

Ks 5h 7h 5s 4h
'''

    try:
        f = U.load(FF.FreeCellFull(), f6)
        f.multi_move_cascade_to_cascade(1, 3, 7)  # not enough spaces!
        assert False
    except F.IllegalMove:
        check_valid(f)

    f = U.load(FF.FreeCellFull(), f6)
    f.multi_move_cascade_to_cascade(1, 3, 5)
    cc = list(map(str, f.cascade[1]))
    assert cc == ['Qc', 'Jd']
    cc = list(map(str, f.cascade[3]))
    assert cc == ['10c', '9d', '8c', '7d', '6s']

    # More error checks.
    f7 = '''
3 2 3 4
10d None None None
6c 8s Jc 4s 9s 7d Kh
Qc Jd 10c 9d 8c 7c 6s
6d 5d Qd Qh 8d Jh 3h

Kd 9h Qs Js 10h 9c
Kc 10s 8h 7s 6h 5c 4d

Ks 5h 7h 5s 4h
'''

    try:
        f = U.load(FF.FreeCellFull(), f7)
        f.multi_move_cascade_to_cascade(1, 3, 5)  # non-sequence
        assert False
    except F.IllegalMove:
        check_valid(f)

def test_automove_to_foundation():
    f1 = '''
None None None None
None None None None
Kc Qc Jc 10c 9c 8c 7c
Ks Qs Js 10s 9s 8s 7s
Kh Qh Jh 10h 9h 8h 7h
Kd Qd Jd 10d 9d 8d 7d
6s 5s 4s 3s 2s As
6d 5d 4d 3d 2d Ad
6h 5h 4h 3h 2h Ah
6c 5c 4c 3c 2c Ac
'''

    f = U.load(FF.FreeCellFull(), f1)
    f.automove_to_foundation(False)
    assert f.foundation == {'S': 'K', 'H': 'K', 'D': 'K', 'C': 'K'}
    assert f.game_is_won()

    f2 = '''
None None None None
Ad 2h 3c 4s
7c Kc Qc Jc 10c 9c 8c
7s Ks Qs Js 10s 9s 8s
7h Kh Qh Jh 10h 9h 8h
7d Kd Qd Jd 10d 9d 8d 
5s 6s 3s 2s As
5d 6d 4d 3d 2d
5h 6h 4h 3h Ah
5c 6c 4c 2c Ac
'''

    f = U.load(FF.FreeCellFull(), f2)
    f.automove_to_foundation(False)
    assert f.foundation == {'S': 4, 'H': 4, 'D': 4, 'C': 4}
    assert f.freecell == [None] * 4
    cc = list(map(str, f.cascade[0]))
    assert cc == ['7c', 'Kc', 'Qc', 'Jc', '10c', '9c', '8c']
    cc = list(map(str, f.cascade[1]))
    assert cc == ['7s', 'Ks', 'Qs', 'Js', '10s', '9s', '8s']
    cc = list(map(str, f.cascade[2]))
    assert cc == ['7h', 'Kh', 'Qh', 'Jh', '10h', '9h', '8h']
    cc = list(map(str, f.cascade[3]))
    assert cc == ['7d', 'Kd', 'Qd', 'Jd', '10d', '9d', '8d']
    cc = list(map(str, f.cascade[4]))
    assert cc == ['5s', '6s']
    cc = list(map(str, f.cascade[5]))
    assert cc == ['5d', '6d']
    cc = list(map(str, f.cascade[6]))
    assert cc == ['5h', '6h']
    cc = list(map(str, f.cascade[7]))
    assert cc == ['5c', '6c']


#
# Entry point.
#

def main():
    print('--> TEST_LONGEST_MOVABLE_SEQUENCE')
    wrapper(test_longest_movable_sequence)

    print('--> TEST_OK_TO_AUTOMOVE')
    wrapper(test_ok_to_automove)

    print('--> TEST_MULTI_MOVE_CASCADE_TO_CASCADE')
    wrapper(test_multi_move_cascade_to_cascade)

    print('--> TEST_AUTOMOVE_TO_FOUNDATION')
    wrapper(test_automove_to_foundation)

main()


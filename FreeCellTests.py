#
# CS 1 Final exam, 2017
#

'''
Test script for FreeCell.py.
'''

import sys, traceback

import Card as C
import FreeCell as F
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

def test_game_is_won():
    f = F.FreeCell()
    assert not f.game_is_won()
    f.foundation['S'] = 'K'
    f.foundation['H'] = 'K'
    f.foundation['D'] = 'K'
    f.foundation['C'] = 'K'
    assert not f.game_is_won()
    f.freecell[0] = None
    f.freecell[1] = None
    f.freecell[2] = None
    f.freecell[3] = None
    assert not f.game_is_won()
    f.cascade[0] = []
    f.cascade[1] = []
    f.cascade[2] = []
    f.cascade[3] = []
    f.cascade[4] = []
    f.cascade[5] = []
    f.cascade[6] = []
    f.cascade[7] = []
    assert f.game_is_won()

def test_move_cascade_to_freecell():
    # String representation of a game.
    # Line 1: foundations
    # Line 2: freecells
    # Line 3: cascade 0
    # ...
    # Line 10: cascade 7

    f1 = '''
None None None None
None None None None
5h Qc 4d 4c 2s 3c 7s
7c Js 3s 10s 5s 5c 5d
6s 4h 8d Ad 9c 2c 8h
Qs 2d 10d 7h Ks 6h 10h
Ah 10c Kd Kc Jh 2h
3d 9h As 8s Qh Qd
9d 3h Jd 8c Ac 9s
6d 4s 6c Kh Jc 7d
'''

    # Create the FreeCell game corresponding to the string.
    f = U.load(F.FreeCell(), f1)

    # Move some cards from cascades to freecells.
    f.move_cascade_to_freecell(0)
    check_valid(f)
    f.move_cascade_to_freecell(3)
    check_valid(f)
    f.move_cascade_to_freecell(7)
    check_valid(f)
    fc = list(map(str, filter(lambda c: c != None, f.freecell)))
    assert len(fc) == 3
    assert '7s' in fc
    assert '10h' in fc
    assert '7d' in fc

    # Move another card.
    f.move_cascade_to_freecell(0)
    check_valid(f)
    fc = list(map(str, filter(lambda c: c != None, f.freecell)))
    assert len(fc) == 4
    assert '3c' in fc

    # Try and fail to move another card.
    try:
        f.move_cascade_to_freecell(4)
        assert False
    except F.IllegalMove:
        check_valid(f)

    # Invalid arguments.
    try:
        f.move_cascade_to_freecell(8)
        assert False
    except F.IllegalMove:
        check_valid(f)

    try:
        f.move_cascade_to_freecell(-1)
        assert False
    except F.IllegalMove:
        check_valid(f)

    try:
        f.move_cascade_to_freecell('foobar')
        assert False
    except F.IllegalMove:
        check_valid(f)

    f2 = '''
None None None None
None None None None
5h Qc 4d 4c 2s 3c 7s 6d
7c Js 3s 10s 5s 5c 5d
6s 4h 8d Ad 9c 2c 8c 7d 6c
Qs 2d 10d 7h Ks 6h 10h
Ah 10c Kd Kc Jh 2h
3d 9h As 8s Qh Qd Jc
9d 3h Jd 8h Ac 9s
4s Kh
'''

    f = U.load(F.FreeCell(), f2)
    f.move_cascade_to_freecell(7)
    check_valid(f)
    f.move_cascade_to_freecell(7)
    check_valid(f)
    fc = list(map(str, filter(lambda c: c != None, f.freecell)))
    assert len(fc) == 2
    assert 'Kh' in fc
    assert '4s' in fc
    assert f.cascade[7] == []

    # Try to move a card from an empty cascade.
    try:
        f.move_cascade_to_freecell(7)
        assert False
    except F.IllegalMove:
        check_valid(f)


def test_move_freecell_to_cascade():
    f1 = '''
None None None None
Jh 4c None None
5d 5s 2d Ac 2h 8h 6s
6c Js As 2c 4d 3s 9s
4h 3h 3c Kc Ah 10h
10d 7d 9h 8s 9d 4s 6h
Ks Qd 7s Qh 10c 2s
7h Ad Kd 5c Kh
Jc 8c 3d Qs 9c 7c
Qc Jd 10s 8d 6d 5h
'''

    # Move a freecell card to a cascade with cards.
    f = U.load(F.FreeCell(), f1)
    f.move_freecell_to_cascade(1, 7)
    check_valid(f)
    cc = list(map(str, f.cascade[7]))
    assert cc == 'Qc Jd 10s 8d 6d 5h 4c'.split()

    f2 = '''
None None A None
Jh 4c None None
5d 5s 2d Ac 2h 8h 6s
6c Js As 2c 4d 3s 9s
Kd 4h 3h 3c Kc Ah 10h
10d 7d 9h 8s 9d 4s 6h 5c
7h Ks Qd 7s Qh 10c 2s

Jc 8c 3d Qs 9c 7c
Qc Jd 10s 8d 6d 5h Kh
'''

    # Move a freecell card to an empty cascade.
    f = U.load(F.FreeCell(), f2)
    f.move_freecell_to_cascade(0, 5)
    check_valid(f)
    cc = list(map(str, f.cascade[5]))
    assert cc == ['Jh']

    # Various error conditions...
    # 1) Card can't be placed on the cascade.
    try:
        f.move_freecell_to_cascade(0, 7)
        assert False
    except F.IllegalMove:
        check_valid(f)

    # 2) No card in freecell 2.
    try:
        f.move_freecell_to_cascade(2, 7)
        assert False
    except F.IllegalMove:
        check_valid(f)

    # 3) Invalid freecell index (6).
    try:
        f.move_freecell_to_cascade(6, 7)
        assert False
    except F.IllegalMove:
        check_valid(f)

    # 4) Invalid freecell index ('foo').
    try:
        f.move_freecell_to_cascade('foo', 7)
        assert False
    except F.IllegalMove:
        check_valid(f)

    # 5) Invalid cascade index (8).
    try:
        f.move_freecell_to_cascade(0, 8)
        assert False
    except F.IllegalMove:
        check_valid(f)

    # 6) Invalid cascade index ('bar').
    try:
        f.move_freecell_to_cascade(0, 'bar')
        assert False
    except F.IllegalMove:
        check_valid(f)

def test_move_cascade_to_cascade():
    f1 = '''
None A A None
8d Qc 6d 5s
Qh 6s 5c 10s 8h 9c 6h
4s 2s 5h 2h 5d 7h 4d
7d Ks Kd 4h 3h Jd 3d
6c 2c Ac 9s Qs 7c 4c

Qd 10h 7s As Js 10d
9h 8s 8c 9d 2d Kh
Kc Jh 10c 3c Jc 3s
'''
    
    f = U.load(F.FreeCell(), f1)

    # No card to move.
    try:
        f.move_cascade_to_cascade(4, 5)
        assert False
    except F.IllegalMove:
        check_valid(f)
    f.move_cascade_to_cascade(3, 4)
    check_valid(f)
    cc = list(map(str, f.cascade[4]))
    assert cc == ['4c']
    f.move_cascade_to_cascade(2, 4)
    check_valid(f)
    cc = list(map(str, f.cascade[4]))
    assert cc == ['4c', '3d']

    # Card being moved doesn't go on second cascade.
    try:
        f.move_cascade_to_cascade(3, 4)
        assert False
    except F.IllegalMove:
        check_valid(f)

    f.move_cascade_to_cascade(0, 3)
    check_valid(f)
    cc = list(map(str, f.cascade[0]))
    assert cc == ['Qh', '6s', '5c', '10s', '8h', '9c']
    cc = list(map(str, f.cascade[3]))
    assert cc == ['6c', '2c', 'Ac', '9s', 'Qs', '7c', '6h']

    # Invalid arguments
    try:
        f.move_cascade_to_cascade(0, 8)
        assert False
    except F.IllegalMove:
        check_valid(f)

    try:
        f.move_cascade_to_cascade(-1, 7)
        assert False
    except F.IllegalMove:
        check_valid(f)

    try:
        f.move_cascade_to_cascade(8, 7)
        assert False
    except F.IllegalMove:
        check_valid(f)

    try:
        f.move_cascade_to_cascade(0, -1)
        assert False
    except F.IllegalMove:
        check_valid(f)

    try:
        f.move_cascade_to_cascade(0, 'foo')
        assert False
    except F.IllegalMove:
        check_valid(f)

    try:
        f.move_cascade_to_cascade('foo', 4)
        assert False
    except F.IllegalMove:
        check_valid(f)

def test_move_cascade_to_foundation():
    f1 = '''
None None None None
None None None None
7c Qd 5d 4s 8d 4d 5s
10c 6d 3s 2h As 10d Qs
Ks Ah 3c 9h Qc 6h 3d
5c 10s 9c 6s 2s 4h 3h
8s 7s Jh Kh 2c 8c
Ad 2d Jc 6c 5h Ac
Kd 7h 8h 9d Jd 7d
10h 9s 4c Qh Js Kc
'''

    f = U.load(F.FreeCell(), f1)
    f.move_cascade_to_foundation(5)
    check_valid(f)
    assert f.foundation == {'C': 'A'}
    cc = list(map(str, f.cascade[5]))
    assert cc == ['Ad', '2d', 'Jc', '6c', '5h']
    f.move_cascade_to_freecell(5)
    f.move_cascade_to_freecell(5)
    f.move_cascade_to_freecell(5)
    cc = list(map(str, f.cascade[5]))
    assert cc == ['Ad', '2d']
    f.move_cascade_to_freecell(5)
    cc = list(map(str, f.cascade[5]))
    assert cc == ['Ad']
    f.move_cascade_to_foundation(5)
    check_valid(f)
    assert f.foundation == {'C': 'A', 'D': 'A'}

    # Various error conditions...
    # 1) No card to move.
    try:
        f.move_cascade_to_foundation(5)
        assert False
    except F.IllegalMove:
        check_valid(f)

    # 2) Card being moved doesn't go on foundation.
    try:
        f.move_cascade_to_foundation(0)
        assert False
    except F.IllegalMove:
        check_valid(f)

    # 3) Invalid arguments.
    try:
        f.move_cascade_to_foundation(-1)
        assert False
    except F.IllegalMove:
        check_valid(f)

    try:
        f.move_cascade_to_foundation(8)
        assert False
    except F.IllegalMove:
        check_valid(f)

    try:
        f.move_cascade_to_foundation('foo')
        assert False
    except F.IllegalMove:
        check_valid(f)


def test_move_freecell_to_foundation():
    f1 = '''
None None A A
5h 6c Jc 2d
7c Qd 5d 4s 8d 4d 5s
10c 6d 3s 2h As 10d Qs
Ks Ah 3c 9h Qc 6h 3d
5c 10s 9c 6s 2s 4h 3h
8s 7s Jh Kh 2c 8c

Kd 7h 8h 9d Jd 7d
10h 9s 4c Qh Js Kc
'''

    f = U.load(F.FreeCell(), f1)
    f.move_freecell_to_foundation(3)
    check_valid(f)
    cc = list(map(str, f.freecell))
    assert cc == ['5h', '6c', 'Jc', 'None']

    # Various error conditions...
    # 1) No card to move.
    try:
        f.move_freecell_to_foundation(3)
        assert False
    except F.IllegalMove:
        check_valid(f)

    # 2) Card being moved doesn't go on foundation.
    try:
        f.move_freecell_to_foundation(0)
        assert False
    except F.IllegalMove:
        check_valid(f)
    
    # 3) Invalid arguments.
    try:
        f.move_freecell_to_foundation(-1)
        assert False
    except F.IllegalMove:
        check_valid(f)

    try:
        f.move_freecell_to_foundation(4)
        assert False
    except F.IllegalMove:
        check_valid(f)

    try:
        f.move_freecell_to_foundation('foo')
        assert False
    except F.IllegalMove:
        check_valid(f)
    

#
# Entry point.
#

def main():
    print('--> TEST_GAME_IS_WON')
    wrapper(test_game_is_won)

    print('--> TEST_MOVE_CASCADE_TO_FREECELL')
    wrapper(test_move_cascade_to_freecell)

    print('--> TEST_MOVE_FREECELL_TO_CASCADE')
    wrapper(test_move_freecell_to_cascade)

    print('--> TEST_MOVE_CASCADE_TO_CASCADE')
    wrapper(test_move_cascade_to_cascade)

    print('--> TEST_MOVE_CASCADE_TO_FOUNDATION')
    wrapper(test_move_cascade_to_foundation)

    print('--> TEST_MOVE_FREECELL_TO_FOUNDATION')
    wrapper(test_move_freecell_to_foundation)

main()


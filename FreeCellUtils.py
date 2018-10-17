#
# CS 1 Final exam, 2017
#

'''
FreeCellUtils.py
    Some utility functions on FreeCell instances.
'''

import Card as C

all_ranks = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
all_suits = ['S', 'H', 'D', 'C']

class InvalidGame(Exception):
    pass

def validate(game):
    '''
    Checks if a FreeCell game object is in a valid state.  All data
    structures must be present and have the right contents.  Every card in the
    deck must be represented somewhere in the foundations, freecells and
    cascades, and there must be no duplicated cards.

    Argument:
      game -- a FreeCell game object

    Return value:
      None.  An InvalidGame exception is raised if there is any problem.
    '''

    # Trivial validations.
    if len(game.cascade) != 8:
        raise InvalidGame(f'wrong number of cascades: {game.cascade}')
    if len(game.freecell) != 4:
        raise InvalidGame(f'wrong number of freecells: {game.freecell}')
    
    # Collect all cards.  Make sure that they include every card in the deck
    # with no duplications.

    cards = []

    for i in range(8):
        cards += game.cascade[i]

    for i in range(4):
        if game.freecell[i]:
            cards.append(game.freecell[i])

    for suit in game.foundation:
        if suit not in all_suits:
            raise InvalidGame(f'invalid suit on foundation: {suit}')
        rank = game.foundation[suit]
        if rank not in all_ranks:
            raise InvalidGame(f'invalid rank on foundation: {rank}')
        rank = game.foundation[suit]
        index = all_ranks.index(rank)
        for i in range(index + 1):
            cards.append(C.Card(all_ranks[i], suit))

    if len(cards) != 52:
        raise \
          InvalidGame('incorrect number of cards in game; should be 52, ' +
            f'was: {len(cards)}')

    # Convert cards to strings. Check that all cards are unique.
    scards = set(map(str, cards))
    if len(scards) != 52:
        raise \
          InvalidGame('incorrect number of unique cards in game; ' +
            'should be 52, ' + f'was: {len(scards)}')

def save(game):
    '''
    Return a string representation of the state of the game.
    '''
    g = game
    s = ''
    for suit in 'SHDC':
        s += g.foundation.get(suit, 'None') + ' '
    s += '\n'
    for i in range(4):
        s += str(g.freecell[i]) + ' '
    s += '\n'
    for i in range(8):
        for j in range(len(g.cascade[i])):
            s += str(g.cascade[i][j]) + ' '
        s += '\n'
    return s

def load(game, s):
    '''
    Overwrite a game's state given the string representation of
    another FreeCell object.  Returns the new game.  The game is
    passed so that this will work with both FreeCell and FreeCellFull
    objects.

    Format of input string:

    xxx xxx xxx xxx   # foundations: S, H, D, C
    yyy yyy yyy yyy   # freecells: 0, 1, 2, 3
    cascade[0]
    cascade[1]
    ...
    cascade[7]

    Example:

None None A 2
6d 5c None None
6c 8s Jc 4s 9s 7c Kh
Qc Jd 10c 9d 8c 7d 6s
Qd As Qh 8d Jh 3h
4c Js Kd 3c Ah 4h
4d 9h Qs 3s 3d 10h
Kc 10s 8h 7s 6h
9c 5h 7h 5s 2h 2s
5d 10d Ks 2d

    This encodes a foundations dictionary {'A': 'D', 2: 'C'},
    a freecell list [Card(6, 'D'), Card(5, 'C'), None, None]
    cascade[0] ==> 6c 8s Jc 4s 9s 7c Kh
    cascade[1] ==> Qc Jd 10c 9d 8c 7d 6s
    etc.

    An empty cascade ==> a blank line

    '''

    def load_card(c):
        '''
        Create a card from its string representation.
        '''
        assert len(c) in [2, 3]
        suit = c[-1].upper()
        rank = c[:-1]
        nranks = map(str, range(2, 11))
        if rank in nranks:
            rank = int(rank)
        return C.Card(rank, suit)
 
    g = game

    # Strip leading and trailing newlines from s.
    lines = s.split('\n')
    while len(lines) > 0 and lines[0] == '':
        lines.pop(0)
    while len(lines) > 0 and lines[-1] == '':
        lines.pop()

    assert len(lines) == 10  # 1 line for foundation, 1 for freecells, 8 for cascades
    foundations = lines[0].split()
    assert len(foundations) == 4
    freecells = lines[1].split()
    assert len(freecells) == 4
    cascades = list(map(lambda s: s.split(), lines[2:]))

    str_ranks = \
      ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    # Load foundations.
    fnd = {}
    for i in range(4):
        suit = 'SHDC'[i]
        rank = foundations[i]
        if rank == 'None':
            continue
        assert rank in str_ranks
        try:
            rank = int(rank)
        except ValueError:
            pass
        fnd[suit] = rank
    game.foundation = fnd

    # Load freecells.
    fc = []
    for i in range(4):
        card = freecells[i]
        if card == 'None':
            fc.append(None)
        else:
            fc.append(load_card(card))
    game.freecell = fc

    # Load cascades.
    cc = []
    for i in range(8):
        cc1 = []
        for card in cascades[i]:
            cc1.append(load_card(card))
        cc.append(cc1)
    game.cascade = cc

    return game

def dump(game):
    '''
    Print the state of the board to the terminal.
    '''

    g = game

    print('---- FOUNDATIONS ----')
    print('Spades:   {}'.format(g.foundation.get('S', '')))
    print('Hearts:   {}'.format(g.foundation.get('H', '')))
    print('Diamonds: {}'.format(g.foundation.get('D', '')))
    print('Clubs:    {}'.format(g.foundation.get('C', '')))
    print('---- FREECELLS ----')
    for i in range(4):
        card = g.freecell[i]
        if card == None:
            card = ''
        print(f'{i+1}: {card}')
    print('---- CASCADES ----')
    for i in range(8):
        print(f'{i + 1}: ', end='')
        cascade = g.cascade[i]
        print(list(map(str, cascade)))

def display(game):
    '''
    Print the state of the board to the terminal in a form
    which is pleasant to read.
    '''

    def freecellsToString(fc):
        if fc == None:
            return '  '
        else:
            return str(fc)

    g   = game
    f   = g.foundation
    cs  = g.cascade
    fs  = [str(f.get(s, '  ')) for s in 'SHDC']
    fcs = list(map(freecellsToString, g.freecell))

    print()
    print('---- FOUNDATIONS ----- ----- FREECELLS ------')
    print('   S    H    D    C       0    1    2    3   ')
    print()
    print(f"  {fs[0]:>2}   {fs[1]:>2}   {fs[2]:>2}   {fs[3]:>2}", end='    ')
    print(f"  {fcs[0]:>2}   {fcs[1]:>2}   {fcs[2]:>2}   {fcs[3]:>2}")
    print()
    print('----------------- CASCADES ------------------')
    print('     0    1    2    3    4    5    6    7')
    print()
    maxlen = max(map(len, cs))
    for i in range(maxlen):
        print('   ', end='')
        for j in range(8):
            if i < len(cs[j]):
                print(f'{str(cs[j][i]):>3}  ', end='')
            else:
                print('     ', end='')
        print()
    print()


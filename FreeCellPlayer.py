#
# CS 1 Final exam, 2017
# Freecell game.
#

import sys

import FreeCell as F
import FreeCellFull as FF
import FreeCellUtils as U
from copy import deepcopy

class FreeCellPlayer:
    '''
    Instances of this class allow the user to play a game of FreeCell
    from the terminal.
    '''

    def __init__(self, game):
        self.game = game
        self.history = []

    def play(self):
        '''Interactively play a game with the user.'''

        def check_cascade(n):
            if n < 0 or n >= 8:
                raise F.IllegalMove('invalid cascade')

        def check_freecell(n):
            if n < 0 or n >= 4:
                raise F.IllegalMove('invalid cascade')
 
        usagestr = '''
  Legal moves that you can enter at the prompt:

    cf n        -- move bottom card of cascade n to foundation
    xf n        -- move freecell card n to foundation
    cx n        -- move bottom card of cascade n to freecells
    xc m n      -- move freecell card m to cascade n
    cc m n      -- move bottom card of cascade m to cascade n
    cc m n p    -- move p bottom cards of cascade m to cascade n  
                   (FreeCellFull only)
    u           -- undo last move
    h           -- print this help message
    q           -- quit
'''

        while True:
            try:
                prev = deepcopy(self.game)
                U.display(self.game)
                if self.game.game_is_won():
                    print('Game over!  You win!\n')
                    return
                move = input('Enter a move: ')
                print()
                cmd = move.strip().split()
                if cmd == []:
                    print('Please enter a move!\n')
                    continue
                elif cmd[0] == 'cf' and len(cmd) == 2:
                    n = int(cmd[1])
                    check_cascade(n)
                    self.game.move_cascade_to_foundation(n)
                elif cmd[0] == 'xf' and len(cmd) == 2:
                    n = int(cmd[1])
                    check_freecell(n)
                    self.game.move_freecell_to_foundation(n)
                elif cmd[0] == 'cx' and len(cmd) == 2:
                    n = int(cmd[1])
                    check_cascade(n)
                    self.game.move_cascade_to_freecell(n)
                elif cmd[0] == 'xc' and len(cmd) == 3:
                    m = int(cmd[1])
                    n = int(cmd[2])
                    check_freecell(m)
                    check_cascade(n)
                    self.game.move_freecell_to_cascade(m, n)
                elif cmd[0] == 'cc' and len(cmd) == 3:
                    m = int(cmd[1])
                    n = int(cmd[2])
                    check_cascade(m)
                    check_cascade(n)
                    self.game.move_cascade_to_cascade(m, n)
                elif isinstance(self.game, FF.FreeCellFull) and \
                        cmd[0] == 'cc' and len(cmd) == 4:
                    m = int(cmd[1])
                    n = int(cmd[2])
                    p = int(cmd[3])
                    check_cascade(m)
                    check_cascade(n)
                    self.game.multi_move_cascade_to_cascade(m, n, p)
                elif cmd[0] == 'u' and len(cmd) == 1:
                    if self.history == []:
                        print('>>> ERROR: No more history to undo.')
                    else:
                        self.game = self.history.pop()
                    continue
                elif cmd[0] == 'h' and len(cmd) == 1:
                    print(usagestr + '\n')
                    continue
                elif cmd[0] == 'q' and len(cmd) == 1:
                    return
                else:
                    raise F.IllegalMove()

                # Automove to foundation if the object supports it.
                if isinstance(self.game, FF.FreeCellFull):
                    self.game.automove_to_foundation()

                self.history.append(prev)
            except F.IllegalMove as e: 
                print('>>> ERROR:', e)
                print('Please enter another move!\n')
            except ValueError as e:  # conversion to int failed
                print('>>> ERROR:', e)
                print('Please enter another move!\n')


if __name__ == '__main__':
    full = True

    # Run this program with an argument of 0 if you want the 
    # bare-bones player.
    if len(sys.argv) == 2 and sys.argv[1] == '0':
        full = False

    if full:
        game = FF.FreeCellFull()
        game.automove_to_foundation()
    else:
        game = F.FreeCell()
    p = FreeCellPlayer(game)
    p.play()


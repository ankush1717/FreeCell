#
# CS 1 Final exam, 2017
#
# Name: Ankush Hommerich-Dutt
# CMS cluster login name: ahommeri


'''
This module has functions and classes that augment the base FreeCell
object to produce a more full-featured FreeCell game.
'''

import random
from Card import *
from FreeCell import *
import FreeCellUtils as U

# Supplied to students:
def max_cards_to_move(nc, nf):
    '''
    Return the maximum number of cards that can be moved as a single sequence
    if the game has 'nc' empty cascades and 'nf' empty freecells.
    If the target cascade is empty then subtract 1 from 'nc'.

    Arguments:
      nc -- number of empty non-target cascades
      nf -- number of empty freecells

    Return value:
      the maximum number of cards that can be moved to the target
    '''

    assert type(nc) is int
    assert 0 <= nc <= 8
    assert type(nf) is int
    assert 0 <= nf <= 4

    return 1 + nf + sum(range(1, nc + 1))

def longest_movable_sequence(cards):
    '''
    Compute the length of the longest sequence of cards at the end of a 
    list of cards that can be moved in a single move.  Cards in the sequence 
    must be in strict descending order and alternate colors.

    Arguments:
      cards -- a list of cards

    Return value:
      the number of cards at the end of the list forming the longest
      sequence
    '''

    assert type(cards) is list
    
    for c in cards:
        assert isinstance(c, Card)
        
    if len(cards) == 0:
        return 0
    
    longest = 1
    for i in reversed(range(1, len(cards))):
        if cards[i].goes_below(cards[i - 1]) == False:
            break
        longest += 1
        
    return longest    
            
def ok_to_automove(card, foundation):
    '''
    Return True if a card can be automoved to a foundation.

    Arguments:
      card       -- a Card object
      foundation -- a foundation dictionary (mapping suits to ranks)

    Return value:
      True if the card can be automoved, else False
    '''

    assert isinstance(card, Card)
    assert type(foundation) is dict

    if card.rank == 'A':
        return True
    if (card.rank == 2) and (card.suit not in foundation):
        return False
    elif card.rank == 2:
        return True
    if card.suit not in foundation:
        return False
    
    foundation_card = Card(foundation[card.suit], card.suit)
    if not card.goes_above(foundation_card):
        return False
    
    if card.color == 'black':
        if 'H' not in foundation or 'D' not in foundation:
            return False
        if (all_ranks.index(foundation['H']) < all_ranks.index(card.rank) - 1)\
           or (all_ranks.index(foundation['D']) < all_ranks.index(card.rank)\
               - 1):
            return False
        
    if card.color == 'red':
        if ('C' not in foundation) or ('S' not in foundation):
            return False
        if (all_ranks.index(foundation['C']) < all_ranks.index(card.rank) - 1)\
           or (all_ranks.index(foundation['S']) < all_ranks.index(card.rank)\
               - 1):
            return False
        
    return True     

class FreeCellFull(FreeCell):
    '''
    FreeCellFull is an enhanced version of FreeCell with extra useful
    features.
    '''

    def multi_move_cascade_to_cascade(self, m, n, p):
        '''
        Move a sequence of 'p' cards from cascade 'm' to cascade 'n'.
        Cascade 'm' must have at least 'p' cards.  The last 'p'
        cards of cascade 'm' must be in descending rank order and
        alternating colors.

        If the move can't be made, raise an IllegalMove exception.

        Arguments:
          m, n -- cascade indices (integers between 0 and 7)
          p    -- an integer >= 0

        Return value: none
        '''

        if (type(m) is not int) or (m not in range(8)):
            raise IllegalMove('Invalid cascade index')
        if (type(n) is not int) or (n not in range(8)):
            raise IllegalMove('Invalid cascade index')      
        
        if p == 0:
            return
        
        if longest_movable_sequence(self.cascade[m]) < p:
            raise IllegalMove('Not enough cards in a sequence to move that '\
                              'many cards')
        
        if self.cascade[n] == []:
            if max_cards_to_move(self.cascade.count([]) - 1, \
                                 self.freecell.count(None)) < p:
                raise IllegalMove('Not enough freecells and empty cascades to '\
                               'make the move')
        else:
            if max_cards_to_move(self.cascade.count([]), \
                                 self.freecell.count(None)) < p:
                raise IllegalMove('Not enough freecells and empty cascades to '\
                                   'make the move') 
            
        if (self.cascade[n] != []): 
            if (self.cascade[m][-p].goes_below(self.cascade[n][-1]) == True)\
               or (self.cascade[n] == []): 
                move = self.cascade[m][-p:]
                self.cascade[n] += move 
                for i in range(p):
                    self.cascade[m].pop()
            else:    
                raise IllegalMove('Sequence can not move to cascade {}'\
                                  .format(n))
        else:
            move = self.cascade[m][-p:]
            self.cascade[n] += move
            for i in range(p):
                self.cascade[m].pop()

    def automove_to_foundation(self, verbose=True):
        '''
        Make as many moves as possible from the cascades/freecells to the
        foundations.

        Argument:
          verbose -- if True, print a message when each card is automoved

        Return value: none
        '''

        while True:
            move = False
            for i in range(8):
                if self.cascade[i] == []:
                    continue
                if ok_to_automove(self.cascade[i][-1], self.foundation):
                    self.foundation[self.cascade[i][-1].suit] = \
                        self.cascade[i][-1].rank
                    self.cascade[i].pop()
                    if verbose == True:
                        print('automove bottom of cascade {} to foundation'\
                              .format(i))
                    move = True
                    
            for i in range(4):
                if self.freecell[i] == None:
                    continue
                if ok_to_automove(self.freecell[i], self.foundation):
                    self.foundation[self.freecell[i].suit] = \
                        self.freecell[i].rank
                    self.freecell[i] = None
                    if verbose == True:
                        print('automove freecell {} to foundation'\
                              .format(i))
                    move = True
                    
            if move == False:
                break
                
                    
                    



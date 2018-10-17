#
# CS 1 Final exam, 2017
#
# Name: Ankush Hommerich-Dutt
# CMS cluster login name: ahommeri


'''
This module has classes that implement a FreeCell game.
'''

import random
from Card import *
import FreeCellUtils as U

class IllegalMove(Exception):
    '''
    Exception class representing illegal moves in a FreeCell game.
    '''
    pass

class FreeCell:
    '''
    A FreeCell game is represented by the following data structures:
      -- the foundation: a dictionary mapping suits to ranks
         e.g. { 'S' : 'A', 'D': 2 }  # other two suits (H, C) empty
      -- the freecells: a list four cards (or None if no card)
      -- the "cascades": a list of eight lists of cards
    '''

    def __init__(self):
        self.foundation = {}   # suit -> number map 
        self.freecell   = [None] * 4
        self.cascade    = [None] * 8

        # Deal cards from a full deck to the cascades.
        i = 0   # current cascade #
        for card in Deck():
            if self.cascade[i] == None:
                self.cascade[i] = []
            self.cascade[i].append(card)
            i = (i + 1) % 8

    def game_is_won(self):
        '''
        Return True if the game is won.
        '''

        for suit in all_suits:
            if suit not in self.foundation:
                return False
            if self.foundation[suit] != 'K':
                return False
            
        for i in range(4):
            if self.freecell[i] != None:
                return False
            
        for i in range(8):
            if self.cascade[i] != []:
                return False
            
        return True    

    #
    # Movement-related functions.
    #

    def move_cascade_to_freecell(self, n):
        '''
        Move the bottom card of cascade 'n' to the freecells.
        Raise an IllegalMove exception if the move can't be made.
        '''

        if None not in self.freecell:
            raise IllegalMove('Freecells are all full')
        if self.cascade[n] == []:
            raise IllegalMove('Cascade is empty')
        if n not in range(8):
            raise IllegalMove('Argument is not a valid cascade')
        
        move = self.cascade[n].pop()
        
        index = 0
        for i in range(4):
            if self.freecell[i] == None:
                index = i
                break
            
        self.freecell[index] = move    

    def move_freecell_to_cascade(self, m, n):
        '''
        Move freecell card 'm' to cascade 'n'.
        Raise an IllegalMove exception if the move can't be made.
        '''

        if (type(m) is not int) or (m not in range(4)):
            raise IllegalMove('Invalid freecell index')
        if (type(n) is not int) or (n not in range(8)):
            raise IllegalMove('Invalid cascade index')
        if self.freecell[m] == None:
            raise IllegalMove('No card on freecell {}'.format(m))
        
        if self.cascade[n] != []:
            if (self.freecell[m].goes_below(self.cascade[n][-1]) == True) or \
               (self.cascade[n] == []):
                self.cascade[n].append(self.freecell[m])
                self.freecell[m] = None            
            else:    
                raise IllegalMove('Card {} can not move to cascade {}'\
                                  .format(str(self.freecell[m]), n))
            
        else:
            self.cascade[n].append(self.freecell[m])
            self.freecell[m] = None

    def move_cascade_to_cascade(self, m, n):
        '''
        Move a single card from one cascade to another.
        Raise an IllegalMove exception if the move can't be made.
        '''

        
        if (type(m) is not int) or (m not in range(8)):
            raise IllegalMove('Invalid 1st cascade index')
        if (type(n) is not int) or (n not in range(8)):
            raise IllegalMove('Invalid 1st cascade index')
        if self.cascade[m] == []:
            raise IllegalMove('Cascade {} is empty'.format(m))
        
        if self.cascade[n] != []:
            if (self.cascade[m][-1].goes_below(self.cascade[n][-1]) == True)\
               or (self.cascade[n] == []):
                self.cascade[n].append(self.cascade[m].pop())               
            else:    
                raise IllegalMove('Card {} can not move to cascade {}'\
                                  .format(str(self.cascade[m][-1]), n))
            
        else:
            self.cascade[n].append(self.cascade[m].pop())   

    def move_cascade_to_foundation(self, n):
        '''
        Move the bottom card of cascade 'n' to the foundation.
        If there is no card, or if the bottom card can't go to the foundation,
        raise an IllegalMove exception.
        '''

        if (type(n) is not int) or (n not in range(8)):
            raise IllegalMove('Invalid cascade index')
        if self.cascade[n] == []:
            raise IllegalMove('Cascade {} is empty'.format(n))
        
        if self.cascade[n][-1].rank != 'A':
            if self.cascade[n][-1].suit not in self.foundation:
                raise IllegalMove('Cant put rank {} in an empty foundation'.\
                                  format(self.cascade[n][-1].rank))
            foundation_card = Card(self.foundation[self.cascade\
                                [n][-1].suit], self.cascade[n][-1].suit)
            if (self.cascade[n][-1].goes_above(foundation_card) == True):
                self.foundation[self.cascade[n][-1].suit] = self.cascade[n][-1]\
                    .rank
                self.cascade[n].pop()
            else:    
                raise IllegalMove('Card {} can not move to foundation'\
                              .format(str(self.cascade[n][-1])))
            
        else:
            self.foundation[self.cascade[n][-1].suit] = 'A'
            self.cascade[n].pop()         

    def move_freecell_to_foundation(self, n):
        '''
        Move the card at index 'n' of the freecells to the foundation.
        If there is no card there, or if the card can't go to the foundation,
        raise an IllegalMove exception.
        '''

        if (type(n) is not int) or (n not in range(4)):
            raise IllegalMove('Invalid freecell index')
        if self.freecell[n] == None:
            raise IllegalMove('Freecell {} is empty'.format(n))
        
        if self.freecell[n].rank != 'A':
            if self.freecell[n].suit not in self.foundation:
                raise IllegalMove('Cant put rank {} in an empty foundation'.\
                                  format(self.freecell[n].rank))
            foundation_card = Card(self.foundation[self.freecell\
                                [n].suit], self.freecell[n].suit)
            if (self.freecell[n].goes_above(foundation_card) == True):
                self.foundation[self.freecell[n].suit] = self.freecell[n]\
                    .rank
                self.freecell[n] = None
            else:    
                raise IllegalMove('Card {} can not move to foundation'\
                              .format(str(self.freecell[n])))
            
        else:
            self.foundation[self.freecell[n].suit] = 'A'
            self.freecell[n] = None               


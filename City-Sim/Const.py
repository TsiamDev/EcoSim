# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 21:21:26 2022

@author: TsiamDev
"""

class CONST(object):
    def __init__(self):
        self.types = {}
        self.types['FIELD'] = 1
        self.types['BARN_SILO'] = 2
        
class FIELD(object):
    def __init__(self):
        self.types = {}
        self.types['BARREN'] = 1
        self.types['CULTIVATED'] = 2
        self.types['PLANTED'] = 3
        
class TRACTOR_ACTIONS(object):
    def __init__(self):
        self.types = {}
        self.types['IDLE'] = 1
        self.types['CULTIVATE'] = 2
        self.types['SOW'] = 3
        self.types['FERTILIZE'] = 4
    

# instantiate Constants
CONST = CONST()
#print(len(CONST.types))

FIELD = FIELD()

TRACTOR_ACTIONS = TRACTOR_ACTIONS()

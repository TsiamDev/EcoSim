# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 21:21:26 2022

@author: TsiamDev
"""

class DISPLAY(object):
    def __init__(self):
        self.X = 750
        self.Y = 750

class CONST(object):
    def __init__(self):
        self.types = {}
        self.types['FIELD'] = 1
        self.types['BARN_SILO'] = 2
        self.types['PASTURE'] = 3
        
class FIELD(object):
    def __init__(self):
        self.types = {}
        self.types['BARREN'] = 1
        self.types['CULTIVATED'] = 2
        self.types['PLANTED'] = 3

class ANIMAL(object):
    def __init__(self):
        self.types = {}
        self.types['COW'] = 1
        
class ANIMAL_SIZE(object):
    def __init__(self):
        self.types = {}
        self.types['COW'] = 15

class TRACTOR_ACTIONS(object):
    def __init__(self):
        self.types = {}
        self.types['IDLE'] = 1
        self.types['CULTIVATE'] = 2
        self.types['SOW'] = 3
        self.types['FERTILIZE'] = 4
        
class OVERLAY(object):
    def __init__(self):
        self.types = {}
        self.types['PH'] = 1
    

# instantiate Constants
CONST = CONST()
#print(len(CONST.types))

FIELD = FIELD()

TRACTOR_ACTIONS = TRACTOR_ACTIONS()

ANIMAL = ANIMAL()
ANIMAL_SIZE = ANIMAL_SIZE()

DISPLAY = DISPLAY()
OVERLAY = OVERLAY()

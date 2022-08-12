# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 21:21:26 2022

@author: TsiamDev
"""

class DISPLAY(object):
    def __init__(self):
        self.X = 750
        self.Y = 750
        self.field_w = 300
        self.field_h = 300

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
        self.types['HARVEST'] = 5
        self.types['WATER'] = 6
        
class OVERLAY(object):
    def __init__(self):
        self.types = {}
        self.types['PH'] = 1
        self.types['HUM'] = 2
        self.types['TEMP'] = 3
        self.types['N'] = 4
        self.types['P'] = 5
        self.types['K'] = 6
        self.types['CROP_GROWTH'] = 7
        
class TIME(object):
    def __init__(self):
        self.types = {}
        self.types['CROP'] = 100
        
class WEATHER(object):
    def __init__(self):
        self.types = {}
        self.types['SNOW'] = 1
        self.types['RAIN'] = 2
    

# instantiate Constants
CONST = CONST()
#print(len(CONST.types))

FIELD = FIELD()

TRACTOR_ACTIONS = TRACTOR_ACTIONS()

ANIMAL = ANIMAL()
ANIMAL_SIZE = ANIMAL_SIZE()

DISPLAY = DISPLAY()
OVERLAY = OVERLAY()

TIME = TIME()

WEATHER = WEATHER()

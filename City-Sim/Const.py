# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 21:21:26 2022

@author: TsiamDev
"""

class DISPLAY(object):
    def __init__(self):
        self.X = 750
        self.Y = 750
        self.FIELD_W = 300
        self.FIELD_H = 300
        self.ROAD_WIDTH = 15
        self.RIVER_H = 30
        self.RIVER_W = 2 * 300 + 6 * self.ROAD_WIDTH
        self.N = 300
        self.ZONE_W = self.N
        self.ZONE_H = self.N
        self.CITY_W = 20
        self.CITY_H = 20
        self.SCOUT_W = 50
        self.SCOUT_H = 50

class CONSTANTS(object):
    def __init__(self):
        self.types = {}
        #CITY_NUM should be divisible by 3
        self.types['CITY_NUM'] = 9
        self.types['LAKES_NUM'] = 5
        self.types['FORESTS_NUM'] = 5
        

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
        
class CONSTRUCT_SIZE(object):
    def __init__(self):
        self.types = {}
        self.types['SHELTER'] = 15

class TRACTOR_ACTIONS(object):
    def __init__(self):
        self.types = {}
        self.types['IDLE'] = 1
        self.types['CULTIVATE'] = 2
        self.types['SOW'] = 3
        self.types['FERTILIZE'] = 4
        self.types['HARVEST'] = 5
        self.types['WATER'] = 6

class TRACTOR_PARAMETERS(object):
    def __init__(self):
        self.W = 15
        self.H = 15

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
        self.types['PLANT_FACE'] = 8
        
class VIEW(object):
    def __init__(self):
        self.types ={}        
        self.types['CITY_VIEW'] = 8
        self.types['MAP_VIEW'] = 9
        
class TIME(object):
    def __init__(self):
        self.types = {}
        self.types['CROP'] = 50
        self.types['ANIMAL_ACT'] = 70
        
class WEATHER(object):
    def __init__(self):
        self.types = {}
        self.types['SNOW'] = 1
        self.types['RAIN'] = 2
        
class CONSUMPTION_POLICY(object):
    def __init__(self):
        self.types = {}
        self.types['DOMESTIC_CONS'] = 0
        self.types['EXPORT'] = 1

class GOODS(object):
    def __init__(self):
        self.types = {}
        self.types['GRAIN'] = 0
        self.types['WOOD'] = 1
        self.types['WATER'] = 2
    
# defines consumption per 100 people
class CONSUMPTION(object):
    def __init__(self):
        self.types = {}
        self.types['GRAIN_CONS'] = 10
        self.types['WOOD_CONS'] = 5
        self.types['WATER_CONS'] = 7
        
class TRAILERS(object):
    def __init__(self):
        self.TRAILER_S = 500
        self.TRAILER_M = 1500
        self.TRAILER_L = 2500
    
# instantiate Constants
CONST = CONST()
#print(len(CONST.types))

FIELD = FIELD()

TRACTOR_ACTIONS = TRACTOR_ACTIONS()
TRACTOR_PARAMETERS = TRACTOR_PARAMETERS()

ANIMAL = ANIMAL()
ANIMAL_SIZE = ANIMAL_SIZE()

DISPLAY = DISPLAY()
OVERLAY = OVERLAY()
VIEW = VIEW()

TIME = TIME()

WEATHER = WEATHER()

CONSUMPTION_POLICY = CONSUMPTION_POLICY()
GOODS = GOODS()
CONSUMPTION = CONSUMPTION()

CONSTANTS = CONSTANTS()

CONSTRUCT_SIZE = CONSTRUCT_SIZE()

TRAILERS = TRAILERS()

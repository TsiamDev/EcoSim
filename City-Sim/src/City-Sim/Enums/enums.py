# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 11:46:44 2022

@author: HomeTheater
"""

from enum import IntEnum

class Goods(IntEnum):
    GRAIN = 0,
    WOOD = 1,
    WATER = 2,

# defines consumption per 100 people
class Consumption(IntEnum):
    GRAIN_CONS = 10,
    WOOD_CONS = 5,
    WATER_CONS = 7,
    
class Consumption_Policy(IntEnum):
    DOMESTIC_CONS = 0,
    EXPORT = 1,

class Global_Market_Prices(IntEnum):
    GRAIN_PRICE = 10,
    WOOD_PRICE = 10,
    WATER_PRICE = 10
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 07:09:19 2022

@author: TsiamDev
"""

from Const import GOODS

#import random

class Plant:
    def __init__(self):
        print("New Plant")
        self.heat_rng = (0, 255)
        self.hum_rng = (0, 255)
        self.PH_rng = (0, 255)
        self.color = (0, 255)
        self.c = (255, 255, 255)
        
        self.type = 'GRAIN'#random.randint(0, len(GOODS.types.items()))
        
    def calc_color(self):
        if (self.heat_rng is not None) and (self.hum_rng is not None) and (self.PH_rng is not None):
            low = 0.33 * self.heat_rng[0] + 0.33 * self.hum_rng[0] + 0.34 * self.PH_rng[0]
            high = 0.33 * self.heat_rng[1] + 0.33 * self.hum_rng[1] + 0.34 * self.PH_rng[1]
        
            self.color = (int(low), int(high))
        
    def __repr__(self):
        return "Plant: heat range-" + str(self.heat_rng) + " hum range-" + \
                str(self.hum_rng) + " PH range-" + str(self.PH_rng)
    """
    def __init__(self, _PH_low, _PH_high, _hum_low, _hum_high, _heat_low, _heat_high):
        self.PH_low = _PH_low
        self.PH_high = _PH_high
        
        self.hum_low = _hum_low
        self.hum_high = _hum_high
        
        self.heat_low = _heat_low
        self.heat_high = _heat_high
    """
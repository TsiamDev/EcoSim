# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 03:15:28 2022

@author: TsiamDev
"""
import numpy as np
import random

from Const import FIELD, DISPLAY

class Field:
    def __init__(self, rect):
        self.state = FIELD.types['BARREN']
        self.has_init = False
        
        #soil stuff
        zone_w = 300
        zone_h = 300
        #zone_w = rect.topright[0] - rect.topleft[0]
        #zone_h = rect.bottomright[1] - rect.topright[1]
        
        #self.PH = np.zeros( (DISPLAY.X, DISPLAY.Y, 3), dtype=np.uint8 )
        self.PH = np.zeros( (zone_w, zone_h, 3), dtype=np.uint8 )
        #get gradient of red/green
        r = [[random.randint(0, 255) for i in range(zone_w)] for j in range(zone_h)]
        g = [[random.randint(0, 255) for i in range(zone_w)] for j in range(zone_h)]
        self.PH[:, :, 0] = r
        self.PH[:, :, 1] = g
        #zero blue
        self.PH[:, :, 2] = np.zeros((zone_w, zone_h))
        #self.PH[:, : , 1] = np.zeros((zone_w, zone_h))
        
        self.temp = np.zeros( (DISPLAY.X, DISPLAY.Y), dtype=np.uint8 )
        self.hum = np.zeros( (DISPLAY.X, DISPLAY.Y), dtype=np.uint8 )
        self.N = np.zeros( (DISPLAY.X, DISPLAY.Y), dtype=np.uint8 )
        self.P = np.zeros( (DISPLAY.X, DISPLAY.Y), dtype=np.uint8 )
        self.K = np.zeros( (DISPLAY.X, DISPLAY.Y), dtype=np.uint8 )
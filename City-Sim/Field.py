# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 03:15:28 2022

@author: TsiamDev
"""
import numpy as np
import random

from Const import FIELD, DISPLAY

class Field:
    def __init__(self, rect, isPasture=None):
        self.state = FIELD.types['BARREN']
        self.has_init = False
        
        #soil stuff
        empty = np.zeros((DISPLAY.field_w, DISPLAY.field_h))
        
        #self.PH = np.random.uniform( 0, 255, size=(DISPLAY.field_w, DISPLAY.field_h, 3))
        self.PH = np.random.uniform( 0, 14, size=(DISPLAY.field_w, DISPLAY.field_h, 3))
        #get gradient of red/green
        #g = [[random.uniform(0, 255) for i in range(w)] for j in range(w)]

        self.PH[:, :, 0] = 0
        #self.PH[:, : ,1] = self.translate(self.PH[:,:,1], 0, 255, 0, 14)
        self.PH[:, :, 2] = 0

        activation_function = np.zeros( (DISPLAY.field_w, DISPLAY.field_h, 3))
        activation_function[:, :, 1] = np.exp(-abs(self.PH[:, :, 1]*0.5 - 3.5))
        #print(activation_function)

        #PH[:, : ,1] = interp(activation_function[:, :, 1], [-7, 7], [0, 255])
        self.PH[:, : ,1] = self.translate(activation_function[:, :, 1], 0, 1, 0, 255)
        
        """
        #self.PH = np.zeros( (DISPLAY.X, DISPLAY.Y, 3), dtype=np.uint8 )
        self.PH = np.zeros( (DISPLAY.field_w, DISPLAY.field_h, 3), dtype=np.uint8 )
        #get gradient of red/green
        r = [[random.randint(0, 255) for i in range(DISPLAY.field_w)] for j in range(DISPLAY.field_h)]
        g = [[random.randint(0, 255) for i in range(DISPLAY.field_w)] for j in range(DISPLAY.field_h)]
        
        self.PH[:, :, 0] = empty#r
        self.PH[:, :, 1] = g
        self.PH[:, :, 2] = empty
        """
        
        self.temp = np.zeros( (DISPLAY.field_w, DISPLAY.field_h, 3), dtype=np.uint8 )
        r = [[random.randint(0, 255) for i in range(DISPLAY.field_w)] for j in range(DISPLAY.field_h)]
        g = [[random.randint(0, 150) for i in range(DISPLAY.field_w)] for j in range(DISPLAY.field_h)]
        b = [[random.randint(0, 255) for i in range(DISPLAY.field_w)] for j in range(DISPLAY.field_h)]
        self.temp[:, :, 0] = r
        self.temp[:, :, 1] = g
        self.temp[:, :, 2] = b
        
        self.hum = np.zeros( (DISPLAY.field_w, DISPLAY.field_h, 3), dtype=np.int32 )
        #r = [[random.randint(0, 255) for i in range(DISPLAY.field_w)] for j in range(DISPLAY.field_h)]
        #g = [[random.randint(0, 255) for i in range(DISPLAY.field_w)] for j in range(DISPLAY.field_h)]
        b = [[random.randint(0, 255) for i in range(DISPLAY.field_w)] for j in range(DISPLAY.field_h)]
        self.hum[:, :, 0] = empty
        self.hum[:, :, 1] = empty
        self.hum[:, :, 2] = b
        
        self.N = np.zeros( (DISPLAY.field_w, DISPLAY.field_h, 3), dtype=np.uint8 )
        r = [[random.randint(0, 255) for i in range(DISPLAY.field_w)] for j in range(DISPLAY.field_h)]
        g = [[random.randint(0, 255) for i in range(DISPLAY.field_w)] for j in range(DISPLAY.field_h)]
        #self.N[:, :, 0] = r
        self.N[:, :, 0] = empty
        self.N[:, :, 1] = g
        self.N[:, :, 2] = empty
        
        self.P = np.zeros( (DISPLAY.field_w, DISPLAY.field_h, 3), dtype=np.uint8 )
        r = [[random.randint(0, 255) for i in range(DISPLAY.field_w)] for j in range(DISPLAY.field_h)]
        g = [[random.randint(0, 255) for i in range(DISPLAY.field_w)] for j in range(DISPLAY.field_h)]
        self.P[:, :, 0] = r
        self.P[:, :, 1] = g
        self.P[:, :, 2] = empty
        
        self.K = np.zeros( (DISPLAY.field_w, DISPLAY.field_h, 3), dtype=np.uint8 )
        r = [[random.randint(0, 255) for i in range(DISPLAY.field_w)] for j in range(DISPLAY.field_h)]
        g = [[random.randint(0, 255) for i in range(DISPLAY.field_w)] for j in range(DISPLAY.field_h)]
        self.K[:, :, 0] = r
        self.K[:, :, 1] = g
        self.K[:, :, 2] = empty
        



        self.crop_growth = np.zeros( (DISPLAY.field_w, DISPLAY.field_h, 3), dtype=np.int32 )
        
        if isPasture is not None:
            self.is_planted = np.ones( (DISPLAY.field_w, DISPLAY.field_h), dtype=np.uint8 )
            
            g = [[random.randint(0, 255) for i in range(DISPLAY.field_w)] for j in range(DISPLAY.field_h)]

            self.crop_growth[:, :, 0] = empty
            self.crop_growth[:, :, 1] = g
        else:
            self.is_planted = np.zeros( (DISPLAY.field_w, DISPLAY.field_h), dtype=np.uint8 )
            r = [[random.randint(70, 83) for i in range(DISPLAY.field_w)] for j in range(DISPLAY.field_h)]
            g = [[random.randint(45, 50) for i in range(DISPLAY.field_w)] for j in range(DISPLAY.field_h)]

            self.crop_growth[:, :, 0] = r
            self.crop_growth[:, :, 1] = g
       
        self.crop_growth[:, :, 2] = empty
        
    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        #valueScaled = float(value - leftMin) / float(leftSpan)
        valueScaled = (value - leftMin) / (leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return (rightMin + (valueScaled * rightSpan))#.astype(int)

# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 21:38:52 2022

@author: TsiamDev
"""

import random

from Const import CONST


from Construct import Construct
from Field import Field
from Pasture import Pasture
from MyRect import MyRect

class Zone:
    # ctors
    def __init__(self):
        self.is_explored = False
        self.ez_idx = None
        self.constructs = []
    
    # _ez_idx: explored zone index
    def __init__(self, _ez_idx, _rect, _type=None):

        self.is_explored = True
        self.ez_idx = _ez_idx
                
        #encompasing rectangle
        self.rect = MyRect(_rect)
        print(self.rect)
        
        if _type is None:
            self.type = CONST.types['PASTURE']#random.randint(1, len(CONST.types))
        else:
            self.type = _type
            
        if self._is(CONST.types['FIELD']):
            # field's state
            self.field = Field(self.rect)
        elif self._is(CONST.types['PASTURE']):
            self.pasture = Pasture(self.rect)
            self.field = Field(self.rect, True)
        elif self._is(CONST.types['BARN_SILO']):
            # constructs list
            #self.constructs = []
            #self.constructs.append(Construct())
            self.construct = Construct()
            self.field = None
            


    def explore(self):
        self.is_explored = True
        #self.constructs.append(Construct())
        #self.construct = Construct()
        #self.type = random.randint(1, len(CONST.types))
        #self.type = CONST.types['PROD_BUILDING']
        
    def _is(self, _type):
        if self.type == _type:
            return True
        else:
            return False
    
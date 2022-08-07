# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 21:38:52 2022

@author: TsiamDev
"""

import random
from Const import CONST
from Construct import Construct

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
        
        # constructs list
        self.constructs = []
        self.constructs.append(Construct())
        
        #encompasing rectangle
        self.rect = _rect
        
        if _type is None:
            self.type = random.randint(1, len(CONST.types))
        else:
            self.type = _type

    def explore(self):
        self.is_explored = True
        self.constructs.append(Construct())
        #self.type = random.randint(1, len(CONST.types))
        self.type = CONST.types['PROD_BUILDING']
        
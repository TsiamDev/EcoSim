# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 03:15:28 2022

@author: TsiamDev
"""

from Const import FIELD

class Field:
    def __init__(self):
        self.state = FIELD.types['BARREN']
        self.has_init = False
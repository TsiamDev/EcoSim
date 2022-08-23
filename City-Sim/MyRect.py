# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 23:01:40 2022

@author: TsiamDev
"""


class MyRect:
    def __init__(self, _rect):#_x, _y, _center, _topleft, _topright, _bottomright):
        self.x = _rect.x
        self.y = _rect.y
        self.center = _rect.center
        self.topleft = _rect.topleft
        self.topright = _rect.topright
        self.bottomright = _rect.bottomright
        
    def move(self, _x, _y):
        self.x = _x
        self.y = _y
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 23:01:40 2022

@author: TsiamDev
"""


class MyRect:
    def __init__(self, *, _rect=None, _x=None, _y=None, _center=None, _topleft=None):#_x, _y, _center, _topleft, _topright, _bottomright):
        if _rect is not None:
            self.x = _rect.x
            self.y = _rect.y
            self.center = _rect.center
            self.topleft = _rect.topleft
            self.topright = _rect.topright
            self.bottomright = _rect.bottomright
            self.bottomleft = _rect.bottomleft
        else:
            self.x = _x
            self.y = _y
            self.center = _center
            self.topleft = _topleft
    
    def move(self, _x, _y):
        self.x = _x
        self.y = _y
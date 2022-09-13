# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 23:01:40 2022

@author: TsiamDev
"""


class MyRect:
    def __init__(self, *, _rect=None, _x=None, _y=None, _center=None, _w=None):#, _topleft=None):#_x, _y, _center, _topleft, _topright, _bottomright):
        if _rect is not None:
            self.x = _rect.x
            self.y = _rect.y
            self.center = _rect.center
            self.topleft = (_rect.x, _rect.y)
            self.topright = ((_rect.center[0] * 2) - _rect.x, _rect.y)
            self.bottomright = ((_rect.center[0] * 2) - _rect.x, (_rect.center[1] * 2) - _rect.y)
            self.bottomleft = (_rect.x , (_rect.center[1] * 2) - _rect.y)
        else:
            self.x = _x
            self.y = _y
            self.center = _center
            self.topleft = (_x, _y)
            self.topright = (_x+(_center[0]*2), _y)
            self.bottomright = (_x+(_center[0]*2), _y+(_center[1]*2))
    
    def move(self, _x, _y):
        self.x = _x
        self.y = _y
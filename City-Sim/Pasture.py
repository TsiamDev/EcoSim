# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 13:44:19 2022

@author: TsiamDev
"""

from Field import Field
from Const import ANIMAL
from Animal import Animal

import random

class Pasture:
    def __init__(self, rect, pygame):
        self.animal_type = ANIMAL.types['COW']
        self.animals_num = random.randint(1, 10)
        self.animals = []
        for i in range(0, self.animals_num):
            #create empty object
            pos = type('', (), {})()
            pos.x = rect.center[0]#random.randint(rect.topleft[0], rect.topright[0])
            pos.y = rect.center[1]#random.randint(rect.topright[1], rect.bottomright[1])
            
            self.animals.append(Animal(pos, self.animal_type, pygame))
        
    def draw_animals(self, pygame, display_surface):
        print("draw animals")
        for i in range (0, self.animals_num):
            self.animals[i].draw(pygame, display_surface)
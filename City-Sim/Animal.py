# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 13:59:44 2022

@author: TsiamDev
"""

import random

from Const import ANIMAL
from Const import ANIMAL_SIZE

class Animal:
    def __init__(self, _pos, _type, pygame):
        self.pos = _pos
        self.type = _type
        self.size = ANIMAL_SIZE.types['COW']
        
        if self.type == ANIMAL.types['COW']:
            self.img = pygame.image.load('cow.png')
            self.img = pygame.transform.scale(self.img, (self.size, self.size))
            
            self.img_rect = self.img.get_rect()    
            self.img_rect = self.img_rect.move(self.pos.x, self.pos.y)    
            print(self.img_rect)
    def draw(self, pygame, display_surface):
        print("draw")
        x_off = random.randint(-1, 1)
        y_off = random.randint(-1, 1)
        print(x_off, y_off)
        
        self.pos.x = self.pos.x + x_off
        self.pos.y = self.pos.y + y_off
        print(self.pos.x, self.pos.y)
        
        self.img_rect = self.img_rect.move((x_off, y_off))
        print(self.img_rect)
        display_surface.blit(self.img, self.img_rect)

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 23:30:34 2022

@author: TsiamDev
"""

import random

from Const import DISPLAY

class Snowflake:
    def __init__(self, pygame):
        self.pos = type('', (), {})()
        self.pos.x = random.randint(-100, DISPLAY.X)
        self.pos.y = random.randint(-100, DISPLAY.Y)
        
        self.img = pygame.image.load('snowflake.svg')
        self.img = pygame.transform.scale(self.img, (10, 10))
        self.rect = self.img.get_rect()
        
class Snow:
    def __init__(self, pygame):
        self.snowflakes = []
        for i in range(0, 100):
            self.snowflakes.append(Snowflake(pygame))
    
    def draw(self, display_surface):
        for i in range(0, len(self.snowflakes)):
            self.snowflakes[i].rect = self.snowflakes[i].rect.move(5, 5)
            display_surface.blit(self.snowflakes[i].img, self.snowflakes[i].rect)
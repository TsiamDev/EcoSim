# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 23:30:34 2022

@author: TsiamDev
"""

import random

from Const import DISPLAY

class Snowflake:
    def __init__(self, pygame):        
        self.img = pygame.image.load('snowflake.svg')
        self.img = pygame.transform.scale(self.img, (10, 10))
        pos = type('', (), {})()
        pos.x = random.randint(-DISPLAY.X, 0)
        pos.y = random.randint(-DISPLAY.Y, 0)
        self.rect = self.img.get_rect().move(pos.x, pos.y)
        
class Snow:
    def __init__(self, pygame):
        self.snowflakes = []
        for i in range(0, 100):
            self.snowflakes.append(Snowflake(pygame))
    
    def draw(self, display_surface):
        for i in range(0, len(self.snowflakes)):
            new_x = random.randint(1, 10)
            new_y = random.randint(1, 10)
            self.snowflakes[i].rect = self.snowflakes[i].rect.move(new_x, new_y)
            if self.snowflakes[i].rect.x > DISPLAY.X:
                self.snowflakes[i].rect.x = random.randint(-DISPLAY.X, 0)
                
            if self.snowflakes[i].rect.y > DISPLAY.Y:
                self.snowflakes[i].rect.y = random.randint(-DISPLAY.Y, 0)
                
            display_surface.blit(self.snowflakes[i].img, self.snowflakes[i].rect)
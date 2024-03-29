# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 23:30:34 2022

@author: TsiamDev
"""

import random

from Const import DISPLAY, WEATHER

class WeatherParticle:
    def __init__(self, pygame, _type):        
        
        pos = type('', (), {})()
        pos.x = random.randint(-DISPLAY.X, 0)
        pos.y = random.randint(-DISPLAY.Y, 0)
        
        if _type == WEATHER.types['SNOW']:
            self.img = pygame.image.load('effects/snowflake.svg')
            self.img = pygame.transform.scale(self.img, (10, 10))
        elif _type == WEATHER.types['RAIN']:
            self.img = pygame.image.load('effects/drop.png')
            self.img = pygame.transform.scale(self.img, (1, 5))
            
        
        self.rect = self.img.get_rect().move(pos.x, pos.y)

class WeatherEffect:
    def __init__(self, pygame, _type):
        self.type = _type
        
        self.particles = []
        for i in range(0, 100):
            self.particles.append(WeatherParticle(pygame, self._type))
            
        
    
    def draw_snow(self, display_surface):
        #while running == True:
        for i in range(0, len(self.particles)):
            new_x = random.randint(1, 10)
            new_y = random.randint(1, 10)
            self.particles[i].rect = self.particles[i].rect.move(new_x, new_y)
            if self.particles[i].rect.x > DISPLAY.X:
                self.particles[i].rect.x = random.randint(-DISPLAY.X, 0)
                
            if self.particles[i].rect.y > DISPLAY.Y:
                self.particles[i].rect.y = random.randint(-DISPLAY.Y, 0)
                
            display_surface.blit(self.particles[i].img, self.particles[i].rect)
            
    def draw_rain(self, display_surface):
        #while running == True:
        for i in range(0, len(self.particles)):
            new_x = random.randint(1, 10)
            new_y = random.randint(1, 10)
            self.particles[i].rect = self.particles[i].rect.move(new_x, new_y)
            if self.particles[i].rect.x > DISPLAY.X:
                self.particles[i].rect.x = random.randint(-DISPLAY.X, 0)
                
            if self.particles[i].rect.y > DISPLAY.Y:
                self.particles[i].rect.y = random.randint(-DISPLAY.Y, 0)
                
            display_surface.blit(self.particles[i].img, self.particles[i].rect)
    
    def draw(self, display_surface):#, running):
        if self._type == WEATHER.types['SNOW']:
            self.draw_snow(display_surface)
        elif self._type == WEATHER.types['RAIN']:
            self.draw_rain(display_surface)
        
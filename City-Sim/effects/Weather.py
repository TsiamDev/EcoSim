# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 23:30:34 2022

@author: TsiamDev
"""

import random

from Const import DISPLAY, WEATHER
from MyRect import MyRect
from MyPoint import MyPoint

class WeatherParticle:
    def __init__(self, _type, _x, _y):        
        
        self.x_speed = random.randint(5, 10)
        self.y_speed = random.randint(5, 10)
        
        if _type == WEATHER.types['SNOW']:
            self.pos = type('', (), {})()
            self.pos.x = random.randint(-DISPLAY.X, 0)
            self.pos.y = random.randint(-DISPLAY.Y, 0)
            
            self.img_key = 'snowflake'
            #self.img = pygame.image.load('effects/snowflake.svg')
            #self.img = pygame.transform.scale(self.img, (10, 10))
        elif _type == WEATHER.types['RAIN']:
            self.pos = type('', (), {})()
            self.pos.x = random.randint(0, DISPLAY.X)
            self.pos.y = random.randint(-DISPLAY.Y, 0)
            
            #self.img = pygame.image.load('effects/drop.png')
            #self.img = pygame.transform.scale(self.img, (1, 5))
            self.img_key = 'drop'
        
        self.img = None
        self.point = MyPoint(_x, _y)#self.img.get_rect().move(pos.x, pos.y)

class WeatherEffect:
    def __init__(self, _type):
        self.type = _type
        
        self.particles = []
        for i in range(0, 100):
            new_x = random.randint(1, 10)
            new_y = random.randint(1, 10)
            self.particles.append(WeatherParticle(self.type, new_x, new_y))
            
        
    
    def draw_snow(self, display_surface):
        #while running == True:
        for i in range(0, len(self.particles)):

            self.particles[i].point.move(self.particles[i].x_speed, self.particles[i].y_speed)
            if self.particles[i].point.x > DISPLAY.X:
                self.particles[i].point.x = random.randint(-DISPLAY.X, 0)
                
            if self.particles[i].point.y > DISPLAY.Y:
                self.particles[i].point.y = random.randint(-DISPLAY.Y, 0)
                
            display_surface.blit(self.particles[i].img, self.particles[i].point)
            
    def draw_rain(self, display_surface, pygame, images):
        #while running == True:
        for i in range(0, len(self.particles)):

            self.particles[i].point.move(0, self.particles[i].y_speed)
            #print(self.particles[i].point)
            if self.particles[i].point.x > DISPLAY.X:
                self.particles[i].point.x = random.randint(-DISPLAY.X, 0)
                
            if self.particles[i].point.y > DISPLAY.Y:
                self.particles[i].point.y = random.randint(-DISPLAY.Y, 0)
                
            rect = pygame.Rect(self.particles[i].point.x, self.particles[i].point.y, 1, 5)
            display_surface.blit(images[self.particles[i].img_key], rect)
    
    def draw(self, display_surface, pygame, images):#, running):
        if self.type == WEATHER.types['SNOW']:
            self.draw_snow(display_surface)
        elif self.type == WEATHER.types['RAIN']:
            self.draw_rain(display_surface, pygame, images)
        
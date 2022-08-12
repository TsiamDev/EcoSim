# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 13:59:44 2022

@author: TsiamDev
"""

import random

from Const import ANIMAL, ANIMAL_SIZE, DISPLAY

class Animal:
    def __init__(self, _pos, _type, pygame):
        self.pos = _pos
        self.type = _type
        self.size = ANIMAL_SIZE.types['COW']
        
        self.stomach = 0
        self.product = 0
        
        if self.type == ANIMAL.types['COW']:
            self.img = pygame.image.load('cow.png')
            self.img = pygame.transform.scale(self.img, (self.size, self.size))
            
            self.img_rect = self.img.get_rect()    
            self.img_rect = self.img_rect.move(self.pos.x, self.pos.y)    
            print(self.img_rect)
    
    def act(self, pygame, display_surface, zone, data):
        self.eat(zone, data)
        self.draw(pygame, display_surface, zone)
        
    
    def draw(self, pygame, display_surface, zone):
        #print("draw animal")      
        if self.pos.x <= zone.rect.topleft[0]:# & (self.pos.x < zone.rect.top_right[0]):
            x_low_bound = 0
        else:
            x_low_bound = -1

        if self.pos.x >= zone.rect.topright[0]:
            x_high_bound = 0
        else:
            x_high_bound = 1

        x_off = random.randint(x_low_bound, x_high_bound)
        
        if self.pos.y <= zone.rect.topleft[1]:# & (self.pos.x < zone.rect.top_right[0]):
            y_low_bound = 0
        else:
            y_low_bound = -1

        if self.pos.y >= zone.rect.bottomleft[1]:
            y_high_bound = 0
        else:
            y_high_bound = 1

        x_off = random.randint(x_low_bound, x_high_bound)
        y_off = random.randint(y_low_bound, y_high_bound)
        
        #print(x_low_bound, x_high_bound, y_low_bound, y_high_bound)
        #print(x_off, y_off)
        #print(self.pos.x, self.pos.y)
        
        self.pos.x = self.pos.x + x_off
        self.pos.y = self.pos.y + y_off
        #print(self.pos.x, self.pos.y)
        
        self.img_rect = self.img_rect.move((x_off, y_off))
        #print(self.img_rect)
        display_surface.blit(self.img, self.img_rect)

    def produce(self, green, red):
        #food = sum((sum(green) + sum(red))) / 2
        food = sum(sum(green))
        self.stomach = self.stomach + food
        
        if self.stomach >= 255:
            self.product = self.product + 255 / 100
            self.stomach = self.stomach - 255
            print("Produced ", 255/100, "L of milk")
            print(self.product)
        
    def eat(self, zone, data):
        field = zone.field
        
        w = len(field.crop_growth[0])
        h = len(field.crop_growth[1])
        
        x_low = self.pos.x - zone.rect.topleft[0]
        x_high = self.pos.x + self.size - zone.rect.topleft[0]
        
        y_low = self.pos.y - zone.rect.topleft[1]
        y_high = self.pos.y + self.size - zone.rect.topleft[1]
        
        if x_low < 0:
            x_low = 0
            
        if y_low < 0:
            y_low = 0
            
        if x_high > w:
            x_high = w
            
        if y_high > h:
            y_high = h  
        #print((x_low, x_high), '-', (y_low, y_high))
        
        #print(x_low, x_high, y_low, y_high)
        #print(field.crop_growth)
        green = field.crop_growth[x_low:x_high, y_low:y_high, 1]
        red = field.crop_growth[x_low:x_high, y_low:y_high, 0]

        #print(any(green[green > 50]))
        #print(red)
        if any(green[green > 50]):
            self.produce(green, red)
        
            
        #if green.any() > 0:
        if any(green[green > 50]):
            #print("eating...")
            r = [[random.randint(70, 83) for i in range(y_low, y_high)] for j in range(x_low, x_high)]
            g = [[random.randint(45, 50) for i in range(y_low, y_high)] for j in range(x_low, x_high)]
            field.is_planted[x_low:x_high, y_low:y_high] = 0
            field.crop_growth[x_low:x_high, y_low:y_high, 0] = r
            field.crop_growth[x_low:x_high, y_low:y_high, 1] = g
            field.crop_growth[x_low:x_high, y_low:y_high, 2] = 0
            #field.crop_growth[field.crop_growth[x_low:x_high, y_low:y_high, :] < 0] = 0
            
            r = [[random.randint(70, 83) for i in range(self.pos.y, self.pos.y+self.size)] for j in range(self.pos.x, self.pos.x+self.size)]
            g = [[random.randint(45, 50) for i in range(self.pos.y, self.pos.y+self.size)] for j in range(self.pos.x, self.pos.x+self.size)]
            data[self.pos.x:self.pos.x+self.size, self.pos.y:self.pos.y+self.size, 0] = r
            data[self.pos.x:self.pos.x+self.size, self.pos.y:self.pos.y+self.size, 1] = g
            data[self.pos.x:self.pos.x+self.size, self.pos.y:self.pos.y+self.size, 2] = 0
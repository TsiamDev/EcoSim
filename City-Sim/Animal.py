# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 13:59:44 2022

@author: TsiamDev
"""

import random
import numpy as np
#import pprint

from perlin_noise import PerlinNoise

from Const import ANIMAL, ANIMAL_SIZE, DISPLAY, GOODS
from MyRect import MyRect


class Animal:
    def __init__(self, _rect, _type):
        self.x = _rect.center[0]
        self.y = _rect.center[1]
        self.rect = MyRect(_x=self.x, _y=self.y)
        self.type = _type
        self.size = ANIMAL_SIZE.types['COW']
        
        self.stomach = 0
        self.product = 0
        
        if self.type == ANIMAL.types['COW']:
            self.img_key = 'cow_scaled_img'
            
            self.img = None
            self.img_rect =  self.rect#MyRect(_rect=_rect)
            #self.img_rect = self.img.get_rect()    
            #self.img_rect = self.img_rect.move(self.pos.x, self.pos.y)    
            #print(self.img_rect)
    
        self.w = None
        
        self.noise = PerlinNoise(octaves=10, seed=42)
        
    def act(self, zone, data, city):
        if self.w is None:
            self.eat(zone, data, city)
            x_dir, y_dir = self.draw(zone)
        else:
            #just produced - go home
            #print(self.w)
            x_dir, y_dir = self.move(self.w, zone)
        
        #print("x,y: ", x_dir, y_dir)
        #mag = random.randint(1, 5)
        self.img_rect.move(x_dir, y_dir)
        #self.img_rect.move(1,1)
        #print(self.img_rect.x, self.img_rect.y, flush=True)
        #rect = self.img_rect
        #rect = pygame.Rect(rect.x, rect.y, rect.topright[0]-rect.topleft[0], rect.bottomright[1]-rect.topright[1])
        #display_surface.blit(images[self.img_key], rect)   
    
    def draw_animal(self, display_surface, images, pygame):
        rect = self.img_rect
        rect = pygame.Rect((rect.x, rect.y), (ANIMAL_SIZE.types['COW'], ANIMAL_SIZE.types['COW']))#rect.topright[0]-rect.topleft[0], rect.bottomright[1]-rect.topright[1])
        #pygame.Rect()
        display_surface.blit(images[self.img_key], (rect.x, rect.y))  
    
    def draw(self, zone):
        #"""
        #print("draw animal")      
        #zone.rect = pygame.Rect(zone.rect.x, zone.rect.y, DISPLAY.ZONE_W, DISPLAY.ZONE_H)
        if self.x <= zone.rect.topleft[0]:# & (self.pos.x < zone.rect.top_right[0]):
            x_low_bound = 0
        else:
            x_low_bound = -1

        if self.x >= zone.rect.topright[0]:
            x_high_bound = 0
        else:
            x_high_bound = 1

        x_off = random.randint(x_low_bound, x_high_bound)
        
        if self.y <= zone.rect.topleft[1]:# & (self.pos.x < zone.rect.top_right[0]):
            y_low_bound = 0
        else:
            y_low_bound = -1

        if self.y >= zone.rect.bottomleft[1]:
            y_high_bound = 0
        else:
            y_high_bound = 1
        
        x_off = random.randint(x_low_bound, x_high_bound)
        y_off = random.randint(y_low_bound, y_high_bound)
        """
        field = zone.field
        
        w = len(field.crop_growth[0])
        h = len(field.crop_growth[1])
        
        x_low = self.x - zone.rect.topleft[0]
        x_high = self.x + self.size - zone.rect.topleft[0]
        
        y_low = self.y - zone.rect.topleft[1]
        y_high = self.y + self.size - zone.rect.topleft[1]
        
        if x_low < 0:
            x_low = 0
            
        if y_low < 0:
            y_low = 0
            
        if x_high > w:
            x_high = w
            
        if y_high > h:
            y_high = h 
        
        x_off = random.randint(x_low, x_high)
        y_off = random.randint(y_low, y_high)
        """
        #print(x_low_bound, x_high_bound, y_low_bound, y_high_bound)
        #print(x_off, y_off)
        #print(self.pos.x, self.pos.y)
        
        self.x = self.x + x_off
        self.y = self.y + y_off
        #print(self.pos.x, self.pos.y)
        
        #self.img_rect = self.img_rect.move((x_off, y_off))
        #print(self.img_rect)
        #display_surface.blit(self.img, self.img_rect)
        
        return self.x, self.y
        #return x_off, y_off

    def move(self, waypoints, zone):    
        if len(waypoints) > 0:      
            if waypoints[0][1] - self.img_rect.y < 0:
                y_dir = -1
            elif waypoints[0][1] - self.img_rect.y > 0:
                y_dir = 1
            else:
                y_dir = 0
                
            if y_dir == 0:
                if waypoints[0][0] - self.img_rect.x < 0:
                    x_dir = -1
                elif waypoints[0][0] - self.img_rect.x > 0:
                    x_dir = 1
                else:
                    x_dir = 0
            else:
                x_dir = 0
            
            self.x = self.x + x_dir
            self.y = self.y + y_dir
            
            #self.img_rect = self.img_rect.move(x_dir, y_dir)
            #display_surface.blit(self.img, self.img_rect)
            
            if (x_dir == 0) & (y_dir == 0):
                del waypoints[0]
                if len(waypoints) == 0:
                    self.w = None 
                    
            return self.x, self.y

    def produce(self, green, red, zone, city):
        #food = sum((sum(green) + sum(red))) / 2
        food = sum(sum(green)) / 1000
        self.stomach = self.stomach + food
        #print("Stomach: ", self.stomach)                  
            
        if self.stomach >= 255:
            #go to shelter to produce
            #if self.homing_changed == False:
            #    self.homing = True
            #    self.homing_changed = True
            
            self.product = self.product + 255 / 100
            self.stomach = self.stomach - 255
            
            #print("Produced ", 255/100, "L of milk")
            #print(self.product)
            
            #excrete
            #print("Produced ", 150 ,"L of manure")
            excrement = np.random.uniform( -50, -10, size=(self.size, self.size)).astype(int)
            #print(self.x, self.x+self.size, self.y, self.y+self.size)
            x_off = self.x - zone.rect.topleft[0]
            y_off = self.y - zone.rect.topleft[1]
            #print(x_off,y_off)
            if (x_off + self.size) > DISPLAY.FIELD_W:
                x_off = DISPLAY.FIELD_W - self.size
            if (y_off + self.size) > DISPLAY.FIELD_H:
                y_off = DISPLAY.FIELD_H - self.size
            #print(x_off, x_off+self.size, y_off, y_off+self.size)
            zone.field.PH[x_off:x_off+self.size, y_off:y_off+self.size, 1] += excrement
            
            #add waypoints
            if self.w is None:
                self.w = []
                self.w.append(zone.pasture.shelter_rect.center)
                #Randomize the go-to location to break out of 
                #the random walk's local minima's
                _x = random.randint(zone.rect.topleft[0], zone.rect.topright[0] - self.size)
                _y = random.randint(zone.rect.topright[1], zone.rect.bottomright[1] - self.size)

                self.w.append((_x, _y))
                #self.w.append(zone.rect.center)
                
                #TODO: Offload the product when you get to the barn
                
                #find the appropriate container
                ind = None
                for key, val in GOODS.types.items():
                    #print(key, plant.type)
                    if key == 'COW_MILK':
                        #found the indice
                        ind = val
                        #print(city.goods_amounts[ind])
                        
                        #unload the harvested amount into the city silo
                        city.goods_amounts[ind] += self.product
                        self.product = 0
                        #print("Cow was milked", flush=True)
                        
                        #print("City ", city.id ," silo amount for ", key, " is ", city.goods_amounts[ind], flush=True)
                        break

    def eat(self, zone, data, city):
        field = zone.field
        
        w = len(field.crop_growth[0])
        h = len(field.crop_growth[1])
        
        x_low = self.x - zone.rect.topleft[0]
        x_high = self.x + self.size - zone.rect.topleft[0]
        
        y_low = self.y - zone.rect.topleft[1]
        y_high = self.y + self.size - zone.rect.topleft[1]
        
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
            self.produce(green, red, zone, city)
        
            
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
            
            r = [[random.randint(70, 83) for i in range(self.y, self.y+self.size)] for j in range(self.x, self.x+self.size)]
            g = [[random.randint(45, 50) for i in range(self.y, self.y+self.size)] for j in range(self.x, self.x+self.size)]
            data[self.x:self.x+self.size, self.y:self.y+self.size, 0] = r
            data[self.x:self.x+self.size, self.y:self.y+self.size, 1] = g
            data[self.x:self.x+self.size, self.y:self.y+self.size, 2] = 0
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 03:58:15 2022

@author: TsiamDev
"""

import random

from Const import TRACTOR_ACTIONS

class Tractor:
    static_id = 0
    
    def __init__(self, _x, _y, _zone, pygame):
        
        self._id = Tractor.static_id
        Tractor.static_id = Tractor.static_id + 1
        
        self.width = 15
        #tractor = pygame.Rect(x, y, tractor_width, tractor_width)
        self.img = pygame.image.load('tractor.jpg')
        self.img = pygame.transform.scale(self.img, (self.width, self.width))
        
        self.rect = self.img.get_rect()
        
        
        self.x = _x
        self.y = _y
        
        self.zone = _zone
        
        self.move_right = True
        
        self.action = TRACTOR_ACTIONS.types['IDLE']
        
    def move(self, waypoints, display_surface, right_expz, left_expz):
        
        if len(waypoints) > 0:
            if waypoints[0][0] - self.rect.x < 0:
                x_dir = -1
            elif waypoints[0][0] - self.rect.x > 0:
                x_dir = 1
            else:
                x_dir = 0
                
            if x_dir == 0:
                if waypoints[0][1] - self.rect.y < 0:
                    y_dir = -1
                elif waypoints[0][1] - self.rect.y > 0:
                    y_dir = 1
                else:
                    y_dir = 0
            else:
                y_dir = 0
            
            self.rect = self.rect.move(x_dir, y_dir)
            display_surface.blit(self.img, self.rect)
            
            if (x_dir == 0) & (y_dir == 0):
                del waypoints[0]
        
    def act(self, data, waypoints, display_surface, right_expz, left_expz):
        if self.action == TRACTOR_ACTIONS.types['IDLE']:
            #print("tractor idling")
            pl = 1 # remove - placeholder
        elif self.action == TRACTOR_ACTIONS.types['CULTIVATE']:
            #data = self.cultivate(data)
            self.move(waypoints, display_surface, right_expz, left_expz)
        elif self.action == TRACTOR_ACTIONS.types['SOW']:
            data = self.sow(data)
            self.move(waypoints, right_expz, left_expz)
        elif self.action == TRACTOR_ACTIONS.types['FERTILIZE']:
            data = self.fertilize_N(data)
            self.move(waypoints, right_expz, left_expz)
        
        return data

    def fertilize_N(self, zone):
        #update the zone's <N> level
        #data[self.x:self.x+self.width, self.y:self.y+self.width] = (0, 0, 255)
        zone.field.N[self.x:self.x+self.width, self.y:self.y+self.width] = (0, 255, 0)
        
        #return data

    def cultivate(self, data):
        
        # pick random <ground> color
        r = [[random.randint(70, 83) for i in range(self.y, self.y+self.width)] for j in range(self.x, self.x+self.width)]
        g = [[random.randint(45, 50) for i in range(self.y, self.y+self.width)] for j in range(self.x, self.x+self.width)]
        
        """
        w = self.x + self.width
        h = self.y + self.width
        data[self.x:w, self.y:h, 0] = r
        data[self.x:w, self.y:h, 1] = g
        data[self.x:w, self.y:h, 2] = 0
        """
        
        #"""
        #reset ground to soil
        #w = self.x + self.width
        #if w >= len(self.zone.field.crop_growth):
        w = len(self.zone.field.crop_growth[0])
        
        #h = self.y + self.width
        
        #if h >= len(self.zone.field.crop_growth[1]):
        h = len(self.zone.field.crop_growth[1])
        
        #because tractor x,y is different from zone x,y
        # - 15 => road width
        x_off = self.x - 15 
        y_off = self.y - 15
        
        #print((x_off, w), (y_off, h))
        if w - x_off < self.width:
            x_low = w - self.width
        else:
            x_low = x_off
            
        x_high = x_off + self.width
        if x_high > w:
            x_high = w
            
        if h - y_off < self.width:
            y_low = h - self.width
        else:
            y_low = y_off
            
        y_high = y_off + self.width
        if y_high > h:
            y_high = h
        #print((x_low, x_high), '-', (y_low, y_high))
        #update crop state
        self.zone.field.crop_growth[x_low:(x_high), y_low:y_high, 0] = r
        self.zone.field.crop_growth[x_low:(x_high), y_low:y_high, 1] = g
        self.zone.field.crop_growth[x_low:(x_high), y_low:y_high, 2] = 0
        data[x_low:x_high, y_low:y_high, 0] = r
        data[x_low:x_high, y_low:y_high, 1] = g
        data[x_low:x_high, y_low:y_high, 2] = 0
        #"""
        
        return data

    def sow(self, data):
        
        #r = [[random.randint(70, 83) for i in range(y, y+tractor_width)] for j in range(y, y+tractor_width)]
        g = [[random.randint(85, 150) for i in range(self.y, self.y+self.width)] for j in range(self.x, self.x+self.width)]
        #r = random.randint(70, 83)
        #g = random.randint(45, 50)
        #data[x:x+tractor_width, y:y+tractor_width, 0] = r#(r, g, 0)
        
        w = range(self.x, self.x + self.width)
        h = range(self.y, self.y + self.width)
        
        x_high = self.x + self.width
        x_low = self.x
        if x_high - x_low < 15:
            x_low = len(self.zone.field.crop_growth[0]) - 15
        else:
            x_low = self.x
        
        y_high = self.y + self.width
        y_low = self.y
        if y_high - y_low < 15:
            y_low = len(self.zone.field.crop_growth[0]) - 15
        else:
            y_low = self.y
        
        data[x_low:x_high, y_low:y_high, 1] = g
        self.zone.field.crop_growth[x_low:x_high, y_low:y_high, 1] = g
    
        return data
    
    def harvest(self, data):
        r = [[random.randint(70, 83) for i in range(self.y, self.y+self.width)] for j in range(self.x, self.x+self.width)]
        g = [[random.randint(45, 50) for i in range(self.y, self.y+self.width)] for j in range(self.x, self.x+self.width)]

        data[self.x:self.x+self.width, self.y:self.y+self.width, 0] = r
        data[self.x:self.x+self.width, self.y:self.y+self.width, 1] = g
        data[self.x:self.x+self.width, self.y:self.y+self.width, 2] = 0
        
        
        self.zone.field.crop_growth[self.x:self.x+self.width, self.y:self.y+self.width, 0] = r
        self.zone.field.crop_growth[self.x:self.x+self.width, self.y:self.y+self.width, 1] = g
        self.zone.field.crop_growth[self.x:self.x+self.width, self.y:self.y+self.width, 2] = 0
        
        return data

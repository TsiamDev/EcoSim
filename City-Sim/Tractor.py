# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 03:58:15 2022

@author: TsiamDev
"""

import random

from Const import TRACTOR_ACTIONS

class Tractor:
    static_id = 0
    
    def __init__(self, x, y, pygame):
        
        self._id = Tractor.static_id
        Tractor.static_id = Tractor.static_id + 1
        
        self.width = 15
        #tractor = pygame.Rect(x, y, tractor_width, tractor_width)
        self.img = pygame.image.load('tractor.jpg')
        self.img = pygame.transform.scale(self.img, (self.width, self.width))
        
        self.x = x
        self.y = y
        
        self.move_right = False
        
        self.action = TRACTOR_ACTIONS.types['IDLE']
        
    def move(self, waypoints, tr_rect, right_expz, left_expz):
        
        if len(waypoints) > 0:
            #move right
            if self.move_right == True:
                self.x = self.x + 1
            elif self.move_right == False:
                self.x = self.x - 1
            #else:
            #    print("dont move on <x>")
                
            #print(tr_rect)
            if tr_rect.colliderect(right_expz):
                #print("right col")
                #move down
                self.y = self.y + 1
                self.move_right = None
                
                #start moving left once you've reached target y
                if waypoints[0][1] < self.y:
                    self.move_right = False
                    self.x = 300
                    del waypoints[0]
                    
                
            if tr_rect.colliderect(left_expz):
                #move down
                self.y = self.y + 1
                self.move_right = None
                
                #start moving right once you've reached target y
                if waypoints[0][1] < self.y:
                    self.move_right = True
                    self.x = 15
                    del waypoints[0]
                    
    def act(self, data, waypoints, tr_rect, right_expz, left_expz):
        if self.action == TRACTOR_ACTIONS.types['IDLE']:
            #print("tractor idling")
            x = 1 # remove - placeholder
        elif self.action == TRACTOR_ACTIONS.types['CULTIVATE']:
            data = self.cultivate(data)
            self.move(waypoints, tr_rect, right_expz, left_expz)
        elif self.action == TRACTOR_ACTIONS.types['SOW']:
            data = self.sow(data)
            self.move(waypoints, tr_rect, right_expz, left_expz)
        elif self.action == TRACTOR_ACTIONS.types['FERTILIZE']:
            data = self.fertilize(data)
            self.move(waypoints, tr_rect, right_expz, left_expz)
        
        return data

    def fertilize(self, data):
        data[self.x:self.x+self.width, self.y:self.y+self.width] = (0, 0, 255)
        
        return data

    def cultivate(self, data):
        r = [[random.randint(70, 83) for i in range(self.y, self.y+self.width)] for j in range(self.y, self.y+self.width)]
        g = [[random.randint(45, 50) for i in range(self.y, self.y+self.width)] for j in range(self.y, self.y+self.width)]
        #r = random.randint(70, 83)
        #g = random.randint(45, 50)
        data[self.x:self.x+self.width, self.y:self.y+self.width, 0] = r#(r, g, 0)
        data[self.x:self.x+self.width, self.y:self.y+self.width, 1] = g#(r, g, 0)
        data[self.x:self.x+self.width, self.y:self.y+self.width, 2] = 0
        return data

    def sow(self, data):
        
        #r = [[random.randint(70, 83) for i in range(y, y+tractor_width)] for j in range(y, y+tractor_width)]
        g = [[random.randint(85, 150) for i in range(self.y, self.y+self.width)] for j in range(self.y, self.y+self.width)]
        #r = random.randint(70, 83)
        #g = random.randint(45, 50)
        #data[x:x+tractor_width, y:y+tractor_width, 0] = r#(r, g, 0)
        data[self.x:self.x+self.width, self.y:self.y+self.width, 1] = g#(r, g, 0)
        
        return data
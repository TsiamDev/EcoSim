# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 17:35:33 2022

@author: Perhaps
"""

import random
import copy

from Constants import *

class Scout:
    def __init__(self, pos, rect):
        self.pos = copy.deepcopy(pos)
        self.home_pos = copy.deepcopy(pos)
        self.rect = rect
        self.radius = rect.width
        
        self.map_w = int(WINDOW_W / self.radius)
        self.map_h = int(WINDOW_H / self.radius)
        
        self.map = [[0]* self.map_w]*self.map_h
        print(self.map)
        
        for i in range(0, self.map_w):
            cnt = 0
            for j in range(0, self.map_h):
                self.map[i][j] = cnt
                cnt = cnt + 1
            
        print(self.map)
        self.last_search_index = 0
        
        # TODO - resupply at city 
        # use resources as supplies e.g. food/materials
        self.supply = SUPPLY # in steps
        
    def Home(self):
        diff_x = self.home_pos[0] - self.pos[0] 
        diff_y = self.home_pos[1] - self.pos[1] 
        if diff_x != 0:
            
            if diff_x == 0:
                diff_x = 0
            elif diff_x > 0:
                diff_x = 1
            else:
                diff_x = -1
            
            self.pos[0] = self.pos[0] + diff_x
        
        if diff_y != 0: 
            if diff_y == 0:
                diff_y = 0
            elif diff_y > 0:
                diff_y = 1
            else:
                diff_y = -1
           
            self.pos[1] = self.pos[1] + diff_y
        
        if (diff_x == 0) and (diff_y == 0):
            #reached home - resupply
            self.supply = SUPPLY
            print("resupplied")
            
        print("home pos: ", self.home_pos[0] , self.home_pos[1])
        print("self pos: ", self.pos[0] , self.pos[1])
        print("diffs: ", diff_x , diff_y)
        
    def RandomWalk(self):
        self.supply = self.supply - 1
        if self.supply > 0:
            ch_x = random.randint(0, 3) 
            if ch_x == 0:
                ch_x = -1
            elif ch_x == 1:
                ch_x = 0
            else:
                ch_x = 1
                
            ch_y = random.randint(0, 3) 
            if ch_y == 0:
                ch_y = -1
            elif ch_y == 1:
                ch_y = 0
            else:
                ch_y = 1
                
            self.pos[0] = self.pos[0] + ch_x
            self.pos[1] = self.pos[1] + ch_y
            
            print("Moved to ", self.pos)
        else:
            # If supply has been depleted return home
            self.Home()
            
    def Choose_Unexplored_Tile(self):
        # X is the city's tile
        # 0 1 2
        # 3 X 4
        # 5 6 7
        for i in range(0, self.supply):
            
            self.last_search_index = self.last_search_index + 1
            
    def Explore(self):
        tile_pos = Choose_Unexplored_Tile()
        Move_To_Tile(tile_pos)
        
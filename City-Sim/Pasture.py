# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 13:44:19 2022

@author: TsiamDev
"""

from Field import Field
from Const import ANIMAL
from Animal import Animal

import random
from threading import Thread

class Pasture:
    def __init__(self, rect, pygame):
        self.animal_type = ANIMAL.types['COW']
        self.animals_num = random.randint(1, 10)
        self.animals = []
        for i in range(0, self.animals_num):
            #create empty object
            pos = type('', (), {})()
            pos.x = rect.center[0]#random.randint(rect.topleft[0], rect.topright[0])
            pos.y = rect.center[1]#random.randint(rect.topright[1], rect.bottomright[1])
            
            self.animals.append(Animal(pos, self.animal_type, pygame))
        
    def animals_act(self, pygame, display_surface, zone, data):
        th_list = []
        kws = {}
        kws['pygame'] = pygame
        kws['display_surface'] = display_surface
        kws['zone'] = zone
        kws['data'] = data
        for i in range (0, self.animals_num):
            #self.animals[i].act(pygame, display_surface, zone, data)
            
            th_list.append(Thread(target=self.animals[i].act, kwargs=kws))
            th_list[-1].start()
            
        for i in range (0, len(th_list)):
            th_list[i].join()
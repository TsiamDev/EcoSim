# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 13:44:19 2022

@author: TsiamDev
"""

from Field import Field
from Const import ANIMAL
from Animal import Animal
from MyRect import MyRect

import random
from threading import Thread

class Pasture:
    def __init__(self, _rect):
        self.animal_type = ANIMAL.types['COW']
        self.animals_num = random.randint(1, 10)
        self.animals = []
        _rect = MyRect(_rect)
        for i in range(0, self.animals_num):
            #create empty object
            #pos = type('pos', (), {})()
            #pos.x = rect.center[0]#random.randint(rect.topleft[0], rect.topright[0])
            #pos.y = rect.center[1]#random.randint(rect.topright[1], rect.bottomright[1])
            
            self.animals.append(Animal(_rect, self.animal_type))
            
        self.shelter_img = None
        self.shelter_rect = MyRect(_rect)
        self.shelter_img_key = 'shelter_scaled_img'
        #self.rect = MyRect(_rect)
        #self.rect.x = rect.x
        #self.rect.y = rect.y
        #self.shelter_rect = self.shelter_img.get_rect()
        #self.shelter_rect = self.shelter_rect.move(rect.topleft)
        
    def animals_act(self, pygame, display_surface, zone, data, images):
        th_list = []
        kws = {}
        kws['pygame'] = pygame
        kws['display_surface'] = display_surface
        kws['zone'] = zone
        kws['data'] = data
        for i in range (0, self.animals_num):
            self.animals[i].act(pygame, display_surface, zone, data, images)
        """   
            th_list.append(Thread(target=self.animals[i].act, kwargs=kws))
            th_list[-1].start()
            
        for i in range (0, len(th_list)):
            th_list[i].join()
        """
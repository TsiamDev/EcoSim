# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 20:02:40 2022

@author: TsiamDev

"""

import multiprocessing as mp
import time
import psutil
import os
import pygame
from Const import DISPLAY, CONST, CONSTANTS, CONSUMPTION_POLICY
import City, Zone, MyRect, Plant, Animal
import copy, random

def Initialize():
    #Cities
    coords = []
    centers = []
    
    #Lakes
    lakes = []
    forests = []
    for i in range(0, CONSTANTS.types['CITY_NUM']):
        #Cities
        x = random.randint(0, DISPLAY.X)
        y = random.randint(0, DISPLAY.Y)
        coords.append([x, y])
        centers.append([x + DISPLAY.CITY_W/2, y + DISPLAY.CITY_H/2])
    
    for i in range(0, CONSTANTS.types['LAKES_NUM']):
        #Lakes
        x = random.randint(0, DISPLAY.X)
        y = random.randint(0, DISPLAY.Y)
        lakes.append([x, y])
        
    for i in range(0, CONSTANTS.types['FORESTS_NUM']):
        #Forests
        x = random.randint(0, DISPLAY.X)
        y = random.randint(0, DISPLAY.Y)
        forests.append([x, y])
        
    return coords, centers, lakes, forests

def Init_Explored_Zones(data, zone):
    global display_surface, pygame, images
    
    #for zone in zones:
    
    if zone.type == CONST.types['FIELD']:
        if zone.field.has_init == False:
            rect = pygame.Rect(zone.rect.x, zone.rect.y, DISPLAY.ZONE_W, DISPLAY.ZONE_H)
            # update the field
            #r = [[random.randint(0, 255) for i in range(N)] for j in range(N)]
            
            #enable?
            g = [[random.randint(0, 255) for i in range(N)] for j in range(N)]
            
            #b = [[random.randint(0, 255) for i in range(N)] for j in range(N)]

            #data[15:N+15,15:N+15,0] = r
            #data[15:N+15,15:N+15,1] = g
            #data[15:N+15,15:N+15,2] = b
            #print(rect.topleft)
            #print(rect.bottomleft)
            #print(rect.topright)
            #print(rect.bottomright)
            #data[rect.topleft[0]:(rect.topright[0] - rect.topleft[0]), rect.topright[1]:(rect.bottomright[1] - rect.topright[1]), 1] = g
            
            #enable?
            data[rect.topleft[0]:(rect.topright[0]), rect.topright[1]:(rect.bottomright[1]), 1] = g
            #zone.field.crop_growth[rect.topleft[0]:(rect.topright[0]), rect.topright[1]:(rect.bottomright[1]), 1] = g
            
            
            zone.field.has_init = True
        """
        elif zone.type == CONST.types['BARN_SILO']:
            #draw the building
            building_img = pygame.image.load('barn_silo.png')
            building_img = pygame.transform.scale(building_img, (N, N))
            bi_rect = building_img.get_rect()
            bi_rect = bi_rect.move((zone.rect.topleft))
            display_surface.blit(building_img, bi_rect)
        """   
    elif zone.type == CONST.types['PASTURE']:
        if zone.field.has_init == False:
            #plant the field
            #plant a specific plant based on user input
            #r = [[random.randint(plant.PH_rng[0], plant.PH_rng[1]) for i in range(N)] for j in range(N)]
            #g = [[random.randint(plant.heat_rng[0], plant.heat_rng[1]) for i in range(N)] for j in range(N)]
            #b = [[random.randint(plant.hum_rng[0], plant.hum_rng[1]) for i in range(N)] for j in range(N)]
            
            #temporary
            g = [[random.randint(0, 255) for i in range(N)] for j in range(N)]
            
            rect = pygame.Rect(zone.rect.x, zone.rect.y, DISPLAY.ZONE_W, DISPLAY.ZONE_H)
            data[rect.topleft[0]:rect.topright[0], rect.topright[1]:rect.bottomright[1], 0] = 0
            data[rect.topleft[0]:rect.topright[0], rect.topright[1]:rect.bottomright[1], 1] = g
            data[rect.topleft[0]:rect.topright[0], rect.topright[1]:rect.bottomright[1], 2] = 0
            
            zone.field.crop_growth[0:DISPLAY.FIELD_W, 0:DISPLAY.FIELD_H, 0] = 0
            zone.field.crop_growth[0:DISPLAY.FIELD_W, 0:DISPLAY.FIELD_H, 1] = g
            zone.field.crop_growth[0:DISPLAY.FIELD_W, 0:DISPLAY.FIELD_H, 2] = 0
            #rect = pygame.draw.rect(display_surface, black, (15, 15, N+15, N+15))
            #unexplored_zones.append(Zone(0, rect))
            #zones.append(Zone(3, rect, 1))
            zone.field.has_init = True
            
            for i in range(0, zone.pasture.animals_num):
                #create empty object
                #pos = type('pos', (), {})()
                #pos.x = rect.center[0]#random.randint(rect.topleft[0], rect.topright[0])
                #pos.y = rect.center[1]#random.randint(rect.topright[1], rect.bottomright[1])
                
                zone.pasture.animals.append(Animal(zone.pasture._rect, zone.pasture.animal_type))
      

if __name__ == "__main__":
    
    plant = Plant()
    font = pygame.font.SysFont("monospace", 15)
    N = 300
    #print(repr(plant))
    plant.calc_color()
    
    #expansion zones
    #font = pygame.font.SysFont("monospace", 15)
    unexplored_zones = {}
    zones = []    
    exp_z_len = len(unexplored_zones)
    rng = range(0, exp_z_len)
    
    #rect = pygame.draw.rect(display_surface, black, (DISPLAY.ROAD_WIDTH, DISPLAY.ROAD_WIDTH, DISPLAY.N, DISPLAY.N))
    rect = pygame.Rect((DISPLAY.ROAD_WIDTH, DISPLAY.ROAD_WIDTH), (DISPLAY.N, DISPLAY.N))
    #unexplored_zones.append(Zone(0, rect))
    zones.append(Zone(0, rect, CONST.types['FIELD']))
    zones[0].field.has_init = True
    
    
    if len(unexplored_zones) == 0:
        """
        rect0 = pygame.draw.rect(display_surface, gray, (330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, 15, DISPLAY.ZONE_W, DISPLAY.ZONE_H))
        rect1 = pygame.draw.rect(display_surface, gray, (15, 330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, DISPLAY.ZONE_W, DISPLAY.ZONE_H))
        rect2 = pygame.draw.rect(display_surface, gray, (330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, 330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, DISPLAY.ZONE_W, DISPLAY.ZONE_H))
    
        unexplored_zones[0] = Zone(0, rect0, images)
        unexplored_zones[1] = Zone(1, rect1, images)
        unexplored_zones[2] = Zone(2, rect2, images)
        """
        #rect0 = pygame.Rect((330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, 15), (DISPLAY.ZONE_W, DISPLAY.ZONE_H))
        rect0 = pygame.Rect((330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, 15), (DISPLAY.ZONE_W, DISPLAY.ZONE_H))
        rect = MyRect(_rect=rect0)#(rect0.x, rect0.y, rect0.center, rect0.topleft, rect0.topright, rect0.bottomright)

        #unexplored_zones[0] = Zone(0, rect0.center, rect0.topleft, rect0.topright, rect0.bottomright, rect0.x, rect0.y)
        unexplored_zones[1] = Zone(1, copy.deepcopy(rect))
        
        
        #"""
        rect1 = pygame.Rect((15, 330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH), (DISPLAY.ZONE_W, DISPLAY.ZONE_H))
        rect = MyRect(_rect=rect1)
        #unexplored_zones[1] = Zone(1, rect1.center, rect1.topleft, rect1.topright, rect1.bottomright, rect1.x, rect1.y)
        unexplored_zones[2] = Zone(2, copy.deepcopy(rect))
        
        rect2 = pygame.Rect((330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, 330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH), (DISPLAY.ZONE_W, DISPLAY.ZONE_H))
        rect = MyRect(_rect=rect2)
        #unexplored_zones[2] = Zone(2, rect2.center, rect2.topleft, rect2.topright, rect2.bottomright, rect2.x, rect2.y)
        #print(type(images['shelter_scaled_img']))
        unexplored_zones[3] = Zone(3, copy.deepcopy(rect))
        #"""
    for key, uz in unexplored_zones.items():
        zones.append(uz)
        
    #Init Cities:
    coords, centers, lakes, forests = Initialize()
    #print(coords)
    centered_centers = copy.deepcopy(centers)
    
    #smm = SharedMemoryManager()
    #smm.start()
    
    
    
    #manager = mp.Manager()
    #cities = []#manager.list()
    cities = list()#mp.Array('Synchronized', range(3))
    for i in range(0, CONSTANTS.types['CITY_NUM'], 1):
        cities.append(City(i, [1, 5, 5], CONSUMPTION_POLICY.types['EXPORT'], 1000, coords[i], centers[i], copy.deepcopy(unexplored_zones), copy.deepcopy(zones), copy.deepcopy(plant), _has_tractor=True, _has_river=True))
        for z in cities[-1].zones:
            Init_Explored_Zones(cities[-1].data, z)
        """
        cities.append(City(i+1, [5, 1, 5], CONSUMPTION_POLICY.types['EXPORT'], 1000, coords[i+1], centers[i+1], copy.deepcopy(unexplored_zones), copy.deepcopy(zones), copy.deepcopy(plant), _has_tractor=True, _has_river=True))
        for z in cities[-1].zones:
            Init_Explored_Zones(cities[-1].data, z)
        cities.append(City(i+2, [5, 5, 1], CONSUMPTION_POLICY.types['EXPORT'], 1000, coords[i+2], centers[i+2], copy.deepcopy(unexplored_zones), copy.deepcopy(zones), copy.deepcopy(plant), _has_tractor=True, _has_river=True))
        for z in cities[-1].zones:
            Init_Explored_Zones(cities[-1].data, z)
        #"""
    #shm = shared_memory.ShareableList(cities, name=c)
    
    #scouts = []
    #scouts.append(Scout(centered_centers[0], pygame.Rect(coords[0][0] + DISPLAY.CITY_W/2 - DISPLAY.SCOUT_W/2, coords[0][1] + DISPLAY.CITY_H/2 - DISPLAY.SCOUT_H/2, DISPLAY.SCOUT_W, DISPLAY.SCOUT_H)))
    
    #Weather effects
    #weather_effect = WeatherEffect(WEATHER.types['RAIN'])
    
    selected_overlay = None
    
    running = True
    
    with mp.Pool(8) as pool:
        proc = psutil.Process()
        pid = os.getpid()
        while True:
            time.sleep(4)
            print("hello from ", pid, flush=True)
            known_words = pool.map(hash_word, words)
    
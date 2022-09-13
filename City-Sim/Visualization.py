# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 23:27:13 2022

@author: Perhaps
"""

# Importing the library
import pygame
import random

from Enums.enums import *
import copy

from City import City
from Scout import Scout
#from Merchant import Merchant
#from Bank import Bank

from Constants import *

def Draw_Lakes(surface, lakes, img):
    for i in range(0, LAKES_NUM):
        pygame.draw.circle(surface, (0, 0, 0), (lakes[i][0],lakes[i][1]), 10, 0)
        img_rect = img.get_rect().move(lakes[i][0]-13, lakes[i][1]-13)
        surface.blit(img, img_rect)

def Draw_Forests(surface, forests, img):
    for i in range(0, FORESTS_NUM):
        #pygame.draw.circle(surface, FOREST_COLOR, forests[i], 10, 0)
        pygame.draw.circle(surface, (0, 0, 0), (forests[i][0], forests[i][1]), 10, 1)
        img_rect = img.get_rect().move(forests[i][0]-13, forests[i][1]-13)
        surface.blit(img, img_rect)

def Draw_Env(surface, lakes, forests, images):
    Draw_Lakes(surface, lakes, images['lake'])
    Draw_Forests(surface, forests, images['forest'])

def Draw_Cities(surface, cities, img):
    # Draw Cities
    city_rects = []
    for i in range(0, len(cities)):
        rect = pygame.Rect(cities[i].pos[0], cities[i].pos[1], CITY_W, CITY_W)
        city_rects.append( pygame.draw.rect(surface, (0, 0, 0), rect)) 
        img_rect = img.get_rect().move(cities[i].pos[0]-5, cities[i].pos[1]-5)
        surface.blit(img, img_rect)
        
        
    return city_rects

def Draw_Routes(surface, cities):
    # Draw Routes
    for i in range(0, len(cities)-1):
        pygame.draw.line(surface, LINE_COLOR, cities[i].center, cities[i+1].center, 3)
    pygame.draw.line(surface, LINE_COLOR, cities[0].center, cities[len(cities)-1].center, 3)

def Draw_Scouts(surface, scouts):
    # Draw Scouts
    for i in range(0, len(scouts)):
        #pygame.draw.rect(surface, SCOUT_COLOR, scouts[i].rect)
        pygame.draw.circle(surface, SCOUT_COLOR, scouts[i].pos, scouts[i].radius)
    
def Draw(surface, scouts, lakes, forests, cities, images):
    surface.fill((83, 50, 0))
    
    #TODO: Enable
    Draw_Scouts(surface, scouts)
    
    Draw_Env(surface, lakes, forests, images)
    
    city_rects = Draw_Cities(surface, cities, images['city'])
    #TODO: Enable:
    #Draw_Routes(surface, cities)  
    
    return city_rects
    
    #pygame.display.flip()

    
def Simulate(coords, centers, lakes, forests, scouts, cities):
    # Initializing Pygame
    pygame.init()
      
    fpsClock = pygame.time.Clock()
    
    # Initializing surface
    surface = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    
    Draw(surface, scouts, lakes, forests, cities)    
    
    run = True
    while run:
        for s in scouts:
            s.RandomWalk()
        Draw(surface, scouts, lakes, forests, cities)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                run = False
    
        fpsClock.tick(FPS)
    
    pygame.quit()


def Initialize():
    #Cities
    coords = []
    centers = []
    
    #Lakes
    lakes = []
    forests = []
    for i in range(0, CITY_NUM):
        #Cities
        x = random.randint(0, WINDOW_W)
        y = random.randint(0, WINDOW_H)
        coords.append([x, y])
        centers.append([x + CITY_W/2, y + CITY_W/2])
    
    for i in range(0, LAKES_NUM):
        #Lakes
        x = random.randint(0, WINDOW_W)
        y = random.randint(0, WINDOW_H)
        lakes.append([x, y])
        
    for i in range(0, FORESTS_NUM):
        #Forests
        x = random.randint(0, WINDOW_W)
        y = random.randint(0, WINDOW_H)
        forests.append([x, y])
        
    return coords, centers, lakes, forests

if __name__ == "__main__":
    
    coords, centers, lakes, forests = Initialize()
    print(coords)
    centered_centers = copy.deepcopy(centers)
    
    cities = []
    cities.append(City(0, [1, 5, 5], Consumption_Policy.EXPORT, 1000, coords[0], centers[0]))
    cities.append(City(1, [5, 1, 5], Consumption_Policy.EXPORT, 1000, coords[1], centers[1]))
    cities.append(City(2, [5, 5, 1], Consumption_Policy.EXPORT, 1000, coords[2], centers[2]))

    scouts = []
    scouts.append(Scout(centered_centers[0], pygame.Rect(coords[0][0] + CITY_W/2 - SCOUT_W/2, coords[0][1] + CITY_W/2 - SCOUT_W/2, SCOUT_W, SCOUT_W)))
    #cities.append(City(1, [5, 1, 5], Consumption_Policy.EXPORT, 1000))
    #cities.append(City(2, [5, 5, 1], Consumption_Policy.DOMESTIC_CONS, 1000)) 
    
    Simulate(coords, centers, lakes, forests, scouts, cities)
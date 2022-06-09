# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 23:27:13 2022

@author: Perhaps
"""

# Importing the library
import pygame
import random

from Enums.enums import *

from City import City
from Scout import Scout
#from Merchant import Merchant
#from Bank import Bank

WINDOW_W = 600
WINDOW_H = 600

CITY_NUM = 3
CITY_W = 20

SCOUT_W = 5

LAKES_NUM = 4
FORESTS_NUM = 5

# Initialize Colors
CITY_COLOR = (255,0,0)
LINE_COLOR = (0,0,0)
FOREST_COLOR = (0,255,0)
LAKE_COLOR = (0,0,255)

SCOUT_COLOR = (50,50,50)

BACK_COLOR = (255,255,255)

def Draw_Lakes(surface, lakes):
    for i in range(0, LAKES_NUM):
        pygame.draw.circle(surface, LAKE_COLOR, lakes[i], 10, 0)

def Draw_Forests(surface, forests):
    for i in range(0, FORESTS_NUM):
        pygame.draw.circle(surface, FOREST_COLOR, forests[i], 10, 0)

def Draw_Env(surface, lakes, forests):
    Draw_Lakes(surface, lakes)
    Draw_Forests(surface, forests)

def Draw_Cities(surface, coords):
    # Draw Cities
    for i in range(0, CITY_NUM):
        pygame.draw.rect(surface, CITY_COLOR, pygame.Rect(coords[i][0], coords[i][1], CITY_W, CITY_W))

def Draw_Routes(surface, centers):
    # Draw Routes
    for i in range(0, CITY_NUM-1):
        pygame.draw.line(surface, LINE_COLOR, centers[i], centers[i+1])
    pygame.draw.line(surface, LINE_COLOR, centers[0], centers[CITY_NUM-1])

def Draw_Scouts(surface, scouts):
    # Draw Scouts
    for i in range(0, len(scouts)):
        pygame.draw.rect(surface, SCOUT_COLOR, scouts[i].rect)
    
def Simulate(coords, centers, lakes, forests, scouts):
    # Initializing Pygame
    pygame.init()
      
    # Initializing surface
    surface = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    surface.fill(BACK_COLOR)
    
    Draw_Env(surface, lakes, forests)
    
    Draw_Cities(surface, coords)
    Draw_Routes(surface, centers)
    
    Draw_Scouts(surface, scouts)
    
    pygame.display.flip()
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                run = False
    
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
    
    cities = []
    cities.append(City(0, [1, 5, 5], Consumption_Policy.EXPORT, 1000, coords[0], centers[0]))
    scouts = []
    scouts.append(Scout(centers[0], pygame.Rect(coords[0][0] + CITY_W/2 - SCOUT_W/2, coords[0][1] + CITY_W/2 - SCOUT_W/2, SCOUT_W, SCOUT_W)))
    #cities.append(City(1, [5, 1, 5], Consumption_Policy.EXPORT, 1000))
    #cities.append(City(2, [5, 5, 1], Consumption_Policy.DOMESTIC_CONS, 1000)) 
    
    Simulate(coords, centers, lakes, forests, scouts)
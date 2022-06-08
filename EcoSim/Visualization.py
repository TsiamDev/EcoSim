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
#from Merchant import Merchant
#from Bank import Bank

WINDOW_W = 600
WINDOW_H = 600

CITY_NUM = 3
CITY_W = 20

def Simulate(coords):
    # Initializing Pygame
    pygame.init()
      
    # Initializing surface
    surface = pygame.display.set_mode((WINDOW_W, WINDOW_H))
      
    # Initializing Color
    city_color = (255,0,0)
    line_color = (0,255,0)
      
    # Draw Cities
    for i in range(0, CITY_NUM):
        pygame.draw.rect(surface, city_color, pygame.Rect(coords[i][0], coords[i][1], CITY_W, CITY_W))
    
    # Draw Routes
    for i in range(0, CITY_NUM-10):
        pygame.draw.line(surface, line_color, (coords[i][0] + CITY_W/2, coords[i][1] + CITY_W/2), (coords[i+1][0] + CITY_W/2, coords[i+1][1] + CITY_W/2), 2)
    
    pygame.display.flip()
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                run = False
    
    pygame.quit()


if __name__ == "__main__":
    
    
    #cities = []
    #cities.append(City(0, [1, 5, 5], Consumption_Policy.EXPORT, 1000))
    #cities.append(City(1, [5, 1, 5], Consumption_Policy.EXPORT, 1000))
    #cities.append(City(2, [5, 5, 1], Consumption_Policy.DOMESTIC_CONS, 1000))
    
    coords = []
    for i in range(0, CITY_NUM):
        x = random.randint(0, WINDOW_W)
        y = random.randint(0, WINDOW_H)
        coords.append([x, y])
    
    print(coords)
    
    Simulate(coords)
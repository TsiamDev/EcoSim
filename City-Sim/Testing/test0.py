# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 21:33:24 2022

@author: kosts
"""

import numpy as np
import random
import pygame
import sys

X = Y = 300
d_X = d_Y = 600

data =  np.zeros( (d_X, d_X, 3), dtype=np.uint8)

r = [[random.randint(0, 255) for i in range(X)] for j in range(X)]
g = [[random.randint(0, 255) for i in range(X)] for j in range(X)]
b = [[random.randint(0, 255) for i in range(X)] for j in range(X)]

data[15:315, 15:315, 0] = r
data[15:315, 15:315, 1] = g
data[15:315, 15:315, 2] = b

pygame.init()

display_surface = pygame.display.set_mode((d_X, d_Y))

while True :

    #clear screen
    display_surface.fill((0,0,0))

    t = np.array(data[:,:,0] > 150)
    data[t[:,:], :] = data[t[:,:], :] + 10

    pygame.surfarray.blit_array(display_surface, data)
    
    pygame.display.update()
    
    # Event loop
    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get() :
  
        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT :
            pygame.display.quit()
            sys.exit()

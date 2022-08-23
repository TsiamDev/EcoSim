# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 09:31:32 2022

@author: ASRock
"""

import pygame
from Const import DISPLAY

import random
import numpy as np
#from numpy import interp

import matplotlib.pyplot as plt

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    #valueScaled = float(value - leftMin) / float(leftSpan)
    valueScaled = (value - leftMin) / (leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return (rightMin + (valueScaled * rightSpan))#.astype(int)

w = 50
PH = np.random.uniform( 0, 14, size=(w, w, 3))
#get gradient of red/green
#g = [[random.uniform(0, 255) for i in range(w)] for j in range(w)]

PH[:, :, 0] = 0
#PH[:, :, 1] = g
PH[:, :, 2] = 0

#PH[:, : ,1] = interp(PH[:,:,1], [0, 255], [-7, 7])

#PH[:, : ,1] = translate(PH[:,:,1], 0, 1, 0, 14)

activation_function = np.zeros( (w, w, 3))
PH2 = np.zeros( (w, w, 3))
activation_function[:, :, 1] = np.exp(-abs(PH[:, :, 1]*0.5 - 3.5))
print(activation_function)

#PH[:, : ,1] = interp(activation_function[:, :, 1], [-7, 7], [0, 255])
PH2[:, : ,1] = translate(activation_function[:, :, 1], 0, 1, 0, 255)

x = PH2[:,0,1]
y = PH2[0,:,1]

y = [[i for i in range(0, w)] for j in range(0, w)]

#plt.scatter(activation_function[:,:,1])
plt.scatter(y, PH2[:,:,1])

WINDOW_SIZE = []
WINDOW_SIZE.append(750)
WINDOW_SIZE.append(750)

pygame.init()

# Zone lists
unexplored_zones = {}
zones = []

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
brown = (255, 248, 220)
red = (255, 0, 0)
gray = (128, 128, 128)  
#grass_col = (86, 125, 70)

# init ground
# assigning values to X and Y variable
X = Y = 750

# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((X, Y ))

display_surface = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]), pygame.RESIZABLE)
pygame.display.set_caption("Pasture Managerv0.01")


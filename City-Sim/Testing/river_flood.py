# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 15:19:02 2022

@author: TsiamDev
"""
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import pygame as pg
import sys

depth = np.zeros((750, 750, 3))

depth[:, :, 0] = [[random.randint(70, 83) for i in range(750)] for j in range(750)]
depth[:, :, 1] = [[random.randint(45, 50) for i in range(750)] for j in range(750)]
depth[:, :, 2] = [[random.randint(0, 0) for i in range(750)] for j in range(750)]
#depth = np.array([[random.randint(255, 255) for i in range(750)] for j in range(750)])

river = np.array([[random.randint(0, 255) for i in range(30)] for j in range(750)])

beach = np.zeros((750, 15, 3))
beach[:, :, 0] = [[random.randint(225, 246) for i in range(15)] for j in range(750)]
beach[:, :, 1] = [[random.randint(191, 215) for i in range(15)] for j in range(750)]
beach[:, :, 2] = [[random.randint(146, 176) for i in range(15)] for j in range(750)]

#depth[:, 315:330, :] = beach
depth[:, 330:360, 2] = river
#depth[:, 360:375, :] = beach

#j = 1
j = 1
pg.init()
ds = pg.display.set_mode((750, 750))
sign = 1
stage = 0
i = 0
"""
while True:
    if stage == 0:
        depth[:, 330:360, 2] += 5
        depth[depth > 255] = 255
        
        depth[:, 330:360, 2] = np.roll(depth[:, 330:360, 2], 1, axis=0)
        
        if (depth[:, 330:360, 2] == 255).all():
            stage = 1
    elif stage == 1:
        
    
    pg.surfarray.blit_array(ds, depth)
    pg.display.update()

    time.sleep(.010)
    for event in pg.event.get() :
        if event.type == pg.QUIT :
            pg.display.quit()
            sys.exit()
"""
while True:
    if stage == 0:
        depth[:, 330:360, 2] += 5
        depth[depth > 255] = 255
        
        depth[:, 330:360, 2] = np.roll(depth[:, 330:360, 2], 1, axis=0)
        
        if (depth[:, 330:360, 2] == 255).all():
            stage = 1
    elif stage == 1:
        #stag = j - 30
        x = 330-j
        if x < 0:
            x = 0
        #change this ! Upwards is later
        if j > 440:
            sign = -sign
        
        #exclude river from flooded-pixels-search
        if (depth[:, 0:330, 2] <= 0).all() and (depth[:, 360:750, 2] <= 0).all():
            j = 1
            sign = -sign
            stage = 0
        
        print("j: ", j)
        print(range(x, 330))
        if sign > 0:
            depth[:, x:330, 2] += sign * 5
            depth[:, (360):(360+j), 2] += sign * 5
            depth[depth > 255] = 255
            depth[depth < 0] = 0
        else:
            depth[:, :, 2] += sign * 1
            depth[:, :, 2] += sign * 1
            depth[ depth < 0] = 0
        depth[:, 330:360, 2] = 200
        #river = np.roll(river[:, :], 1, axis=0)
        #depth[:, 330:360, 2] = river
        j += sign * 1
            

    pg.surfarray.blit_array(ds, depth)
    pg.display.update()

    time.sleep(.010)
    for event in pg.event.get() :
        if event.type == pg.QUIT :
            pg.display.quit()
            sys.exit()
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 15:19:02 2022

@author: TsiamDev
"""
import matplotlib.pyplot as plt
import numpy as np
import random
import time
time.sleep(5)
#depth = np.zeros((750, 750), dtype=np.uint32)
depth = np.array([[random.randint(128, 255) for i in range(750)] for j in range(750)])
#river = np.array([[random.randint(0, 128) for i in range(750)] for j in range(30)])
river = np.array([[0 for i in range(750)] for j in range(30)])
depth[330:360, :] = river
#np.put(depth, [range((750*330), (750*360))], random.randint(0, 128))
#flood = 
plt.imshow(depth, cmap='winter', interpolation='nearest')
#ax1.show()
#"""
j = 1
for i in range(0, 330):

    x = 330-j
    print("j: ", j)
    print(range(x, 329))
    depth[x:329, :] -= 5
    depth[360:(360+j), :] -= 5
    depth[ depth < 128] = 0
    depth[330:360, :] = river
    j +=1
    plt.imshow(depth, cmap='winter', interpolation='nearest')
    plt.show()
    if x == 0:
        break
    #time.sleep(.400)
#"""
#j = 329
for i in range(j, 750-j, 2):

    print("i: ", i)
    print(range(360, 30+i))
    depth[360:(360+i), :] -= 5
    depth[ depth < 128] = 0
    depth[330:360, :] = river
    j +=1
    plt.imshow(depth, cmap='winter', interpolation='nearest')
    plt.show()
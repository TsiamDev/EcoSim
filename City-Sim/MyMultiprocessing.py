# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 01:19:30 2022

@author: TsiamDev
"""

import numpy as np
import random
import os

from multiprocessing import Process

from Const import DISPLAY

def Q_Consumer(q):
    rain_b_inc = np.zeros( (DISPLAY.FIELD_W, DISPLAY.FIELD_H), dtype=np.int32 )
    rain_b_inc += [[random.randint(1, 3) for i in range(DISPLAY.FIELD_W)] for j in range(DISPLAY.FIELD_H)]
    print("consumer ", os.getpid(), " started")
    while True:
        zones = q.get(True)
        if zones is not None:
            for z in zones:
                z.field.hum[:, :, 2] +=  rain_b_inc
                z.field.hum[z.field.hum[:, :, 2] > 255] = 255
                print("Hum changed")
        else: 
            break
    print("consumer ", os.getpid(), " finished")  

def Weather_Effect_To_Ground_Proc3(q, num_consumers):
    consumers = []
    print("Starting consumers...")
    for i in range(0, num_consumers):
        
        consumer = Process(target=Q_Consumer, args=(q,))
        consumer.daemon = True
        consumer.start()  # Launch consumer() as another proc
    
        consumers.append(consumer)
    print("Returning consumers...")
    return consumers

def Weather_Effect_To_Ground_Proc2(q):
    rain_b_inc = np.zeros( (DISPLAY.FIELD_W, DISPLAY.FIELD_H), dtype=np.int32 )
    rain_b_inc += [[random.randint(1, 3) for i in range(DISPLAY.FIELD_W)] for j in range(DISPLAY.FIELD_H)]
    
    zones = q.get(True)
    print(zones)
    for z in zones:
        #print(len(rain_b_inc))
        #print(len(rain_b_inc[0]))
        #print((rain_b_inc[0][0]))
        #print(z.field.hum)
        #z.field.hum[:, :, 2] += rain_b_inc if any(z.field.hum[:, :, 2] < 255) else 255
        z.field.hum[:, :, 2] +=  rain_b_inc
        #z.field.hum += rain_b_inc if z.field.hum[:,:,2] < 255 else 255
        #i = z.field.hum[:,:,2] + rain_b_inc
        #i = z.field.hum[:][:][2] < 255
        #i = z.field.hum[:,:,2] < 255
        #np.where(i, z.field.hum[i] + rain_b_inc , 255)
        
        #z.field.hum[z.field.hum[:, :, 0] > 0] = 0
        #z.field.hum[z.field.hum[:, :, 1] > 0] = 0
        z.field.hum[z.field.hum[:, :, 2] > 255] = 255

def Weather_Effect_To_Ground_Proc(mp_queue):#, _weather_effect_type):
    #global weather_effect_type
    #weather_effect_type = _weather_effect_type
    #Weather effects
    #weather_effect = WeatherEffect(pygame, WEATHER.types['RAIN'])
    #lock.acquire()
    print("1")
    rain_b_inc = np.zeros( (DISPLAY.FIELD_W, DISPLAY.FIELD_H), dtype=np.int32 )
    rain_b_inc += [[random.randint(1, 3) for i in range(DISPLAY.FIELD_W)] for j in range(DISPLAY.FIELD_H)]
    print("2")
    print (os.getpid() , "working")
    #lock.release()
    while True:
        zones = mp_queue.get(True)
        #lock.acquire()
        print(os.getpid(), "got", zones)
        #lock.release()
        #time.sleep(1) # simulate a "long" operation
    
        #if weather_effect_type == WEATHER.types['RAIN']:
            
        for z in zones:
            #print(len(rain_b_inc))
            #print(len(rain_b_inc[0]))
            #print((rain_b_inc[0][0]))
            #print(z.field.hum)
            #z.field.hum[:, :, 2] += rain_b_inc if any(z.field.hum[:, :, 2] < 255) else 255
            z.field.hum[:, :, 2] +=  rain_b_inc
            #z.field.hum += rain_b_inc if z.field.hum[:,:,2] < 255 else 255
            #i = z.field.hum[:,:,2] + rain_b_inc
            #i = z.field.hum[:][:][2] < 255
            #i = z.field.hum[:,:,2] < 255
            #np.where(i, z.field.hum[i] + rain_b_inc , 255)
            
            #z.field.hum[z.field.hum[:, :, 0] > 0] = 0
            #z.field.hum[z.field.hum[:, :, 1] > 0] = 0
            z.field.hum[z.field.hum[:, :, 2] > 255] = 255
        
        #time.sleep(1./120)
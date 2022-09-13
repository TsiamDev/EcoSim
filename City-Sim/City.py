# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 11:47:03 2022

@author: TsiamDev
"""

from Tractor import Tractor
from effects.Weather import WeatherEffect

from Zone import Zone
from MyRect import MyRect
from Const import TIME, DISPLAY, GOODS, CONSUMPTION_POLICY, CONSUMPTION, WEATHER, CONST
from Const import WEATHER_SEVERITY

import numpy as np
import random
import copy
import math
import time

class City:
    def __init__(self, j=None, prices=None, cons_policy=None, reserve=None, _coords=None, _center=None, _unexplored_zones=None, _zones=None, _plant=None, _has_tractor=None, _has_river=None):
        if j is not None:
            self.id = j
        else:
            self.id = 10
        
        self.pos = _coords
        self.center = _center
        
        #City's money
        self.reserve = reserve
        
        self.consumption_policy = cons_policy
        
        # Goods 
        #Prices
        #self.goods_prices = prices
        self.goods_prices = []
        for g in GOODS.types.items():
            self.goods_prices.append((random.randint(10, 25)))
            #print(g)
        #Silos
        self.goods_amounts = []
        for g in GOODS.types.items():
            self.goods_amounts.append(20)
            #print(g)
        
        # Population
        self.population = 100
        
        # Consumption
        self.consumption = int(self.population / 100)
        
        # Production - Deprecated
        self.production = [0 for i in GOODS.types.items()]
        #?
        #self.production[j%3] = 51
        
        # temporary storage for traded resources
        self._in = [0 for i in GOODS.types.items()]
        self._out = [0 for i in GOODS.types.items()]
        
        
        
        self.zones = None
        #Simulation stuff
        if _zones is None:
            self.zones = []
            rect = MyRect(_x=DISPLAY.ROAD_WIDTH, _y=DISPLAY.ROAD_WIDTH, _center=(int(DISPLAY.ZONE_W/2), int(DISPLAY.ZONE_H/2)))#, _topleft=(DISPLAY.ROAD_WIDTH, DISPLAY.ROAD_WIDTH))
            self.zones.append(Zone(0, copy.deepcopy(rect), CONST.types['FIELD']))
            self.zones[0].field.has_init = True
            rect0 = MyRect(_x=330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, _y=15, _center=(int(DISPLAY.ZONE_W/2), int(DISPLAY.ZONE_H/2)))
            self.zones.append(Zone(1, copy.deepcopy(rect0)))
            rect1 = MyRect(_x=15, _y=330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, _center=(int(DISPLAY.ZONE_W/2), int(DISPLAY.ZONE_H/2)))
            self.zones.append(Zone(2, copy.deepcopy(rect1)))
            rect2 = MyRect(_x=330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, _y=330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, _center=(int(DISPLAY.ZONE_W/2), int(DISPLAY.ZONE_H/2)))
            self.zones.append(Zone(3, copy.deepcopy(rect2)))
        else:
            self.zones = _zones
            self.zones[0].is_explored = True
        self.unexplored_zones = _unexplored_zones
        self.time_cnt = 0
        self.data = np.zeros( (DISPLAY.X, DISPLAY.Y, 3), dtype=np.uint8 )
        self.is_active = False
        
        """
            #river stuff
        if _has_river is not None:
            
            r = [[random.randint(0, 25) for i in range(DISPLAY.RIVER_H)] for j in range(DISPLAY.RIVER_W)]
            g = [[random.randint(0, 50) for i in range(DISPLAY.RIVER_H)] for j in range(DISPLAY.RIVER_W)]
            b = [[random.randint(100, 255) for i in range(DISPLAY.RIVER_H)] for j in range(DISPLAY.RIVER_W)]
            
            self.data[0:DISPLAY.RIVER_W, (DISPLAY.N+DISPLAY.RIVER_H):(DISPLAY.N+60), 0] = r
            self.data[0:DISPLAY.RIVER_W, (DISPLAY.N+DISPLAY.RIVER_H):(DISPLAY.N+60), 1] = g
            self.data[0:DISPLAY.RIVER_W, (DISPLAY.N+DISPLAY.RIVER_H):(DISPLAY.N+60), 2] = b
        """
            #plant stuff
        self.plant = _plant
        
            #tractor stuff
        #print("_has_tractor: ", _has_tractor)
        self.tractor = None
        if _has_tractor == True:
            self.tractor = Tractor(15, 15, self.zones[0], self)
            #self.tractor = Tractor(0, 0, self.zones[0])
        
        self.weather_effect = WeatherEffect(WEATHER.types['RAIN'])
        
        #surface level relative to water level: "sea level" 0, is 128
        #river has 0 depth everywhere
        self.terrain = np.zeros((750, 750, 3), dtype=np.int32)
        self.Update_Terrain()
        #self.terrain[:, :, 2] = np.array([[random.randint(0, 128) for i in range(DISPLAY.X)] for j in range(DISPLAY.Y)])
        #self.river = np.array([[255 for i in range(DISPLAY.RIVER_H)] for j in range(DISPLAY.X)])
        #_x = DISPLAY.ROAD_WIDTH * 2 + DISPLAY.ZONE_H
        #self.terrain[:, _x:_x+DISPLAY.RIVER_H, 2] = self.river
        self.ind = 1
        self.sign = 1
        self.stage = 0
        self.lag = 0
        self.start = time.time()
        self.end = time.time()
        self.we_was_active = False
        
        #self.terrain = self.terrain.astype('uint32')
        #self.river = self.river.astype('uint32')
        
        #self.weather_effect.is_active = False
        
        self.stop_updating_terrain = False
        
        #set ground colors
        self.r = [[random.randint(70, 83) for i in range(DISPLAY.FIELD_W)] for j in range(DISPLAY.FIELD_H)]  
        self.g = [[random.randint(45, 50) for i in range(DISPLAY.FIELD_W)] for j in range(DISPLAY.FIELD_H)]

    """DEPRECATED
    def Produce(self):        
        for i in range(0, len(GOODS.types.items())):
            self.goods_amounts[i] = self.goods_amounts[i] + self.production[i] 
            print("City " + str(self.id) + " produced " + str(self.production[i]))
    """ 
    def Consume(self):
        # Calculate consumption rate    
        self.consumption = int(self.population / 100)
        if self.consumption == 0:
            self.consumption = 1
        
        print("City Resources: " + str(self.goods_amounts))
        
        # Calculate surplus
        avail_goods_cnt = 0
        i = 0
        for key, cons in CONSUMPTION.types.items():
            #print(self.consumption)
            #print("c" + str(int(cons)))
            #print("cons: " + str(int(cons) * self.consumption) )
            amount = int(cons) * self.consumption
            if self.goods_amounts[i] >= amount:
                self.goods_amounts[i] -= amount
                print("City consumed " + str(amount) + " of " + str(i))
                self.reserve += amount * self.goods_prices[i]
                avail_goods_cnt += 1
            elif self.goods_amounts[i] > 0:
                print("City consumed " + str(self.goods_amounts[i]) + " of " + str(i))
                self.goods_amounts[i] = 0
                self.reserve += self.consumption * self.goods_prices[i]
                avail_goods_cnt += 1
            else:
                print("City did not have enough, of resource " + str(i) + ", to consume.")
            print("City reserve: " + str(self.reserve))
            i += 1
        #print(avail_goods_cnt)
        print("City Surplus: " + str(self.goods_amounts))
        
        # Enforce Policy                
        if self.consumption_policy == CONSUMPTION_POLICY.types['DOMESTIC_CONS']:
            # Consume Surplus
            for i in range(1, len(self.goods_amounts)):
                if self.goods_amounts[i] > 0:
                    avail_goods_cnt = avail_goods_cnt + 1
                self._out[i] = 0
        else:
            # Export Surplus
            for i in range(0, len(self.goods_amounts)):
                if self.goods_amounts[i] > 0:
                    self._out[i] = self.goods_amounts[i]
                    self.goods_amounts[i] = 0
                else:
                    self._out[i] = 0
        
        # Population growth/decline
        
        if avail_goods_cnt > 1:
            self.population = self.population + 30
            print("City " + str(self.id) + " grew by 30 people -> " + str(self.population))
        elif avail_goods_cnt == 1:
            self.population = self.population + 10
            print("City " + str(self.id) + " grew by 10 people -> " + str(self.population))
        elif avail_goods_cnt == 0:
            self.population = self.population - 10
            print("City " + str(self.id) + " diminished by 10 people -> " + str(self.population))
        
        print("City " + str(self.id) + " consumed " + str(avail_goods_cnt) + " goods.")
    
    def Consume_Traded_Goods(self):
        for i in range(0, len(self.goods_amounts)):
            self.goods_amounts[i] = self.goods_amounts[i] + self._in[i]
            self._in[i] = 0
        print("added traded goods to stockpiles: " + str(self.goods_amounts))
    
    def Crop_Growth(self):
        #global zones, time_cnt, data, pygame
        
        self.time_cnt += 1
        
        if self.time_cnt >= TIME.types['CROP']:
            for z in self.zones:
                #if z.type == CONST.types['FIELD']:
                if z.field is not None:
                    if z.field.has_init == True:
                        if (z.field.is_planted > 0).any():
                            #crops grow - if <pixel> is planted
                            #TODO: handle dividing by zero (z.field.PH)
                            new_growth = np.zeros((len(z.field.N), len(z.field.N), 2), dtype=np.uint32)
                            new_growth[:,:,0] = (z.field.N[:,:,0] * 0.1 + z.field.P[:,:,0] * 0.1 + z.field.K[:,:,2] * 0.1 + z.field.hum[:,:,2] * 0.2) / (z.field.PH[:,:,1] / 2)
                            new_growth[:,:,1] = (z.field.N[:,:,1] * 0.1 + z.field.P[:,:,1] * 0.1 + z.field.K[:,:,2] * 0.1 + z.field.hum[:,:,2] * 0.2) / (z.field.PH[:,:,1] / 2)
                            #t = z.field.is_planted * new_growth
                            #print(t)
                            #print(len(t))
                            z.field.crop_growth[:,:,0] += (z.field.is_planted[:,:,0] * new_growth[:,:,0]).astype(int)#new_growth.astype(int)#(5, 0, 0)
                            z.field.crop_growth[z.field.crop_growth[:,:,0] > 255, 0] = 255
                            z.field.crop_growth[:,:,1] += (z.field.is_planted[:,:,1] * new_growth[:,:,1]).astype(int)
                            z.field.crop_growth[z.field.crop_growth[:,:,1] > 255, 1] = 255
                            #remove moisture from the top soil
                            z.field.hum[z.field.is_planted[:,:,1] == 1, 2] -= (0.1 * z.field.hum[z.field.is_planted[:,:,1] == 1, 2]).astype(int)
            self.time_cnt = 0
        
    def Move_River(self):
        N = 300
        #circularly shift the river portion of <data>
        self.data[0:DISPLAY.RIVER_W, (N+30):(N+60), :] = np.roll(self.data[0:DISPLAY.RIVER_W, (N+30):(N+60), :], 1, axis=0)
    """
    def Draw_Unexplored_Zones(self):
        global unexplored_zones, display_surface, gray, label
        
        for key, uz in unexplored_zones.items():
            pygame.draw.rect(display_surface, gray, uz.rect)
            label_rect = label.get_rect(center=(uz.rect.center))
            display_surface.blit(label, label_rect)
    """
    
    def Plot(self, plot):
        if plot == True:
            print("Drawing plot")
            #TODO: Draw the plot
        elif plot == False:
            print("Hiding plot")
            #TODO: Hide the plot
        else:
            print("something went wrong with <plot> variable")
            return
    
    def Re_Init_After_Flood(self):
        for zone in self.zones:
            if zone._is(CONST.types['FIELD']) or zone._is(CONST.types['PASTURE']):
                #reset crop_growth to zero (plain ground)
                zone.field.crop_growth[:, :, 0] = self.r
                zone.field.crop_growth[:, :, 1] = self.g
                zone.field.crop_growth[:, :, 2] = 0
                
                #remove is_planted status
                zone.field.is_planted[:, :] = 0
                
                #reset plant_face to plain ground
                zone.field.plant_face[:, :, 0] = self.r
                zone.field.plant_face[:, :, 1] = self.g
                zone.field.plant_face[:, :, 2] = 0
                
                #reinitialize humidity to "soaking wet"
                zone.field.hum[:, :, 0:1] = 0 
                zone.field.hum[:, :, 2] = 255
                
                #reinitialize temperature to "very cold"
                zone.field.temp[:, :, 0:1] = 0
                zone.field.temp[:, :, 2] = 255
                print("field reinitialized")
                
    def Overflow_River(self):
        self.end = time.time()
        #print(self.end - self.start)
        
        if self.stage == 0:
            threshold = 0.01
        elif self.stage == 1:
            threshold = 0.005
            
        if (self.end - self.start) >= threshold:
            if self.stage == 0:
                #"""
                #print("Stage 0 - river overflows")
                self.terrain[:, 330:360, 2] += 5
                self.terrain[self.terrain > 255] = 255
                
                self.terrain[:, 330:360, 2] = np.roll(self.terrain[:, 330:360, 2], 1, axis=0)
                
                if (self.terrain[:, 330:360, 2] == 255).all():
                    self.stage = 1
                #"""
            elif self.stage == 1:
                #print("Stage 1 - waves emerge from the river")
                #stag = j - 30
                self.upper_y = 330-self.ind
                if self.upper_y < 0:
                    self.upper_y = 0
                #change this ! Upwards is later
                if self.ind > 440:
                    self.sign = -self.sign
                    
                if self.ind < 0:
                    self.ind = 0
                    
                    #delay changing the sign, so that there is enough time for the 
                    #flood water to drain
                    if self.lag >= 80:
                        self.sign = -self.sign
                        self.lag = 0
                    else:
                        self.lag += 1
                
                #exclude river from flooded-pixels-search
                if (self.terrain[:, 0:330, 2] >= 255).all() and (self.terrain[:, 360:750, 2] >= 255).all():
                    self.ind = 1
                    self.sign = -self.sign
                    self.stage = 0
                
                #print("ind: ", self.ind)
                #print(range(self.upper_y, 330))
                if self.sign > 0:
                    self.terrain[:, self.upper_y:330, 2] += self.sign * 5
                    self.terrain[:, (360):(360+self.ind), 2] += self.sign * 5
                    self.terrain[self.terrain > 255] = 255
                    self.terrain[self.terrain < 0] = 0
                    #print(len(self.terrain[0]), len(self.terrain[1]))
                else:
                    self.terrain[:, :, 2] += (np.uint32)(self.sign * 1)
                    self.terrain[:, :, 2] += (np.uint32)(self.sign * 1)
                    self.terrain[ self.terrain < 0] = 0
                    #print(len(self.terrain[0]), len(self.terrain[1]))
                self.terrain[:, 330:360, 2] = 200
                #print(len(self.terrain[0]), len(self.terrain[1]))
                #river = np.roll(river[:, :], 1, axis=0)
                #depth[:, 330:360, 2] = river
                self.ind += self.sign * 1

            self.start = time.time()
                
    def Update_Terrain(self):
        for zone in self.zones:
            if not zone._is(CONST.types['BARN_SILO']):
                rect = MyRect(_x=zone.rect.x, _y=zone.rect.y, _center=(math.floor((zone.rect.x+DISPLAY.ZONE_W)/2), math.floor((zone.rect.y+DISPLAY.ZONE_H)/2)), _w=DISPLAY.ZONE_W)
                self.terrain[rect.topleft[0]:rect.topright[0], rect.topright[1]:rect.bottomright[1], :] = self.data[rect.topleft[0]:rect.topright[0], rect.topright[1]:rect.bottomright[1], :]
    
    #Move the animals
    def Move_Animals(self):
        for zone in self.zones:               
            if zone._is(CONST.types['PASTURE']):              
                for i in range (0, len(zone.pasture.animals)):
                    zone.pasture.animals[i].act(zone, self.data, self)
    
    def Normal_City_Workflow(self):
        if self.we_was_active == True:
            #print("Stage 2 - flood water drains")
            self.end = time.time()
            #print(self.end - self.start)
                
            if (self.end - self.start) >= 0.005:
                #weather effect was just active, give some time for
                #water drainage animation
                #print(range(self.upper_y, 330))
                #print(range(360, 360+self.ind))
                
                #self.terrain[:, :, 2] -= 5
                #self.terrain[self.terrain < 0] = 0
                flag = False
                
                if (self.terrain[:, self.upper_y:330, 2] > 0).any():
                    temp = self.terrain[:, self.upper_y:330, 2] 
                    temp -= 10
                    temp[temp < 0] = 0
                    self.terrain[:, self.upper_y:330, 2] = temp
                    flag = True
                
                if (self.terrain[:, 360:, 2] > 0).any():
                    temp = self.terrain[:, 360:, 2]
                    temp -= 10
                    temp[temp < 0] = 0
                    self.terrain[:, 360:, 2] = temp
                    flag = True
                print(self.upper_y, self.ind)
                print(self.terrain[:, 360:, :])
                
                #self.terrain[:, self.upper_y:self.ind, 2] < 0 = 0
               
                #if self.lag >= 150:
                if flag == False:
                    #self.lag = 0
                    self.we_was_active = False
                    self.Re_Init_After_Flood()
                #else:
                #self.lag += 1
                
                self.start = time.time()
        else:
            #business as usual
            self.stop_updating_terrain = False
            self.ind = 1
            self.sign = 1
            self.upper_y = 330
            
            #crops grow
            self.Crop_Growth()
            
            #animals move
            self.Move_Animals()
            
            #tractor acts
            self.tractor.act(self.data, self.plant)
            
            #river flows normally
            self.Move_River()
            
    #Update the city parameters
    def Draw(self):     
        
        #If flood hits
        if self.weather_effect.is_active == True:
            #print("True")
            if self.weather_effect.type == WEATHER.types['RAIN']:
                if self.weather_effect.severity == WEATHER_SEVERITY.types['HIGH']:
                    self.Overflow_River()
                    #self.Move_River()
                    self.stop_updating_terrain = True
                    self.we_was_active = True
                else:
                    self.Normal_City_Workflow()
        else:
            self.Normal_City_Workflow()
            
        if self.stop_updating_terrain == False:
            self.Update_Terrain()
        
            
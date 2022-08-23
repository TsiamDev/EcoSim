# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 11:47:03 2022

@author: TsiamDev
"""

from Enums.enums import *
from Const import TIME, DISPLAY

import numpy as np

class City:
    def __init__(self, j, prices, cons_policy, reserve, zones):
        self.id = j
        
        self.reserve = reserve
        
        self.consumption_policy = cons_policy
        
        # Goods
        self.goods_prices = prices
        self.goods_amounts = []
        for g in Goods:
            self.goods_amounts.append(20)
            #print(g)
        
        # Population
        self.population = 100
        
        # Consumption
        self.consumption = int(self.population / 100)
        
        # Production
        self.production = [0 for i in Goods]
        self.production[j] = 51
        
        # temporary storage for traded resources
        self._in = [0 for i in Goods]
        self._out = [0 for i in Goods]
        
        #Simulation stuff
        self.zones = zones
        self.time_cnt = 0
        self.data = np.zeros( (DISPLAY.X, DISPLAY.Y, 3), dtype=np.uint8 )
        
            #river stuff
        r = [[random.randint(0, 25) for i in range(DISPLAY.river_H)] for j in range(DISPLAY.river_W)]
        g = [[random.randint(0, 50) for i in range(DISPLAY.river_H)] for j in range(DISPLAY.river_W)]
        b = [[random.randint(100, 255) for i in range(DISPLAY.river_H)] for j in range(DISPLAY.river_W)]
        
        self.data[0:DISPLAY.river_W, (DISPLAY.N+DISPLAY.river_H):(DISPLAY.N+60), 0] = r
        self.data[0:DISPLAY.river_W, (DISPLAY.N+DISPLAY.river_H):(DISPLAY.N+60), 1] = g
        self.data[0:DISPLAY.river_W, (DISPLAY.N+DISPLAY.river_H):(DISPLAY.N+60), 2] = b
        
        self.tractor = Tractor(15, 15, zones[0])
        
    def Produce(self):        
        for i in range(0, len(Goods)):
            self.goods_amounts[i] = self.goods_amounts[i] + self.production[i] 
            print("City " + str(self.id) + " produced " + str(self.production[i]))
        
    def Consume(self):
        # Calculate consumption rate    
        self.consumption = int(self.population / 100)
        if self.consumption == 0:
            self.consumption = 1
        
        print("City Resources: " + str(self.goods_amounts))
        
        # Calculate surplus
        avail_goods_cnt = 0
        i = 0
        for cons in Consumption:
            #print(self.consumption)
            #print("c" + str(int(cons)))
            #print("cons: " + str(int(cons) * self.consumption) )
            amount = int(cons) * self.consumption
            if self.goods_amounts[i] >= amount:
                self.goods_amounts[i] = self.goods_amounts[i] - amount
                print("City consumed " + str(amount) + " of " + str(i))
                self.reserve = self.reserve + amount * self.goods_prices[i]
                avail_goods_cnt = avail_goods_cnt + 1
            elif self.goods_amounts[i] > 0:
                print("City consumed " + str(self.goods_amounts[i]) + " of " + str(i))
                self.goods_amounts[i] = 0
                self.reserve = self.reserve + self.consumption * self.goods_prices[i]
                avail_goods_cnt = avail_goods_cnt + 1
            else:
                print("City did not have enough, of resource " + str(i) + ", to consume.")
            print("City reserve: " + str(self.reserve))
            i = i + 1
        #print(avail_goods_cnt)
        print("City Surplus: " + str(self.goods_amounts))
        
        # Enforce Policy                
        if self.consumption_policy == Consumption_Policy.DOMESTIC_CONS:
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
        
        if self.time_cnt > TIME.types['CROP']:
            for z in self.zones:
                if z.field is not None:
                    if z.field.has_init == True:
                        """
                        #crops grow - if <pixel> is planted
                        #growth_denominator = np.ones((z.rect.width, z.rect.height))
                        #t = np.where(np.logical_and(z.field.PH>=110, z.field.PH<=140))
                        #print(t[0])
                        #growth_denominator = z.field.PH[t]
                        #print(growth_denominator)
                        new_growth = (z.field.N * 0.3 + z.field.P * 0.3 + z.field.K * 0.4) / z.field.PH
                        z.field.crop_growth[z.field.is_planted > 0] += new_growth.astype(int)#(5, 0, 0)
                        #print(z.field.crop_growth[:, :, 1] > z.field.crop_growth[:, :, 0])
                        #print(z.field.crop_growth[:, :, 0])
                        z.field.crop_growth[(z.field.is_planted[:, :] == 1) & (z.field.crop_growth[:, :, 1] < z.field.crop_growth[:, :, 0])] -= (10, 0, 0)
                        z.field.crop_growth[z.field.crop_growth < 0] = 0
                        """
                        #data[z.rect.topleft[0]:z.rect.topright[0], z.rect.topright[1]:z.rect.bottomright[1], :] = z.field.crop_growth
            self.time_cnt = 0
        
        #pygame.surfarray.blit_array(display_surface, data)
        return self.data
    
    def Move_River(self):
        N = 300
        #circularly shift the river portion of <data>
        self.data[0:DISPLAY.river_W, (N+30):(N+60), :] = np.roll(self.data[0:DISPLAY.river_W, (N+30):(N+60), :], 1, axis=0)
    """
    def Draw_Unexplored_Zones(self):
        global unexplored_zones, display_surface, gray, label
        
        for key, uz in unexplored_zones.items():
            pygame.draw.rect(display_surface, gray, uz.rect)
            label_rect = label.get_rect(center=(uz.rect.center))
            display_surface.blit(label, label_rect)
    """
    def Draw(self):
        self.Crop_Growth()
        self.Move_River()
        
        #self.Draw_Unexplored_Zones()
        
        d = self.tractor.act2(data, display_surface, plant)
        if d is not None:
            data = d
        
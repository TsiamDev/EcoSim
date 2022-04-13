# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 11:47:03 2022

@author: TsiamDev
"""

from Enums.enums import *

class City:
    def __init__(self, j, prices, cons_policy, reserve):
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
    
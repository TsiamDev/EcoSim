# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 09:51:57 2022

@author: TsiamDev
"""

from enums import Goods

class Business:
    def __init__(self, city, _type):
        self.city = city
        self._type = _type
        
        self.goods_amounts = [0 for i in Goods]
        
        self.lvl = 1
        self.production = self.lvl * 10
        
    def Produce(self):
        self.goods_amounts[self._type] = self.goods_amounts[self._type] + self.production
        
    def Sell_To_City(self, dest_city):
        for i in range(0, len(self.goods_amounts)):
            if self.goods_price_thresh[i] <= dest_city.goods_prices[i]:
                dest_city._in[i] = dest_city._in[i] + self.goods_amounts[i]
                print("BUsiness traded " + str(self.goods_amounts[i]) + " of " + str(i))
            
                self.goods_amounts[i] = 0
        
    def Upgrade(self):
        self.lvl = self.lvl + 1
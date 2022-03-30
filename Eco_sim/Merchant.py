# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 11:47:25 2022

@author: HomeTheater
"""
import random
from Enums.enums import *

class Merchant:
    def __init__(self, _id):
        self.id = _id
        
        self.goods_amounts = [0 for i in Goods]
        self.goods_price_thresh = [4, 4, 4]
        # generate random amounts for goods to trade
        #self.Purchase_Random()
        
    def Purchase_Random(self):
        for g in Goods:
            self.goods_amounts[g] = random.randint(21, 22)
        #print(self.goods_amounts)
        
    def Buy_From_City(self, dest_city):
        print("trader stocks: " + str(self.goods_amounts))
        for i in range(0, len(dest_city._out)):
            self.goods_amounts[i] = self.goods_amounts[i] + dest_city._out[i]
            dest_city._out[i] = 0
        print("trader new stocks: " + str(self.goods_amounts))
        print("City new stocks: " + str(dest_city.goods_amounts))
        
    def Sell_To_City(self, dest_city):
        for i in range(0, len(self.goods_amounts)):
            if self.goods_price_thresh[i] <= dest_city.goods_prices[i]:
                dest_city._in[i] = dest_city._in[i] + self.goods_amounts[i]
                print("Merchant traded " + str(self.goods_amounts[i]) + " of " + str(i))
            
                self.goods_amounts[i] = 0
    
    def Purchase_Grain(self):
        self.goods_amounts[0] = random.randint(21, 221)
    
    def Raid(self):
        ch = random.randint(0, 10)
        if ch < 3:
            print("Merchant is raided - lost all goods")
            self.goods_amounts = [0 for i in Goods]
            return True
        return False
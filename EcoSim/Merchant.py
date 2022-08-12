# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 11:47:25 2022

@author: TsiamDev
"""
import random
#from Enums.enums import *
from enums import *
from City import City

class Merchant:
    def __init__(self, _id, home):
        assert (isinstance(_id, int)), "_id should be an Int"
        self.id = _id
        
        assert (isinstance(home, City)), "home should be a City"
        self.home_city = home
        
        self.reserve = 1000
        
        self.goods_amounts = [0 for i in Goods]
        self.goods_price_thresh = [4, 4, 4]
        # generate random amounts for goods to trade
        #self.Purchase_Random()
        
    def Get_Random_Amount(self, upper):
        assert (isinstance(upper, int)), "upper should be an Int"
        if upper > 1:
            return random.randint(1, upper)
        elif upper == 1:
            return 1
        else:
            return 0
        
    def Purchase_Random(self):
        for g in Goods:
            self.goods_amounts[g] = random.randint(21, 22)
        #print(self.goods_amounts)
        
    def Buy_From_City(self, dest_city):
        print("trader stocks: " + str(self.goods_amounts))
        alocated_reserve = int(self.reserve / len(self.goods_amounts))
        for i in range(0, len(dest_city._out)):
            upper =  int(alocated_reserve / dest_city.goods_prices[i])
            amount = self.Get_Random_Amount(upper)
            price = amount * dest_city.goods_prices[i]
            if alocated_reserve - price >= 0:
                self.goods_amounts[i] = self.goods_amounts[i] + amount
                dest_city._out[i] = dest_city._out[i] - amount
                self.reserve = self.reserve - price
                dest_city.reserve = dest_city.reserve + price
                print("trader bought " + str(price) + " worth of goods")
        print("trader new stocks: " + str(self.goods_amounts))
        print("trader new reserve: " + str(self.reserve))
        print("City new stocks: " + str(dest_city.goods_amounts))
        
    def Sell_To_City(self, dest_city):
        alocated_reserve = int(self.reserve / len(self.goods_amounts))
        for i in range(0, len(self.goods_amounts)):
            upper =  int(alocated_reserve / dest_city.goods_prices[i])
            amount = self.Get_Random_Amount(upper)
            price = amount * dest_city.goods_prices[i]
            if self.goods_price_thresh[i] <= dest_city.goods_prices[i]:
                if alocated_reserve - price >= 0:
                    dest_city._in[i] = dest_city._in[i] + amount
                    print("Merchant sold " + str(amount) + " of " + str(i))
                    print("Merchant new reserve: " + str(self.reserve))
                    self.goods_amounts[i] = self.goods_amounts[i] - amount
                    self.reserve = self.reserve + price
                    dest_city.reserve = dest_city.reserve - price
    
    def GetLoan(self, bank):
        if self.reserve < 50:
            if self.home_city.reserve >= 2000:
                self.reserve = self.reserve + 1000
                self.home_city.reserve = self.home_city.reserve - 1000
            else:
                got_loan = bank.Loan(self, 1000)
                if got_loan:
                    self.reserve = self.reserve + 1000    
                    print("Merchant got loan!")
    
    def Resuply(self):
        upper = self.home_city.production[self.home_city.id]
        amount = self.Get_Random_Amount(upper)
        self.goods_amounts[self.home_city.id] = self.goods_amounts[self.home_city.id] + amount
    
    def Purchase_Grain(self):
        upper =  int(self.reserve / Global_Market_Prices.GRAIN_PRICE)
        amount = self.Get_Random_Amount(upper)
        price = amount * Global_Market_Prices.GRAIN_PRICE
        if self.reserve - price >= 0:
            self.goods_amounts[0] = self.goods_amounts[0] + amount
            self.reserve = self.reserve - price
    
    def Raid(self):
        ch = random.randint(0, 10)
        goods_lost = 0
        if ch < 1:
            print("Merchant is raided - lost all goods")
            for g in self.goods_amounts:
                goods_lost = goods_lost + g
            self.goods_amounts = [0 for i in Goods]
            
        return goods_lost
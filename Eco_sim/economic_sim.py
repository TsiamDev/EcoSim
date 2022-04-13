# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 18:29:09 2022

@author: TsiamDev
"""

from time import * 


import matplotlib.pyplot as plt

from Enums.enums import *

from City import City
from Merchant import Merchant
from Bank import Bank


cities = []
cities.append(City(0, [1, 5, 5], Consumption_Policy.EXPORT, 1000))
cities.append(City(1, [5, 1, 5], Consumption_Policy.EXPORT, 1000))
cities.append(City(2, [5, 5, 1], Consumption_Policy.DOMESTIC_CONS, 1000))
ln_cities = len(cities)

m = Merchant(0, cities[1])
food_m = Merchant(1, cities[0])
food_m.Purchase_Grain()

bank = Bank()

max_it = 0

pop = []
goods = []
raids = []
goods_lost = []
merchant_reserve = []
city_reserve = []
loans = []
while max_it < 500:
    print("iteration: " + str(max_it))
    avg_raids = 0
    goods_lost_to_raids = 0
    for c in cities:
        c.Produce()
        c.Consume() 
        #print(c.goods_amounts)
        #print(c.population)
        m.GetLoan(bank)
        #m.Resuply()
        m.Buy_From_City(c)
        wasRaided = m.Raid()
        #wasRaided = 0
        if wasRaided > 0:
            goods_lost_to_raids = goods_lost_to_raids + wasRaided
            avg_raids = avg_raids + 1
        m.Sell_To_City(c)
        #m.Purchase_Random()
        
        food_m.GetLoan(bank)
        #food_m.Resuply()
        food_m.Sell_To_City(c)
        food_m.Purchase_Grain()
        wasRaided = food_m.Raid()
        if wasRaided > 0:
            goods_lost_to_raids = goods_lost_to_raids + wasRaided
            avg_raids = avg_raids + 1
        
        c.Consume_Traded_Goods()
    
    #if len(cities) > 1:
        #cities[0].Trade(cities[1])
        #cities[1].Trade(cities[0])
    
    #m.Trade(cities[0], len(cities))
    #m.Purchase_Random()
    #m.Trade(cities[1], len(cities))
    #m.Purchase_Random()
    
    #for c in cities:
    #    c.Consume_Traded_Goods()
        #print(c.goods_amounts)
    
    #if c.population <= 0:
    #    break

    # city reserve    
    city_res = 0
    # flag dead cities
    to_remove = []
    for i in range(0, len(cities)):
        if cities[i].population <= 0:
            to_remove.append(cities[i])
        city_res = city_res + cities[i].reserve
    city_reserve.append(city_res)
        
    # remove dead cities
    for i in range(0, len(to_remove)):
        cities.remove(to_remove[i])

    if len(cities) == 0:
        break         

    # metrics
    raids.append(avg_raids)
    goods_lost.append(goods_lost_to_raids)
    
    avg_pop = 0
    avg_goods = 0
    for c in cities:
        avg_pop = avg_pop + c.population
        for i in range(0, len(c.goods_amounts)):
            avg_goods = avg_goods + c.goods_amounts[i]    
    avg_pop = avg_pop / ln_cities
    pop.append(avg_pop)
    avg_goods = avg_goods / ln_cities
    goods.append(avg_goods)

    # merchant reserve
    merchant_res = m.reserve + food_m.reserve
    merchant_reserve.append(merchant_res)

    temp = 0
    for k in bank.loans:
        temp = temp + bank.loans[k]
    loans.append(temp)
    
    # set the simulation frequency    
    #sleep(1)
    
    max_it = max_it + 1
    print("-------------------------------------")
xs = [i for i in range(0, max_it)]

plt.plot(xs, pop)
plt.plot(xs, goods)
plt.plot(xs, goods_lost)
plt.show()
plt.plot(xs, raids)
plt.show()
plt.plot(xs, merchant_reserve)
plt.plot(xs, city_reserve)
plt.show()
plt.plot(xs, loans)
plt.show()

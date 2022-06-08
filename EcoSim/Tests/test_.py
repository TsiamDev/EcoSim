# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 16:37:29 2022

@author: Perhaps
"""
from EcoSim.Enums.enums import *
from EcoSim import Merchant, City

def test_create_City():
    c = City.City(0, [1, 5, 5], Consumption_Policy.EXPORT, 1000)

def test_create_Merchant():
    c = City.City(0, [1, 5, 5], Consumption_Policy.EXPORT, 1000)
    m = Merchant.Merchant(1, c)

#"""    
if __name__ == "__main__":
    #test_create_Merchant()
    test_create_City()
#"""  
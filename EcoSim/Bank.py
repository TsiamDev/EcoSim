# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 14:56:38 2022

@author: TsiamDev
"""

class Bank:
    def __init__(self):
        self.reserve = 500000
        self.loans = {}
        
    def Loan(self, target, amnt):
        if self.reserve >= amnt:
            if target in self.loans:
                self.loans[target] = self.loans[target] + amnt
            else:
                self.loans[target] = amnt
            self.reserve = self.reserve - amnt
            return True
        else:
            print("Bank does not have enough reserves for this loan!")
            return False

    def Payment(self, target, amnt):
        if target in self.loans:
            self.loans[target] = self.loans[target] - amnt
            self.reserve = self.reserve + amnt
        else:
            print(target, " has no loan to repay!")
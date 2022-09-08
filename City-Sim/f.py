# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 01:18:29 2022

@author: TsiamDev
"""
import os
import time

def d2(q, wb_q):
    print(os.getpid(), flush=True)
    print(q.get(True), flush=True)
    wb_q.put("Bye")

def d(q):
    print(os.getpid(), flush=True)
    print(q.get(True), flush=True)
    

def f(q):
    #time.sleep(3)
    print(os.getpid(), "working")
    while True:
        #print(os.getpid())
        try:
            print(q.get(False))
        except:
            print("Empty Q")
            break
        #time.sleep(1/5)
       

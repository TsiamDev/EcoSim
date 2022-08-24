# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 01:14:17 2022

@author: TsiamDev
"""

import multiprocessing as mp
import time
import os

from f import f, d, d2

def start_reader_procs(qq, num_of_reader_procs):
    """Start the reader processes and return all in a list to the caller"""
    all_reader_procs = list()
    for ii in range(0, num_of_reader_procs):
        ### reader_p() reads from qq as a separate process...
        ###    you can spawn as many reader_p() as you like
        ###    however, there is usually a point of diminishing returns
        reader_p = Process(target=reader_proc, args=((qq),))
        reader_p.daemon = True
        reader_p.start()  # Launch reader_p() as another proc

        all_reader_procs.append(reader_p)

    return all_reader_procs

def d2(q, wb_q):
    global nums
    nums = [1, 2, 3, 4, 5, 6]
    print(os.getpid(), flush=True)
    i, num = q.get(True)
    print(i, flush=True)
    #wb_q.put((i, num+1))
    nums[i] = num+1
    
def wb_Consumer(wb_q, _nums):
    #global nums
    #nums = _nums
    i, num = wb_q.get()
    #print(i, num, flush=True)
    nums[i] = num

def main(nums):
    

    #mp.set_start_method('spawn')
    #global nums
    q = mp.Queue()
    wb_q = mp.Queue()
    #pool = mp.Pool(8)#, f, (q,))
    #with mp.Pool(8, d, (q,)) as pool:
    
    #wb_proc = mp.Process(target=wb_Consumer, args=(wb_q,nums))
    #wb_proc.start()
    with mp.Pool(6, d2, (q, wb_q)) as pool:
        while True:
            #pool.map(d, range(0, 100))
            #for i in range(0, 14):
            #q.put("Hello")
            for i in range(0, len(nums)):
                q.put((i, nums[i]))
            time.sleep(1)
            print(q.qsize())
            """
            if wb_q.empty:
                break
            print(wb_q.get())
            """
    #wb_proc.join()       
    #print("1")
    #for i in range(0, 1000):
    #    q.put(i)
    #print(q.qsize())
    #q.close()
    #time.sleep(1./12)
    #pool.close()
            
    #pool.join()
    print(nums)

if __name__ == "__main__":
    #mp.set_start_method('spawn')
    #global nums
    manager = mp.Manager()
    nums = manager.list([1, 2, 3, 4, 5, 6])
    main(nums)
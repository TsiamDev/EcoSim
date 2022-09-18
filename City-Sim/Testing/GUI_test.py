# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 22:32:55 2022

@author: TsiamDev
"""

import pygame, sys, random
#from collections import deque

def Draw_Line_Graph():
    global pygame, window, surface
    
    
    background_colour = (255,255,255)
    
    color = (176, 73, 0)
    blip = (24, 58, 55)
    bg = (243, 255, 185)
    closed = False
    
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("City Population vs Days passed", 1, (0,0,0))
    days_label = myfont.render("Days", 1, (0,0,0))
    pop_label = myfont.render("Population", 1, (0,0,0))
    pop_label = pygame.transform.rotate(pop_label, 90)


    off = 50
    
    x_ls = []
    y_ls = []
    amnt_ls = []
    #points = deque([(0,50), (50, 40), (100, 160), (150, 20)])
    #points = [(x + off, y + off) for x in range(0, 400-25, 25) for y in range(0, 400-25, 25)]
    x = off
    y = off
    w = h = 400
    points = []
    days_ls = []
    amnt_ls.append(myfont.render(str(0), 1, (0,0,0)))
    #days_ls.append(myfont.render(str(0), 1, (0,0,0)))
    for i in range(0, 15):
        points.append((x, random.randint(y, h)))
        x_ls.append(x)
        y_ls.append(y-25)
        amnt_ls.append(myfont.render(str(x), 1, (0,0,0)))
        days_ls.append(myfont.render(str(i), 1, (0,0,0)))
        x += 25
        y += 25
    amnt_ls.reverse()
    d = [x for x in range(off, h+1, 25)]
    f = [x for x in range(off, h+1, 25)]
    xs = []
    for x in range(0, len(d)):
        xs.append((f[x], off))
        xs.append((f[x], h))
    
    ys = []
    for y in range(0, len(d)):
        ys.append((off, f[y]))
        ys.append((w, f[y]))
    
    #points.rotate(1)
    #print(off)
    pygame.draw.rect(surface, bg, (off, off, w-off, h-off))
    #surface.blit(img, (0,0))
    for l in range(0, len(xs)-1, 2):
        pygame.draw.lines(surface, (0, 0, 0), closed, (xs[l], xs[l+1]), 2)
        pygame.draw.lines(surface, (0, 0, 0), closed, (ys[l], ys[l+1]), 2)
    
    
    for i in range(0, len(x_ls)):
        surface.blit(amnt_ls[i], (15, y_ls[i]+15))
        surface.blit(days_ls[i], (x_ls[i], h))
    surface.blit(label, (w/2 - 120, 12))
    surface.blit(pop_label, (-5, h/2))
    surface.blit(days_label, (w/2, h + 15))
    
    
    pygame.draw.lines(surface, color, closed, points, 3)
    for p in points:
        pygame.draw.circle(surface, blip, p, 3)
    window.fill(background_colour)
    window.blit(surface, (50, 50))
    
    window = pygame.transform.smoothscale(surface, (500, 500))
    surface.fill((255, 255, 255))
    surface.blit(window, (50, 50))
    
    
if __name__ == "__main__":
    global window, surface, pygame
    pygame.init()
    (width, height) = (500, 500)
    surface = pygame.display.set_mode((width, height))
    window = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('Tutorial 1')
   
    #lines_points = deque(lines_points)
    running = True
    while running:
        
        Draw_Line_Graph()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
                
   
        pygame.display.flip()
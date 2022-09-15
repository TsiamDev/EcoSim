# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 22:32:55 2022

@author: TsiamDev
"""

import pygame, sys
from collections import deque

if __name__ == "__main__":
    background_colour = (255,255,255)
    (width, height) = (500, 500)
    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Tutorial 1')
    
    img = pygame.image.load('background.png')
    
    color = (53, 88, 52)
    blip = (255, 82, 27)
    bg = (64, 37, 17)
    closed = False
    
    points = deque([(0,50), (10, 40), (20, 60), (30, 20)])
    
    running = True
    while running:
        surface.fill(background_colour)
        #points.rotate(1)
        pygame.draw.rect(surface, bg, (0,0, 400, 400))
        #surface.blit(img, (0,0))
        pygame.draw.lines(surface, color, closed, points, 5)
        for p in points:
            pygame.draw.circle(surface, blip, p, 4)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
                
   
        pygame.display.flip()
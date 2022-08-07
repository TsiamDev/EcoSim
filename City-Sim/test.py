# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 14:07:50 2022

@author: TsiamDev
"""

import random
from PIL import Image
import numpy as np
#import scipy.misc as smp

# import pygame module in this program
import pygame
import time
import events


from Construct import Construct
from Const import CONST
from Zone import Zone


# Zone lists
unexplored_zones = {}
zones = []

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
brown = (255, 248, 220)
red = (255, 0, 0)
gray = (128, 128, 128)

grass_col = (86, 125, 70)

# init ground
# assigning values to X and Y variable
X = Y = 700
N = 300
road_width = 15

# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((X, Y ))

# Create a 1024x1024x3 array of 8 bit unsigned integers
data = np.zeros( (X,Y,3), dtype=np.uint8 )

r = [[random.randint(0, 255) for i in range(N)] for j in range(N)]
g = [[random.randint(0, 255) for i in range(N)] for j in range(N)]
b = [[random.randint(0, 255) for i in range(N)] for j in range(N)]

#data[15:N+15,15:N+15,0] = r
data[15:N+15,15:N+15,1] = g
#data[15:N+15,15:N+15,2] = b
rect = pygame.draw.rect(display_surface, black, (15, 15, N+15, N+15))
#unexplored_zones.append(Zone(0, rect))
zones.append(Zone(3, rect, 1))

#data[512,512] = [254,0,0]       # Makes the middle pixel red
#data[512,513] = [0,0,255]       # Makes the next pixel blue

#img = Image.fromarray ( data )       # Create a PIL image
#img.show()                      # View in default viewer

  
# activate the pygame library .
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()
  

  

  

  
# set the pygame window name
pygame.display.set_caption('Image')
  

#init tractor
x = y = 15
tractor_width = 15
#tractor = pygame.Rect(x, y, tractor_width, tractor_width)
tractor_img = pygame.image.load('tractor.jpg')
tractor_img = pygame.transform.scale(tractor_img, (tractor_width, tractor_width))

lst = [[(300, 15 + tractor_width * i), (15, 15 + tractor_width * (i+1))] for i in range(0, 21, 2)]
waypoints = [item for sublist in lst for item in sublist]
#waypoints = [(300, 15 + tractor_width), (15, 15 + 2*tractor_width), (300, 15 + 3*tractor_width)]

def move_tractor4(tr_rect):
    global x, y, waypoints, move_right, tractor_width, tractor_img
    
    if len(waypoints) > 0:
        #move right
        if move_right == True:
            x = x + 1
        elif move_right == False:
            x = x - 1
        #else:
        #    print("dont move on <x>")
            
        #print(tr_rect)
        if tr_rect.colliderect(right_expz):
            print("right col")
            #move down
            y = y + 1
            move_right = None
            
            #start moving left once you've reached target y
            if waypoints[0][1] < y:
                move_right = False
                x = 300
                del waypoints[0]
                
            
        if tr_rect.colliderect(left_expz):
            #move down
            y = y + 1
            move_right = None
            
            #start moving right once you've reached target y
            if waypoints[0][1] < y:
                move_right = True
                x = 15
                del waypoints[0]
                
""" older versions
def move_tractor3(tractor):
    global x, y, waypoints, move_right, tractor_width
    
    if len(waypoints) > 0:
        #move right
        if move_right == True:
            x = x + 1
        elif move_right == False:
            x = x - 1
        else:
            print("dont move on <x>")
            
        if tractor.colliderect(right_expz):
            print("right col")
            #move down
            y = y + 1
            move_right = None
            
            #start moving left once you've reached target y
            if waypoints[0][1] < y:
                move_right = False
                x = 300
                del waypoints[0]
                
            
        if tractor.colliderect(left_expz):
            #move down
            y = y + 1
            move_right = None
            
            #start moving left once you've reached target y
            if waypoints[0][1] < y:
                move_right = True
                x = 15
                del waypoints[0]
                
        print(x, y)
            
            
    return pygame.Rect(x, y, tractor_width, tractor_width)

def move_tractor2(tractor):
    global waypoints, x, y, move_right
    
    if len(waypoints) > 0:
        #move right
        if move_right:
            x = x + 1
        else:
            x = x - 1
            
        if waypoints[0][0] <= x:
            #move down until you reach the target y
            y = y + 1
            if waypoints[0][1] >= y:
                # move left
                move_right = False
            #y = y + 1
            #if waypoints[0][1] <= y:
                
                # waypoint reached
                #del waypoints[0]
    
    return pygame.Rect(x, y, tractor_width, tractor_width)

def move_tractor(tractor):
    global x, y, top_expz, right_expz, left_expz, bot_expz, tractor_it, tractor_width
    x = x + 1
    #y = y + 1
    if tractor.colliderect(right_expz):
        #y = y + 1 + tractor_it * tractor_width
        y = y + tractor_width
        x = x - 1 + tractor_it * tractor_width
        print("right")
    
    if tractor.colliderect(bot_expz):
        x = x - 2 + tractor_it * tractor_width
        print("bot")
    
    if tractor.colliderect(left_expz):
        y = y - 1 + tractor_it * tractor_width
        x = x - 1 + tractor_it * tractor_width
        print("left")
        
        if tractor.colliderect(top_expz):
            x = x + 1 + tractor_it * tractor_width
            print("top")
        
    if x < 15:
        x = 14
    
    if x > 300:
        x = 301
        
    if y < 15:
        y = 14
        
    if y > 300:
        y = 301
        
    if x == 14 and y == 14:
        tractor_it = tractor_it + 1
    
    #print(x, y)
        
    return pygame.Rect(x, y, tractor_width, tractor_width)
"""

def fertilize():
    global data, x, y, tractor_width
    data[x:x+tractor_width, y:y+tractor_width] = (0, 0, 255)

def cultivate():
    global data, x, y, tractor_width
    r = [[random.randint(70, 83) for i in range(y, y+tractor_width)] for j in range(y, y+tractor_width)]
    g = [[random.randint(45, 50) for i in range(y, y+tractor_width)] for j in range(y, y+tractor_width)]
    #r = random.randint(70, 83)
    #g = random.randint(45, 50)
    data[x:x+tractor_width, y:y+tractor_width, 0] = r#(r, g, 0)
    data[x:x+tractor_width, y:y+tractor_width, 1] = g#(r, g, 0)

#river
#river_data = np.zeros( (X,Y,3), dtype=np.uint8 )

river_H = 30

river_W = 2*N+6*road_width

r = [[random.randint(0, 25) for i in range(river_H)] for j in range(river_W)]
g = [[random.randint(0, 50) for i in range(river_H)] for j in range(river_W)]
b = [[random.randint(100, 255) for i in range(river_H)] for j in range(river_W)]

data[0:river_W, (N+river_H):(N+60), 0] = r
data[0:river_W, (N+river_H):(N+60), 1] = g
data[0:river_W, (N+river_H):(N+60), 2] = b

def move_river():
    global data, river_W
    
    data[0:river_W, (N+30):(N+60), :] = np.roll(data[0:river_W, (N+30):(N+60), :], 1, axis=0)

#expansion zones
font = pygame.font.SysFont("monospace", 15)
label = font.render("Expansion zone", 1, blue)

def Display_Roads():
    global display_surface, brown, gray, river_H, unexplored_zones
    #left expansion zone
    left_expz = pygame.draw.rect(display_surface, brown ,(0, 0, 15, 330))
    #display_surface.blit(label,(0, 15))
    
    #bottom expansion zone
    bot_expz = pygame.draw.rect(display_surface, brown ,(0, 315, 330, 15))
    #display_surface.blit(label,(15, 315))
    
    #right expansion zone
    right_expz = pygame.draw.rect(display_surface, brown ,(315, 15, 15, 300))
    #display_surface.blit(label,(0, 300))
    
    #top expansion zone
    top_expz = pygame.draw.rect(display_surface, brown ,(0, 0, 330, 15))
    #display_surface.blit(label,(0, 300))   

    return left_expz, bot_expz, right_expz, top_expz

    
def Draw_Explored_Zones():
    global data, display_surface, zones, N
    
    for zone in zones:
    
        if zone.type == CONST.types['FIELD']:
            r = zone.rect
            # update the field
            #data[r.topleft:r.bottomleft, r.topright:r.bottomright] =
        elif zone.type == CONST.types['PROD_BUILDING']:
            #draw the building
            building_img = pygame.image.load('barn_silo.png')
            building_img = pygame.transform.scale(building_img, (N, N))
            bi_rect = building_img.get_rect()
            bi_rect = bi_rect.move((zone.rect.topleft))
            display_surface.blit(building_img, bi_rect)
    

def Draw_Unexplored_Zones():
    global unexplored_zones, display_surface, gray, label
    
    for key, uz in unexplored_zones.items():
        pygame.draw.rect(display_surface,gray, uz.rect)
        label_rect = label.get_rect(center=(uz.rect.center))
        display_surface.blit(label, label_rect)
        #label_rect = label.get_rect(center=((3*N+2*road_width)/2 + river_H + road_width, 330/2))
        #display_surface.blit(label, label_rect)
        
        #label_rect = label.get_rect(center=((N+road_width)/2, 1040/2))
        #display_surface.blit(label, label_rect)
        
        #label_rect = label.get_rect(center=((3*N+road_width)/2 + river_H + road_width, 1040/2))
        #display_surface.blit(label, label_rect)


#init unexplored zones
#if len(unexplored_zones) > 0:
zone_W = N+2*road_width
zone_H = N+2*road_width
exp_z_len = len(unexplored_zones)
rng = range(0, exp_z_len)

if len(unexplored_zones) == 0:
    rect0 = pygame.draw.rect(display_surface, gray, (330+river_H, 0, zone_W, zone_H))
    rect1 = pygame.draw.rect(display_surface, gray, (0, 330+river_H, zone_W, zone_H))
    rect2 = pygame.draw.rect(display_surface, gray, (330+river_H, 330+river_H, zone_W, zone_H))

    unexplored_zones[0] = Zone(0, rect0)
    unexplored_zones[1] = Zone(1, rect1)
    unexplored_zones[2] = Zone(2, rect2)

move_right = True

# infinite loop
while True :
  
    # clear the screen
    display_surface.fill(black)
  
    
  
    
  
    move_river()  
  
    # copying the image surface object
    # to the display surface object at
    # (0, 0) coordinate.
    #display_surface.blit_array(data, (0, 0))
    
    #Update the initial zone and the river
    pygame.surfarray.blit_array( display_surface, data )
    #Update the explored Zones
    Draw_Unexplored_Zones()
    Draw_Explored_Zones()
    
    
    
    #"""
    
    # draw the unexplored zone rectangles
    left_expz, bot_expz, right_expz, top_expz = Display_Roads()
    

    
    
    
    
    
    
    
    # draw the tractor and move the tractor
    #tractor = pygame.draw.rect(display_surface, (0, 255, 0), tractor)
    #tractor_img = pygame.transform.flip(tractor_img, True, False)
    tr_rect = tractor_img.get_rect()
    tr_rect = tr_rect.move((x, y))
    #print(tr_rect)
    display_surface.blit(tractor_img, tr_rect)#(x, y))#, (15, 15))
    #display_surface.blit()
    
    #fertilize()
    cultivate()
    
    #tractor = move_tractor3(tractor)
    move_tractor4(tr_rect)
  
    #"""
  
    
  
    # Event loop
    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get() :
  
        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT :
  
            # deactivates the pygame library
            pygame.quit()
  
            # quit the program.
            quit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            #if pygame.Rect(0,15,15,300).collidepoint(pygame.mouse.get_pos()):
            
                
            
            # Explore clicked zone
            for key, ez in unexplored_zones.items():
                if ez.rect.collidepoint(pygame.mouse.get_pos()):                    
                    print("expansion zone " + str(key) + " clicked")
                    unexplored_zones[key].explore()
                    zones.append(unexplored_zones[key])
            
                    if key in unexplored_zones.keys():
                        del unexplored_zones[key]
                    break
  
    #Draw the surface object to the screen.  
    pygame.display.update() 
        
    time.sleep(1./500)
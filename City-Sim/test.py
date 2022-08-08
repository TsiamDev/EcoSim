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
import pygame_menu
import time
import sys
import copy

from Construct import Construct
from Const import CONST
from Zone import Zone
from Tractor import Tractor


def move_river():
    global data, river_W
    
    data[0:river_W, (N+30):(N+60), :] = np.roll(data[0:river_W, (N+30):(N+60), :], 1, axis=0)



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
    global data, display_surface, zones, N, road_width
    
    for zone in zones:
    
        if zone.type == CONST.types['FIELD']:
            if zone.field.has_init == False:
                rect = zone.rect
                # update the field
                #r = [[random.randint(0, 255) for i in range(N)] for j in range(N)]
                g = [[random.randint(0, 255) for i in range(N)] for j in range(N)]
                #b = [[random.randint(0, 255) for i in range(N)] for j in range(N)]
    
                #data[15:N+15,15:N+15,0] = r
                #data[15:N+15,15:N+15,1] = g
                #data[15:N+15,15:N+15,2] = b
                print(rect.topleft)
                print(rect.bottomleft)
                print(rect.topright)
                print(rect.bottomright)
                #data[rect.topleft[0]:(rect.topright[0] - rect.topleft[0]), rect.topright[1]:(rect.bottomright[1] - rect.topright[1]), 1] = g
                data[rect.topleft[0]:(rect.topright[0]), rect.topright[1]:(rect.bottomright[1]), 1] = g
                
                zone.field.has_init = True
        elif zone.type == CONST.types['BARN_SILO']:
            #draw the building
            building_img = pygame.image.load('barn_silo.png')
            building_img = pygame.transform.scale(building_img, (N, N))
            bi_rect = building_img.get_rect()
            bi_rect = bi_rect.move((zone.rect.topleft))
            display_surface.blit(building_img, bi_rect)
    

def Draw_Unexplored_Zones():
    global unexplored_zones, display_surface, gray, label
    
    for key, uz in unexplored_zones.items():
        pygame.draw.rect(display_surface, gray, uz.rect)
        label_rect = label.get_rect(center=(uz.rect.center))
        display_surface.blit(label, label_rect)


# Player Action Buttons - Crude GUI
def Draw_Action_Buttons():
    global displlay_surface
    
    cultivate_btn = pygame.draw.rect(display_surface, brown ,(X-50, 0, 50, 50))
    label_rect = label.get_rect(center=(cultivate_btn.center))
    display_surface.blit(label, label_rect)


""""""""""""""""""""""""""""""""""" GUI """

#import sys

#from Test import Loop as loop

def on_resize() -> None:
    """
    Function checked if the window is resized.
    """
    global display_surface
    window_size = display_surface.get_size()
    new_w, new_h = 0.75 * window_size[0], 0.7 * window_size[1]
    if menu.is_enabled:
        menu.resize(new_w, new_h)
        
    if plant_menu.is_enabled:
        plant_menu.resize(new_w, new_h)
    print(f'New menu size: {menu.get_size()}')
    
def start_sim():
    global running
    
    running = False
    #menu.disable()

def Main_Menu():
    global display_surface, menu, plant_menu, running, pygame
    
    WINDOW_SIZE = []
    WINDOW_SIZE.append(700)
    WINDOW_SIZE.append(700)
    
    display_surface = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]), pygame.RESIZABLE)
    pygame.display.set_caption("Pasture Managerv0.01")
    
    menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        theme=pygame_menu.themes.THEME_BLUE,
        title='Welcome',
        width=WINDOW_SIZE[0] * 0.75
    )
    
    plant_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        theme=pygame_menu.themes.THEME_BLUE,
        title='Plants',
        width=WINDOW_SIZE[0] * 0.75
    )
    
    
    
    #My plants Menu
    #show plant img
    plant_menu.add.image('barn_silo.png', align=pygame_menu.locals.ALIGN_RIGHT)
    #show sliders for tolerance levels
    i = [i for i in range(0, 256)]
    plant_menu.add.range_slider('heat tolerance', default=[i[0], i[-1]], range_values=i, increment=1)
    plant_menu.add.range_slider('% of water tolerance', default=[i[0], i[-1]], range_values=i, increment=1)
    plant_menu.add.range_slider('PH tolerance', default=[i[0], i[-1]], range_values=i, increment=1)
    #TODO:
        #save changes
        #add selectable image
    
    
    
    #Main menu
    menu.add.label('Resize the window!')
    user_name = menu.add.text_input('Name: ', default='John Doe', maxchar=10)
    menu.add.selector('Difficulty: ', [('Easy', 1), ('Medium', 2), ('Hard', 3)])
    #pg = {'pg':pg}
    menu.add.button('Start', lambda: start_sim() )
    menu.add.button('My Plants', plant_menu)
    #menu.add.button('Quit', pygame_menu.events.EXIT) #restarts kernel
    menu.enable()
    on_resize()  # Set initial size
    
    #if __name__ == '__main__':
    running = True
    while running:  
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                break
    
            if event.type == pygame.VIDEORESIZE:
                # Update the surface
                display_surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                # Call the menu event
                on_resize()
    
        if running == True:
            # Draw the menu
            display_surface.fill((25, 0, 50))
            
            menu.update(events)
            menu.draw(display_surface)
    
            pygame.display.flip()
        
    pygame.display.quit()
    pygame.quit()
    #sys.exit()
""""""""""""""""""""""""""""""""""""""

pygame.init()
Main_Menu()

#def Loop(pg):
#global unexplored_zones, zones, white, black, blue, brown, red, gray, X, Y, N, road_width, display_surface, data, pygame
#pygame = pg

pygame.init()

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
#grass_col = (86, 125, 70)

# init ground
# assigning values to X and Y variable
X = Y = 750
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
zones[0].field.has_init = True

#data[512,512] = [254,0,0]       # Makes the middle pixel red
#data[512,513] = [0,0,255]       # Makes the next pixel blue

#img = Image.fromarray ( data )       # Create a PIL image
#img.show()                      # View in default viewer

  
# activate the pygame library .
# initiate pygame and give permission
# to use pygame's functionality.
#pygame.init()
  
# set the pygame window name
pygame.display.set_caption('City-Sim')
  

#init tractor
x = y = 15
tractor = Tractor(x, y, pygame)


lst = [[(300, 15 + tractor.width * i), (15, 15 + tractor.width * (i+1))] for i in range(0, 21, 2)]
waypoints = [item for sublist in lst for item in sublist]
#waypoints = [(300, 15 + tractor_width), (15, 15 + 2*tractor_width), (300, 15 + 3*tractor_width)]



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

#expansion zones
font = pygame.font.SysFont("monospace", 15)
label = font.render("Expansion zone", 1, blue)

#init unexplored zones
#if len(unexplored_zones) > 0:
zone_W = N#+2*road_width
zone_H = N#+2*road_width
exp_z_len = len(unexplored_zones)
rng = range(0, exp_z_len)

if len(unexplored_zones) == 0:
    rect0 = pygame.draw.rect(display_surface, gray, (330+river_H+road_width, 15, zone_W, zone_H))
    rect1 = pygame.draw.rect(display_surface, gray, (15, 330+river_H+road_width, zone_W, zone_H))
    rect2 = pygame.draw.rect(display_surface, gray, (330+river_H+road_width, 330+river_H+road_width, zone_W, zone_H))

    unexplored_zones[0] = Zone(0, rect0)
    unexplored_zones[1] = Zone(1, rect1)
    unexplored_zones[2] = Zone(2, rect2)

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
    

    
    Draw_Action_Buttons()
    
    
    
    
    
    # draw the tractor and move the tractor
    #tractor = pygame.draw.rect(display_surface, (0, 255, 0), tractor)
    #tractor_img = pygame.transform.flip(tractor_img, True, False)
    tr_rect = tractor.img.get_rect()
    tr_rect = tr_rect.move((tractor.x, tractor.y))
    #print(tr_rect)
    display_surface.blit(tractor.img, tr_rect)#(x, y))#, (15, 15))
    #display_surface.blit()
    
    
    # Tractor Action
    #data = tractor.cultivate(data)
    #data = tractor.sow(data)
    data = tractor.fertilize(data)
    #move_tractor(tr_rect)
    tractor.move(waypoints, tr_rect, right_expz, left_expz)
  
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
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            #if pygame.Rect(0,15,15,300).collidepoint(pygame.mouse.get_pos()):
            
            #Player Actions
            #if 
            
            # Explore clicked zone
            for key, ez in unexplored_zones.items():
                if ez.rect.collidepoint(pygame.mouse.get_pos()):                    
                    print("Expanded to zone " + str(key))
                    unexplored_zones[key].explore()
                    zones.append(unexplored_zones[key])
            
                    if key in unexplored_zones.keys():
                        del unexplored_zones[key]
                    break
  
    #Draw the surface object to the screen.  
    pygame.display.update() 
        
    #time.sleep(1./120)
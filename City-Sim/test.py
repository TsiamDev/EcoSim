# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 14:07:50 2022

@author: TsiamDev
"""

import random
#from PIL import Image
import numpy as np
#import scipy.misc as smp

import pygame
import pygame_menu
import time
import sys

import cProfile as profile
from threading import Thread

from Const import CONST, TRACTOR_ACTIONS, OVERLAY, TIME, DISPLAY, WEATHER

from Zone import Zone
from Tractor import Tractor
from Plant import Plant
from effects.Weather import WeatherEffect


def move_river():
    global data, river_W
    
    #circularly shift the river portion of <data>
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
    global data, display_surface, zones, N, road_width, pygame
    
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
            
        elif zone.type == CONST.types['PASTURE']:
            if zone.field.has_init == False:
                #plant the field
                #plant a specific plant based on user input
                #r = [[random.randint(plant.PH_rng[0], plant.PH_rng[1]) for i in range(N)] for j in range(N)]
                #g = [[random.randint(plant.heat_rng[0], plant.heat_rng[1]) for i in range(N)] for j in range(N)]
                #b = [[random.randint(plant.hum_rng[0], plant.hum_rng[1]) for i in range(N)] for j in range(N)]
                
                #temporary
                g = [[random.randint(0, 255) for i in range(N)] for j in range(N)]
                
                rect = zone.rect
                data[rect.topleft[0]:rect.topright[0], rect.topright[1]:rect.bottomright[1], 0] = 0
                data[rect.topleft[0]:rect.topright[0], rect.topright[1]:rect.bottomright[1], 1] = g
                data[rect.topleft[0]:rect.topright[0], rect.topright[1]:rect.bottomright[1], 2] = 0
                
                zone.field.crop_growth[0:DISPLAY.field_w, 0:DISPLAY.field_h, 0] = 0
                zone.field.crop_growth[0:DISPLAY.field_w, 0:DISPLAY.field_h, 1] = g
                zone.field.crop_growth[0:DISPLAY.field_w, 0:DISPLAY.field_h, 2] = 0
                #rect = pygame.draw.rect(display_surface, black, (15, 15, N+15, N+15))
                #unexplored_zones.append(Zone(0, rect))
                #zones.append(Zone(3, rect, 1))
                zone.field.has_init = True
            
            #draw - move the animals
            zone.pasture.animals_act(pygame, display_surface, zone, data)

def Draw_Unexplored_Zones():
    global unexplored_zones, display_surface, gray, label
    
    for key, uz in unexplored_zones.items():
        pygame.draw.rect(display_surface, gray, uz.rect)
        label_rect = label.get_rect(center=(uz.rect.center))
        display_surface.blit(label, label_rect)


# Player Action Buttons - Crude GUI
def Draw_Action_Buttons():
    global display_surface
    
    #buttons
    global cultivate_btn, sow_btn, PH_btn, hum_btn, temp_btn, N_btn, P_btn, K_btn, crop_growth_btn, harvest_btn, water_btn
    
    btn_h = 15
    btn_w = 70
    btn_padding = 2
    
    font = pygame.font.SysFont("monospace", 10)
    
    cultivate_btn = pygame.draw.rect(display_surface, brown ,(X-btn_w, 0, btn_w, btn_h))
    label = font.render("Cultivate", 1, blue)
    label_rect = label.get_rect(center=(cultivate_btn.center))
    display_surface.blit(label, label_rect)

    sow_btn = pygame.draw.rect(display_surface, brown ,(X-btn_w, btn_h + btn_padding, btn_w, btn_h))
    label = font.render("Sow", 1, blue)
    label_rect = label.get_rect(center=(sow_btn.center))
    display_surface.blit(label, label_rect)
    
    PH_btn = pygame.draw.rect(display_surface, brown ,(X-btn_w, 2*btn_h + 2*btn_padding, btn_w, btn_h))
    label = font.render("PH", 1, blue)
    label_rect = label.get_rect(center=(PH_btn.center))
    display_surface.blit(label, label_rect)
    
    temp_btn = pygame.draw.rect(display_surface, brown ,(X-btn_w, 3*btn_h + 3*btn_padding, btn_w, btn_h))
    label = font.render("Temperature", 1, blue)
    label_rect = label.get_rect(center=(temp_btn.center))
    display_surface.blit(label, label_rect)
    
    hum_btn = pygame.draw.rect(display_surface, brown ,(X-btn_w, 4*btn_h + 4*btn_padding, btn_w, btn_h))
    label = font.render("Humidity", 1, blue)
    label_rect = label.get_rect(center=(hum_btn.center))
    display_surface.blit(label, label_rect)
    
    N_btn = pygame.draw.rect(display_surface, brown ,(X-btn_w, 5*btn_h + 5*btn_padding, btn_w, btn_h))
    label = font.render("N", 1, blue)
    label_rect = label.get_rect(center=(N_btn.center))
    display_surface.blit(label, label_rect)
    
    P_btn = pygame.draw.rect(display_surface, brown ,(X-btn_w, 6*btn_h + 6*btn_padding, btn_w, btn_h))
    label = font.render("P", 1, blue)
    label_rect = label.get_rect(center=(P_btn.center))
    display_surface.blit(label, label_rect)
    
    K_btn = pygame.draw.rect(display_surface, brown ,(X-btn_w, 7*btn_h + 7*btn_padding, btn_w, btn_h))
    label = font.render("K", 1, blue)
    label_rect = label.get_rect(center=(K_btn.center))
    display_surface.blit(label, label_rect)
    
    crop_growth_btn = pygame.draw.rect(display_surface, brown ,(X-btn_w, 8*btn_h + 8*btn_padding, btn_w, btn_h))
    label = font.render("Crop Growth", 1, blue)
    label_rect = label.get_rect(center=(crop_growth_btn.center))
    display_surface.blit(label, label_rect)

    harvest_btn = pygame.draw.rect(display_surface, brown ,(X-btn_w, 9*btn_h + 9*btn_padding, btn_w, btn_h))
    label = font.render("Harvest", 1, blue)
    label_rect = label.get_rect(center=(harvest_btn.center))
    display_surface.blit(label, label_rect)
    
    water_btn = pygame.draw.rect(display_surface, brown ,(X-btn_w, 10*btn_h + 10*btn_padding, btn_w, btn_h))
    label = font.render("Water", 1, blue)
    label_rect = label.get_rect(center=(water_btn.center))
    display_surface.blit(label, label_rect)

""""""""""""""""""""""""""""""""""" GUI """
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

#My plants Menu

def get_heat_val(rng):
    global plant, pb
    
    plant.heat_rng = rng
    print(rng)
    
    # the middle point of a line segment is calculated as:
    # (b-a)/2 + a
    #r = (plant.PH_rng[1] - plant.PH_rng[0]) / 2 + plant.PH_rng[1]
    g = (plant.heat_rng[1] - plant.heat_rng[0]) / 2 + plant.heat_rng[0]
    #b = (plant.hum_rng[1] - plant.hum_rng[0]) / 2 + plant.hum_rng[1]
    plant.c = (plant.c[0], int(g), plant.c[2])
    pb.set_background_color(plant.c)
    
def get_hum_val(rng):
    global plant, pb
    
    plant.hum_rng = rng
    print(rng)
    
    # the middle point of a line segment is calculated as:
    # (b-a)/2 + a
    #r = (plant.PH_rng[1] - plant.PH_rng[0]) / 2 + plant.PH_rng[1]
    #g = (plant.heat_rng[1] - plant.heat_rng[0]) / 2 + plant.heat_rng[1]
    b = (plant.hum_rng[1] - plant.hum_rng[0]) / 2 + plant.hum_rng[0]
    plant.c = (plant.c[0], plant.c[1], int(b))
    pb.set_background_color(plant.c)

def get_PH_val(rng):
    global plant, pb
    
    plant.PH_rng = rng
    print(rng)
    
    # the middle point of a line segment is calculated as:
    # (b-a)/2 + a
    r = (plant.PH_rng[1] - plant.PH_rng[0]) / 2 + plant.PH_rng[0]
    #g = (plant.heat_rng[1] - plant.heat_rng[0]) / 2 + plant.heat_rng[1]
    #b = (plant.hum_rng[1] - plant.hum_rng[0]) / 2 + plant.hum_rng[1]
    plant.c = (int(r), plant.c[1], plant.c[2])
    pb.set_background_color(plant.c)

def Main_Menu():
    global display_surface, menu, plant_menu, running, pygame, plant, pb
    
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
        title='My Plants',
        width=WINDOW_SIZE[0] * 0.75
    )
    
    
    
    
    
    #show plant img
    plant_menu.add.image('barn_silo.png', align=pygame_menu.locals.ALIGN_RIGHT)
    #show sliders for tolerance levels
    i = [i for i in range(0, 256)]
    plant_menu.add.range_slider('Heat tolerance', default=[i[0], i[-1]], range_values=i, increment=1, onchange=get_heat_val)
    plant_menu.add.range_slider('Humidity tolerance', default=[i[0], i[-1]], range_values=i, increment=1, onchange=get_hum_val)
    plant_menu.add.range_slider('PH tolerance', default=[i[0], i[-1]], range_values=i, increment=1, onchange=get_PH_val)
    
    #sur = pygame.surface.Surface((15,15))
    #plant_menu.draw.rect(sur, (128, 128, 128), pygame.Rect(0, 0, 15, 15))
    #plant_menu.draw(sur, clear_surface=False)
    #bi = pygame_menu.baseimage.BaseImage('placeholder.png', drawing_mode=pygame_menu.baseimage.IMAGE_MODE_SIMPLE, load_from_file=True)
    #plant_menu.draw(bi.get_surface(), clear_surface=True)
    pb = plant_menu.add.progress_bar('Preview average color of plant', box_background_color=(255, 0, 0),
                                progress_text_enabled=False,)
    plant_menu.add.button('Start', lambda: start_sim() )
    #TODO:
        #save changes
        #add selectable image
    
    
    
    #Main menu
    menu.add.label('Resize the window!')
    user_name = menu.add.text_input('Name: ', default='John Doe', maxchar=10)
    menu.add.selector('Difficulty: ', [('Easy', 1), ('Medium', 2), ('Hard', 3)])
    #pg = {'pg':pg}
    
    menu.add.button('Embark', plant_menu)
    #menu.add.button('Quit', pygame_menu.events.EXIT) #restarts kernel
    menu.enable()
    on_resize()  # Set initial size
    
    #if __name__ == '__main__':
    running = True
    while running:  
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
    
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
        
    #pygame.display.quit()
    #pygame.quit()
    #sys.exit()
""""""""""""""""""""""""""""""""""""""        

def Crop_Growth():
    global zones, time_cnt, data, pygame
    
    time_cnt = time_cnt + 1
    
    if time_cnt > TIME.types['CROP']:
        for z in zones:
            if z.field is not None:
                #crops grow - if <pixel> is planted
                z.field.crop_growth[z.field.is_planted[:, :] == 1] += (5, 0, 0)
                #print(z.field.crop_growth[:, :, 1] > z.field.crop_growth[:, :, 0])
                #print(z.field.crop_growth[:, :, 0])
                z.field.crop_growth[(z.field.is_planted[:, :] == 1) & (z.field.crop_growth[:, :, 1] < z.field.crop_growth[:, :, 0])] -= (10, 0, 0)
                z.field.crop_growth[z.field.crop_growth < 0] = 0
                
                #data[z.rect.topleft[0]:z.rect.topright[0], z.rect.topright[1]:z.rect.bottomright[1], :] = z.field.crop_growth
        time_cnt = 0
    
    pygame.surfarray.blit_array(display_surface, data)
    #return data

def Display_Overlay():
    global display_surface, selected_overlay
    
    data_temp = np.zeros((X, Y, 3), dtype=np.uint8)
    """
    data_PH = np.zeros((X, Y, 3), dtype=np.uint8)
    data_hum = np.zeros((X, Y, 3), dtype=np.uint8)
    data_temp = np.zeros((X, Y, 3), dtype=np.uint8)
    data_N = np.zeros((X, Y, 3), dtype=np.uint8)
    data_P = np.zeros((X, Y, 3), dtype=np.uint8)
    data_K = np.zeros((X, Y, 3), dtype=np.uint8)
    """
    
    #if selected_overlay is None do nothing
    if selected_overlay is not None:
        #clear the screen
        display_surface.fill(black)
        for zone in zones:
            if zone.type is not CONST.types['BARN_SILO']:
                if selected_overlay is OVERLAY.types['PH']:
                    data_temp[zone.rect.topleft[0]:zone.rect.topright[0], zone.rect.topright[1]:zone.rect.bottomright[1], :] = zone.field.PH
                elif selected_overlay is OVERLAY.types['HUM']:
                    data_temp[zone.rect.topleft[0]:zone.rect.topright[0], zone.rect.topright[1]:zone.rect.bottomright[1], :] = zone.field.hum
                elif selected_overlay is OVERLAY.types['TEMP']:
                    data_temp[zone.rect.topleft[0]:zone.rect.topright[0], zone.rect.topright[1]:zone.rect.bottomright[1], :] = zone.field.temp
                elif selected_overlay is OVERLAY.types['N']:
                    data_temp[zone.rect.topleft[0]:zone.rect.topright[0], zone.rect.topright[1]:zone.rect.bottomright[1], :] = zone.field.N
                elif selected_overlay is OVERLAY.types['P']:
                    data_temp[zone.rect.topleft[0]:zone.rect.topright[0], zone.rect.topright[1]:zone.rect.bottomright[1], :] = zone.field.P
                elif selected_overlay is OVERLAY.types['K']:
                    data_temp[zone.rect.topleft[0]:zone.rect.topright[0], zone.rect.topright[1]:zone.rect.bottomright[1], :] = zone.field.K 
                elif selected_overlay is OVERLAY.types['CROP_GROWTH']:
                    data_temp[zone.rect.topleft[0]:zone.rect.topright[0], zone.rect.topright[1]:zone.rect.bottomright[1], :] = zone.field.crop_growth
                    
                pygame.surfarray.blit_array(display_surface, data_temp)

def Weather_Effect_To_Ground():
    global weather_effect, zones, rain_b_inc
    
    if weather_effect.type == WEATHER.types['RAIN']:
        
        for z in zones:
            #print(rain_b_inc)
            #print(z.field.hum[:, :, 2])
            z.field.hum[:, :, 2] += rain_b_inc
            z.field.hum[z.field.hum > 255] = 255

def main():
    global data, selected_overlay
    
    #crops_thread = Thread(target=Crop_Growth, kwargs=data)
    #roads_thread = Thread(target=Display_Roads)
    #buttons_thread = Thread(target=Draw_Action_Buttons)

    running = True

    #kw = {}
    #kw['display_surface'] = display_surface
    #kw['running'] = running
    #snow_thread = Thread(target=Snow.draw, kwargs=kw)
    #snow_thread.start()
    
    #Snow.draw(display_surface)
    
    # infinite loop
    while running :
      
        #roads_thread = Thread(target=Display_Roads)
        #roads_thread.start()
      
        # clear the screen
        display_surface.fill(black)
      
        
      
        Weather_Effect_To_Ground()
      
        move_river()  
        
        #data = Crop_Growth(data)
        Crop_Growth()
        #crops_thread = Thread(target=Crop_Growth)
        #crops_thread.start()
        #Update the initial zone and the river
        pygame.surfarray.blit_array(display_surface, data)
        
        #Update the explored Zones
        Draw_Unexplored_Zones()
        Draw_Explored_Zones()
        
        
  
        
        # draw the unexplored zone rectangles
        #left_expz, bot_expz, right_expz, top_expz = Display_Roads()
        Display_Roads()
             
        # draw the tractor and move the tractor  
        # Tractor Action
        #data = tractor.act(data, waypoints, display_surface, right_expz, left_expz)
        d = tractor.act(data, waypoints, display_surface, plant)
        if d is not None:
            data = d

        # Display Overlay
        Display_Overlay()

        Draw_Action_Buttons()
        #buttons_thread = Thread(target=Draw_Action_Buttons)
        #buttons_thread.start()
      
        weather_effect.draw(display_surface)
      
        #roads_thread.join()
        #buttons_thread.join()  
        #crops_thread.join()
      
        # Event loop
        # iterate over the list of Event objects
        # that was returned by pygame.event.get() method.
        for event in pygame.event.get() :
      
            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT :
                #running = False
                #snow_thread.join()
                
                pygame.display.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if pygame.Rect(0,15,15,300).collidepoint(pygame.mouse.get_pos()):
                
                #Player Actions
                if cultivate_btn.collidepoint(pygame.mouse.get_pos()):
                    tractor.action = TRACTOR_ACTIONS.types['CULTIVATE']
                elif sow_btn.collidepoint(pygame.mouse.get_pos()):
                    tractor.action = TRACTOR_ACTIONS.types['SOW']
                elif water_btn.collidepoint(pygame.mouse.get_pos()):
                    tractor.action = TRACTOR_ACTIONS.types['WATER']
                elif harvest_btn.collidepoint(pygame.mouse.get_pos()):
                    tractor.action = TRACTOR_ACTIONS.types['HARVEST']
                elif PH_btn.collidepoint(pygame.mouse.get_pos()):
                    if selected_overlay == OVERLAY.types['PH']:
                        selected_overlay = None
                    elif selected_overlay == None:
                        selected_overlay = OVERLAY.types['PH']
                elif hum_btn.collidepoint(pygame.mouse.get_pos()):
                    if selected_overlay == OVERLAY.types['HUM']:
                        selected_overlay = None
                    elif selected_overlay == None:
                        selected_overlay = OVERLAY.types['HUM']
                elif temp_btn.collidepoint(pygame.mouse.get_pos()):
                    if selected_overlay == OVERLAY.types['TEMP']:
                        selected_overlay = None
                    elif selected_overlay == None:
                        selected_overlay = OVERLAY.types['TEMP']
                elif N_btn.collidepoint(pygame.mouse.get_pos()):
                    if selected_overlay == OVERLAY.types['N']:
                        selected_overlay = None
                    elif selected_overlay == None:
                        selected_overlay = OVERLAY.types['N']
                elif P_btn.collidepoint(pygame.mouse.get_pos()):
                    if selected_overlay == OVERLAY.types['P']:
                        selected_overlay = None
                    elif selected_overlay == None:
                        selected_overlay = OVERLAY.types['P']
                elif K_btn.collidepoint(pygame.mouse.get_pos()):
                    if selected_overlay == OVERLAY.types['K']:
                        selected_overlay = None
                    elif selected_overlay == None:
                        selected_overlay = OVERLAY.types['K']
                elif crop_growth_btn.collidepoint(pygame.mouse.get_pos()):
                    if selected_overlay == OVERLAY.types['CROP_GROWTH']:
                        selected_overlay = None
                    elif selected_overlay == None:
                        selected_overlay = OVERLAY.types['CROP_GROWTH']
                        
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
            
        time.sleep(1./120)
    
    

if __name__ == "__main__":
    global time_cnt, rain_b_inc
    
    global cultivate_btn, sow_btn, PH_btn, hum_btn, temp_btn, N_btn, P_btn, K_btn, crop_growth_btn, harvest_btn, water_btn
    cultivate_btn = None
    sow_btn = None
    PH_btn = None
    hum_btn = None
    temp_btn = None
    N_btn = None
    P_btn = None
    K_btn = None
    crop_growth_btn = None
    harvest_btn = None
    
    rain_b_inc = [[random.randint(1, 3) for i in range(DISPLAY.field_w)] for j in range(DISPLAY.field_h)]
    
    time_cnt = 0
    
    pygame.init()
    plant = Plant()
    Main_Menu()
    
    print(repr(plant))
    plant.calc_color()
    
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
    
    """ plant initial zone
    #r = [[random.randint(0, 255) for i in range(N)] for j in range(N)]
    g = [[random.randint(0, 255) for i in range(N)] for j in range(N)]
    #b = [[random.randint(0, 255) for i in range(N)] for j in range(N)]
    
    
    #plant a specific plant based on user input
    #r = [[random.randint(plant.PH_rng[0], plant.PH_rng[1]) for i in range(N)] for j in range(N)]
    #g = [[random.randint(plant.heat_rng[0], plant.heat_rng[1]) for i in range(N)] for j in range(N)]
    #b = [[random.randint(plant.hum_rng[0], plant.hum_rng[1]) for i in range(N)] for j in range(N)]
    
    #data[15:N+15,15:N+15,0] = r
    data[15:N+15,15:N+15,1] = g
    #data[15:N+15,15:N+15,2] = b
    """
    rect = pygame.draw.rect(display_surface, black, (road_width, road_width, N, N))
    #unexplored_zones.append(Zone(0, rect))
    zones.append(Zone(3, rect, pygame, CONST.types['FIELD']))
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
    tractor = Tractor(x, y, zones[0], pygame)
    
    
    lst = [[(300, 15 + tractor.width * i), (15, 15 + tractor.width * (i+1))] for i in range(0, 20, 2)]
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
    
        unexplored_zones[0] = Zone(0, rect0, pygame)
        unexplored_zones[1] = Zone(1, rect1, pygame)
        unexplored_zones[2] = Zone(2, rect2, pygame)
    

    #Weather effects
    weather_effect = WeatherEffect(pygame, WEATHER.types['RAIN'])
    
    selected_overlay = None
    
    main()
    #profile.run('main()')
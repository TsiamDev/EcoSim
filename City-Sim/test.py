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
import copy

import cProfile as profile
#from threading import Thread
#import threading

#from multiprocessing import Process
#import multiprocessing as mp
#from multiprocessing.pool import Pool

from Const import CONST, TRACTOR_ACTIONS, OVERLAY, TIME, DISPLAY, WEATHER, TRACTOR_PARAMETERS
from Const import CONSUMPTION_POLICY, CONSTANTS, VIEW

from Zone import Zone
#from Tractor import Tractor
from Plant import Plant
from City import City
from Scout import Scout
from effects.Weather import WeatherEffect
from Visualization import Draw

from networking.Networking import Set_Globals, Set_Tractor_Actions

def move_river(data):
    
    #circularly shift the river portion of <data>
    data[0:DISPLAY.RIVER_W, (DISPLAY.N+30):(DISPLAY.N+60), :] = np.roll(data[0:DISPLAY.RIVER_W, (DISPLAY.N+30):(DISPLAY.N+60), :], 1, axis=0)
    return data


def Display_Roads():
    global display_surface, brown, pygame
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
    global data, display_surface, zones, N, ROAD_WIDTH, pygame
    
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
                
                zone.field.crop_growth[0:DISPLAY.FIELD_W, 0:DISPLAY.FIELD_H, 0] = 0
                zone.field.crop_growth[0:DISPLAY.FIELD_W, 0:DISPLAY.FIELD_H, 1] = g
                zone.field.crop_growth[0:DISPLAY.FIELD_W, 0:DISPLAY.FIELD_H, 2] = 0
                #rect = pygame.draw.rect(display_surface, black, (15, 15, N+15, N+15))
                #unexplored_zones.append(Zone(0, rect))
                #zones.append(Zone(3, rect, 1))
                zone.field.has_init = True
            
            #draw - move the animals
            zone.pasture.animals_act(pygame, display_surface, zone, data)
            
            #draw the shelter
            display_surface.blit(zone.pasture.shelter_img, zone.pasture.shelter_rect)

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
    global cultivate_btn, sow_btn, PH_btn, hum_btn, temp_btn, fertilize_btn
    global N_btn, P_btn, K_btn, crop_growth_btn, harvest_btn, water_btn
    global switch_scene_btn
    
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
    
    fertilize_btn = pygame.draw.rect(display_surface, brown ,(X-btn_w, 11*btn_h + 11*btn_padding, btn_w, btn_h))
    label = font.render("Fertilize N-P-K", 1, blue)
    label_rect = label.get_rect(center=(fertilize_btn.center))
    display_surface.blit(label, label_rect)
    
    switch_scene_btn = pygame.draw.rect(display_surface, brown ,(X-btn_w, 12*btn_h + 12*btn_padding, btn_w, btn_h))
    label = font.render("Switch View", 1, blue)
    label_rect = label.get_rect(center=(switch_scene_btn.center))
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
                if z.field.has_init == True:
                    """
                    #crops grow - if <pixel> is planted
                    #growth_denominator = np.ones((z.rect.width, z.rect.height))
                    #t = np.where(np.logical_and(z.field.PH>=110, z.field.PH<=140))
                    #print(t[0])
                    #growth_denominator = z.field.PH[t]
                    #print(growth_denominator)
                    new_growth = (z.field.N * 0.3 + z.field.P * 0.3 + z.field.K * 0.4) / z.field.PH
                    z.field.crop_growth[z.field.is_planted > 0] += new_growth.astype(int)#(5, 0, 0)
                    #print(z.field.crop_growth[:, :, 1] > z.field.crop_growth[:, :, 0])
                    #print(z.field.crop_growth[:, :, 0])
                    z.field.crop_growth[(z.field.is_planted[:, :] == 1) & (z.field.crop_growth[:, :, 1] < z.field.crop_growth[:, :, 0])] -= (10, 0, 0)
                    z.field.crop_growth[z.field.crop_growth < 0] = 0
                    """
                    #data[z.rect.topleft[0]:z.rect.topright[0], z.rect.topright[1]:z.rect.bottomright[1], :] = z.field.crop_growth
        time_cnt = 0
    
    pygame.surfarray.blit_array(display_surface, data)
    #return data

def Display_Overlay():
    global selected_overlay
    
    
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
        data_temp = np.zeros((X, Y, 3), dtype=np.uint8)
        #clear the screen
        #display_surface.fill(black)
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
                    
                #pygame.surfarray.blit_array(display_surface, data_temp)
        
        return data_temp
    return None

def Weather_Effect_To_Ground_Proc():
    global weather_effect, zones, running
    
    #Weather effects
    #weather_effect = WeatherEffect(pygame, WEATHER.types['RAIN'])
    
    rain_b_inc = np.zeros( (DISPLAY.FIELD_W, DISPLAY.FIELD_H), dtype=np.int32 )
    rain_b_inc += [[random.randint(1, 3) for i in range(DISPLAY.FIELD_W)] for j in range(DISPLAY.FIELD_H)]
    
    
    while running:
    
        if weather_effect.type == WEATHER.types['RAIN']:
            
            for z in zones:
                #print(len(rain_b_inc))
                #print(len(rain_b_inc[0]))
                #print((rain_b_inc[0][0]))
                #print(z.field.hum)
                #z.field.hum[:, :, 2] += rain_b_inc if any(z.field.hum[:, :, 2] < 255) else 255
                z.field.hum[:, :, 2] +=  rain_b_inc
                #z.field.hum += rain_b_inc if z.field.hum[:,:,2] < 255 else 255
                #i = z.field.hum[:,:,2] + rain_b_inc
                #i = z.field.hum[:][:][2] < 255
                #i = z.field.hum[:,:,2] < 255
                #np.where(i, z.field.hum[i] + rain_b_inc , 255)
                
                #z.field.hum[z.field.hum[:, :, 0] > 0] = 0
                #z.field.hum[z.field.hum[:, :, 1] > 0] = 0
                z.field.hum[z.field.hum[:, :, 2] > 255] = 255
        
        time.sleep(1./120)

def Weather_Effect_To_Ground():
    global weather_effect, zones, rain_b_inc
    
    if weather_effect.type == WEATHER.types['RAIN']:
        
        for z in zones:
            #print(len(rain_b_inc))
            #print(len(rain_b_inc[0]))
            #print((rain_b_inc[0][0]))
            #print(z.field.hum)
            #z.field.hum[:, :, 2] += rain_b_inc if any(z.field.hum[:, :, 2] < 255) else 255
            z.field.hum[:, :, 2] +=  rain_b_inc
            #z.field.hum += rain_b_inc if z.field.hum[:,:,2] < 255 else 255
            #i = z.field.hum[:,:,2] + rain_b_inc
            #i = z.field.hum[:][:][2] < 255
            #i = z.field.hum[:,:,2] < 255
            #np.where(i, z.field.hum[i] + rain_b_inc , 255)
            
            #z.field.hum[z.field.hum[:, :, 0] > 0] = 0
            #z.field.hum[z.field.hum[:, :, 1] > 0] = 0
            z.field.hum[z.field.hum[:, :, 2] > 255] = 255
            
    #time.sleep(1./120)
    
def Populate_Tractor_Q(tractor, lst):
    tractor.init_Q(lst)

def Define_Policies(tractor):
    #TODO prompt users to decide which actions the tractors will perform,
    #and in what order
    
    Set_Tractor_Actions(TRACTOR_ACTIONS.types)
    #lst = [TRACTOR_ACTIONS.types['CULTIVATE'], TRACTOR_ACTIONS.types['SOW'], 
    #       TRACTOR_ACTIONS.types['WATER'], TRACTOR_ACTIONS.types['HARVEST']]
    #print(lst)
    
    #lst = Get_Tractor_Actions()
    
    #Populate_Tractor_Q(tractor, lst)
    
def init_worker(_running, _zones, _weather_effect):
    global running, zones, weather_effect

    running = _running
    zones = zones
    weather_effect = weather_effect
    
def main():
    global data, selected_overlay, tractor, display_surface, pygame
    
    global cultivate_btn, sow_btn, PH_btn, hum_btn, temp_btn, fertilize_btn
    global N_btn, P_btn, K_btn, crop_growth_btn, harvest_btn, water_btn
    global switch_scene_btn
    
    global scouts, forests, lakes, cities
    global rain_b_inc
    #crops_thread = Thread(target=Crop_Growth, kwargs=data)
    
    #Define_Policies(tractor)

    rain_b_inc = np.zeros( (DISPLAY.FIELD_W, DISPLAY.FIELD_H), dtype=np.int32 )
    rain_b_inc += [[random.randint(1, 3) for i in range(DISPLAY.FIELD_W)] for j in range(DISPLAY.FIELD_H)]

    running = True
    selected_view = VIEW.types['MAP_VIEW']
    """
    kw = {}
    #kw['display_surface'] = display_surface
    kw['running'] = mp.Value('b', running)
    lst =  mp.Manager().list()
    kw['zones'] = lst#mp.Value(zones)
    #kw['rain_b_inc'] = rain_b_inc
    kw['weather_effect'] = mp.Value('WeatherEffect', weather_effect)
    
    #snow_thread = Thread(target=Snow.draw, kwargs=kw)
    #snow_thread.start()
    
    weather_effects_proc = Process(target=Weather_Effect_To_Ground_Proc, kwargs=kw)
    weather_effects_proc.start()
    #Snow.draw(display_surface)
    """
    active_city = cities[0]
    
    # infinite loop
    while running :
        
        if selected_view == VIEW.types['MAP_VIEW']:
            Draw(display_surface, scouts, lakes, forests, cities)    
        elif selected_view == VIEW.types['CITY_VIEW']:
        
            Weather_Effect_To_Ground()
            d = Display_Overlay()
            if d is not None:
                data = d
                
            data = move_river(data) 
            tractor_img, tractor_rect = active_city.Draw()
            
            #Crop_Growth()
            
            display_surface.fill(black)
            pygame.surfarray.blit_array(display_surface, data)
            display_surface.blit(tractor_img, tractor_rect)
    
            Draw_Unexplored_Zones()
            Draw_Explored_Zones()
            
        Draw_Action_Buttons()

      
        weather_effect.draw(display_surface)
      
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
                """
                if cultivate_btn.collidepoint(pygame.mouse.get_pos()):
                    tractor.action = TRACTOR_ACTIONS.types['CULTIVATE']
                elif sow_btn.collidepoint(pygame.mouse.get_pos()):
                    tractor.action = TRACTOR_ACTIONS.types['SOW']
                elif water_btn.collidepoint(pygame.mouse.get_pos()):
                    tractor.action = TRACTOR_ACTIONS.types['WATER']
                elif harvest_btn.collidepoint(pygame.mouse.get_pos()):
                    tractor.action = TRACTOR_ACTIONS.types['HARVEST']
                elif fertilize_btn.collidepoint(pygame.mouse.get_pos()):
                    tractor.action = TRACTOR_ACTIONS.types['FERTILIZE']
                """
                if PH_btn.collidepoint(pygame.mouse.get_pos()):
                    if selected_overlay == OVERLAY.types['PH']:
                        selected_overlay = None
                    else:#if selected_overlay == None:
                        selected_overlay = OVERLAY.types['PH']
                elif hum_btn.collidepoint(pygame.mouse.get_pos()):
                    if selected_overlay == OVERLAY.types['HUM']:
                        selected_overlay = None
                    else:#if selected_overlay == None:
                        selected_overlay = OVERLAY.types['HUM']
                elif temp_btn.collidepoint(pygame.mouse.get_pos()):
                    if selected_overlay == OVERLAY.types['TEMP']:
                        selected_overlay = None
                    else:#if selected_overlay == None:
                        selected_overlay = OVERLAY.types['TEMP']
                elif N_btn.collidepoint(pygame.mouse.get_pos()):
                    if selected_overlay == OVERLAY.types['N']:
                        selected_overlay = None
                    else:#if selected_overlay == None:
                        selected_overlay = OVERLAY.types['N']
                elif P_btn.collidepoint(pygame.mouse.get_pos()):
                    if selected_overlay == OVERLAY.types['P']:
                        selected_overlay = None
                    else:#if selected_overlay == None:
                        selected_overlay = OVERLAY.types['P']
                elif K_btn.collidepoint(pygame.mouse.get_pos()):
                    if selected_overlay == OVERLAY.types['K']:
                        selected_overlay = None
                    else:#if selected_overlay == None:
                        selected_overlay = OVERLAY.types['K']
                elif crop_growth_btn.collidepoint(pygame.mouse.get_pos()):
                    if selected_overlay == OVERLAY.types['CROP_GROWTH']:
                        selected_overlay = None
                    else:#if selected_overlay == None:
                        selected_overlay = OVERLAY.types['CROP_GROWTH']
                
                if switch_scene_btn.collidepoint(pygame.mouse.get_pos()):
                    if selected_view == VIEW.types['CITY_VIEW']:
                        selected_view = VIEW.types['MAP_VIEW']
                    else:#if selected_view == OVERLAY.types['MAP_VIEW']:
                        selected_view = VIEW.types['CITY_VIEW']
                        
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
    
    #weather_effects_proc.join()

def Load_Images(pygame):
    images = {}
    img = pygame.image.load('tractor.jpg')
    images['tractor_scaled_img'] = pygame.transform.scale(img, (TRACTOR_PARAMETERS.W, TRACTOR_PARAMETERS.H))

    return images

def Initialize():
    #Cities
    coords = []
    centers = []
    
    #Lakes
    lakes = []
    forests = []
    for i in range(0, CONSTANTS.types['CITY_NUM']):
        #Cities
        x = random.randint(0, DISPLAY.X)
        y = random.randint(0, DISPLAY.Y)
        coords.append([x, y])
        centers.append([x + DISPLAY.CITY_W/2, y + DISPLAY.CITY_H/2])
    
    for i in range(0, CONSTANTS.types['LAKES_NUM']):
        #Lakes
        x = random.randint(0, DISPLAY.X)
        y = random.randint(0, DISPLAY.Y)
        lakes.append([x, y])
        
    for i in range(0, CONSTANTS.types['FORESTS_NUM']):
        #Forests
        x = random.randint(0, DISPLAY.X)
        y = random.randint(0, DISPLAY.Y)
        forests.append([x, y])
        
    return coords, centers, lakes, forests

if __name__ == "__main__":
    global time_cnt, rain_b_inc, tractor
    
    global cultivate_btn, sow_btn, PH_btn, hum_btn, temp_btn, fertilize_btn 
    global N_btn, P_btn, K_btn, crop_growth_btn, harvest_btn, water_btn
    global scouts, forests, lakes, cities
    
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
    
    #rain_b_inc = np.zeros( (DISPLAY.FIELD_W, DISPLAY.FIELD_H), dtype=np.int32 )
    #rain_b_inc += [[random.randint(1, 3) for i in range(DISPLAY.FIELD_W)] for j in range(DISPLAY.FIELD_H)]
    
    time_cnt = 0
    
    pygame.init()
    plant = Plant()
    Main_Menu()
    
    #print(repr(plant))
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
    ROAD_WIDTH = 15
    
    # create the display surface object
    # of specific dimension..e(X, Y).
    display_surface = pygame.display.set_mode((X, Y ))
    
    # Create a 1024x1024x3 array of 8 bit unsigned integers
    data = np.zeros( (DISPLAY.X, DISPLAY.Y, 3), dtype=np.uint8 )
    
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
    rect = pygame.draw.rect(display_surface, black, (DISPLAY.ROAD_WIDTH, DISPLAY.ROAD_WIDTH, DISPLAY.N, DISPLAY.N))
    #unexplored_zones.append(Zone(0, rect))
    zones.append(Zone(3, rect, pygame, CONST.types['FIELD']))
    zones[0].field.has_init = True
      
    # set the pygame window name
    pygame.display.set_caption('City-Sim')
      
    #expansion zones
    font = pygame.font.SysFont("monospace", 15)
    label = font.render("Expansion zone", 1, blue)
    
    exp_z_len = len(unexplored_zones)
    rng = range(0, exp_z_len)
    
    if len(unexplored_zones) == 0:
        rect0 = pygame.draw.rect(display_surface, gray, (330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, 15, DISPLAY.ZONE_W, DISPLAY.ZONE_H))
        rect1 = pygame.draw.rect(display_surface, gray, (15, 330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, DISPLAY.ZONE_W, DISPLAY.ZONE_H))
        rect2 = pygame.draw.rect(display_surface, gray, (330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, 330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, DISPLAY.ZONE_W, DISPLAY.ZONE_H))
    
        unexplored_zones[0] = Zone(0, rect0, pygame)
        unexplored_zones[1] = Zone(1, rect1, pygame)
        unexplored_zones[2] = Zone(2, rect2, pygame)
    
    imgs = Load_Images(pygame)
    
    #Init Cities:
    #cities = []
    #cities.append(City(0, [1, 5, 5], CONSUMPTION_POLICY.types['EXPORT'], 1000, unexplored_zones, zones, plant, imgs['tractor_scaled_img']))
    #cities.append(City(1, [5, 1, 5], CONSUMPTION_POLICY.types['EXPORT'], 1000, unexplored_zones, zones, plant, imgs['tractor_scaled_img']))
    #cities.append(City(2, [5, 5, 1], CONSUMPTION_POLICY.types['DOMESTIC_CONS'], 1000, unexplored_zones, zones, plant, imgs['tractor_scaled_img']))
    
    coords, centers, lakes, forests = Initialize()
    #print(coords)
    centered_centers = copy.deepcopy(centers)
    
    cities = []
    cities.append(City(0, [1, 5, 5], CONSUMPTION_POLICY.types['EXPORT'], 1000, coords[0], centers[0], unexplored_zones, zones, plant, imgs['tractor_scaled_img']))
    cities.append(City(1, [5, 1, 5], CONSUMPTION_POLICY.types['EXPORT'], 1000, coords[1], centers[1], unexplored_zones, zones, plant, imgs['tractor_scaled_img']))
    cities.append(City(2, [5, 5, 1], CONSUMPTION_POLICY.types['EXPORT'], 1000, coords[2], centers[2], unexplored_zones, zones, plant, imgs['tractor_scaled_img']))

    scouts = []
    scouts.append(Scout(centered_centers[0], pygame.Rect(coords[0][0] + DISPLAY.CITY_W/2 - DISPLAY.SCOUT_W/2, coords[0][1] + DISPLAY.CITY_H/2 - DISPLAY.SCOUT_H/2, DISPLAY.SCOUT_W, DISPLAY.SCOUT_H)))
    
    #Weather effects
    weather_effect = WeatherEffect(pygame, WEATHER.types['RAIN'])
    
    selected_overlay = None
    
    running = True
     
    main()
    #profile.run('main()')
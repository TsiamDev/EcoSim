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
#import time
import sys
import copy
import os
#from pprint import pprint
import math
import tracemalloc
import linecache

import cProfile as profile
#from threading import Thread
#import threading

#from multiprocessing.managers import SharedMemoryManager
from multiprocessing import Process#, shared_memory, current_process, Pool
import multiprocessing as mp

#from queue import Queue

from Const import CONST, TRACTOR_ACTIONS, OVERLAY, TIME, DISPLAY, WEATHER, TRACTOR_PARAMETERS
from Const import CONSUMPTION_POLICY, CONSTANTS, VIEW, ANIMAL_SIZE, CONSTRUCT_SIZE, DAY

from Zone import Zone
#from Tractor import Tractor
from Plant import Plant
from City import City
from Scout import Scout
from effects.Weather import WeatherEffect
from Visualization import Draw
from MyRect import MyRect
from Animal import Animal
#from  MyMultiprocessing import Weather_Effect_To_Ground_Proc3

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

    
def Init_Explored_Zones(data, zone):
    global display_surface, pygame, images
    
    #for zone in zones:
    
    if zone.type == CONST.types['FIELD']:
        if zone.field.has_init == False:
            rect = pygame.Rect(zone.rect.x, zone.rect.y, DISPLAY.ZONE_W, DISPLAY.ZONE_H)
            # update the field
            #r = [[random.randint(0, 255) for i in range(N)] for j in range(N)]
            g = [[random.randint(0, 255) for i in range(N)] for j in range(N)]
            #b = [[random.randint(0, 255) for i in range(N)] for j in range(N)]

            #data[15:N+15,15:N+15,0] = r
            #data[15:N+15,15:N+15,1] = g
            #data[15:N+15,15:N+15,2] = b
            #print(rect.topleft)
            #print(rect.bottomleft)
            #print(rect.topright)
            #print(rect.bottomright)
            #data[rect.topleft[0]:(rect.topright[0] - rect.topleft[0]), rect.topright[1]:(rect.bottomright[1] - rect.topright[1]), 1] = g
            data[rect.topleft[0]:(rect.topright[0]), rect.topright[1]:(rect.bottomright[1]), 1] = g
            
            zone.field.has_init = True
        """
        elif zone.type == CONST.types['BARN_SILO']:
            #draw the building
            building_img = pygame.image.load('barn_silo.png')
            building_img = pygame.transform.scale(building_img, (N, N))
            bi_rect = building_img.get_rect()
            bi_rect = bi_rect.move((zone.rect.topleft))
            display_surface.blit(building_img, bi_rect)
        """   
    elif zone.type == CONST.types['PASTURE']:
        if zone.field.has_init == False:
            #plant the field
            #plant a specific plant based on user input
            #r = [[random.randint(plant.PH_rng[0], plant.PH_rng[1]) for i in range(N)] for j in range(N)]
            #g = [[random.randint(plant.heat_rng[0], plant.heat_rng[1]) for i in range(N)] for j in range(N)]
            #b = [[random.randint(plant.hum_rng[0], plant.hum_rng[1]) for i in range(N)] for j in range(N)]
            
            #temporary
            g = [[random.randint(0, 255) for i in range(N)] for j in range(N)]
            
            rect = pygame.Rect(zone.rect.x, zone.rect.y, DISPLAY.ZONE_W, DISPLAY.ZONE_H)
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
            
            for i in range(0, zone.pasture.animals_num):
                #create empty object
                #pos = type('pos', (), {})()
                #pos.x = rect.center[0]#random.randint(rect.topleft[0], rect.topright[0])
                #pos.y = rect.center[1]#random.randint(rect.topright[1], rect.bottomright[1])
                
                zone.pasture.animals.append(Animal(zone.pasture._rect, zone.pasture.animal_type))
        
        #draw - move the animals
        #zone.pasture.animals_act(pygame, display_surface, zone, data, images)
        
        #draw the shelter
        #rect = zone.pasture.shelter_rect
        #rect = pygame.Rect(rect.x, rect.y, rect.topright[0]-rect.topleft[0], rect.topright[1]-rect.bottomright[1])
        #display_surface.blit(images[zone.pasture.shelter_img_key], rect)

def Update_Explored_Zones(city):
    for zone in city.zones:
        #print(zone.type, flush=True)
        #if zone.is_explored == True:
        #print("A", flush=True)
        if zone.type == CONST.types['BARN_SILO']:
            #draw the building
            building_img = pygame.image.load('barn_silo.png')
            building_img = pygame.transform.scale(building_img, (N, N))
            bi_rect = building_img.get_rect()
            bi_rect = bi_rect.move((zone.rect.topleft))
            display_surface.blit(building_img, bi_rect)
            
        elif zone.type == CONST.types['PASTURE']:
            
            #if animal_act_timer > TIME.types['ANIMAL_ACT']:
            #print("HERE", flush=True)
            #move the animals
            #zone.pasture.animals_act(zone, city.data)                
            for i in range (0, len(zone.pasture.animals)):
                zone.pasture.animals[i].act(zone, city.data, city)
                #print((zone.pasture.animals[i].rect.x,zone.pasture.animals[i].rect.y))
            #animal_act_timer = 0
            #else:
            #animal_act_timer += 1
    #return city

def Draw_Explored_Zones(zones):
    global display_surface, pygame, images
    #print("EDW")
    for zone in zones:
        if zone.type == CONST.types['BARN_SILO']:
            #draw the building
            building_img = pygame.image.load('barn_silo.png')
            building_img = pygame.transform.scale(building_img, (N, N))
            bi_rect = building_img.get_rect()
            bi_rect = bi_rect.move((zone.rect.topleft))
            display_surface.blit(building_img, bi_rect)
            
        elif zone.type == CONST.types['PASTURE']:
            if zone.is_explored == True:             
                #draw the animals
                #print("MESA")
                for an in zone.pasture.animals:
                    
                    #an.draw_animal(display_surface, images, pygame)
                    
                    #rect = an.img_rect                    
                    #print("MESA AN ", (rect.x, rect.y))
                    #rect = pygame.Rect(rect.x, rect.y, rect.topright[0]-rect.topleft[0], rect.topright[1]-rect.bottomright[1])
                    
                    #rect = pygame.Rect((an.img_rect.x, an.img_rect.y), (ANIMAL_SIZE.types['COW'], ANIMAL_SIZE.types['COW']))
                    display_surface.blit(images[an.img_key], pygame.Rect((an.img_rect.x, an.img_rect.y), (ANIMAL_SIZE.types['COW'], ANIMAL_SIZE.types['COW'])))
                    #pprint(an.img_rect)
                #draw the shelter
                rect = zone.pasture.shelter_rect
                #rect = pygame.Rect(rect.x, rect.y, rect.topright[0]-rect.topleft[0], rect.topright[1]-rect.bottomright[1])
                rect = pygame.Rect((rect.x, rect.y), (CONSTRUCT_SIZE.types['SHELTER'], CONSTRUCT_SIZE.types['SHELTER']))
                display_surface.blit(images[zone.pasture.shelter_img_key], rect)
                
def Draw_Unexplored_Zones(unexplored_zones):
    global display_surface, gray, label, pygame
    
    for key, uz in unexplored_zones.items():
        pygame.draw.rect(display_surface, gray, pygame.Rect(uz.rect.x, uz.rect.y, DISPLAY.ZONE_W, DISPLAY.ZONE_H))
        label_rect = label.get_rect(center=(uz.rect.center))
        display_surface.blit(label, label_rect)


# Player Action Buttons - Crude GUI
def Draw_Action_Buttons():
    global display_surface, font
    
    #buttons
    global cultivate_btn, sow_btn, PH_btn, hum_btn, temp_btn, fertilize_btn
    global N_btn, P_btn, K_btn, crop_growth_btn, harvest_btn, water_btn
    global switch_scene_btn, city_statistics_btn
    
    btn_h = 15
    btn_w = 70
    btn_padding = 2
    
    #font = pygame.font.SysFont("monospace", 10)
    
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
    
    city_statistics_btn = pygame.draw.rect(display_surface, brown ,(X-btn_w, 13*btn_h + 13*btn_padding, btn_w, btn_h))
    label = font.render("City Statistics", 1, blue)
    label_rect = label.get_rect(center=(city_statistics_btn.center))
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
    global plant, transparent_plant_image, plant_img_widget
    
    plant.heat_rng = rng
    #print(rng)
    
    # the middle point of a line segment is calculated as:
    # (b-a)/2 + a
    #r = (plant.PH_rng[1] - plant.PH_rng[0]) / 2 + plant.PH_rng[1]
    g = (plant.heat_rng[1] - plant.heat_rng[0]) / 2 + plant.heat_rng[0]
    #b = (plant.hum_rng[1] - plant.hum_rng[0]) / 2 + plant.hum_rng[1]
    plant.c = (plant.c[0], int(g), plant.c[2])
    
    #Update the colour of the plant
    plant_image = transparent_plant_image.copy()
    w_surface = plant_img_widget.get_surface()
    h = w_surface.get_height()
    w = w_surface.get_width()
    
    rect = np.ones((w, h, 3), dtype=np.int32)
    rect *= plant.c
    
    pygame.surfarray.blit_array(w_surface, rect)
    w_surface.blit(plant_image, (0,0))
    
def get_hum_val(rng):
    global plant, transparent_plant_image, plant_img_widget
    
    plant.hum_rng = rng
    #print(rng)
    
    # the middle point of a line segment is calculated as:
    # (b-a)/2 + a
    #r = (plant.PH_rng[1] - plant.PH_rng[0]) / 2 + plant.PH_rng[1]
    #g = (plant.heat_rng[1] - plant.heat_rng[0]) / 2 + plant.heat_rng[1]
    b = (plant.hum_rng[1] - plant.hum_rng[0]) / 2 + plant.hum_rng[0]
    plant.c = (plant.c[0], plant.c[1], int(b))
    
    #Update the colour of the plant
    plant_image = transparent_plant_image.copy()
    w_surface = plant_img_widget.get_surface()
    h = w_surface.get_height()
    w = w_surface.get_width()
    
    rect = np.ones((w, h, 3), dtype=np.int32)
    rect *= plant.c
    
    pygame.surfarray.blit_array(w_surface, rect)
    w_surface.blit(plant_image, (0,0))

def get_PH_val(rng):
    global plant, transparent_plant_image, plant_img_widget
    
    plant.PH_rng = rng
    #print(rng)
    
    # the middle point of a line segment is calculated as:
    # (b-a)/2 + a
    r = (plant.PH_rng[1] - plant.PH_rng[0]) / 2 + plant.PH_rng[0]
    #g = (plant.heat_rng[1] - plant.heat_rng[0]) / 2 + plant.heat_rng[1]
    #b = (plant.hum_rng[1] - plant.hum_rng[0]) / 2 + plant.hum_rng[1]
    plant.c = (int(r), plant.c[1], plant.c[2])
    
    #Update the colour of the plant
    plant_image = transparent_plant_image.copy()
    w_surface = plant_img_widget.get_surface()
    h = w_surface.get_height()
    w = w_surface.get_width()
    
    rect = np.ones((w, h, 3), dtype=np.int32)
    rect *= plant.c
    
    pygame.surfarray.blit_array(w_surface, rect)
    w_surface.blit(plant_image, (0,0))

def Update_Plant_Img(widget, menu):
    global plant_img_widget
    
    plant_img_widget = widget
    print(widget)
    print(menu)

def Main_Menu():
    global display_surface, menu, plant_menu, running, pygame, plant, font
    
    global transparent_plant_image, plant_image, plant_img_widget
    
    WINDOW_SIZE = []
    WINDOW_SIZE.append(850)
    WINDOW_SIZE.append(850)
    
    display_surface = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]), pygame.RESIZABLE)
    pygame.display.set_caption("Pasture Managerv0.01")
    
    menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.5,
        theme=pygame_menu.themes.THEME_BLUE,
        title='Welcome',
        width=WINDOW_SIZE[0] * 0.75
    )
    
    plant_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.5,
        theme=pygame_menu.themes.THEME_BLUE,
        title='My Plants',
        width=WINDOW_SIZE[0] * 0.8
    )
    
    
    
    
    
    #show plant img
    transparent_plant_image = pygame.image.load('Assets/Pictures/plant2.png')
    transparent_plant_image = pygame.transform.scale(transparent_plant_image, (0.3*764, 0.3*545))
    #plant_menu.add.image('barn_silo.png', align=pygame_menu.locals.ALIGN_RIGHT)
    plant_img_widget = plant_menu.add.image('Assets/Pictures/plant.png', image_id='plant_img_widget', scale=(0.3, 0.3), scale_smooth=True)#, align=pygame_menu.locals.ALIGN_CENTER)
    plant_img_widget.add_draw_callback(Update_Plant_Img)
    
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
    #pb = plant_menu.add.progress_bar('Preview average color of plant', default=50, box_progress_color=(255, 0, 0), progress_text_enabled=False)
    plant_menu.add.button('Start', lambda: start_sim() )
    #TODO save changes
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
    
    FPS = 60 # frames per second setting
    fpsClock = pygame.time.Clock()
    
    #if __name__ == '__main__':
    running = True
    while running:  
        #display_surface.blit(plant_img, (0,0))
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
            #Draw the current FPS on the screen
            Render_Current_FPS(str(int(fpsClock.get_fps())), font)
            menu.draw(display_surface)
    
            pygame.display.flip()
            fpsClock.tick(FPS)
        
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

def Display_Overlay(zones):
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
        data_temp = np.zeros((DISPLAY.X, DISPLAY.Y, 3), dtype=np.uint8)
        #clear the screen
        #display_surface.fill(black)
        for zone in zones:
            if zone.type is not CONST.types['BARN_SILO']:
                #print(zone.rect.topleft, zone.rect.topright)
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
                    #print(range(zone.rect.topleft[0], zone.rect.topright[0]))
                    #print(zone.rect.topleft[0], zone.rect.topright[0], zone.rect.topright[1], zone.rect.bottomright[1])
                    data_temp[zone.rect.topleft[0]:zone.rect.topright[0], zone.rect.topright[1]:zone.rect.bottomright[1], :] = zone.field.crop_growth
                elif selected_overlay is OVERLAY.types['PLANT_FACE']:
                    data_temp[zone.rect.topleft[0]:zone.rect.topright[0], zone.rect.topright[1]:zone.rect.bottomright[1], :] = zone.field.plant_face
                #pygame.surfarray.blit_array(display_surface, data_temp)
        
        return data_temp
    return None

def Weather_Effect_To_Ground(weather_effect, zones, rain_b_inc):    
    if weather_effect.type == WEATHER.types['RAIN']:
        #print(zones)
        #for zi in range(0, len(zones)):
        #arr = []
        #lock.acquire()
        for z in zones:
            #print(len(rain_b_inc))
            #print(len(rain_b_inc[0]))
            #print((rain_b_inc[0][0]))
            #print(z.field.hum)
            #z.field.hum[:, :, 2] += rain_b_inc if any(z.field.hum[:, :, 2] < 255) else 255
            
            #zones[zi].field.hum[zones[zi].field.hum[:, :, 2] + rain_b_inc - 255 >= 0] += rain_b_inc
            #zones[zi].field.hum[:, :, 2] +=  rain_b_inc
            #_parent_zones[zi].field.hum[:, :, 2] +=  rain_b_inc
            z.field.hum[:, :, 2] +=  rain_b_inc
            #zn = z.field.hum[:, :, 2] + rain_b_inc
                
            #z.field.hum += rain_b_inc if z.field.hum[:,:,2] < 255 else 255
            #i = z.field.hum[:,:,2] + rain_b_inc
            #i = z.field.hum[:][:][2] < 255
            #i = z.field.hum[:,:,2] < 255
            #np.where(i, z.field.hum[i] + rain_b_inc , 255)
            
            #z.field.hum[z.field.hum[:, :, 0] > 0] = 0
            #z.field.hum[z.field.hum[:, :, 1] > 0] = 0
            
            #zones[zi].field.hum[zones[zi].field.hum[:, :, 2] > 240] = 240
            #_parent_zones[zi].field.hum[zones[zi].field.hum[:, :, 2] > 240] = 240
            z.field.hum[z.field.hum[:, :, 2] > 240] = 240
            #zn[zn > 240] = 240
            #arr.append(zn)
            
            #print(zones[zi].field.hum)
        #lock.release()
        #return arr
    #return None
    
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

def Render_Current_FPS(text, font):
    global display_surface, blue

    fps_rect = pygame.draw.rect(display_surface, (255, 255, 150), (0, 0, 25, 25))
    #font = pygame.font.SysFont("monospace", 15)
    label = font.render(text, 1, (0, 0, 255))
    label_rect = label.get_rect(center=(fps_rect.center))
    display_surface.blit(label, label_rect)

def Deal_Chunks(num_producers, wb_q, stop_q, rain_b_inc):
    global cities
    producers = []
    indices = []
    lst = []
    print("Starting producers...")
    #chunk_mod = int(math.floor(len(cities) % (num_producers +1)))
    wb_qs = []
    to_background_qs = []
    if num_producers >= len(cities):
        print("num_producers >= len(cities)")
        #assign one city to one process
        for i in range(0, len(cities)):
            to_background_q = mp.Queue()
            wb_q = mp.Queue()
            ind = []
            city_chunk = []
            for k in range(i, i+1):
                ind.append(k)
                city_chunk.append(cities[k])
            print("ind:", ind, " cc:", city_chunk)
            producer = Process(target=Producer, args=[i, ind, city_chunk, wb_q, to_background_q, stop_q, rain_b_inc])
            
            producer.start()
            producers.append(producer)
            
            to_background_qs.append(mp.Queue())
            wb_qs.append(wb_q)
            indices.append(ind)
            lst.append(city_chunk)
            
    else:
        print("num_producers < len(cities)")
        chunk = int(math.floor(len(cities) / num_producers))
        print("chunk:", chunk, flush=True)

        i = 0
        for i in range(0, num_producers - 1): 
            to_background_q = mp.Queue()
            wb_q = mp.Queue()
            ind = []
            start = i*chunk
            end = (i+1)*chunk - 1
            ind.append(start)
            if start != end:
                ind.append(end)
            
            if len(ind) > 1:
                city_chunk = cities[ind[0]:(ind[1]+2)]
            else:
                city_chunk = [cities[ind[0]]]
                
            print("ind: ", ind, " cc: ", city_chunk)
            producer = Process(target=Producer, args=[i, ind, city_chunk, wb_q, to_background_q, stop_q, rain_b_inc])
            
            producer.start()
            producers.append(producer)
            
            to_background_qs.append(to_background_q)
            wb_qs.append(wb_q)
            indices.append(ind)
            lst.append(city_chunk)

        ind = []
        to_background_q = mp.Queue()
        wb_q = mp.Queue()
        start = (i+1)*chunk
        end = (i+2)*chunk
        ind.append(start)
        ind.append(end)
        
        if len(ind) > 1:
            city_chunk = cities[ind[0]:(ind[1]+2)]
        else:
            city_chunk = cities[ind[0]]
        
        producer = Process(target=Producer, args=[i, ind, city_chunk, wb_q, to_background_q, stop_q, rain_b_inc])
        
        producer.start()
        producers.append(producer)
        
        to_background_qs.append(to_background_q)
        wb_qs.append(wb_q)
        indices.append(ind)
        lst.append(city_chunk)
            
    return producers, to_background_qs, wb_qs

def Producer(_id, ind, city_chunk, wb_q, to_background_q, stop_q, rain_b_inc):
    cnt = 0
    FPS = 60
    fps_cnt = 0
    pid = os.getpid()
    print("Producer: ", pid, "ind:", ind, " cc: ", city_chunk, flush=True)
    
    new_city_id = None
    
    day_cnt = 0
    
    while True:
        #print("Producer: ", _id, flush=True)
        #print("Producer:", ind, " cc:", city_chunk)
        #if a city state-update request has been made
        if not to_background_q.empty():
            active_city = to_background_q.get(True)
            print(pid, ind, ": received ", active_city.id, flush=True)
            #the parent process has sent you a city state-update
            #so, update the city
            for ci in range(0, len(city_chunk)):
                #new_city is just an integer here!
                if city_chunk[ci].id == active_city.id:
                    city_chunk[ci] = active_city
                    print(pid, ind, ": has ", active_city.id, flush=True)
                    break
            
            #if not to_background_q.empty():
            new_city_id = to_background_q.get(True)
            #if you were assigned this city, send a city state-update 
            #to the parent process
            found = False
            for ci in range(0, len(city_chunk)):
                #new_city is just an integer here!
                if city_chunk[ci].id == new_city_id:
                    wb_q.put((_id, city_chunk[ci]))
                    print(pid, ind, ": sent ", (_id, city_chunk[ci].id), flush=True)
                    found = True
                    break
            
            #if you don't possess the requested city,
            #you have to notify the parent process
            if found == False:
                wb_q.put((-1, -1))
                
        
        if fps_cnt >= FPS:
            #print(ind)
            #print(len(ind))
            #print("ind[i]:", ind[i])
            #print("i:", i)
            if len(ind) > 1:
                cnt = 0
                for m in range(ind[0], ind[1]):
                    #print(m)
                    if new_city_id is not None:
                        if m == new_city_id:
                            continue
                    Weather_Effect_To_Ground(city_chunk[cnt].weather_effect, city_chunk[cnt].zones, rain_b_inc)
                    Update_Explored_Zones(city_chunk[cnt])
                    city_chunk[cnt].Draw()
                    if day_cnt >= DAY.TICKS_TILL_DAY:
                        city_chunk[cnt].Consume()
                        day_cnt = 0
                    else:
                        day_cnt += 1
                    cnt += 1
            else:
                if new_city_id is not None:
                    if new_city_id != 0:
                        Weather_Effect_To_Ground(city_chunk[0].weather_effect, city_chunk[0].zones, rain_b_inc)
                        Update_Explored_Zones(city_chunk[0])
                        #move river and tractor
                        city_chunk[0].Draw()
                        if day_cnt >= DAY.TICKS_TILL_DAY:
                            city_chunk[0].Consume()
                            day_cnt = 0
                        else:
                            day_cnt += 1
            fps_cnt = 0
        else:
            fps_cnt += 1
        #time.sleep(1./120)
        #print()
        #UNCOMMENT!
        #wb_q.put((ind, city_chunk))
        #print(stop_q.qsize(), flush=True)
        if not stop_q.empty():
            msg = stop_q.get(True)
            print(os.getpid(), " exited with msg ", msg, flush=True)
            #print("Producer: ", cnt)
            return

#def Event_Loop(pygame, consumers, stop_q, wb_q_thread, selected_overlay, selected_view, active_city, city_rects):
    
def display_top(snapshot, key_type='lineno', limit=10):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        print("#%s: %s:%s: %.1f KiB"
              % (index, frame.filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))

def Weather_Effect_To_Ground_Pool(city, rain_b_inc):    
    if city.weather_effect.type == WEATHER.types['RAIN']:
        for z in city.zones:
            z.field.hum[:, :, 2] +=  rain_b_inc
            z.field.hum[z.field.hum[:, :, 2] > 240] = 240

def Update_Cities(args):
    Weather_Effect_To_Ground_Pool(args[0], args[1])

    #cities[ci] = Update_Explored_Zones(cities[ci])
    Update_Explored_Zones(args[0])
    
    return args[0]

"""
def Init_Event_Proc():
    
    while running:
        
        #TODO implement event handling in a separate subprocess
"""   
    
def main():
    global data, selected_overlay, tractor, display_surface, pygame
    
    global cultivate_btn, sow_btn, PH_btn, hum_btn, temp_btn, fertilize_btn
    global N_btn, P_btn, K_btn, crop_growth_btn, harvest_btn, water_btn
    global switch_scene_btn, city_statistics_btn
    
    global scouts, forests, lakes, cities
    global rain_b_inc, images, multiproc_Q
    
    global brown
    
    global animal_act_timer, weather_effect
    animal_act_timer = 0
    #crops_thread = Thread(target=Crop_Growth, kwargs=data)
    
    #Define_Policies(tractor)

    rain_b_inc = np.zeros( (DISPLAY.FIELD_W, DISPLAY.FIELD_H), dtype=np.int32 )
    rain_b_inc += [[random.randint(1, 3) for i in range(DISPLAY.FIELD_W)] for j in range(DISPLAY.FIELD_H)]

    running = True
    selected_view = VIEW.types['CITY_VIEW']
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
    active_city.is_active = True
    city_rects = []
    
    #events_proc = Process(target=Init_Event_Proc).start()
    
    FPS = 60 # frames per second setting
    fpsClock = pygame.time.Clock()
    
    #direction: from the main process to the subprocesses
    #q = mp.Queue()
    #direction: from the subprocesses to the main process
    wb_q = mp.Queue()
    stop_q = mp.Queue()
    #req_upd_q = mp.Queue()
    print("CPUs", mp.cpu_count())
    
    lock = mp.Lock()
    
    num_producers = mp.cpu_count()
    #consumers = Weather_Effect_To_Ground_Proc3(cities, num_producers)
    #print(q_consumers)
    #l = mp.Lock()
    #multiproc_pool = mp.Pool(mp.cpu_count())#, Weather_Effect_To_Ground_Proc, (multiproc_Q, l,))
    #multiproc_pool.start()# weather_effect.type))
    #with mp.Pool(num_producers, City_Consumer, (q, wb_q)) as pool:#, Weather_Effect_To_Ground_Proc2, (multiproc_Q,)) as multiproc_pool:
    #pool.map_async(Q_Consumer6, (q, wb_q))
    
    producers, to_background_qs, wb_qs = Deal_Chunks(num_producers, wb_q, stop_q, rain_b_inc)
    #pool = mp.Pool()
    print(len(to_background_qs))
    print(len(producers))
    print(len(wb_qs))
    
    
    #wbthreads = []
    #DO NOT DO THIS
    #for i in range(0, 5):
        
    #wb_q_thread = Thread(target=Wb_Q_Thread, args=(wb_q, stop_q, lock))
    #wb_q_thread.start()
    
    #wbthreads.append(wb_q_thread)
    
    #event_thread = Thread(target=Event_Loop, args=(pygame, consumers, stop_q, wb_q_thread, selected_overlay, selected_view, active_city, city_rects))
    #event_thread.start()
    #timer_cnt = 0
    
    origin = None
    cur_i = None
    
    active_city_changed = False
    
    plot = False
    
    day_cnt = 0
    
    print("Main loop:", os.getpid())
    # infinite loop
    while running :
        #snapshot1 = tracemalloc.take_snapshot()
        #start_time = pygame.time.get_ticks()
        #clear screen
        display_surface.fill(brown)

        #TODO: enable
        #update the active city
        #Weather_Effect_To_Ground(active_city.weather_effect, active_city.zones, rain_b_inc)
        Update_Explored_Zones(active_city)
        
        if day_cnt >= DAY.TICKS_TILL_DAY:
            active_city.Consume()
            day_cnt = 0
        
        #Update the active_city's pixels (data)
        active_city.Draw()
        d = Display_Overlay(active_city.zones)
        #lock.release()
        if d is not None:
            active_city.data = d
        #tractor_img_key, tractor_rect = active_city.Draw()
        
        #draw map view
        if selected_view == VIEW.types['MAP_VIEW']:            
            city_rects = Draw(display_surface, scouts, lakes, forests, cities)
        #draw active city view
        elif selected_view == VIEW.types['CITY_VIEW']:           
            #If active city has changed, request update from process that
            #has been simulating the particular city
            if active_city_changed == True:
                #push active_city to the background process
                #push the active_city to all children
                for p_i in range(0, num_producers):
                    to_background_qs[p_i].put(active_city)
                    print("Sent ", active_city.id, " to process ", p_i)
                
                #request new city
                #push the new city id
                for p_i in range(0, num_producers):
                    to_background_qs[p_i].put(cur_i)
                    print("Sent ", cur_i, " to process ", p_i)
                    
                ctys = []
                origs = []
                for p_i in range(0, num_producers):
                    origin, new_city = wb_qs[p_i].get(True)
                    ctys.append(new_city)
                    origs.append(origin)
                
                print("Received all messages") 
                
                for j in range(0, len(ctys)):
                    if ctys[j] != -1:
                        active_city = ctys[j]
                        print("Received ", active_city.id, " from ", origin)
                        break
                
                active_city_changed = False
                
            #draw the active_city's data to screen
            pygame.surfarray.blit_array(display_surface, active_city.data)
            
            #Draw tractor of active_city to screen
            display_surface.blit(images[active_city.tractor.img_key], (active_city.tractor.rect.x, active_city.tractor.rect.y))
            
                        
            if len(active_city.unexplored_zones) > 0:
                #print("UZ")
                Draw_Unexplored_Zones(active_city.unexplored_zones)
           
            
            #draw the active city
            Draw_Explored_Zones(active_city.zones)   
            
        

        #draw GUI
        Draw_Action_Buttons()

        #TODO: enable
        #draw weather effects on screen
        #active_city.weather_effect.draw(display_surface, pygame, images)
        
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
                #weather_effects_proc.join()
                #multiproc_pool.close()
                #multiproc_pool.join()
                #"""
                for i in range(0, len(producers)):
                    stop_q.put("BREAK")
                
                for idx, prod in enumerate(producers):
                        print("    Waiting for producer.join() index %s" % idx)
                        if not prod.is_alive():
                            prod.join()  # Wait for consumer() to finish
                        print("        producer() idx:%s is done" % idx)
                #stop_q.put("BREAK")
                """
                for wbt in wbthreads:
                    stop_q.put("BREAK")
                    if not wbt.is_alive():
                        wbt.join()
                """
                #if not wb_q_thread.is_alive():
                #    wb_q_thread.join()
                #"""
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
                        selected_overlay = OVERLAY.types['PLANT_FACE']
                    else:#if selected_overlay == None:
                        selected_overlay = OVERLAY.types['CROP_GROWTH']
                
                if switch_scene_btn.collidepoint(pygame.mouse.get_pos()):
                    if selected_view == VIEW.types['CITY_VIEW']:
                        selected_view = VIEW.types['MAP_VIEW']
                    else:#if selected_view == OVERLAY.types['MAP_VIEW']:
                        selected_view = VIEW.types['CITY_VIEW']
                
                if city_statistics_btn.collidepoint(pygame.mouse.get_pos()):
                    plot = not plot
                    active_city.Plot(plot)
                
                if selected_view == VIEW.types['CITY_VIEW']:
                    # Explore clicked zone
                    for key, uz in active_city.unexplored_zones.items():
                        if pygame.Rect(uz.rect.x, uz.rect.y, DISPLAY.ZONE_W, DISPLAY.ZONE_H).collidepoint(pygame.mouse.get_pos()):                    
                            print("Expanded to zone " + str(key))
                            active_city.zones[key].is_explored = True
                            Init_Explored_Zones(active_city.data, active_city.zones[key])
                            
                            if key in active_city.unexplored_zones.keys():
                                del active_city.unexplored_zones[key]
                                
                            break
                        
                elif selected_view == VIEW.types['MAP_VIEW']:
                    #Click on a city
                    for i in range(0, len(city_rects)):
                        if city_rects[i].collidepoint(pygame.mouse.get_pos()):
                            print("clicked on city")
                            selected_view = VIEW.types['CITY_VIEW']
                            
                            cur_i = i
                            active_city_changed = True
                                
                            break
        
        #lock.release()
        #Draw the current FPS on the screen
        Render_Current_FPS(str(int(fpsClock.get_fps())), font)
        #Draw the surface object to the screen.  
        pygame.display.update() 
        day_cnt += 1
        #print("Day_Tick: ", day_cnt)
        fpsClock.tick(FPS)
        #time.sleep(1./120)
        #time_since_enter = pygame.time.get_ticks() - start_time
        #print('Milliseconds since enter: ', str(time_since_enter), flush=True)
        #snapshot2 = tracemalloc.take_snapshot()
        #display_top(snapshot2)
        #top_stats = snapshot2.compare_to(snapshot1, 'lineno')       
        #for stat in top_stats[:10]:
        #    print(stat)
    
def Load_Images(pygame):
    images = {}
    img = pygame.image.load('tractor.jpg')
    images['tractor_scaled_img'] = pygame.transform.scale(img, (TRACTOR_PARAMETERS.W, TRACTOR_PARAMETERS.H))
    
    img = pygame.image.load('cowbarn.svg')
    images['shelter_scaled_img'] = pygame.transform.scale(img, (60, 60))
    
    img = pygame.image.load('cow.png')
    images['cow_scaled_img'] = pygame.transform.scale(img, (ANIMAL_SIZE.types['COW'], ANIMAL_SIZE.types['COW']))
    
    img = pygame.image.load('effects/snowflake.svg')
    images['snowflake'] = pygame.transform.scale(img, (10, 10))
    
    img = pygame.image.load('effects/drop.png')
    images['drop'] = pygame.transform.scale(img, (1, 5))
    
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

def Init_Rects():
    global images, cities, weather_effect
    """
    for c in cities:
        for key, uz in c.unexplored_zones.items():
            #shelter_img = images[uz.pasture.shelter_img_key]
            #rect = shelter_img.get_rect()
            #uz.pasture.shelter_rect = MyRect(rect)
            #uz.pasture.shelter_rect = uz.pasture.shelter_rect.move(uz.rect.x, uz.rect.y)
            for a in uz.pasture.animals:
                a.img = images[a.img_key]
                a.img_rect = a.img.get_rect()
                a.img_rect = a.img_rect.move(a.x, a.y)
    """          
    for wp in weather_effect.particles:
        wp.img = images[wp.img_key]
        wp.rect = wp.img.get_rect().move(wp.pos.x, wp.pos.y)

        
if __name__ == "__main__":
    
    #tracemalloc.start()

    global time_cnt, rain_b_inc, tractor
    
    global cultivate_btn, sow_btn, PH_btn, hum_btn, temp_btn, fertilize_btn 
    global N_btn, P_btn, K_btn, crop_growth_btn, harvest_btn, water_btn
    global scouts, forests, lakes, cities
    global images, weather_effect, font
    
    
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
    font = pygame.font.SysFont("monospace", 15)
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
    display_surface = pygame.display.set_mode((DISPLAY.X, DISPLAY.Y ))
    
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
    images = Load_Images(pygame)
      
    # set the pygame window name
    pygame.display.set_caption('City-Sim')
      
    #expansion zones
    #font = pygame.font.SysFont("monospace", 15)
    label = font.render("Expansion zone", 1, blue)
    
    exp_z_len = len(unexplored_zones)
    rng = range(0, exp_z_len)
    
    #rect = pygame.draw.rect(display_surface, black, (DISPLAY.ROAD_WIDTH, DISPLAY.ROAD_WIDTH, DISPLAY.N, DISPLAY.N))
    rect = pygame.Rect((DISPLAY.ROAD_WIDTH, DISPLAY.ROAD_WIDTH), (DISPLAY.N, DISPLAY.N))
    #unexplored_zones.append(Zone(0, rect))
    zones.append(Zone(0, rect, CONST.types['FIELD']))
    zones[0].field.has_init = True
    
    
    if len(unexplored_zones) == 0:
        """
        rect0 = pygame.draw.rect(display_surface, gray, (330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, 15, DISPLAY.ZONE_W, DISPLAY.ZONE_H))
        rect1 = pygame.draw.rect(display_surface, gray, (15, 330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, DISPLAY.ZONE_W, DISPLAY.ZONE_H))
        rect2 = pygame.draw.rect(display_surface, gray, (330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, 330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, DISPLAY.ZONE_W, DISPLAY.ZONE_H))
    
        unexplored_zones[0] = Zone(0, rect0, images)
        unexplored_zones[1] = Zone(1, rect1, images)
        unexplored_zones[2] = Zone(2, rect2, images)
        """
        #rect0 = pygame.Rect((330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, 15), (DISPLAY.ZONE_W, DISPLAY.ZONE_H))
        rect0 = pygame.Rect((330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, 15), (DISPLAY.ZONE_W, DISPLAY.ZONE_H))
        rect = MyRect(_rect=rect0)#(rect0.x, rect0.y, rect0.center, rect0.topleft, rect0.topright, rect0.bottomright)

        #unexplored_zones[0] = Zone(0, rect0.center, rect0.topleft, rect0.topright, rect0.bottomright, rect0.x, rect0.y)
        unexplored_zones[1] = Zone(1, copy.deepcopy(rect))
        
        
        #"""
        rect1 = pygame.Rect((15, 330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH), (DISPLAY.ZONE_W, DISPLAY.ZONE_H))
        rect = MyRect(_rect=rect1)
        #unexplored_zones[1] = Zone(1, rect1.center, rect1.topleft, rect1.topright, rect1.bottomright, rect1.x, rect1.y)
        unexplored_zones[2] = Zone(2, copy.deepcopy(rect))
        
        rect2 = pygame.Rect((330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH, 330+DISPLAY.RIVER_H+DISPLAY.ROAD_WIDTH), (DISPLAY.ZONE_W, DISPLAY.ZONE_H))
        rect = MyRect(_rect=rect2)
        #unexplored_zones[2] = Zone(2, rect2.center, rect2.topleft, rect2.topright, rect2.bottomright, rect2.x, rect2.y)
        #print(type(images['shelter_scaled_img']))
        unexplored_zones[3] = Zone(3, copy.deepcopy(rect))
        #"""
    for key, uz in unexplored_zones.items():
        zones.append(uz)
        
    #Init Cities:
    coords, centers, lakes, forests = Initialize()
    #print(coords)
    centered_centers = copy.deepcopy(centers)
    
    #smm = SharedMemoryManager()
    #smm.start()
    
    
    
    #manager = mp.Manager()
    #cities = []#manager.list()
    cities = list()#mp.Array('Synchronized', range(3))
    for i in range(0, CONSTANTS.types['CITY_NUM'], 3):
        cities.append(City(i, [1, 5, 5], CONSUMPTION_POLICY.types['EXPORT'], 1000, coords[i], centers[i], copy.deepcopy(unexplored_zones), copy.deepcopy(zones), copy.deepcopy(plant), _has_tractor=True, _has_river=True))
        for z in cities[-1].zones:
            Init_Explored_Zones(cities[-1].data, z)
        #"""
        cities.append(City(i+1, [5, 1, 5], CONSUMPTION_POLICY.types['EXPORT'], 1000, coords[i+1], centers[i+1], copy.deepcopy(unexplored_zones), copy.deepcopy(zones), copy.deepcopy(plant), _has_tractor=True, _has_river=True))
        for z in cities[-1].zones:
            Init_Explored_Zones(cities[-1].data, z)
        cities.append(City(i+2, [5, 5, 1], CONSUMPTION_POLICY.types['EXPORT'], 1000, coords[i+2], centers[i+2], copy.deepcopy(unexplored_zones), copy.deepcopy(zones), copy.deepcopy(plant), _has_tractor=True, _has_river=True))
        for z in cities[-1].zones:
            Init_Explored_Zones(cities[-1].data, z)
        #"""
    #shm = shared_memory.ShareableList(cities, name=c)
    
    scouts = []
    scouts.append(Scout(centered_centers[0], pygame.Rect(coords[0][0] + DISPLAY.CITY_W/2 - DISPLAY.SCOUT_W/2, coords[0][1] + DISPLAY.CITY_H/2 - DISPLAY.SCOUT_H/2, DISPLAY.SCOUT_W, DISPLAY.SCOUT_H)))
    
    #Weather effects
    #weather_effect = WeatherEffect(WEATHER.types['RAIN'])
    
    selected_overlay = None
    
    running = True
    
    #Init_Rects()
    
    main()
    #profile.run('main()')
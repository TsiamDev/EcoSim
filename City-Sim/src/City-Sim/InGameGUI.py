# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 03:56:01 2022

@author: TsiamDev
"""

"""
pygame-menu
https://github.com/ppizarror/pygame-menu
EXAMPLE - WINDOW RESIZE
Resize the menu when the window is resized.
"""

import pygame
import pygame_menu

import sys

from test import main

pygame.init()

WINDOW_SIZE = []
WINDOW_SIZE.append(750)
WINDOW_SIZE.append(750)

surface = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]), pygame.RESIZABLE)
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

def on_resize() -> None:
    """
    Function checked if the window is resized.
    """
    window_size = surface.get_size()
    new_w, new_h = 0.75 * window_size[0], 0.7 * window_size[1]
    if menu.is_enabled:
        menu.resize(new_w, new_h)
        
    if plant_menu.is_enabled:
        plant_menu.resize(new_w, new_h)
    print(f'New menu size: {menu.get_size()}')

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
menu.add.button('Start', )
menu.add.button('My Plants', plant_menu)
#menu.add.button('Quit', pygame_menu.events.EXIT) #restarts kernel
menu.enable()
#on_resize()  # Set initial size

if __name__ == '__main__':
    running = True
    while running:  
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.VIDEORESIZE:
                # Update the surface
                surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                # Call the menu event
                on_resize()

        # Draw the menu
        surface.fill((25, 0, 50))

        menu.update(events)
        menu.draw(surface)

        pygame.display.flip()
        
    pygame.display.quit()
    pygame.quit()
    sys.exit()
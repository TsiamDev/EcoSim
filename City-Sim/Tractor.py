# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 03:58:15 2022

@author: TsiamDev
"""

import random

from MyPoint import MyPoint

from Const import TRACTOR_ACTIONS, TRACTOR_PARAMETERS, DISPLAY
from networking.Networking import Set_Globals, Set_Tractor_Actions

class Tractor:
    static_id = 0
    waypoints = []
    
    def __init__(self, _x, _y, _zone, ):
        
        self._id = Tractor.static_id
        Tractor.static_id += 1
        
        self.width = 15
        #tractor = pygame.Rect(x, y, tractor_width, tractor_width)
        #self.img = pygame.image.load('tractor.jpg')
        #self.img = pygame.transform.scale(self.img, (self.width, self.width))
        self.img_key = 'tractor_scaled_img'
        
        self.rect = MyPoint(_x, _y)
        print("Tractor rect:", self.rect)
        #self.rect = type('', (), {})()
        #self.rect.x = _x#self.img.get_rect().x
        #self.rect.y = _y#self.img.get_rect().y
        #self.rect.topleft = self.img.get_rect().topleft
        #self.rect
        #self.rect = self.rect.move(_x, _y)
        
        
        #self.x = _x
        #self.y = _y
        
        self.zone = _zone
        
        #self.move_right = True
        
        self.action = TRACTOR_ACTIONS.types['IDLE']
        self.action_Q = []
        self.action_Q_ind = -1
        
        self.tractor_Q = []
        self.tractor_Q_ind = -1
        
        lst = [[(300, 15 + self.width * i), (15, 15 + self.width * (i+1))] for i in range(0, 20, 2)]
        Tractor.waypoints = [item for sublist in lst for item in sublist]
        
        self.Define_Policies()
        
    def move(self):
        print(self.waypoints)
        if len(self.waypoints) > 0:
            if self.waypoints[0][0] - self.rect.x < 0:
                x_dir = -1
            elif self.waypoints[0][0] - self.rect.x > 0:
                x_dir = 1
            else:
                x_dir = 0
            
                
            if x_dir == 0:
                if self.waypoints[0][1] - self.rect.y < 0:
                    y_dir = -1
                elif self.waypoints[0][1] - self.rect.y > 0:
                    y_dir = 1
                else:
                    y_dir = 0
            else:
                y_dir = 0
            
            self.rect.move(x_dir*15, y_dir*15)
            print(self.rect.x, self.rect.y)
            
            if (x_dir == 0) & (y_dir == 0):
                del self.waypoints[0]
                print(self.waypoints)
                if len(self.waypoints) == 0:
                    #self.action = TRACTOR_ACTIONS.types['IDLE']
                    lst = [[(300, 15 + self.width * i), (15, 15 + self.width * (i+1))] for i in range(0, 20, 2)]
                    #lst = [(15,15), (300,15), (300, 30), (15, 30), (15, 45), (300, 45), (300, 60), (15, 60)]
                    """
                    lst.append((15, 15))
                    lst.append((300, 15))
                    lst.append((300, 30))
                    lst.append((30, 30))
                    lst = [[(15, self.width * i), (300, self.width * (i+1))] for i in range(2, 20, 2)]
                    """
                    #print(lst)
                    self.waypoints = [item for sublist in lst for item in sublist]
                    #self.waypoints = lst
                    self.action_Q_ind += 1
                    if self.action_Q_ind >= len(self.action_Q):
                        self.action_Q_ind = 0
                    self.action = self.action_Q[self.action_Q_ind]
        
    def act(self, data, plant):
        if self.action == TRACTOR_ACTIONS.types['IDLE']:
            data = None
        elif self.action == TRACTOR_ACTIONS.types['CULTIVATE']:
            data = self.cultivate(data)
            self.move()
        elif self.action == TRACTOR_ACTIONS.types['SOW']:
            data = self.sow(data, plant)
            #print(self.waypoints)
            self.move()
        elif self.action == TRACTOR_ACTIONS.types['WATER']:
            data = self.water(data)
            self.move()
        elif self.action == TRACTOR_ACTIONS.types['FERTILIZE']:
            data = self.fertilize_N(data)
            data = self.fertilize_P(data)
            data = self.fertilize_K(data)
            self.move()
        elif self.action == TRACTOR_ACTIONS.types['HARVEST']:
            data = self.harvest(data)
            self.move()
        
        #print("tractor rect: ", self.rect)
        
        return data, self.img_key, self.rect             

    def render_soil(self, w, h, _r, _g, _b, data, target, isSowing=None):
        #because tractor x,y is different from zone x,y
        # - 15 => road width
        # if tractor starts at (15,15) => top left corner of field
        x_off = self.rect.x #- 15 
        y_off = self.rect.y #- 15
        is_out_of_field_bounds = False

        #Calculate how many of the field's pixels
        #the tractor will actually change
        x_low = x_off
        if (x_low - self.width) < 0:
            is_out_of_field_bounds = True
            
        x_high = x_low + self.width
        if x_high > (w + self.width):
            x_high = w + self.width
        
        if x_low == x_high:
            is_out_of_field_bounds = True
        
        y_low = y_off
        if (y_low - self.width) < 0:
            is_out_of_field_bounds = True
            
        y_high = y_low + self.width
        if y_high > (h + self.width):
            y_high = h + self.width
            
        if y_low == y_high:
            is_out_of_field_bounds = True

        #print((x_low, x_high), '-', (y_low, y_high))

        if is_out_of_field_bounds == False:
            # pick random <ground> color
            r = [[random.randint(_r[0], _r[1]) for i in range(y_low, y_high)] for j in range(x_low, x_high)]
            g = [[random.randint(_g[0], _g[1]) for i in range(y_low, y_high)] for j in range(x_low, x_high)]
            b = [[random.randint(_b[0], _b[1]) for i in range(y_low, y_high)] for j in range(x_low, x_high)]
            
            #update crop state
            #target[x_low:(x_high), y_low:y_high, 0] = r
            #target[x_low:(x_high), y_low:y_high, 1] = g
            #target[x_low:(x_high), y_low:y_high, 2] = b
            target[self.rect.x-self.width:self.rect.x, self.rect.y-self.width:self.rect.y, 0] = r
            target[self.rect.x-self.width:self.rect.x, self.rect.y-self.width:self.rect.y, 1] = g
            target[self.rect.x-self.width:self.rect.x, self.rect.y-self.width:self.rect.y, 2] = b
    
            if data is not None:
                #update displayed field state
                #data[self.rect.x:self.rect.x+self.width, self.rect.y:self.rect.y+self.width, 0] = r
                #data[self.rect.x:self.rect.x+self.width, self.rect.y:self.rect.y+self.width, 1] = g
                #data[self.rect.x:self.rect.x+self.width, self.rect.y:self.rect.y+self.width, 2] = b
                
                #data[self.rect.x:self.rect.x+self.width, self.rect.y:self.rect.y+self.width, 0] = r
                #data[self.rect.x:self.rect.x+self.width, self.rect.y:self.rect.y+self.width, 1] = g
                #data[self.rect.x:self.rect.x+self.width, self.rect.y:self.rect.y+self.width, 2] = b
                
                data[self.zone.rect.x:w+DISPLAY.ROAD_WIDTH, self.zone.rect.y:h+DISPLAY.ROAD_WIDTH, 0] = target[:, :, 0]
                data[self.zone.rect.x:w+DISPLAY.ROAD_WIDTH, self.zone.rect.y:h+DISPLAY.ROAD_WIDTH, 1] = target[:, :, 1]
                data[self.zone.rect.x:w+DISPLAY.ROAD_WIDTH, self.zone.rect.y:h+DISPLAY.ROAD_WIDTH, 2] = target[:, :, 2]
                
            if isSowing == True:
                self.zone.field.is_planted[self.rect.x-self.width:self.rect.x, self.rect.y-self.width:self.rect.y] = 1
            
        return data

    def fertilize_N(self, data):
        #reset <ground> color to <soil> color
        w = len(self.zone.field.N[0])
        h = len(self.zone.field.N[1])
        
        r = (0, 0)
        g = (255, 255)
        b = (0, 0)
        
        return self.render_soil(w, h, r, g, b, None, self.zone.field.N)
    
    def fertilize_P(self, data):
        #reset <ground> color to <soil> color
        w = len(self.zone.field.P[0])
        h = len(self.zone.field.P[1])
        
        r = (0, 0)
        g = (255, 255)
        b = (0, 0)
        
        return self.render_soil(w, h, r, g, b, None, self.zone.field.P)

    def fertilize_K(self, data):
        #reset <ground> color to <soil> color
        w = len(self.zone.field.K[0])
        h = len(self.zone.field.K[1])
        
        r = (0, 0)
        g = (255, 255)
        b = (0, 0)
        
        return self.render_soil(w, h, r, g, b, None, self.zone.field.K)

    def cultivate(self, data):
        #reset <ground> color to <soil> color
        w = len(self.zone.field.crop_growth[0])
        h = len(self.zone.field.crop_growth[1])
        
        r = (70, 83)
        g = (45, 50)
        b = (0, 0)
        
        return self.render_soil(w, h, r, g, b, data, self.zone.field.crop_growth)

    def sow(self, data, plant):
        
        #reset <ground> color to <soil> color
        w = len(self.zone.field.crop_growth[0])
        h = len(self.zone.field.crop_growth[1])
        
        r = (0, plant.c[0])
        g = (0, plant.c[1])
        b = (0, plant.c[2])
        
        return self.render_soil(w, h, r, g, b, data, self.zone.field.crop_growth, True)  
    
    #data is unused here
    def water(self, data):
        #reset <ground> color to <soil> color
        w = len(self.zone.field.hum[0])
        h = len(self.zone.field.hum[1])
        
        r = (0, 0)
        g = (0, 0)
        b = (255, 255)
        
        return self.render_soil(w, h, r, g, b, None, self.zone.field.hum) 
    
    def harvest(self, data):
       
        #reset <ground> color to <soil> color
        w = len(self.zone.field.crop_growth[0])
        h = len(self.zone.field.crop_growth[1])
        
        r = (70, 83)
        g = (45, 50)
        b = (0, 0)
        
        return self.render_soil(w, h, r, g, b, data, self.zone.field.crop_growth)

    def Define_Policies(self):
        #TODO prompt users to decide which actions the tractors will perform,
        #and in what order
        #Set_Globals()
        #Set_Tractor_Actions(TRACTOR_ACTIONS.types)
        self.action_Q = list([TRACTOR_ACTIONS.types['CULTIVATE'], TRACTOR_ACTIONS.types['SOW'],
                   TRACTOR_ACTIONS.types['FERTILIZE'], TRACTOR_ACTIONS.types['WATER'],
                   TRACTOR_ACTIONS.types['HARVEST']])
        self.action_Q_ind = 0
        
        self.action = self.action_Q[self.action_Q_ind]
        
        #lst = [(15, 15), (300, 15), (300, 30), (15, 30), (15, 45), (300, 45), (300, 60), (15, 60),
        #       (15, 75), (300, 75), (300, 90), (15, 90), (15, 105), (300, 105), (300, 120),
        #       (15, 120), (15, 135), (300, 135), (300, 150), (15, 150), (15, 165)]
        #lst = [(15, 15), (300, 15), (300, 30), (15, 30)]
        #lst = [[(300, 15 + self.width * i), (15, 15 + self.width * (i+1))] for i in range(0, 20, 2)]
        
        lst = [[(300, 15 + self.width * i), (15, 15 + self.width * (i+1))] for i in range(0, 20, 2)]
        self.waypoints = [item for sublist in lst for item in sublist]
        
        #self.tractor_Q = [item for sublist in lst for item in sublist]
        #self.tractor_Q = lst
        #self.tractor_Q_ind = 0
        
        #self.waypoints = self.tractor_Q
        

    def init_Q(self, lst):
        self.tractor_Q = lst
        self.tractor_Q_ind = 0
        
        self.action = self.tractor_Q[0]
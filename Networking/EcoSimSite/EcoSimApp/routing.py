# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 10:44:30 2022

@author: kosts
"""

from channels.routing import URLRouter
from EcoSimApp.consumers import Consumer
from django.urls import re_path

url_router = URLRouter([
    re_path(r"ws/EcoSimApp/(?P<room_name>\w+)/$", Consumer.as_asgi()),
])
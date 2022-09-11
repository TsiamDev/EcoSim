# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 11:05:02 2022

@author: kosts
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("<str:room_name>/", views.room, name="room"),
]
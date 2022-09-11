"""EcoSimSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from EcoSimApp.views import *

urlpatterns = [
    path('EcoSimApp/', include('EcoSimApp.urls')),
    path('admin/', admin.site.urls),
    path('index/', index, name='index'),
    path('set_tractor_actions/', set_tractor_actions, name='set_tractor_actions'),
    path('index/success', success, name='success'),
    #path('user_list', user_list, name='user_list'),
]

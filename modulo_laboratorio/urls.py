from django import views
from django.contrib import admin
from django.urls import path

from modulo_laboratorio.views import sala_laboratorio


urlpatterns = [
    path('sala/', sala_laboratorio, name='prueba'),

]

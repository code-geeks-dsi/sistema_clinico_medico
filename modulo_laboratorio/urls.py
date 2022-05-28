from webbrowser import get
from django import views
from django.contrib import admin
from django.urls import path

from modulo_laboratorio.views import sala_laboratorio, get_categoria_examen


urlpatterns = [
    path('sala/', sala_laboratorio, name='prueba'),

    path('get-select-examen/<int:id_categoria>', get_categoria_examen, name='get_select_examen' ),

]

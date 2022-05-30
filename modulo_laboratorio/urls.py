from webbrowser import get
from django import views
from django.contrib import admin
from django.urls import path
from modulo_expediente.views import agregar_cola

from modulo_laboratorio.views import agregar_examen_cola, sala_laboratorio, get_categoria_examen


urlpatterns = [
    path('sala/', sala_laboratorio, name='prueba'),

    path('cola/', agregar_examen_cola, name='agregar_examen_cola' ),

    path('get-select-examen/<int:id_categoria>', get_categoria_examen, name='get_select_examen' ),

]

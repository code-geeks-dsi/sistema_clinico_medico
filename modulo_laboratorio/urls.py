from webbrowser import get
from django import views
from django.contrib import admin
from django.urls import path
from modulo_expediente.views import agregar_cola

from modulo_laboratorio.views import agregar_examen_cola, generar_pdf, get_cola_examenes, sala_laboratorio, get_categoria_examen


urlpatterns = [
    path('sala/', sala_laboratorio, name='prueba'),

    path('cola/', agregar_examen_cola, name='agregar_examen_cola' ),

    path('get-select-examen/<int:id_categoria>', get_categoria_examen, name='get_select_examen' ),

    path('cola/get_cola_examenes', get_cola_examenes, name='get_cola_examenes'),

    path('resultados/', generar_pdf, name='generar_pdf')

]

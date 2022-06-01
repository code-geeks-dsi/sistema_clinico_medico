from webbrowser import get
from django import views
from django.contrib import admin
from django.urls import path
from modulo_expediente.views import agregar_cola

from modulo_laboratorio.views import agregar_examen_cola, get_cola_examenes, sala_laboratorio, get_categoria_examen,elaborar_resultados_examen


urlpatterns = [
    path('sala/', sala_laboratorio, name='prueba'),

    path('examen/', agregar_examen_cola, name='agregar_examen_cola' ),

    path('examen/<int:id_categoria>', get_categoria_examen, name='get_select_examen' ),

    path('examen/cola/', get_cola_examenes, name='get_cola_examenes'),
    path('examen/resultado/<int:id_resultado>', elaborar_resultados_examen, name='elaborar_resultado')


]

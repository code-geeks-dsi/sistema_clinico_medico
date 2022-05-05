from django import views
from django.contrib import admin
from django.urls import path
from modulo_expediente.views import busqueda_paciente, autocompletado_apellidos,sala_consulta


urlpatterns = [
    path('paciente/',busqueda_paciente, name='busqueda_paciente'),
    path('paciente/autocompletado',autocompletado_apellidos, name='autocompletado_apellidos'),
    path('sala/',sala_consulta, name='sala_consulta'),
]
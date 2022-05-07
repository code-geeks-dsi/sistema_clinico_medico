from django import views
from django.contrib import admin
from django.urls import path
from modulo_expediente.views import busqueda_paciente , get_paciente,crear_expediente


urlpatterns = [
    path('paciente/',busqueda_paciente, name='busqueda_paciente'),
    path('paciente/<int:id_paciente>',get_paciente, name='get_paciente'),
    path('paciente/datos',crear_expediente,name='crear_expediente')
]
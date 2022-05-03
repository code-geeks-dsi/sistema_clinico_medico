from django import views
from django.contrib import admin
from django.urls import path
from modulo_expediente.views import busqueda_paciente


urlpatterns = [
    path('paciente/',busqueda_paciente, name='busqueda_paciente'),
]
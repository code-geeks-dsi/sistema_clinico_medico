from django import views
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('busqueda/paciente', busqueda_paciente, name='busqueda_paciente'),
]
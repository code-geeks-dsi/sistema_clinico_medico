from django import views
from django.contrib import admin
from django.urls import path
from modulo_expediente.views import busqueda_paciente, autocompletado_apellidos,sala_consulta,get_contieneConsulta,get_paciente,agregar_cola


urlpatterns = [
    path('paciente/',busqueda_paciente, name='busqueda_paciente'),
    path('paciente/autocompletado',autocompletado_apellidos, name='autocompletado_apellidos'),
    path('sala/',sala_consulta, name='sala_consulta'),
     path('paciente/<int:id_paciente>', get_paciente, name='get_paciente'),
    path('cola/<int:id_paciente>', agregar_cola,name='agregar_cola' ),
    path('cola/', get_contieneConsulta, name='get_contieneConsulta')
]
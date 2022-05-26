from django import views
from django.contrib import admin
from django.urls import path
from modulo_expediente.views import agregar_medicamento, busqueda_paciente, autocompletado_apellidos, eliminar_cola,sala_consulta,get_cola,get_paciente,agregar_cola, modificar_signosVitales, crear_expediente



urlpatterns = [
    path('paciente/',busqueda_paciente, name='busqueda_paciente'),

    path('paciente/<int:id_paciente>',get_paciente, name='get_paciente'),

    path('paciente/datos',crear_expediente,name='crear_expediente'),

    path('paciente/autocompletado',autocompletado_apellidos, name='autocompletado_apellidos'),
    path('sala/',sala_consulta, name='sala_consulta'),
    path('cola/<int:id_paciente>', agregar_cola,name='agregar_cola' ),
    path('cola/', get_cola, name='get_contieneConsulta'),
    path('cola/eliminar-paciente/<int:id_paciente>', eliminar_cola, name='eliminar_cola'),
    path('modificar-signosVitales/<int:id_signos_vitales>',modificar_signosVitales, name='modificar_signosVitales'),
    path('receta_medica/agregar-medicamento', agregar_medicamento, name='agregar_medicamento')
]


from django import views
from django.contrib import admin
from django.urls import path
from modulo_expediente.views import agregar_medicamento, busqueda_paciente, autocompletado_apellidos, eliminar_cola, eliminar_dosis,sala_consulta,get_cola,get_paciente,agregar_cola, modificar_signosVitales, crear_expediente, editar_consulta
from modulo_expediente.views import busqueda_medicamento, autocompletado_medicamento,dosis_medicamento

from modulo_expediente.views import buscar_expediente, ConstanciaMedicaView, ConstanciaMedicaCreate, templete_agenda


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
    path('receta_medica/agregar-medicamento', agregar_medicamento, name='agregar_nuevo_medicamento'),
    path('consulta/<int:id_consulta>/',editar_consulta,name='editar_consulta'),
    path('medicamento/',busqueda_medicamento, name='agregar_medicamento'),
    path('receta/dosis',dosis_medicamento,name='agregar_dosis'),

    path('medicamento/autocompletado/',autocompletado_medicamento, name='agregar_medicamento_2'),
    path('receta/dosis/eliminar_dosis/<int:id_dosis>',eliminar_dosis,name='eliminar_dosis'),

    path('buscar/',buscar_expediente,name='buscar_expediente'),

    path('constancia-medica-pdf/',ConstanciaMedicaView.as_view(),name='constancia-medica'),
    path('constancia-medica/',ConstanciaMedicaCreate.as_view(),name='crear-constancia-medica'),

    path('agenda/',templete_agenda,name='ver_agenda'),

]


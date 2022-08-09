from django import views
from django.contrib import admin
from django.urls import path
from modulo_expediente.views import (
    AgendaView, ReferenciaMedicaUpdate, agregar_medicamento, busqueda_paciente, autocompletado_apellidos, 
    eliminar_cola, eliminar_dosis,sala_consulta,get_cola,get_paciente,agregar_cola, 
    modificar_signosVitales, crear_expediente, editar_consulta, CreateHojaEvolucion, ListaHojaEvolucion
    )
from modulo_expediente.views import (
    busqueda_medicamento, autocompletado_medicamento,dosis_medicamento, ConstanciaMedica)

from modulo_expediente.views import (
    buscar_expediente, ConstanciaMedicaView, ConstanciaMedicaCreate, 
    ReferenciaMedicaView, ConstanciaMedicaUpdate, ConstanciaMedicaPDFView,
    AgendaView, ConsultaView, RecetaMedicaPdfView, ReferenciaMedicaPdfView
    )



urlpatterns = [
    path('paciente/',busqueda_paciente, name='busqueda_paciente'),

    path('paciente/<int:id_paciente>',get_paciente, name='get_paciente'),

    path('paciente/datos',crear_expediente,name='crear_expediente'),

    path('paciente/autocompletado',autocompletado_apellidos, name='autocompletado_apellidos'),
    path('sala/',sala_consulta, name='sala_consulta'),
    path('cola/<int:id_paciente>', agregar_cola,name='agregar_cola' ),
    path('cola/', get_cola, name='get_contieneConsulta'),
    path('cola/eliminar-paciente/<int:id_paciente>', eliminar_cola, name='eliminar_cola'),
    path('modificar-signosVitales/<int:id_consulta>',modificar_signosVitales, name='modificar_signosVitales'),
    path('receta_medica/agregar-medicamento', agregar_medicamento, name='agregar_nuevo_medicamento'),
    path('consulta/<int:id_consulta>/',ConsultaView.as_view(),name='editar_consulta'),
    path('medicamento/',busqueda_medicamento, name='agregar_medicamento'),
    path('receta/dosis',dosis_medicamento,name='agregar_dosis'),

    path('medicamento/autocompletado/',autocompletado_medicamento, name='agregar_medicamento_2'),
    path('receta/dosis/eliminar_dosis/<int:id_dosis>',eliminar_dosis,name='eliminar_dosis'),

    path('buscar/',buscar_expediente,name='buscar_expediente'),

    path('consulta/<int:id_consulta>/constancia-medica/pdf',ConstanciaMedicaPDFView.as_view(),name='constancia-medica'),
    path('constancia-medica/',ConstanciaMedicaCreate.as_view(),name='crear-constancia-medica'),
    
    path('constancia-medica/<str:id>',ConstanciaMedicaView.as_view(),name='constancia-medica'),
    path('constancia-medica/',ConstanciaMedicaCreate.as_view(),name='crear-constancia-medica'),
    path('consulta/<int:id_consulta>/referencia-medica/',ReferenciaMedicaView.as_view(),name='referencia-medica'),
    path('consulta/<int:id_consulta>/referencia-medica/<int:id_referencia>/',ReferenciaMedicaUpdate.as_view(),name='referencia-medica-update'),
    path('consulta/<int:id_consulta>/hoja-evolucion/',CreateHojaEvolucion.as_view(),name='hoja-evolucion-create'),
    path('consulta/<int:id_consulta>/hoja-evolucion/lista',ListaHojaEvolucion.as_view(),name='hoja-evolucion-lista'),
    path('agenda/', AgendaView.as_view(),name='ver_agenda'),
    path('consulta/<int:id_consulta>/constancia-medica/',ConstanciaMedicaView.as_view(),name='constancia-medica'),
    path('consulta/<int:id_consulta>/constancia-medica/<int:id_constancia>/',ConstanciaMedicaUpdate.as_view(),name='constancia-medica-update'),

    path('consulta/<int:id_consulta>/referencia-medica/pdf',ReferenciaMedicaPdfView.as_view(),name='referencia-medica-pdf' ),
    path('consulta/<int:id_consulta>/receta-medica/pdf',RecetaMedicaPdfView.as_view(),name='receta-medica-pdf' ),

    path('consulta/<int:id_consulta>/constancia-medica/',ConstanciaMedicaView.as_view(),name='constancia-medica'),
    path('consulta/<int:id_consulta>/constancia-medica/<int:id_constancia>/',ConstanciaMedicaUpdate.as_view(),name='constancia-medica-update')
]


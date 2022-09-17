from django.urls import path
from modulo_laboratorio.views.CategoriaExamen import *
from modulo_laboratorio.views.EsperaExamen import *
from modulo_laboratorio.views.Resultado import *
from modulo_laboratorio.views.OrdenExamenes import *
from modulo_laboratorio.views.Bitacora import *

urlpatterns = [
    # Vista cola de ordenes de examenes de laboratorio: Secretaria
    path('sala/', sala_laboratorio, name='sala_laboratorio'),

    path('inicio/', inicio, name='inicio_lab'),
    # path('examen/', agregar_examen_cola, name='agregar_examen_cola' ),

    path('examen/<int:id_categoria>', get_categoria_examen, name='get_select_examen' ),
    # Elaboracion de Resultados Lic de Laboratorio
    path('examen/resultado/<int:id_resultado>', elaborar_resultados_examen, name='elaborar_resultado'),
    # Generacion de PDFs
    path('examen/orden/<int:orden_id>/pdf', generar_orden_pdf, name='generar_orden_pdf'),
    path('examen/resultado/<int:id_resultado>/pdf', generar_resultado_pdf, name='generar_pdf'),
    # Cambios de fase resultado
    path('examen/fase/2',cambiar_fase_a_en_proceso,name="cambiar_fase_secretaria"),#cambia a fase en proceso
    path('examen/fase/3',cambiar_fase_a_listo,name="cambiar_fase_laboratorio"),#cambia a listo
    # Cola de Examenes Lic de Laboratorio
    path('pendientes/', examenes_pendientes, name='pendientes_lab'),
    path('bitacora/', BitacoraView.as_view(), name='bitacora_lab'),

    # Gestion de Resultados en Orden Examenes Secretaria
    path('orden/<int:id_paciente>', OrdenExamenCreate.as_view(),name="crear_orden_examenes"),
    path('orden/<int:id_paciente>/<int:id_orden>', ResultadoView.as_view(),name="update_orden_examenes")

]

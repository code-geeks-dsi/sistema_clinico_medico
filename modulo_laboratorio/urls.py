from django.urls import path
from .views import agregar_examen_cola, cambiar_fase_secretaria, cambiar_fase_laboratorio,get_cola_examenes, sala_laboratorio
from .views import get_categoria_examen,elaborar_resultados_examen, generar_pdf, inicio, examenes_pendientes, bitacora_templete

urlpatterns = [
    path('sala/', sala_laboratorio, name='sala_laboratorio'),

    path('examen/', agregar_examen_cola, name='agregar_examen_cola' ),

    path('examen/<int:id_categoria>', get_categoria_examen, name='get_select_examen' ),

    path('examen/cola/', get_cola_examenes, name='get_cola_examenes'),
    path('examen/resultado/<int:id_resultado>', elaborar_resultados_examen, name='elaborar_resultado'),

    path('examen/resultado/<int:id_resultado>/pdf', generar_pdf, name='generar_pdf'),
    path('examen/cola/fase/2',cambiar_fase_secretaria,name="cambiar_fase_secretaria"),#cambia a fase en proceso
    path('examen/cola/fase/3',cambiar_fase_laboratorio,name="cambiar_fase_laboratorio"),#cambia a fase en proceso

    path('inicio/', inicio, name='inicio_lab'),
    path('pendientes/', examenes_pendientes, name='pendientes_lab'),
    path('bitacora/', bitacora_templete, name='bitacora_lab'),

]

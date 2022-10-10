from django.urls import path
from modulo_publicidad.views.AdministracionPublicidad import *

urlpatterns = [
    path('inicio/', InicioPublicidad.as_view(), name='inicio_publicidad'),
    path('clinica/', ClinicaPublicidad.as_view(), name='clinica_publicidad'),
    
    # Crea y Edita promociones
    path('clinica/<int:id_promocion>', PromocionClinica.as_view(), name='clinica_publicidad_promocion'),
    path('laboratorio/', InicioPublicidad.as_view(), name='laboratorio_publicidad'),
    path('farmacia/', InicioPublicidad.as_view(), name='farmacia_publicidad'),

]
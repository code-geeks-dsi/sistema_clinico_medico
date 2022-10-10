from django.urls import path
from modulo_publicidad.views.AdministracionPublicidad import *

urlpatterns = [
    path('inicio/', InicioPublicidad.as_view(), name='inicio_publicidad'),
    path('clinica/', ClinicaPublicidad.as_view(), name='clinica_publicidad'),
    path('laboratorio/', InicioPublicidad.as_view(), name='laboratorio_publicidad'),
    path('farmacia/', InicioPublicidad.as_view(), name='farmacia_publicidad'),
    
    # publica promociones
    path('promociones/', CrearPromocion.as_view(), name='crear_publicacion'),
    # edita promociones
    path('promociones/<int:id_publicidad>', EditarPromocion.as_view(), name='editar_publicacion'),

]
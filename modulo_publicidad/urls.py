from django.urls import path
from modulo_publicidad.views.AdministracionPublicidad import *

urlpatterns = [
    path('inicio/', InicioPublicidad.as_view(), name='inicio_publicidad'),
    path('clinica/', ClinicaPublicidad.as_view(), name='clinica_publicidad'),
    path('laboratorio/', InicioPublicidad.as_view(), name='laboratorio_publicidad'),
    path('farmacia/', InicioPublicidad.as_view(), name='farmacia_publicidad'),
    
    #lista promociones
    path('promociones/', PublicacionListView.as_view(), name='ver_publicaciones'),
    # publica promociones
    path('promociones/new', CrearPromocion.as_view(), name='crear_publicacion'),
    # edita promociones
    path('promociones/<int:id_publicidad>', EditarPromocion.as_view(), name='editar_publicacion'),

]
from django.urls import path
from modulo_publicidad.views.AdministracionPublicidad import *
from modulo_publicidad.views.PaginaPrincipal import *
from modulo_publicidad.views.ServiciosMedicos import *

urlpatterns = [
    path('inicio/', InicioPublicidad.as_view(), name='inicio_publicidad'),
    path('clinica/', ClinicaPublicidad.as_view(), name='clinica_publicidad'),
    path('laboratorio/', InicioPublicidad.as_view(), name='laboratorio_publicidad'),
    path('farmacia/', InicioPublicidad.as_view(), name='farmacia_publicidad'),
    path('paginaClinica/', PaginaClinica.as_view(), name='paginaClinica'),
    path('paginaLaboratorio/', PaginaLaboratorio.as_view(), name='paginaLaboratorio'),

    # administración de publicaciones
    #lista publicaciones
    path('publicaciones/', PublicacionListView.as_view(), name='ver_publicaciones'),
    # crea publicaciones
    path('publicaciones/new', CrearPromocion.as_view(), name='crear_publicacion'),
    # edita publicaciones
    path('publicaciones/<int:id_publicidad>', EditarPromocion.as_view(), name='editar_publicacion'),

    # servicios
    # detalle de servicio
    # 🤔 creo que seria mejor si unieramos la publicación con el descuento y que se editen y eliminen en conjunto
    #  y en la de servicios solo que se edite el precio y nombre
    # path('servicios/<int:pk>', ServicioDetailView.as_view(), name='ver_servicio')

    # Administrar servicios clínica médica.
    path('servicios/medicos/', ServiciosMedicosListView.as_view(), name='lista_servicios_medicos'),
    path('servicios/medicos/new', crearServicioMedico.as_view(), name='crear_servicio_medico'),

    
]
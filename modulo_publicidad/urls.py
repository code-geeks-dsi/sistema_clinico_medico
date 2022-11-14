from django.urls import path
from modulo_publicidad.views.AdministracionPublicidad import *
from modulo_publicidad.views.PaginaPrincipal import *
from modulo_publicidad.views.ServiciosMedicos import *
from modulo_publicidad.views.ServiciosLaboratorioClinico import *
from modulo_publicidad.views.PaginaClinica import *
from modulo_publicidad.views.PaginaLaboratorio import *

urlpatterns = [
    path('inicio/', InicioPublicidad.as_view(), name='inicio_publicidad'),
    path('inicio/publicaciones', get_publicaciones, name='get_pub'),
    path('inicio/servicios', get_servicios_medicos, name='get_servicios_medicos'),
    path('inicio/<int:id_publicacion>', vista, name="vista_publicacion"),
    path('inicio/servicios/laboratorio', get_servicios_laboratorio, name='get_servicios_laboratorio'),
    path('clinica/', ClinicaPublicidad.as_view(), name='clinica_publicidad'),
    path('laboratorio/', InicioPublicidad.as_view(), name='laboratorio_publicidad'),
    path('farmacia/', InicioPublicidad.as_view(), name='farmacia_publicidad'),

    path('serviciosMedicos/', SeccionServiciosMedicos.as_view(), name='servicios_medicos'),
    path('serviciosLaboratorio/', SeccionServiciosLaboratorio.as_view(), name='servicios_laboratorio'),

    # Administrar servicios clínica médica.
    path('servicios/medicos/', ServiciosMedicosListView.as_view(), name='lista_servicios_medicos'),
    path('servicios/medicos/new', CrearServicioMedico.as_view(), name='crear_servicio_medico'),
    path('servicios/medicos/<int:id_servicio>', EditarServicioMedico.as_view(), name='editar_servicio_medico'),
    path('servicios/medicos/<int:pk>/delete', EliminarServicioMedicoView.as_view(), name='eliminar_servicio_medico'),
    
    # Administrar servicios laboratorio clínico
    path('servicios/laboratorio/', ServiciosLaboratorioListView.as_view(), name='lista_servicios_laboratorio'),
    path('servicios/laboratorio/new', CrearServicioLaboratorio.as_view(), name='crear_servicio_laboratorio'),
    path('servicios/laboratorio/<int:id_servicio>', EditarServicioLaboratorio.as_view(), name='editar_servicio_laboratorio'),
    path('servicios/laboratorio/<int:pk>/delete', EliminarServicioLaboratorioView.as_view(), name='eliminar_servicio_laboratorio'),

    #Administrar Promociones de servicios
    #lista publicaciones
    path('servicios/<str:servicio>/<int:id_servicio>/promociones/', PublicacionListView.as_view(), name='ver_publicaciones'),
    # crea publicaciones
    path('servicios/<str:servicio>/<int:id_servicio>/promociones/new', CrearPromocion.as_view(), name='crear_publicacion'),
    path('servicios/<str:servicio>/<int:id_servicio>/promociones/<int:id_promocion>', EditarPromocion.as_view(), name='editar_publicacion'),
    path('servicios/<str:servicio>/<int:id_servicio>/promociones/<int:pk>/delete', EliminarPromocionView.as_view(), name='eliminar_publicacion'),

]
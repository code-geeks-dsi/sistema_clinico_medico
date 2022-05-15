from unicodedata import name
from django import views
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from modulo_control.views import registrar_empleado, editar_empleado, vista_adminitracion_empleados, lista_empleados, get_empleado

urlpatterns = [

    # path('agregarEmpleado', agregar_empleado, name= 'agregarEmpleado'),
    # path('', indexEmpleado, name='indexEmpleado'),
    # path('registrarDoctor', registrarDoctor, name= 'registrarDoctor'),
    # path('agregarDoctor', agregarDoctor, name= 'agregarDoctor'),
    # path('registrarEnfermera', registrarEnfermera, name= 'registrarEnfermera'),
    # path('agregarEnfermera', agregarEnfermera, name= 'agregarEnfermera'),
    path('registrar/empleado', registrar_empleado, name= 'registrarEmpleado'),
    path('editar/empleado/', editar_empleado, name= 'editarEmpleado'),
    # path('registrarLicLaboratorioClinico', registrarLicLaboratorioClinico, name= 'registrarLicLaboratorioClinico'),
    # path('agregarLicLaboratorioClinico', agregarLicLaboratorioClinico, name= 'agregarLicLaboratorioClinico'),
    # path('registrarSecretaria', registrarSecretaria, name= 'registrarSecretaria'),
    # path('agregarSecretaria', agregarSecretaria, name= 'agregarSecretaria'),
    path('empleados/', vista_adminitracion_empleados, name= 'vistaGestionEmpleados'),
    path('empleados/lista/', lista_empleados, name="listaEmpleados"),
    path('empleados/lista/<str:cod_empleado>', get_empleado, name='get_empleado'),
    
    
]
urlpatterns += staticfiles_urlpatterns()

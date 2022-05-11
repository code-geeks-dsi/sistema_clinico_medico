from unicodedata import name
from django import views
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from modulo_control.views import *

urlpatterns = [

    path('admin/', admin.site.urls),
    path('agregarEmpleado', agregarEmpleado, name= 'agregarEmpleado'),
    path('admin/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('', indexEmpleado, name='indexEmpleado'),
    path('registrarDoctor', registrarDoctor, name= 'registrarDoctor'),
    path('agregarDoctor', agregarDoctor, name= 'agregarDoctor'),
    path('registrarEnfermera', registrarEnfermera, name= 'registrarEnfermera'),
    path('agregarEnfermera', agregarEnfermera, name= 'agregarEnfermera'),
    path('registrarEmpleado', registrarEmpleado, name= 'registrarEmpleado'),
    path('agregarEmpleado', agregarEmpleado, name= 'agregarEmpleado'),
    path('registrarLicLaboratorioClinico', registrarLicLaboratorioClinico, name= 'registrarLicLaboratorioClinico'),
    path('agregarLicLaboratorioClinico', agregarLicLaboratorioClinico, name= 'agregarLicLaboratorioClinico'),
    path('registrarSecretaria', registrarSecretaria, name= 'registrarSecretaria'),
    path('agregarSecretaria', agregarSecretaria, name= 'agregarSecretaria'),
    
    
]
urlpatterns += staticfiles_urlpatterns()

"""sistema_clinico_medico URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    probando cambios
"""
from django import views
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from modulo_control.views import vista_iniciarsesion, logearse, cerrar_sesion, home, LoginView
from modulo_publicidad.views.PaginaPrincipal import PaginaPrincipal
from modulo_publicidad.views.PaginaClinica import PaginaClinica
from modulo_publicidad.views.PaginaLaboratorio import PaginaLaboratorio
# from modulo_expediente.views import vista_sala_espera

urlpatterns = [
    path('admin/', admin.site.urls),
    #Login
    path('login/', LoginView.as_view(), name='login'),
    path('logearse/', LoginView.as_view(), name='logearse'),
    path('logout/', cerrar_sesion, name='logout'),
    path('', PaginaPrincipal.as_view(), name='paginaPrincipal'),
    path('consultorio/', PaginaClinica.as_view(), name='paginaClinica'),
    path('laboratorio/', PaginaLaboratorio.as_view(), name='paginaLaboratorio'),
    path('home/', home, name='home'),
    #Sala de Espera
    path('expediente/', include('modulo_expediente.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('control/', include('modulo_control.urls')),
    path('laboratorio/', include('modulo_laboratorio.urls')),
    path('publicidad/', include('modulo_publicidad.urls'))

]
urlpatterns += staticfiles_urlpatterns()

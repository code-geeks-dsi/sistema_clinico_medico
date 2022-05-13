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
from modulo_control.views import vista_iniciarsesion, logearse
# from modulo_expediente.views import vista_sala_espera

urlpatterns = [
    path('admin/', admin.site.urls),
    #Login
    path('login/', vista_iniciarsesion, name='login'),
    path('logearse/', logearse, name='logearse'),
    path('', RedirectView.as_view(url='login/')),
    #Sala de Espera
    path('expediente/', include('modulo_expediente.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('control/', include('modulo_control.urls')),

]
urlpatterns += staticfiles_urlpatterns()

#Python

#Django
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView

#Propias

##La url de esta pagina se invoca desde el archivo principal de url
class InicioPublicidad(TemplateView):
    template_name = "publicidad/administracion/inicio.html"

class ClinicaPublicidad(TemplateView):
    template_name = "publicidad/administracion/tablaPublicidad.html"

# Publicaciones
class CrearPromocion(TemplateView):
    template_name = "publicidad/administracion/crearActualizar.html"
    

class EditarPromocion(TemplateView):
    template_name = "publicidad/administracion/crearActualizar.html"
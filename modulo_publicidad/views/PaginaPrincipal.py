#Python

#Django
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView

#Propias

##La url de esta pagina se invoca desde el archivo principal de url
class PaginaPrincipal(TemplateView):
    template_name = "publicidad/paginaPrincipal/paginaPrincipal.html"

class PaginaClinica(TemplateView):
    template_name= "publicidad/paginaDeClinica/paginaDeClinica.html"
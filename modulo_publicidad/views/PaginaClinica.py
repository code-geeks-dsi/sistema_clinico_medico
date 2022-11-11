#Python

#Django
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView
from modulo_publicidad.models import *
from modulo_expediente.models import TipoConsulta


class PaginaClinica(TemplateView):
    template_name= "publicidad/paginaDeClinica/paginaDeClinica.html"

class SeccionServiciosMedicos(TemplateView):
    template_name="publicidad/paginaDeClinica/secciones/serviciosMedicos.html"
    #consultando los servicios medicos
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["serviciosMedicos"] = ServicioMedico.objects.all()
        return context
        
    
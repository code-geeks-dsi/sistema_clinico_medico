#Python

#Django
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView
from modulo_publicidad.models import *
from modulo_expediente.models import TipoConsulta


class PaginaClinica(TemplateView):
    template_name= "publicidad/paginaDeClinica/paginaDeClinica.html"

class SeccionServiciosMedicos(View):
    template_name="publicidad/paginaDeClinica/secciones/serviciosMedicos.html"
    #consultando los servicios medicos
    def get(self, request, *args, **kwargs):
        servicioMedico= ServicioMedico.objects.all()
        imagen=ImagenServicio.objects.all()
        data={
            'serviciosMedicos':servicioMedico,
            'imagenes':imagen
        }
        
        return render(request, self.template_name, data)
        
    
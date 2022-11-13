#Python

#Django
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView
from modulo_publicidad.models import *
class PaginaLaboratorio(TemplateView):
    template_name= "publicidad/paginaDeLaboratorio/paginaDeLaboratorio.html"

class SeccionServiciosLaboratorio(View):
    template_name="publicidad/paginaDeLaboratorio/secciones/serviciosLaboratorio.html"
    #consultando los servicios medicos
    def get(self, request, *args, **kwargs):
        serviciolaboratorio= ServicioLaboratorioClinico.objects.all()
        imagen=ImagenServicio.objects.all()
        data={
            'servicioslaboratorios':serviciolaboratorio,
            'imagenes':imagen
        }
        
        return render(request, self.template_name, data)
#Django
from django.views.generic import ListView
from django.views import View
from django.shortcuts import render
from modulo_publicidad.forms import PublicacionForm, PublicacionImagenForm, ServicioMedicoForm
#Propias
from modulo_publicidad.models import *

class ServiciosMedicosListView(ListView):
    model=ServicioMedico
    paginate_by = 10
    template_name= "servicios/medicos/lista.html"

class crearServicioMedico(View):
    template_name="servicios/medicos/crear_editar.html"

    def get(self, request, *args, **kwargs):
        data={
            'formServicioMedico':ServicioMedicoForm(),
            'formPublicacion':PublicacionForm(),
            'formImagen':PublicacionImagenForm()
        }
        return render(request, self.template_name, data)

#Django
from django.views.generic import ListView
#Propias
from modulo_publicidad.models import *

class ServiciosMedicosListView(ListView):
    model=ServicioMedico
    paginate_by = 1
    template_name= "servicios/medicos/lista.html"
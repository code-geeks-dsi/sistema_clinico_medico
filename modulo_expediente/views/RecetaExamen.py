from django.shortcuts import redirect, render
from datetime import datetime

from modulo_control.models import Doctor
from modulo_expediente.forms import ConstanciaMedicaForm
from django.http import JsonResponse
from django.urls import reverse
from dateutil.relativedelta import relativedelta
from django.views.generic import View, TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import Http404

##Libreria Propias
from modulo_expediente.models import (Consulta,ContieneConsulta,ConstanciaMedica)
from modulo_laboratorio.models import (Categoria)

class RecetaExamenView(TemplateView):
    template_name = 'expediente/recetaExamen/create_update.html'

    def get(self, request, *args, **kwargs):
        ##Datos de la consulta
        id_consulta=int(self.kwargs['id_consulta'])
        contiene_consulta=ContieneConsulta.objects.get(consulta__id_consulta=id_consulta)
        categorias=Categoria.objects.all()
        paciente=contiene_consulta.expediente.id_paciente
        edad = relativedelta(datetime.now(), paciente.fecha_nacimiento_paciente)
        return render(request, self.template_name, {'Categoria':categorias,'id_consulta':id_consulta, 'paciente':paciente, 'edad': edad})

"""  def post(self, request, *args, **kwargs):
        id_consulta=int(self.kwargs['id_consulta']) 
        form = self.form_class(request.POST)
        if form.is_valid():
            referencia_medica=form.save(commit=False)
            referencia_medica.consulta=Consulta.objects.get(id_consulta=id_consulta)
            referencia_medica.save()
            return redirect(reverse('referencia-medica-update',
                            kwargs={'id_consulta': id_consulta,'id_referencia':referencia_medica.id_referencia_medica},))
"""

""" class ReferenciaMedicaUpdate(View):
    form_class = ReferenciaMedicaForm
    template_name = 'expediente/referencia/create_update_referencia_medica.html'

    def get(self, request, *args, **kwargs):
        ##Datos de la consulta
        id_consulta=int(self.kwargs['id_consulta'])
        contiene_consulta=ContieneConsulta.objects.get(consulta__id_consulta=id_consulta)
        consulta=contiene_consulta.consulta
        paciente=contiene_consulta.expediente.id_paciente
        edad = relativedelta(datetime.now(), paciente.fecha_nacimiento_paciente)

        id_referencia=int(self.kwargs['id_referencia']) 
        initial_data={'id_referencia_medica':int(id_referencia)}
        form = self.form_class(instance=ReferenciaMedica.objects.get(**initial_data))
        return render(request, self.template_name, {'form': form, 'update':True, 'id_consulta':id_consulta, 'paciente':paciente, 'edad': edad})

    def post(self, request, *args, **kwargs):
        id_referencia=int(self.kwargs['id_referencia']) 
        initial_data={'id_referencia_medica':int(id_referencia)}
        form = self.form_class(request.POST, instance=ReferenciaMedica.objects.get(**initial_data))
        if form.is_valid():
            form.save()
            response={
                'type':'success',
                'data':'Guardado!'
            }
            return JsonResponse(response)
 """

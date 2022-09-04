from django.shortcuts import redirect, render
from datetime import datetime
from modulo_expediente.models import (
    ConstanciaMedica, Consulta, Dosis,ContieneConsulta, Expediente, 
    RecetaMedica, SignosVitales,ReferenciaMedica)
from ..forms import ( ConsultaFormulario, ControlSubsecuenteform,  DosisFormulario, 
                        HojaEvolucionForm, SignosVitalesForm,antecedentesForm, CitaConsultaForm)
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.views.generic import View, TemplateView
from django.http import Http404

#view Para Consulta
##Para acceder a esto es necesario que el usuario tenga el permiso para editar consulta
class ConsultaView(PermissionRequiredMixin, TemplateView):
    permission_required = ('modulo_expediente.change_consulta')
    template_name = "expediente/consulta/consulta.html"
    login_url='/login/'  

    def get(self, request, *args, **kwargs):
        id_consulta=self.kwargs['id_consulta'] 
        try:
            #Consultando Instancias
            contiene_consulta=ContieneConsulta.objects.filter(consulta__id_consulta=id_consulta).order_by('-fecha_de_cola').first()
            paciente=contiene_consulta.expediente.id_paciente
            expediente=contiene_consulta.expediente.id_expediente
            consulta=contiene_consulta.consulta   
            receta=RecetaMedica.objects.filter(consulta=consulta).first()
            # receta=RecetaMedica.objects.filter(consulta=consulta).latest('fecha')
            dosis=Dosis.objects.filter(receta_medica=receta)
            consulta_form=ConsultaFormulario(instance=consulta)
            edad = relativedelta(datetime.now(), paciente.fecha_nacimiento_paciente)
            referencias_medicas= ReferenciaMedica.objects.filter(consulta=consulta)
            constancias_medicas=ConstanciaMedica.objects.filter(consulta=consulta)
            cita_form=CitaConsultaForm()
            cita_form.fields['expediente'].initial=expediente
            
            datos={
                'paciente':paciente,
                'id_consulta':id_consulta,
                'id_expediente':expediente,
                'id_receta':receta.id_receta_medica,
                'consulta_form':consulta_form,
                'signos_vitales_form':SignosVitalesForm(),
                'hoja_evolucion_form':HojaEvolucionForm(),
                'control_subsecuente_form':ControlSubsecuenteform(),
                'antecedentes_form':antecedentesForm(instance=contiene_consulta.expediente),
                'edad':edad,
                'dosis_form':DosisFormulario(),
                'dosis':dosis,
                'referencias':referencias_medicas,
                'constancias_medicas':constancias_medicas,
                'cita_form':cita_form
            }
        except ContieneConsulta.DoesNotExist:
            raise Http404("Consulta no encontrada")
        return render(request, self.template_name, datos)
    
    def post(self, request, *args, **kwargs):
        consulta_form=ConsultaFormulario(request.POST, instance=Consulta.objects.get(id_consulta=self.kwargs['id_consulta']))
        if consulta_form.is_valid():
            consulta=consulta_form.save()
            ContieneConsulta.objects.filter(consulta=consulta).update(fase_cola_medica='6')
            messages.add_message(request=request, level=messages.SUCCESS, message="Consulta Guardada!")
            return redirect(reverse('editar_consulta', kwargs={'id_consulta':consulta.id_consulta}))

##Se sustituyo la funcion de ancedentes por una clase
class antecedentesUpdateView(PermissionRequiredMixin, View):
    permission_required = ('modulo_expediente.change_consulta')
    login_url='/login/'

    def post(self, request, *args, **kwargs):
        id_expediente=self.kwargs['id_expediente'] 
        expediente = Expediente.objects.get(id_expediente=id_expediente)
        form = antecedentesForm(request.POST, instance=expediente)
        if form.is_valid():
            form.save()
            response={
                'type':'success',
                'data':'Guardado!',
                'antecedentes_personales':form.cleaned_data['antecedentes_personales'],
                'antecedentes_familiares':form.cleaned_data['antecedentes_familiares']
            }

        else:
            response={
                'type':'warning',
                'data':'No se pudo guardar. Intente de nuevo.'
            }
        return JsonResponse(response)

    
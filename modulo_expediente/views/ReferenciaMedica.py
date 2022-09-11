from django.shortcuts import redirect, render
from datetime import datetime
from modulo_control.models import Doctor
from modulo_expediente.models import (
        Consulta, ContieneConsulta,SignosVitales,ReferenciaMedica) 
from modulo_expediente.forms import ReferenciaMedicaForm 
from django.http import JsonResponse
from django.urls import reverse
from dateutil.relativedelta import relativedelta
from django.views.generic import View
from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string
import tempfile

class ReferenciaMedicaView(View):
    form_class = ReferenciaMedicaForm
    template_name = 'expediente/referencia/create_update_referencia_medica.html'

    def get(self, request, *args, **kwargs):
        ##Datos de la consulta
        id_consulta=int(self.kwargs['id_consulta'])
        contiene_consulta=ContieneConsulta.objects.get(consulta__id_consulta=id_consulta)
        consulta=contiene_consulta.consulta
        paciente=contiene_consulta.expediente.id_paciente
        edad = relativedelta(datetime.now(), paciente.fecha_nacimiento_paciente)
        ##Formulario
        form = self.form_class()
        form.fields['consulta_por'].initial=consulta.consulta_por
        return render(request, self.template_name, {'form': form, 'id_consulta':id_consulta, 'paciente':paciente, 'edad': edad})

    def post(self, request, *args, **kwargs):
        id_consulta=int(self.kwargs['id_consulta']) 
        form = self.form_class(request.POST)
        if form.is_valid():
            referencia_medica=form.save(commit=False)
            referencia_medica.consulta=Consulta.objects.get(id_consulta=id_consulta)
            referencia_medica.save()
            return redirect(reverse('referencia-medica-update',
                            kwargs={'id_consulta': id_consulta,'id_referencia':referencia_medica.id_referencia_medica},))

class ReferenciaMedicaUpdate(View):
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



class ReferenciaMedicaPdfView(View):
        def get(self, request, *args, **kwargs):
            id_consulta=int(self.kwargs['id_consulta'])
            id_referencia_medica=int(self.kwargs['id_referencia_medica'])
            doctora=Doctor.objects.get(empleado=request.user)
            jvmp=doctora.jvmp
            #Colsultando datos ddel paciente
            contiene_consulta=ContieneConsulta.objects.get(consulta__id_consulta=id_consulta)
            paciente=contiene_consulta.expediente.id_paciente
            edad = relativedelta(datetime.now(), paciente.fecha_nacimiento_paciente)
            #Consultando signos vitales
            signos_vitales=SignosVitales.objects.filter(consulta=contiene_consulta.consulta)
            #Consultando datos de referencia
            referencia_medica=ReferenciaMedica.objects.get(id_referencia_medica=id_referencia_medica)

            data={'paciente':paciente,'edad':edad,'signos_vitales':signos_vitales,'referencia_medica':referencia_medica,'nombre':doctora,'jvmp':jvmp}
            #generando pdf
            #puede recibir la info como diccionario
            html_string = render_to_string('expediente/referencia/reporteReferenciaMedica.html',data)
            html = HTML(string=html_string, base_url=request.build_absolute_uri())
            result = html.write_pdf()
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="referenciaMedica.pdf"'
            response['Content-Transfer-Encoding'] = 'binary'
            #Crea un archivo temporal
            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()
                output = open(output.name, 'rb')
                response.write(output.read())
            return response
  


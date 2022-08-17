from django.shortcuts import redirect, render
from datetime import datetime
from modulo_expediente.models import (Consulta,ContieneConsulta,ConstanciaMedica)
from modulo_control.models import Doctor
from modulo_expediente.forms import ConstanciaMedicaForm
from django.http import JsonResponse
from django.urls import reverse
from dateutil.relativedelta import relativedelta
from django.views import View 
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string
import tempfile
from django.http import Http404

class ConstanciaMedicaPDFView(View):

    def get(self, request, *args, **kwargs):
        id_consulta=int(self.kwargs['id_consulta'])
        #Consultando datos de la doctora
        doctora=Doctor.objects.get(empleado=request.user)
        jvmp=doctora.jvmp
        #consultando datos del paciente
        contiene_consulta=ContieneConsulta.objects.get(consulta__id_consulta=id_consulta)
        paciente=contiene_consulta.expediente.id_paciente
        edad = relativedelta(datetime.now(), paciente.fecha_nacimiento_paciente)
        constanciamedica=ConstanciaMedica.objects.get(consulta__id_consulta=id_consulta)
        data={'nombre':doctora,'jvmp':jvmp,'paciente':paciente,'edad':edad, 'constanciamedica':constanciamedica}
        #generando pdf
        #puede recibir la info como diccionario
        html_string = render_to_string('expediente/constancia/reporteConstanciaMedica.html',data)
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="constanciaMedica.pdf"'
        response['Content-Transfer-Encoding'] = 'binary'
        #Crea un archivo temporal
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
        return response
    def post(self, request, *args, **kwargs): 
        #crear constancia medica
        pass

    def put(self, request, *args, **kwargs): 
        #update constancia medica
        pass


class ConstanciaMedicaCreate(CreateView):
    model = ConstanciaMedica
    template_name = 'expediente/crear_constancia_medica.html'
    fields = ['dias_reposo','fecha_de_emision','consulta','diagnostico_constancia',]
    success_url = reverse_lazy('constancia-medica',
                            kwargs={'id': 1},)


class ConstanciaMedicaView(View):
    form_class = ConstanciaMedicaForm
    template_name = 'expediente/constancia/create_update_constancia_medica.html'

    def get(self, request, *args, **kwargs):
        id_consulta=int(self.kwargs['id_consulta'])
        #Verificar si existe constancia medica
        try: 
            constancia_medica= ConstanciaMedica.objects.get(consulta__id_consulta=id_consulta)
            return redirect(reverse('constancia-medica-update',
                            kwargs={'id_consulta': id_consulta,'id_constancia':constancia_medica.id_constancia_medica},))
        #Si no se ha creado la constancia
        except ConstanciaMedica.DoesNotExist:
            #Datos de la consulta
            contiene_consulta=ContieneConsulta.objects.get(consulta__id_consulta=id_consulta)
            paciente=contiene_consulta.expediente.id_paciente
            edad = relativedelta(datetime.now(), paciente.fecha_nacimiento_paciente)
            ##Formulario
            form = self.form_class()
            form.fields['diagnostico_constancia'].initial=contiene_consulta.consulta.consulta_por
            return render(request, self.template_name, {'form': form, 'id_consulta':id_consulta, 'paciente':paciente, 'edad': edad})

    def post(self, request, *args, **kwargs):
        id_consulta=int(self.kwargs['id_consulta']) 
        form = self.form_class(request.POST)
        if form.is_valid():
            constancia_medica=form.save(commit=False)
            constancia_medica.consulta=Consulta.objects.get(id_consulta=id_consulta)
            constancia_medica.save()
            return redirect(reverse('constancia-medica-update',
                            kwargs={'id_consulta': id_consulta,'id_constancia':constancia_medica.id_constancia_medica},))
       
class ConstanciaMedicaUpdate(View):
    form_class = ConstanciaMedicaForm
    template_name = 'expediente/constancia/create_update_constancia_medica.html'

    def get(self, request, *args, **kwargs):
        #Datos de la consulta
        id_consulta=int(self.kwargs['id_consulta'])
        try:
            contiene_consulta=ContieneConsulta.objects.get(consulta__id_consulta=id_consulta)
            paciente=contiene_consulta.expediente.id_paciente
            edad = relativedelta(datetime.now(), paciente.fecha_nacimiento_paciente)
            #Datos de la constancia
            id_constancia=int(self.kwargs['id_constancia']) 
            initial_data={'id_constancia_medica':int(id_constancia)}
            form = self.form_class(instance=ConstanciaMedica.objects.get(**initial_data))
            return render(request, self.template_name, {'form': form, 'update':True, 'id_consulta':id_consulta, 'paciente':paciente, 'edad': edad})
        except ConstanciaMedica.DoesNotExist:
            raise Http404("Constancia médica no encontrada.")

    def post(self, request, *args, **kwargs):
        id_constancia=int(self.kwargs['id_constancia']) 
        initial_data={'id_constancia_medica':int(id_constancia)}
        form = self.form_class(request.POST, instance=ConstanciaMedica.objects.get(**initial_data))
        if form.is_valid():
            form.save()
            response={
                'type':'success',
                'data':'Guardado!'
            }
            return JsonResponse(response)

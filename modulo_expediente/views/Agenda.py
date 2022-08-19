#Django
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.utils import timezone

#Librerias Propias
from modulo_expediente.models import CitaConsulta
from modulo_control.models import Empleado
from ..forms import CitaConsultaForm, CitaConsultaSecretariaForm
from ..serializers import CitaConsultaSerializer

#View Para imprimir Agenda
class AgendaView(TemplateView):
    response={'type':'','data':''}
    template_name = "expediente/agenda.html"  
    def get(self, request, *args, **kwargs):
        form=CitaConsultaSecretariaForm()
        form.fields['empleado'].queryset = Empleado.objects.filter(roles__codigo_rol='ROL_DOCTOR')
        return render(request, self.template_name, {'form':form})

    #Crear citas
    def post(self, request, *args, **kwargs):
        form = CitaConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            self.response['type']='success'
            self.response['data']='Cita Programada'
        else:
            self.response['type']='warning'
            self.response['data']='No se pudo guardar. Intente de nuevo.'
        return JsonResponse(self.response)

class CitaConsultaView(View):
    response={'type':'','data':''}
    #Regresa con json con las citas del mes
    def get(self, request, *args, **kwargs):
        fecha=timezone.now()
        citas=CitaConsulta.objects.filter(fecha_cita__year=fecha.year, fecha_cita__month=fecha.month)
        serializer=CitaConsultaSerializer(citas, many= True)
        return JsonResponse(serializer.data, safe=False)

    #Crear citas
    def post(self, request, *args, **kwargs):
        id_expediente=self.kwargs['id_expediente'] 
        form = CitaConsultaForm(request.POST)
        if form.is_valid():
            cita=form.save(commit=False)
            cita.empleado=request.user
            cita.save()
            self.response['type']='success'
            self.response['data']='Cita Programada'
        else:
            self.response['type']='warning'
            self.response['data']='No se pudo guardar. Intente de nuevo.'
        return JsonResponse(self.response)
        
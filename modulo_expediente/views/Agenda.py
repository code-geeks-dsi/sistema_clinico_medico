#Django
from django.http import JsonResponse
from django.views.generic import View, TemplateView
from django.utils import timezone

#Librerias Propias
from modulo_expediente.models import CitaConsulta
from ..forms import CitaConsultaForm
from ..serializers import CitaConsultaSerializer

#View Para imprimir Agenda
class AgendaView(TemplateView):
    template_name = "expediente/agenda.html"  

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
        
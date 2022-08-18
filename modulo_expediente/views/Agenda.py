#Django
from django.http import JsonResponse
from django.views.generic import View
#Librerias Propias
from ..forms import CitaConsultaForm

class CrearCitaConsultaView(View):
    response={'type':'','data':''}

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
        
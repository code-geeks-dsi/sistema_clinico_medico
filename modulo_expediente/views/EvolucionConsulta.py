from datetime import datetime
from modulo_expediente.forms import HojaEvolucionForm
from modulo_expediente.models import Consulta, EvolucionConsulta
from django.http import JsonResponse
from django.views.generic import View
from django.db.models import F, Func, Value, CharField
from django.urls import reverse_lazy

class CreateHojaEvolucion(View):
    form_class = HojaEvolucionForm

    def post(self, request, *args, **kwargs):
        id_consulta=int(self.kwargs['id_consulta']) 
        form = self.form_class(request.POST)
        if form.is_valid():
            nota=form.save(commit=False)
            nota.fecha=datetime.now()
            nota.consulta=Consulta.objects.get(id_consulta=id_consulta)
            nota.save()
            response={
                'type':'success',
                'data':'Guardado!'
            }
            return JsonResponse(response) 

class ListaHojaEvolucion(View):
    def get(self, request, *args, **kwargs):
        id_consulta=int(self.kwargs['id_consulta'])
        data = list(EvolucionConsulta.objects.filter(consulta__id_consulta=id_consulta).annotate(
        fecha_hora=Func(
            F('fecha'),
            Value('DD/MM/YYYY HH:MI:SS'),
            function='to_char',
            output_field=CharField()
        )).values('observacion','fecha_hora','id_evolucion', 'consulta'))
        for item in data:
            item['delete_url']=reverse_lazy('hoja-evolucion-delete',
                            kwargs={'id_consulta': item['consulta'],
                            'id_nota_evolucion': item['id_evolucion']},)
        return JsonResponse({'data':data}) 

class DeleteNotaEvolucion(View):
    def post(self, request, *args, **kwargs):
        id_nota_evolucion=int(self.kwargs['id_nota_evolucion'])
        try:
            nota=EvolucionConsulta.objects.get(id_evolucion=id_nota_evolucion)
            if(EvolucionConsulta.objects.validar_caducidad(nota)):
                nota.delete()
                response={
                'type':'success',
                'data':'Eliminado!'
            }
            else:
                response={
                'type':'warning',
                'data':'El tiempo para eliminar esta nota ha caducado.'
            }


        except EvolucionConsulta.DoesNotExist:
            response={
                'type':'danger',
                'data':'Nota de Evolución no existe.'
            }
        
        return JsonResponse(response)

class UpdateNotaEvolucion(View):
    form_class = HojaEvolucionForm
    def post(self, request, *args, **kwargs):
        id_nota_evolucion=int(request.POST.get('id_evolucion'))
        try:
            nota=EvolucionConsulta.objects.get(id_evolucion=id_nota_evolucion)
            new_nota= self.form_class(request.POST,instance=nota)        
            if(EvolucionConsulta.objects.validar_caducidad(nota) and new_nota.is_valid()):
                new_nota.save()
                response={
                'type':'success',
                'data':'Guardado!'
            }
            else:
                response={
                'type':'warning',
                'data':'El tiempo aceptado para editar esta nota ha caducado.'
            }


        except EvolucionConsulta.DoesNotExist:
            response={
                'type':'danger',
                'data':'Nota de Evolución no existe.'
            }
        
        return JsonResponse(response)
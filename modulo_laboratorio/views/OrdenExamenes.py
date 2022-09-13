#Django
from django.http import JsonResponse, QueryDict
from django.urls import reverse
from dateutil.relativedelta import relativedelta
from django.views.generic import View, TemplateView
from django.shortcuts import redirect, render
from django.db.utils import IntegrityError
#Python 
from datetime import datetime

##Libreria Propias
from modulo_expediente.models import (Paciente)
from modulo_laboratorio.models import (Categoria, EsperaExamen, Resultado)
from modulo_laboratorio.serializers import Examenserializer, ResultadoSerializer

class OrdenExamenCreate(TemplateView):
    template_name = 'expediente/recetaExamen/create_update.html'
    response={'type':'','data':'', 'info':''}
    #Imprimir en pantalla el formulario de creación de orden
    def get(self, request, *args, **kwargs):
        ##Creando Orden
        id_paciente=int(self.kwargs['id_paciente'])
        orden=EsperaExamen.create(
            id_paciente=id_paciente
        )
        orden.save()
        return redirect(reverse('update_orden_examenes',
                            kwargs={'id_paciente':id_paciente,'id_orden':orden.id},))
    def delete(self, request, *args, **kwargs):
        id_consulta=int(self.kwargs['id_consulta'])
        data = QueryDict(request.body)
        RecetaOrdenExamenLaboratorio.objects.filter(
            id_receta_orden_examen_laboratorio=data['id_receta'],
            consulta_id=id_consulta
        ).delete()

        print(data)
        self.response['type']='success'
        self.response['data']='Receta de examenes eliminada.'

        return JsonResponse(self.response)


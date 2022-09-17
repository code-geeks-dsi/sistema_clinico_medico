#Django
from django.urls import reverse
from django.views.generic import  TemplateView
from django.shortcuts import redirect
from modulo_expediente.models import Expediente
##Libreria Propias
from modulo_laboratorio.models import ( EsperaExamen)
from modulo_laboratorio.views.Resultado import sync_cola
from datetime import datetime
from django.http import JsonResponse

class OrdenExamenCreate(TemplateView):

    def get(self, request, *args, **kwargs):
        self.response={}
        ##Creando Orden
        try:
            id_paciente=int(self.kwargs['id_paciente'])
            # revisar si la orden ya existe
            fecha_hoy=datetime.now()
            orden=EsperaExamen.objects.filter(expediente__id_paciente__id_paciente=id_paciente,fecha__year=fecha_hoy.year, 
                                fecha__month=fecha_hoy.month, 
                                fecha__day=fecha_hoy.day).first()
            if (orden is not None):
                if (orden.fase_examenes_lab==EsperaExamen.OPCIONES_FASE_ORDEN[0][0]
                    or orden.fase_examenes_lab==EsperaExamen.OPCIONES_FASE_ORDEN[1][0]):
                    self.response['type']='info'
                    self.response['title']='Orden de Exámenes Ya Existe!'
                    self.response['data']='Puede agregar examenes en la orden existente.'
                    return JsonResponse(self.response)
            orden=EsperaExamen.create(
                id_paciente=id_paciente
            )
            orden.save()
            sync_cola()
            self.response['type']='success'
            self.response['title']='Guardado!'
            self.response['data']='Orden En Recepcion de Muestras.'


        except Expediente.DoesNotExist:
            self.response['type']='error'
            self.response['title']='Error al crear orden de examenes.'
            self.response['data']='El expediente no existe'

        return JsonResponse(self.response)



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
from ..models import (ContieneConsulta, RecetaOrdenExamenLaboratorio, RecetaOrdenExamenLaboratorioItem)
from ..serializers import RecetaOrdenExamenLaboratorioItemSerializer
from modulo_laboratorio.models import (Categoria)
from modulo_laboratorio.serializers import Examenserializer

class RecetaExamenView(TemplateView):
    template_name = 'expediente/recetaExamen/create_update.html'
    response={'type':'','data':'', 'info':''}
    #Imprimir en pantalla el formulario de creación de orden
    def get(self, request, *args, **kwargs):
        ##Creando Orden
        id_consulta=int(self.kwargs['id_consulta'])
        receta=RecetaOrdenExamenLaboratorio.objects.create(
            consulta_id=id_consulta
        )
        return redirect(reverse('receta-examen-update',
                            kwargs={'id_consulta': id_consulta,'id_receta_examen':receta.id_receta_orden_examen_laboratorio},))
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

class RecetaExamenUpdate(View):
    template_name = 'expediente/recetaExamen/create_update.html'
    response={'type':'','data':'', 'info':''}
    #Imprimir en pantalla el formulario de creación de orden
    def get(self, request, *args, **kwargs):
        ##Datos de la consulta
        id_consulta=int(self.kwargs['id_consulta'])
        id_receta_examen=int(self.kwargs['id_receta_examen'])
        contiene_consulta=ContieneConsulta.objects.get(consulta__id_consulta=id_consulta)
        categorias=Categoria.objects.all()
        paciente=contiene_consulta.expediente.id_paciente
        edad = relativedelta(datetime.now(), paciente.fecha_nacimiento_paciente)
        item_recetas=RecetaOrdenExamenLaboratorioItem.objects.filter(receta_orden_examen_laboratorio=id_receta_examen)
        return render(request, self.template_name, {'Categoria':categorias,'id_consulta':id_consulta, 'paciente':paciente, 'edad': edad, 'item_recetas':item_recetas})
    
    #Actualizando/Se agregan items a la orden de examen
    def put(self, request, *args, **kwargs):
        id_receta_examen=int(self.kwargs['id_receta_examen'])
        data = QueryDict(request.body)
        try:
            item=RecetaOrdenExamenLaboratorioItem.objects.create(
                receta_orden_examen_laboratorio_id=id_receta_examen,
                examen_id=data['id_examen']
            )
            examen=Examenserializer(item.examen)
            numero=RecetaOrdenExamenLaboratorioItem.objects.filter(receta_orden_examen_laboratorio_id=id_receta_examen).count()
            self.response['data']='Examen agregado'
            self.response['type']='success'
            self.response['info']={
                'id_receta_examen':item.id_receta_orden_examen_laboratorio_item,
                'numero': numero,
                'examen': examen.data
            }
        except IntegrityError:
            self.response['type']='warning'
            self.response['data']='El examen ya existe en la orden.'
            return JsonResponse(self.response, status=500)
        return JsonResponse(self.response)

    ##Para eliminar
    def delete(self, request, *args, **kwargs):
        id_receta_examen=int(self.kwargs['id_receta_examen'])
        data = QueryDict(request.body)
        RecetaOrdenExamenLaboratorioItem.objects.filter(
            id_receta_orden_examen_laboratorio_item=data['id_item'],
            receta_orden_examen_laboratorio_id=id_receta_examen
        ).delete()
        recetasItems=RecetaOrdenExamenLaboratorioItem.objects.filter(receta_orden_examen_laboratorio_id=id_receta_examen)
        recetasItems=RecetaOrdenExamenLaboratorioItemSerializer(recetasItems, many=True)

        self.response['type']='success'
        self.response['data']='Examen removido de la orden.'
        self.response['info']=recetasItems.data
        return JsonResponse(self.response)

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
from modulo_expediente.models import (Paciente, RecetaOrdenExamenLaboratorio, RecetaOrdenExamenLaboratorioItem)
from modulo_expediente.serializers import RecetaOrdenExamenLaboratorioItemSerializer
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

class OrdenExamenUpdate(View):
    template_name = 'laboratorio/recetaExamen/create_update.html'
    response={'type':'','data':'', 'info':''}
    #Imprimir en pantalla el formulario de creación de orden
    def get(self, request, *args, **kwargs):
        ##Datos de la consulta
        id_paciente=int(self.kwargs['id_paciente'])
        id_orden=int(self.kwargs['id_orden'])
        # id_receta_examen=int(self.kwargs['id_receta_examen'])
        # contiene_consulta=ContieneConsulta.objects.get(consulta__id_consulta=id_consulta)
        categorias=Categoria.objects.all()
        paciente=Paciente.objects.get(id_paciente=id_paciente)
        edad = relativedelta(datetime.now(), paciente.fecha_nacimiento_paciente)
        resultados=Resultado.objects.filter(orden_de_laboratorio=id_orden)
        return render(request, self.template_name, {'Categoria':categorias, 'paciente':paciente, 'edad': edad, 'item_recetas':resultados})
    
    #Actualizando/Se agregan items a la orden de examen
    def put(self, request, *args, **kwargs):
        id_paciente=int(self.kwargs['id_paciente'])
        id_orden=int(self.kwargs['id_orden'])
        data = QueryDict(request.body)
        try:
            item=Resultado.create(
                id_examen=data['id_examen'],
                id_orden=id_orden
            )
            item.save()
            examen=ResultadoSerializer(item)
            numero=Resultado.objects.filter(orden_de_laboratorio=id_orden).count()
            self.response['data']='Examen agregado'
            self.response['type']='success'
            self.response['info']={
                'id_resultado':item.id_resultado,
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
        id_orden=int(self.kwargs['id_orden'])
        data = QueryDict(request.body)
        resultado=Resultado.objects.filter(
            id_resultado=data['id_resultado']
        )
        resultado.delete()
        recetasItems=Resultado.objects.filter(orden_de_laboratorio=id_orden)
        recetasItems=ResultadoSerializer(recetasItems, many=True)

        self.response['type']='sucess'
        self.response['data']='Examen Eliminado!'
        self.response['info']=recetasItems.data
        return JsonResponse(self.response)

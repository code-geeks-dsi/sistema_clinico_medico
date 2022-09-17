import json
from unittest import result
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from datetime import datetime
from django.db.models import Q
from modulo_laboratorio.serializers import ResultadoLaboratorioSerializer, ResultadoSerializer
from .models import EsperaExamen, Resultado
from django.urls import reverse
from channels.exceptions import StopConsumer
from dateutil.relativedelta import relativedelta

class ColaLaboratorioConsumer(WebsocketConsumer):
      
        def cola_ordenes(self,data):
                lista=[]
                espera_examen=EsperaExamen.objects.filter(~Q(fase_examenes_lab=EsperaExamen.OPCIONES_FASE_ORDEN[3][0])).select_related('expediente__id_paciente').order_by('numero_cola_orden')
                for fila in espera_examen:
                        diccionario={
                        "numero_cola_orden":"",
                        "nombre":"",
                        "apellidos":"",
                        "fase_examenes_lab":"",
                        "fecha":"",
                        "estado_pago_laboratorio":"",
                        }
                        edad=relativedelta(datetime.now(), fila.expediente.id_paciente.fecha_nacimiento_paciente).years 
                        diccionario["numero_cola_orden"]= fila.numero_cola_orden
                        diccionario["nombre"]=fila.expediente.id_paciente.nombre_paciente
                        diccionario["apellidos"]=fila.expediente.id_paciente.apellido_paciente
                        diccionario["fase_examenes_lab"]= fila.get_fase_examenes_lab_display()
                        diccionario["fecha"]=fila.fecha.strftime("%d/%b/%Y")
                        diccionario["estado_pago_laboratorio"]= fila.get_estado_pago_laboratorio_display()
                        #  en caso de ser secretaria la url debe de cambiarse a cambiar fase
                        diccionario["id_expediente"]= fila.expediente.id_expediente
                        diccionario["url_orden_examenes"]= reverse('update_orden_examenes',kwargs={'id_paciente':fila.expediente.id_paciente.id_paciente,'id_orden':fila.id})
                        lista.append(diccionario)
                        del diccionario
                if len(lista)==0:
                        response={
                        'type':'warning',
                        'data':'No hay examenes pendientes'
                        }
                else:
                        response={'data':lista}
                print('cola_ordenes')
                return self.send(text_data=json.dumps(response))

        def cola_de_resultados_por_orden_de_laboratorio(self,data):
                id_orden=self.scope["url_route"]["kwargs"]["id_orden"]
                resultados=Resultado.objects.filter(orden_de_laboratorio__id=id_orden).select_related('orden_de_laboratorio__expediente__id_paciente').order_by('numero_cola_resultado')
                resultados=ResultadoSerializer(resultados,many=True)
        
                if len(resultados.data)==0:
                        response={
                        'type':'warning',
                        'data':'No hay examenes pendientes'
                        }
                else:
                        url_orden_pdf=reverse('generar_orden_pdf',kwargs={'orden_id':id_orden})
                        orden=EsperaExamen.objects.get(id=id_orden)
                        if (orden.fase_examenes_lab==EsperaExamen.OPCIONES_FASE_ORDEN[2][0]):
                                puede_descargar=True
                        else: puede_descargar=False
                        response={
                                'data':resultados.data,
                                'url_orden_pdf':url_orden_pdf,
                                'puede_descargar':puede_descargar
                                }
                print('cola_de_resultados_por_orden_de_laboratorio')
                return self.send(text_data=json.dumps(response))

        def cola_de_resultados(self,data):
                resultados=Resultado.objects.filter(fase_examenes_lab=Resultado.OPCIONES_FASE[1][0]).select_related('orden_de_laboratorio__expediente__id_paciente').order_by('numero_cola_resultado')                
                resultados=ResultadoLaboratorioSerializer(resultados,many=True)
                if len(resultados.data)==0:
                        response={
                        'type':'warning',
                        'data':'No hay examenes pendientes'
                        }
                else:
                        response={'data':resultados.data}
                print('cola_de_resultados')
                return self.send(text_data=json.dumps(response))

        
        def connect(self):
                self.room_group_name=self.scope["url_route"]["kwargs"]["tipo"]
                async_to_sync(self.channel_layer.group_add)(
                        self.room_group_name,
                        self.channel_name
                        )
                self.accept()
                # if(self.room_group_name=='cola_de_resultados' or
                # self.room_group_name=='cola_ordenes'):
                async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {'type':self.room_group_name}
                )
                # else:   
                #         id_orden=self.scope["url_route"]["kwargs"]["id_orden"]
                #         async_to_sync(self.channel_layer.group_send)(
                #                 self.room_group_name,
                #                 {
                #                         'type':self.room_group_name,
                #                         'id_orden':id_orden
                #                 }
                #         )


        # def receive(self,text_data):
        #         text_data_json = json.loads(text_data)
        #         data={
        #                 'type':self.room_group_name
        #         }
        #         try:
        #                 id_orden = text_data_json['id_orden']
        #                 data["id_orden"]=id_orden
        #         except:
        #                 id_orden=None
        #         async_to_sync(self.channel_layer.group_send)(
        #                 self.room_group_name,
        #                 data
        #         )
        def disconnect(self, code):
                # super().disconnect(code)
                raise StopConsumer()
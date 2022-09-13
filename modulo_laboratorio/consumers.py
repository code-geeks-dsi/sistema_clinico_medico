import json
from unittest import result
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from datetime import datetime

from modulo_laboratorio.serializers import ResultadoLaboratorioSerializer, ResultadoSerializer
from .models import EsperaExamen, Resultado
from django.urls import reverse
from channels.exceptions import StopConsumer
from dateutil.relativedelta import relativedelta

class ColaLaboratorioConsumer(WebsocketConsumer):
      
        def cola_ordenes(self):
                fecha_hoy=datetime.now()
                lista=[]
                espera_examen=EsperaExamen.objects.filter(fecha__year=fecha_hoy.year, 
                                        fecha__month=fecha_hoy.month, 
                                        fecha__day=fecha_hoy.day).select_related('expediente__id_paciente').order_by('numero_cola_orden')
                   
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
                return self.send(text_data=json.dumps(response))

        def cola_de_resultados_por_orden_de_laboratorio(self,id_orden):
                fecha_hoy=datetime.now()
                lista=[]
                resultados=Resultado.objects.filter(orden_de_laboratorio__id=id_orden).select_related('orden_de_laboratorio__expediente__id_paciente').order_by('numero_cola_resultado')
                resultados=ResultadoSerializer(resultados,many=True)
        
                if len(resultados.data)==0:
                        response={
                        'type':'warning',
                        'data':'No hay examenes pendientes'
                        }
                else:
                        response={'data':resultados.data}
                return self.send(text_data=json.dumps(response))

        def cola_de_resultados(self):
                fecha_hoy=datetime.now()
                lista=[]
                resultados=Resultado.objects.filter(fase_examenes_lab=EsperaExamen.OPCIONES_FASE[1][0]).select_related('expediente__id_paciente').order_by('numero_cola_resultado')                
                resultados=ResultadoLaboratorioSerializer(resultados,many=True)
                if len(resultados.data)==0:
                        response={
                        'type':'warning',
                        'data':'No hay examenes pendientes'
                        }
                else:
                        response={'data':resultados.data}
                # return self.send(text_data=json.dumps(response))
                return self.send(text_data=response)


        def cola_laboratorio(self,event):
                id_orden = event['id_orden']
                tipo=event['tipo']
                print(id_orden)
                print(tipo)
                if( tipo=='cola_de_resultados_por_orden_de_laboratorio'):
                        self.cola_de_resultados_por_orden_de_laboratorio(id_orden)
                elif ( tipo=='cola_de_resultados'):
                        self.cola_de_resultados()
        
        def connect(self):
                self.room_group_name='laboratorio'
                async_to_sync(self.channel_layer.group_add)(
                        self.room_group_name,
                        self.channel_name
                        )
                self.accept()
                # if(self.scope["user"].roles.codigo_rol=='ROL_SECRETARIA'):
                #         self.cola_inicial_ordenes()
                # else:
                #         self.cola_inicial_resultados()


        def receive(self,text_data):
                text_data_json = json.loads(text_data)
                id_orden = text_data_json['id_orden']
                tipo = text_data_json['tipo']

                async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                                'type':'cola_laboratorio',
                                'id_orden':id_orden,
                                'tipo':tipo
                        }
                )
        def disconnect(self, code):
                # super().disconnect(code)
                raise StopConsumer()
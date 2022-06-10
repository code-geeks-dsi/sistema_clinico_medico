import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from datetime import datetime
from modulo_laboratorio.models import EsperaExamen
from django.urls import reverse

class ColaLaboratorioConsumer(WebsocketConsumer):
        # def agregar_examen_cola(self):
        #         id_paciente=request.POST.get('id_paciente',0)
        #         id_examen_laboratorio=request.POST.get('id_examen_laboratorio',0)
        #         fecha_hoy=datetime.now()
        #         examen_item=EsperaExamen.objects.filter(expediente__id_paciente__id_paciente=id_paciente,resultado__examen_laboratorio__id_examen_laboratorio=id_examen_laboratorio,fecha__year=fecha_hoy.year, 
        #                                 fecha__month=fecha_hoy.month, 
        #                                 fecha__day=fecha_hoy.day).first()
        #         if examen_item is None:
        #                 examen_item=EsperaExamen.create(id_paciente,id_examen_laboratorio)
        #                 examen_item.save()
        #                 response={
        #                         'type':'success',
        #                         'title':'Guardado!',
        #                         'data':'Examen agregado a la cola'
        #                 }
        #         else:
        #                 response={
        #                         'type':'warning',
        #                         'data':'El examen ya existe en la cola!'
        #                 }
        #         return JsonResponse(response, safe=False)
        def cola_inicial(self):
                fecha_hoy=datetime.now()
                lista=[]
                if(self.scope["user"].roles.codigo_rol=='ROL_SECRETARIA'):
                        espera_examen=EsperaExamen.objects.filter(fecha__year=fecha_hoy.year, 
                                        fecha__month=fecha_hoy.month, 
                                        fecha__day=fecha_hoy.day).select_related('expediente__id_paciente').order_by('numero_cola_laboratorio')
                elif (self.scope["user"].roles.codigo_rol=='ROL_LIC_LABORATORIO'):
                                espera_examen=EsperaExamen.objects.filter(fase_examenes_lab=EsperaExamen.OPCIONES_FASE[1][0]).select_related('expediente__id_paciente').order_by('numero_cola_laboratorio')                
                        
                        
                for fila in espera_examen:
                        diccionario={
                        "numero_cola_laboratorio":"",
                        "nombre":"",
                        "apellidos":"",
                        "examen":"",
                        "fase_examenes_lab":"",
                        "fecha":"",
                        "consumo_laboratorio":"",
                        "estado_pago_laboratorio":"",
                        }
                        diccionario["numero_cola_laboratorio"]= fila.numero_cola_laboratorio
                        diccionario["nombre"]=fila.expediente.id_paciente.nombre_paciente
                        diccionario["apellidos"]=fila.expediente.id_paciente.apellido_paciente
                        diccionario["examen"]=fila.resultado.examen_laboratorio.nombre_examen
                        diccionario["fase_examenes_lab"]= fila.get_fase_examenes_lab_display()
                        diccionario["fecha"]=fila.fecha.strftime("%d/%b/%Y")
                        diccionario["consumo_laboratorio"]= str(fila.consumo_laboratorio)
                        diccionario["estado_pago_laboratorio"]= fila.get_estado_pago_laboratorio_display()
                        #  en caso de ser secretaria la url debe de cambiarse a cambiar fase
                        
                        diccionario["id_resultado"]= fila.resultado.id_resultado
                        diccionario["id_expediente"]= fila.expediente.id_expediente
                        if (self.scope["user"].roles.codigo_rol=='ROL_LIC_LABORATORIO'):
                                diccionario["url_resultado"]= reverse('elaborar_resultado',kwargs={'id_resultado':fila.resultado.id_resultado})
                        if (self.scope["user"].roles.codigo_rol=='ROL_SECRETARIA'):
                                diccionario["url_resultado_pdf"]= reverse('generar_pdf',kwargs={'id_resultado':fila.resultado.id_resultado})
                        lista.append(diccionario)
                        del diccionario
                if len(lista)==0:
                        response={
                        'type':'warning',
                        'data':'No hay examenes pendientes'
                        }
                else:
                        response={'data':lista}
                # return self.send(text_data=json.dumps({'data':response,'type':'laboratorio_cola'}))
                return self.send(text_data=json.dumps(response))
        def cola_laboratorio(self,event):
                fecha_hoy=datetime.now()
                lista=[]
                if(self.scope["user"].roles.codigo_rol=='ROL_SECRETARIA'):
                        espera_examen=EsperaExamen.objects.filter(fecha__year=fecha_hoy.year, 
                                        fecha__month=fecha_hoy.month, 
                                        fecha__day=fecha_hoy.day).select_related('expediente__id_paciente').order_by('numero_cola_laboratorio')
                elif (self.scope["user"].roles.codigo_rol=='ROL_LIC_LABORATORIO'):
                                espera_examen=EsperaExamen.objects.filter(fase_examenes_lab=EsperaExamen.OPCIONES_FASE[1][0]).select_related('expediente__id_paciente').order_by('numero_cola_laboratorio')                
                        
                        
                for fila in espera_examen:
                        diccionario={
                        "numero_cola_laboratorio":"",
                        "nombre":"",
                        "apellidos":"",
                        "examen":"",
                        "fase_examenes_lab":"",
                        "fecha":"",
                        "consumo_laboratorio":"",
                        "estado_pago_laboratorio":"",
                        }
                        diccionario["numero_cola_laboratorio"]= fila.numero_cola_laboratorio
                        diccionario["nombre"]=fila.expediente.id_paciente.nombre_paciente
                        diccionario["apellidos"]=fila.expediente.id_paciente.apellido_paciente
                        diccionario["examen"]=fila.resultado.examen_laboratorio.nombre_examen
                        diccionario["fase_examenes_lab"]= fila.get_fase_examenes_lab_display()
                        diccionario["fecha"]=fila.fecha.strftime("%d/%b/%Y")
                        diccionario["consumo_laboratorio"]= str(fila.consumo_laboratorio)
                        diccionario["estado_pago_laboratorio"]= fila.get_estado_pago_laboratorio_display()
                        #  en caso de ser secretaria la url debe de cambiarse a cambiar fase
                        
                        diccionario["id_resultado"]= fila.resultado.id_resultado
                        diccionario["id_expediente"]= fila.expediente.id_expediente
                        if (self.scope["user"].roles.codigo_rol=='ROL_LIC_LABORATORIO'):
                                diccionario["url_resultado"]= reverse('elaborar_resultado',kwargs={'id_resultado':fila.resultado.id_resultado})
                        if (self.scope["user"].roles.codigo_rol=='ROL_SECRETARIA'):
                                diccionario["url_resultado_pdf"]= reverse('generar_pdf',kwargs={'id_resultado':fila.resultado.id_resultado})
                        lista.append(diccionario)
                        del diccionario
                if len(lista)==0:
                        response={
                        'type':'warning',
                        'data':'No hay examenes pendientes'
                        }
                else:
                        response={'data':lista}
                # return self.send(text_data=json.dumps({'data':response,'type':'laboratorio_cola'}))
                return self.send(text_data=json.dumps(response))
        
        def connect(self):
                # print(self.scope["user"].rol_empleado)
                self.room_group_name='laboratorio'
                async_to_sync(self.channel_layer.group_add)(
                        self.room_group_name,
                        self.channel_name
                        )
                self.accept()
                # self.send(text_data=json.dumps({
                #         'type':'Connection established',
                #         'message':'You are now connected to lab!'}))
                #mandando la cola inicial
                # print(self.scope["method"])
                self.cola_inicial()
                

        # def receive(self,text_data):
        #         text_data_json=json.loads(text_data)
        #         message=text_data_json['message']
        #         async_to_sync(self.channel_layer.group_send)(
        #                 self.room_group_name,
        #                 {
        #                 'type':'laboratorio',
        #                 'message':message
        #                 }
        #         )
        def receive(self,text_data):
                text_data_json=json.loads(text_data)
                message=text_data_json['message']
                async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {'type':'cola_laboratorio'}
                )
        # def sync_cola_laboratorio(self):
        #         response=self.cola_laboratorio()
        #         async_to_sync(self.channel_layer.group_send)(
        #                 self.room_group_name,
        #                 {'data':response['data'],'type':'laboratorio_cola'}
        #         )
                
        # def cola_laboratorio(self, event):
        #         message=event['message']
        #         self.send(text_data=json.dumps({
        #                 'type':'chat',
        #                 'message':message
        #         }))
        
        
        # def disconnect(self, code):
        #         pass
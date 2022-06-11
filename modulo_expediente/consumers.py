import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from datetime import datetime
from modulo_expediente.models import ContieneConsulta
from channels.exceptions import StopConsumer
class ColaExpedienteConsumer(WebsocketConsumer):
       
        def cola_inicial(self):
                fecha=datetime.now()
                lista=[]
                rol=self.scope["user"].roles.codigo_rol

                if(rol=='ROL_SECRETARIA'):
                        contiene_consulta=ContieneConsulta.objects.filter(fecha_de_cola__year=fecha.year, 
                                        fecha_de_cola__month=fecha.month, 
                                        fecha_de_cola__day=fecha.day).select_related('expediente__id_paciente')
                        
                        for fila in contiene_consulta:
                                diccionario={
                                        "id_consulta":"",
                                        "numero_cola":"",
                                        "nombre":"",
                                        "apellidos":"",
                                        "fase_cola_medica":"",
                                        "consumo_medico":"",
                                        "estado_cola_medica":"",
                                }
                                diccionario['id_consulta']=fila.consulta.id_consulta
                                diccionario["numero_cola"]= fila.numero_cola
                                diccionario["nombre"]=fila.expediente.id_paciente.nombre_paciente
                                diccionario["apellidos"]=fila.expediente.id_paciente.apellido_paciente
                                diccionario["fase_cola_medica"]= fila.get_fase_cola_medica_display()
                                diccionario["consumo_medico"]= str(fila.consumo_medico)
                                diccionario["estado_cola_medica"]= fila.get_estado_cola_medica_display()
                                lista.append(diccionario)
                elif(rol=='ROL_DOCTOR'):
                        filterData={}
                        filterData['fase_cola_medica']=ContieneConsulta.OPCIONES_FASE[2][0]
                        filterData['fecha_de_cola__year']=fecha.year 
                        filterData['fecha_de_cola__month']=fecha.month
                        filterData['fecha_de_cola__day']=fecha.day

                        contiene_consulta=ContieneConsulta.objects.filter(**filterData).select_related('expediente__id_paciente')
                        
                        for fila in contiene_consulta:
                                diccionario={
                                        "id_consulta":"",
                                        "numero_cola":"",
                                        "nombre":"",
                                        "apellidos":"",
                                        "fase_cola_medica":"",
                                        "fecha_de_cola":""
                                }
                                #En id_consulta devuelve el id_de los signos
                                diccionario['id_consulta']=fila.consulta.id_consulta
                                diccionario["numero_cola"]= fila.numero_cola
                                diccionario["nombre"]=fila.expediente.id_paciente.nombre_paciente
                                diccionario["apellidos"]=fila.expediente.id_paciente.apellido_paciente
                                diccionario["fase_cola_medica"]= fila.get_fase_cola_medica_display()
                                diccionario["fecha_de_cola"]= fila.fecha_de_cola.strftime("%d/%b/%Y")
                                lista.append(diccionario)
                                
                elif (rol=='ROL_ENFERMERA'):
                        # recupera los pacientes en cola en fase anotado
                        contiene_consulta=ContieneConsulta.objects.filter(fecha_de_cola__year=fecha.year, 
                                        fecha_de_cola__month=fecha.month, 
                                        fecha_de_cola__day=fecha.day,fase_cola_medica=ContieneConsulta.OPCIONES_FASE[1][0]).select_related('expediente__id_paciente')         
                        
                        for fila in contiene_consulta:
                                diccionario={
                                        "id_consulta":"",
                                        "numero_cola":"",
                                        "nombre":"",
                                        "apellidos":"",
                                }
                                diccionario['id_consulta']=fila.consulta.id_consulta
                                diccionario["numero_cola"]= fila.numero_cola
                                diccionario["nombre"]=fila.expediente.id_paciente.nombre_paciente
                                diccionario["apellidos"]=fila.expediente.id_paciente.apellido_paciente
                                lista.append(diccionario)
                return self.send(text_data=json.dumps(lista))
        
        def cola_expediente(self,event):
                self.cola_inicial()
        
        def connect(self):
                self.room_group_name='expediente'
                async_to_sync(self.channel_layer.group_add)(
                        self.room_group_name,
                        self.channel_name
                        )
                self.accept()
                self.cola_inicial()
   
        def receive(self,text_data):
                async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {'type':'cola_expediente'}# aqui se especifica el handler para enviar este mensaje, para el caso es el metodo cola_expediente
                )
        def disconnect(self, code):
                # super().disconnect(code)
                raise StopConsumer()
from django.shortcuts import redirect, render
from modulo_expediente.serializers import PacienteSerializer
from datetime import datetime
from modulo_expediente.filters import PacienteFilter
from modulo_expediente.models import (Paciente, Expediente)
from modulo_control.models import Rol
from ..forms import ( DatosDelPaciente)
from django.http import JsonResponse
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic import TemplateView

from django.core import serializers
from django.db.utils import IntegrityError

###Para los expedientes masivos
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import QueryDict
import pandas as pd
import pathlib 

def busqueda_paciente(request):

    result= PacienteFilter(request.GET, queryset=Paciente.objects.all())
    pacientes =PacienteSerializer(result.qs, many=True)
    return JsonResponse({'data':pacientes.data})
     #la clave tiene que ser data para que funcione con el metodo. 

def buscar_expediente(request):
    if request.user.roles.codigo_rol=='ROL_DOCTOR':
        return render(request,"expediente/buscar_expediente.html")
    else:
        return render(request,"Control/error403.html")
    
def autocompletado_apellidos(request):
    
    apellidos=Paciente.objects.values("apellido_paciente").all()
    apellidosList=[]
    for apellido in apellidos:
        apellidosList.append(apellido['apellido_paciente'])
    return JsonResponse({"data":apellidosList})
    #la clave tiene que ser data para que funcione con el metodo. 



#Metodo que devuelve los datos del paciente en json
@login_required
def get_paciente(request, id_paciente):
    paciente=Paciente.objects.filter(id_paciente=id_paciente)
    serializer=PacienteSerializer(paciente, many= True)
    return JsonResponse(serializer.data, safe=False)

@login_required(login_url='/login/')
def sala_consulta(request):
    roles=Rol.objects.values_list('codigo_rol','id_rol').all()
    data={}
    data['titulo']="Sala de Espera"
    data['rol']=request.user.roles.id_rol
    for rol in roles:
        data[rol[0]]=rol[1]
    if request.user.roles.codigo_rol =="ROL_SECRETARIA" or request.user.roles.codigo_rol=="ROL_DOCTOR" or request.user.roles.codigo_rol =="ROL_ENFERMERA":
        return render(request,"expediente/salaEspera.html",data)
    else:
        return render(request,"Control/error403.html", data)

#Método que crea un nuevo paciente y lo asigna a un expediente
def crear_expediente(request):
    idpaciente=request.GET.get('id', None)
    if request.method == 'GET':
        if idpaciente==None:
            formulario= DatosDelPaciente()
        else:     
            paciente=Paciente.objects.get(id_paciente=idpaciente)
            formulario = DatosDelPaciente(instance=paciente)

    else:
        if idpaciente==None:
            formulario= DatosDelPaciente(request.POST)
            if  formulario.is_valid():
                new_paciente=formulario.save()
                expediente=Expediente()
                expediente.fecha_creacion_expediente=datetime.now()
                #Generando código expediente
                nombrepaciente = formulario["nombre_paciente"].value()
                apellidopaciente=formulario["apellido_paciente"].value()
                year=datetime.now().date().strftime("%Y")[2:]
                texto=nombrepaciente[0]+apellidopaciente[0]
                texto=texto.lower()#Solo texto en minusculas
                texto=texto+year
                try:
                    correlativo = correlativo = Expediente.objects.filter(codigo_expediente__startswith=texto).last().codigo_expediente
                    correlativo=int(correlativo[4:])
                except:
                    correlativo=0 
                correlativo=correlativo+1
                if correlativo < 10:
                    correlativo="00"+str(correlativo)
                elif correlativo < 100:
                    correlativo = "0"+str(correlativo)
                #Codigo de Usuario al estilo -- mv17012 ---
                codigo=texto+correlativo
                expediente.codigo_expediente=codigo
                idpaciente=list(Paciente.objects.values("id_paciente").all())
                idList=[]
                for i in idpaciente:
                    idList.append(i['id_paciente'])
                expediente.id_paciente_id=idList[-1]
                expediente.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Paciente registrado con exito")
                base_url = reverse('crear_expediente')
                query_string =  urlencode({'id': new_paciente.id_paciente})
                url = '{}?{}'.format(base_url, query_string)
                return redirect(url)
            
        else:
            paciente=Paciente.objects.get(id_paciente=idpaciente)
            formulario = DatosDelPaciente(request.POST, instance=paciente)
            formulario.save()
            messages.add_message(request=request, level=messages.SUCCESS, message="El Paciente se ha modificado con exito")
        
    return render(request,"datosdelPaciente.html",{'formulario':formulario})

#Registro masivo de expedientes
class RegistroMasivoExpedientesView(TemplateView):
    template_name = "expediente/registro_masivo/registro_masivo.html"
    response={'type':'','data':''}

    def post(self, request, *args, **kwargs):
        archivo=request.FILES['file']
        file_extension = pathlib.Path(archivo.name).suffix 
        if file_extension in ('.xls', '.xlsx'):

            xlsx = pd.read_excel(archivo)
            xlsx.fillna("", inplace=True)
            expedientes=xlsx.to_dict(orient='records')
            cantidad=len(expedientes)

            self.notificar_avance("Archivo leído con éxito.", "notificacion","")
            self.notificar_avance(f'{cantidad}', "header","")
            procesados=0
            exitos=0
            fracasos=0
            for expediente in expedientes:
                paciente = Paciente(
                    nombre_paciente=expediente["Nombres"],
                    apellido_paciente=expediente["Apellidos"],
                    fecha_nacimiento_paciente=expediente["Fecha de nacimiento (dd/mm/yyyy)"],
                    sexo_paciente=expediente["Sexo (M/F)"],
                    direccion_paciente=expediente["Dirección"],
                    email_paciente=expediente["Email"],
                    responsable=expediente["Responsable"],
                    dui=expediente["Dui"],
                    pasaporte=expediente["Pasaporte"],
                    numero_telefono=str(expediente["Número de Telefono"])[:8]
                )
                procesados +=1
                try:
                    paciente.save()
                    
                    Expediente.objects.create(
                        id_paciente=paciente,
                    )
                    exitos +=1
                    self.notificar_avance(f'{procesados}', "dato", "")
                except IntegrityError:
                    fracasos +=1
                    json_paciente = serializers.serialize('json', [paciente ])
                    self.notificar_avance(json_paciente, "objetoError",expediente["#"])
            self.notificar_avance(f'Expedientes registrados: {exitos}, \nExpedientes pendientes de revisión: {fracasos}', "notificacion", expediente["#"])
            self.notificar_avance(f'{procesados}', "dato", "")
            respuesta={
                'data':'Enviado'
            }

        else:
            respuesta={
                'data':'error'
            }
        return JsonResponse(respuesta)
    ##Voy a acupar este metodo para alamacenar de forma individual
    def put(self, request, *args, **kwargs):
        data = QueryDict(request.body)
        paciente_form= DatosDelPaciente(data)
        if paciente_form.is_valid():
            paciente=paciente_form.save()
            Expediente.objects.create(
                id_paciente=paciente,
            )
            self.response['type']='success'
            self.response['data']='Expediente Registrado'
        else:
            self.response['type']='warning'
            self.response['data']=paciente_form.errors.get_json_data()

        return JsonResponse(self.response)
        
    def notificar_avance(self, data, tipo, numero):
        layer = get_channel_layer() 
        async_to_sync(layer.group_send)('archivos',{# _archivos_ Este es el nombre del channel
        "type": "archivos",
        "room_id": 'archivos',
        "toast":"info",
        "data":data,
        "tipo": tipo,
        "numero":numero
        })

 

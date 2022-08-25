from http.client import HTTPResponse
from django.shortcuts import redirect, render
from modulo_expediente.serializers import ConsultaSerializers, ContieneConsultaSerializer, ControlSubsecuenteConsultaSerializer, PacienteSerializer, SignosVitalesSerializer
from datetime import datetime
from modulo_expediente.filters import PacienteFilter
from modulo_expediente.models import (Consulta, ContieneConsulta, ControlSubsecuente,  Paciente, Expediente, SignosVitales)
from modulo_control.models import Rol
from ..forms import ( ConsultaFormulario, ControlSubsecuenteform, DatosDelPaciente)
from django.http import JsonResponse
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View 
from django.views.generic import View, TemplateView
from django.views.generic import TemplateView

from django.core import serializers

###Para los examenes masivos
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
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

    def post(self, request, *args, **kwargs):
        archivo=request.FILES['file']
        file_extension = pathlib.Path(archivo.name).suffix 
        if file_extension in ('.xls', '.xlsx'):

            xlsx = pd.read_excel(archivo)
            xlsx.fillna(0, inplace=True)
            expedientes=xlsx.to_dict(orient='records')
            cantidad=len(expedientes)

            self.notificar_avance("Archivo leído con éxito.", "notificacion","")
            self.notificar_avance(f'{cantidad}', "header","")
            procesados=0
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
                    """ 
                    Expediente.objects.create(
                        id_paciente=paciente,
                    ) """
                    self.notificar_avance(f'{procesados}', "dato", "")
                except:
                    json_paciente = serializers.serialize('json', [paciente ])
                    self.notificar_avance(json_paciente, "objetoError",expediente["#"])

            

            self.notificar_avance(f'{"100%"}', "notificacion", "")

            respuesta={
                'data':'Enviado'
            }

        else:
            respuesta={
                'data':'error'
            }
        return JsonResponse(respuesta)
    
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

 
class ControlSubsecuenteView(View): 
        template_name = "expediente/consulta/control_subsecuente.html"

        def get(self, request, *args, **kwargs):

            id_consulta=int(self.kwargs['id_consulta']) 
            contiene_consulta=ContieneConsulta.objects.filter(consulta__id_consulta=id_consulta).first()
            expediente=contiene_consulta.expediente_id
            contiene_consulta=ContieneConsulta.objects.filter(expediente_id=expediente).exclude(consulta__id_consulta=id_consulta).select_related('consulta')
            lista=[]
            for i in range(len(contiene_consulta)):
                
                c={
                     'id_consulta':"",
                     'fecha':"",
                     'diagnostico':"",
                }
                c['id_consulta']=contiene_consulta[i].consulta.id_consulta
                c['fecha']=contiene_consulta[i].consulta.fecha
                c['diagnostico']=contiene_consulta[i].consulta.diagnostico
            
                lista.append(c)
            
            return render(request,self.template_name,{'consultas':lista, 'id_consulta':id_consulta})
           
class ControlSubsecuenteConsultaView(View): 
    def get(self, request, *args, **kwargs):
        id_consulta=int(self.kwargs['id_consulta']) 
        signos_vitales_data=SignosVitales.objects.filter(consulta_id=id_consulta).order_by('-fecha').first()
        # consulta_data=Consulta.objects.get(id_consulta=id_consulta)
        signos_vitales=ControlSubsecuenteConsultaSerializer(signos_vitales_data,many=False)
        print(signos_vitales.data)
        # consulta=ConsultaSerializers(consulta)
        return JsonResponse({'signos_vitales':signos_vitales.data})
        



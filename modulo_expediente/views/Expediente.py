from django.shortcuts import redirect, render
from modulo_expediente.serializers import ConsultaSerializers, ContieneConsultaSerializer, PacienteSerializer
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
            expedientes=xlsx.to_dict(orient='records')
            cantidad=len(expedientes)

            self.notificar_avance("Archivo leído con éxito.")
            self.notificar_avance(f'El archivo cuenta con: {cantidad} registros')
            procesados=0
            for expediente in expedientes:
                """paciente = Paciente.objects.create(
                    nombre_paciente=expediente["Nombre"],
                    apellido_paciente=expediente["Apellido"]
                    fecha_nacimiento_paciente=datetime.strptime(expediente["Fecha de nacimiento (dd-mm-yyyy)"], "%d-%m-%Y"),
                    sexo_paciente=expediente["Sexo (M/F)"],
                    direccion_paciente=expediente["Dirección"],
                    email_paciente=expediente["Email"],
                    
                ) """
                print(expediente)
                procesados +=1
                self.notificar_avance(f' se han procesado {procesados} de {cantidad} registros.')

            respuesta={
                'data':'Enviado'
            }

        else:
            respuesta={
                'data':'error'
            }
        return JsonResponse(respuesta)
    
    def notificar_avance(self, data):
        layer = get_channel_layer()
        async_to_sync(layer.group_send)('archivos',{
        "type": "archivos",
        "room_id": 'archivos',
        "toast":"info",
        "data":data
        })

 
class ControlSubsecuenteView(TemplateView): 
        template_name = "expediente/consulta/control_subsecuente.html"

        def get(self, request, *args, **kwargs):

            id_consulta=int(self.kwargs['id_consulta']) 
            contiene_consulta=ContieneConsulta.objects.filter(consulta__id_consulta=id_consulta).order_by('-fecha_de_cola').first()
            expediente=contiene_consulta.expediente_id
            contiene_consulta=list(ContieneConsulta.objects.filter(expediente_id=expediente))
            print(contiene_consulta)
            contiene_serializer=ContieneConsultaSerializer(contiene_consulta, many= True)
            signos_vitales=SignosVitales.objects.filter(consulta_id=id_consulta).order_by('-fecha').first()
            print(signos_vitales)
            lista=[]
            for i in range(len(contiene_consulta)):
                c={
                    'id_consulta':"",
                    'consulta_por':"",
                    'presente_enfermedad':"",
                    'examen_fisico':"",
                    'diagnostico':"",
                    'plan_tratamiento':""
                }
                c['id_consulta']=contiene_consulta[i].consulta.id_consulta
                c['consulta_por']=contiene_consulta[i].consulta.consulta_por
                c['presente_enfermedad']=contiene_consulta[i].consulta.presente_enfermedad
                c['examen_fisico']=contiene_consulta[i].consulta.examen_fisico
                c['diagnostico']=contiene_consulta[i].consulta.diagnostico
                c['plan_tratamiento']=contiene_consulta[i].consulta.plan_tratamiento
                lista.append(c)

        
            diccionario={
                    "id_signos_vitales":signos_vitales.id_signos_vitales,
                    "unidad_temperatura":signos_vitales.unidad_temperatura,
                    "unidad_peso":signos_vitales.unidad_peso,
                    "valor_temperatura":signos_vitales.valor_temperatura,
                    "valor_peso":signos_vitales.valor_peso,
                    "valor_arterial_diasolica":signos_vitales.valor_presion_arterial_diastolica,
                    "valor_arterial_sistolica":signos_vitales.valor_presion_arterial_sistolica,
                    "valor_frecuencia_cardiaca":signos_vitales.valor_frecuencia_cardiaca,
                    "valor_saturacion_oxigeno":signos_vitales.valor_saturacion_oxigeno
            }
            datos={
                'consultas':lista,
                'signo_vital':diccionario
            }
            
            return render(request, self.template_name, datos)
           


        



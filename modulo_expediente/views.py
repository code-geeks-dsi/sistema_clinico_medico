from django.shortcuts import render
from modulo_expediente.filters import PacienteFilter
from modulo_expediente.forms import DatosDelPaciente
from modulo_expediente.models import Paciente
from django.http import JsonResponse
# Create your views here.

def busqueda_paciente(request):
    
    filter = PacienteFilter(request.GET, queryset=Paciente.objects.all())
    apellidosList=Paciente.objects.values("apellido_paciente").all()
    # queryset=Paciente.objects.filter(nombre_paciente=request.GET.get('nombre_paciente',""),apellido_paciente=request.GET.get('apellido_paciente',""))
    return render(request, 'busquedaPaciente.html', {'filter': filter,'apellidosList':apellidosList})


def vista_sala_espera(request):
    return render(request,"salaEspera.html")

def get_paciente (request , id_paciente):
        paciente=list(Paciente.objects.values())
        lista =[]
        for i in range(len(paciente)):
            if paciente[i]["id_paciente"] == id_paciente:
                diccionario={
                    "id_paciente":"",
                    "nombre_paciente":"",
                    "apellido_paciente":"",
                    "fecha_nacimiento_paciente":"",
                    "sexo_paciente":"",
                    "direccion_paciente":"",
                    "email_paciente":"",
                    "responsable":""
                }
                diccionario["id_paciente"]= paciente[i]["id_paciente"]
                diccionario["nombre_paciente"]= paciente[i]["nombre_paciente"]
                diccionario["apellido_paciente"]= paciente[i]["apellido_paciente"]
                diccionario["fecha_nacimiento_paciente"]= paciente[i]["fecha_nacimiento_paciente"]
                diccionario["sexo_paciente"]= paciente[i]["sexo_paciente"]
                diccionario["direccion_paciente"]= paciente[i]["direccion_paciente"]
                diccionario["email_paciente"]= paciente[i]["email_paciente"]
                diccionario["responsable"]= paciente[i]["responsable"]
                lista.append(diccionario);
                del diccionario
        return JsonResponse(lista, safe=False)

def crear_expediente(request):
    formulario = DatosDelPaciente(request.GET)
    print(formulario.is_valid)
    if request.method == "POST": 
        if formulario.is_valid():
            formulario.save()
            
    return render(request,"datosdelPaciente.html",{'formulario':formulario})

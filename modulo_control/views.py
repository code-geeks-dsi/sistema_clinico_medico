from contextlib import nullcontext
from multiprocessing import context
import select
from urllib import request
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotFound,Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from modulo_control.forms import EmpleadoForm,LicLaboratorioClinicoForm,DoctorForm
from modulo_control.models import *
from modulo_control.serializers import EmpleadoSerializer, RolSerializer, SimpleEmpleadoSerializer
from .forms import *
from datetime import datetime
from django.utils import timezone


"""
-------------------------------------------------------------------------
Para almacenar archivos estaticos se esta utilizando AWS S3, es necesario
ejecutar el comando < python manage.py collectstatic > cada vez que se 
agreguen archivos estaticos.
-------------------------------------------------------------------------
"""

#Login
def vista_iniciarsesion(request):
    return render(request,"login.html")

@csrf_exempt
def logearse(request):
    mensaje=""
    if request.method =="POST":
        email = request.POST.get("usuario")
        password = request.POST.get("password")
        aux=str(email).find('@') #Si encuentra una @ significa que ha recibido un correo
        #mensaje="Si recibí los datos"

        if aux != -1:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                mensaje="Estas Logeado"
                return redirect('vistaGestionEmpleados')
            else:
                mensaje="Password o correo incorrecto"
        else:
            #mensaje="No se recibio un correo"
            try:
                correo=Empleado.objects.filter(codigoUsuario=email).first().email
                user = authenticate(request, email=correo, password=password)
                if user is not None:
                    login(request, user)
                    mensaje="Estas logeado"
                else:
                    mensaje="password incorrecta"
            except:
                mensaje="Empleado o correo incorrectos"
    else:
        mensaje="Los datos no se enviaron de forma segura"
    
    data={'Mensaje':mensaje}
    return JsonResponse(data)

    

""" def registrarEmpleado(request):
    empleadoForm = EmpleadoForm()
    return render(request, 'registroEmpleado.html', {'empleadoForm':empleadoForm})
    
@csrf_exempt
def agregarEmpleado(request):
    if request.method == 'POST':
        empleado = Empleado()
        empleadoForm = EmpleadoForm(request.POST)

        if empleadoForm.is_valid():
            empleado = empleadoForm.save(commit=False)
            empleado.save()

    return redirect('index') ##luego cambiar a que redireccione a lista de enpleados o algo asi  """

@csrf_exempt
def registrar_empleado(request):
    data={
                'type':'warning',
                'title':'',
                'data':'',
                'pass':''
            }

    if request.method == 'POST':

        #Recuperando Datos
        nombres = request.POST['nombre_empleado']
        apellidos = request.POST['apellido_empleado']
        email =  request.POST['email_empleado']
        password = request.POST['password_empleado']
        direccion = request.POST['direccion_empleado']
        fecha_nacimiento = request.POST['fecha_nacimiento']
        sexo_empleado = request.POST['sexo_empleado']
        rol_empleado = request.POST['rol_empleado']

        if nombres != "" and apellidos != "" and email != "" and password != "" and fecha_nacimiento != "" and direccion != "" and sexo_empleado != "" and rol_empleado != "":
            if (len(password)>5):
                if (password.isdigit()): 
                    data['data']="Contraseña debe tener numeros y letras"
                    data['pass']="0"
                else:
                    try:
                        #Creando objeto fecha
                        fecha_nacimiento = datetime.strptime(fecha_nacimiento,"%Y-%m-%d").date()
                        empleado = Empleado.objects.create_user(nombres, apellidos, email, password)
                        empleado.direccion = direccion
                        empleado.fechaNacimiento = fecha_nacimiento
                        empleado.sexo = sexo_empleado
                        empleado.roles=Rol.objects.get(id_rol=int(rol_empleado))
                        empleado.save()

                        data['type']="success"
                        data['data']="Empleado Registrado"
                    except:
                        data['data']="Ya se a registrado el correo"
            else:
                data['data']="Contraseña debe tener por lo menos 6 caracteres"
                data['pass']="0"
        else:
            data['data']="Ingrese todos los campos"
    return JsonResponse(data, safe=False)


def editar_empleado(request):
    codigo_empleado=request.GET.get('id',None)
    try:
        empleado=Empleado.objects.get(codigo_empleado=codigo_empleado)
        form_roles=[]
        for rol in empleado.roles.all():
            if(rol==Rol.objects.get(nombre_rol='Doctor')):
                form_roles.append(DoctorForm(empleado=empleado))
            if (rol==Rol.objects.get(nombre_rol='Laboratorio')):
                form_roles.append(LicLaboratorioClinicoForm(empleado=empleado))

        form=EmpleadoForm(instance=empleado)
        print({'form':form,'form_roles':form_roles})
        return render(request, 'registroEmpleado.html',{'form':form,'form_roles':form_roles})
    except Empleado.DoesNotExist:
        raise Http404("Empleado no existe.")
        
def vista_adminitracion_empleados(request):
    roles = Rol.objects.all()
    
    return render(request,"Control/gestionEmpleados.html", {"Rol":roles})

def lista_empleados(request):
    empleados = Empleado.objects.all().order_by('-roles').reverse()
    serializer = EmpleadoSerializer(empleados, many=True)
    return JsonResponse(serializer.data, safe=False)  

def get_empleado(request, cod_empleado):
    empleado=Empleado.objects.filter(codigo_empleado=cod_empleado)
    serializer=SimpleEmpleadoSerializer(empleado, many=True)
    return JsonResponse(serializer.data, safe=False)  

# def registrarEmpleado(request):
#     form=EmpleadoForm(request.GET)
#     return render(request, 'registroEmpleado.html',{'form':form})


# def registrarDoctor(request):
#     doctorForm = DoctorForm()
#     return render(request, 'registroDoctor.html', {'doctorForm':doctorForm})

# @csrf_exempt
# def agregarDoctor(request):
#     if request.method == 'POST':
#         doctor = Doctor()
#         doctorForm = DoctorForm(request.POST)

#         if doctorForm.is_valid():
#             doctor = doctorForm.save(commit=False)
#             doctor.save()


#     return redirect('index') ##luego cambiar a que redireccione a lista de doctores o algo asi

# def registrarEnfermera(request):
#     enfermeraForm = EnfermeraForm()
#     return render(request, 'registroEnfermera.html', {'enfermeraForm':enfermeraForm})


# def agregarEnfermera(request):
#     if request.method == 'POST':
#         enfermera = Enfermera()
#         enfermeraForm = EnfermeraForm(request.POST)

#         if enfermeraForm.is_valid():
#             enfermera = enfermeraForm.save(commit=False)
#             enfermera.save()
    
#     return redirect('index') ##luego cambiar a que redireccione a lista de enfermeras o algo asi

# def registrarLicLaboratorioClinico(request):
#     licLaboratorioClinicoForm = LicLaboratorioClinicoForm()
#     return render(request, 'registroLicLaboratorioClinico.html', {'licLaboratorioClinicoForm':licLaboratorioClinicoForm})

# @csrf_exempt
# def agregarLicLaboratorioClinico(request):
#     if request.method == 'POST':
#         licLaboratorioClinico = LicLaboratorioClinico()
#         licLaboratorioClinicoForm = LicLaboratorioClinicoForm(request.POST)

#         if licLaboratorioClinicoForm.is_valid():
#             licLaboratorioClinico = licLaboratorioClinicoForm.save()
#             licLaboratorioClinico.save()
#     return redirect('index') ##luego cambiar a que redireccione a lista de lics o algo asi

# def registrarSecretaria(request):
#     secretariaForm = SecretariaForm()
#     return render(request, 'registroSecretaria.html', {'secretariaForm':secretariaForm})

# @csrf_exempt
# def agregarSecretaria(request):
#     if request.method == 'POST':
#         secretaria = Secretaria()
#         secretariaForm = SecretariaForm(request.POST)

#         if secretaria.is_valid():
#             secretaria = secretariaForm.save()
#             secretaria.save()
#     return redirect('index') ##luego cambiar a que redireccione a lista de secretaria o algo asi


# def indexEmpleado(request):
#     return render(request, 'indexEmpleado.html')


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
from .forms import *
from datetime import datetime


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
                mensaje="Usuario o correo incorrectos"
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
    if request.method == 'POST':
        empleado = Empleado()

        empleado.codigo_empleado = request.POST['codigoEmp']
        empleado.nombres = request.POST['nombresEmp']
        empleado.apellidos = request.POST['apellidosEmp']
        empleado.sexo = request.POST['sexoEmp']
        empleado.direccion = request.POST['direccionEmp']
        empleado.email = None
        empleado.es_activo = True
        empleado.es_staff = True
        empleado.es_superuser = False
        empleado.last_login = None
        empleado.fechaCreacion = datetime.now()
        empleado.fechaNacimiento = '2022-01-2'

        empleado.save()

        return redirect('index')


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


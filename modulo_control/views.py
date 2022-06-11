from contextlib import nullcontext
from multiprocessing import context
from pickle import TRUE
import select
from urllib import request
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotFound,Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from pkg_resources import normalize_path
from modulo_control.forms import EmpleadoForm,LicLaboratorioClinicoForm,DoctorForm
from modulo_control.models import *
from modulo_control.serializers import EmpleadoSerializer, RolSerializer, SimpleEmpleadoSerializer
from .forms import *
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required


"""
-------------------------------------------------------------------------
Para almacenar archivos estaticos se esta utilizando AWS S3, es necesario
ejecutar el comando < python manage.py collectstatic > cada vez que se 
se coloque en modo producción.
-------------------------------------------------------------------------
"""

#Login
def vista_iniciarsesion(request):
    data={'mensaje':"",
          'type':'',
        }
    return render(request,"login.html",data)

def cerrar_sesion(request):
    logout(request)
    return redirect('login')

@csrf_exempt
def logearse(request):
    mensaje=""
    if request.method =="POST":
        email = request.POST.get("usuario")
        password = request.POST.get("password")
        aux=str(email).find('@') #Si encuentra una @ significa que ha recibido un correo
        #mensaje="Si recibí los datos"

        if aux != -1:
            email=email.lower()
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                mensaje="Estas Logeado"
                if request.user.roles.codigo_rol=='ROL_ADMIN':
                    return redirect('vistaGestionEmpleados')
                elif request.user.roles.codigo_rol=='ROL_SECRETARIA' or request.user.roles.codigo_rol=='ROL_DOCTOR' or request.user.roles.codigo_rol=='ROL_ENFERMERA':
                    return redirect('sala_consulta')
                elif request.user.roles.codigo_rol=='ROL_LIC_LABORATORIO':
                    return redirect('inicio_lab')
            else:
                mensaje="usuario/contraseña no válido"
        else:
            #mensaje="No se recibio un correo"
            try:
                correo=Empleado.objects.filter(codigoUsuario=email).first().email
                user = authenticate(request, email=correo, password=password)
                if user is not None:
                    login(request, user)
                    mensaje="Estas logeado"
                else:
                    mensaje="usuario/contraseña no válido"
            except:
                mensaje="usuario/contraseña no válido"
    else:
        mensaje="Los datos no se enviaron de forma segura"
    
    data={'mensaje':mensaje,
          'type':'warning',
        }
    return render(request,"login.html",data)

    

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
    if request.user.roles.codigo_rol == 'ROL_ADMIN':
        if request.method == 'POST':

            #Recuperando Datos
            nombres = request.POST['nombre_empleado']
            apellidos = request.POST['apellido_empleado']
            email =  request.POST['email_empleado']
            password = request.POST['password_empleado']
            password2 = request.POST['password_empleado_2']
            direccion = request.POST['direccion_empleado']
            fecha_nacimiento = request.POST['fecha_nacimiento']
            sexo_empleado = request.POST['sexo_empleado']
            rol_empleado = request.user.roles.codigo_rol

            if nombres != "" and apellidos != "" and email != "" and password != "" and fecha_nacimiento != "" and direccion != "" and sexo_empleado != "" and rol_empleado != "":
                if (len(password)>5):
                    if (password.isdigit()): 
                        data['data']="Contraseña debe tener numeros y letras"
                        data['pass']="0"
                    elif (password!=password2):
                        data['data']="Las dos contraseñas deben ser iguales"
                        data['pass']="0"
                    else:
                        try:
                            #Creando objeto fecha
                            fecha_nacimiento = datetime.strptime(fecha_nacimiento,"%Y-%m-%d").date()
                            nuevo_empleado = Empleado.objects.create_user(nombres, apellidos, email, password)
                            nuevo_empleado.direccion = direccion
                            nuevo_empleado.fechaNacimiento = fecha_nacimiento
                            nuevo_empleado.sexo = sexo_empleado
                            nuevo_empleado.roles=Rol.objects.get(id_rol=int(rol_empleado))
                            nuevo_empleado.save()
                            
                            if rol_empleado == 'ROL_DOCTOR':
                                #De momento todos los medicos van a tener la especialidad General y 
                                #JVPM 12345678
                                #La gestión de las especialidades constituye a mi criterio una Historia adicional
                                #--- Es necesario agregar la TABLA ---ESPECIALIDAD---
                                especialidad="Medicina General"
                                jvmp_d=12345678
                                Doctor.objects.create(especialidad_doctor=especialidad, jvmp=jvmp_d, empleado=nuevo_empleado)
                            elif rol_empleado == 'ROL_ENFERMERA':
                                Enfermera.objects.create(empleado = nuevo_empleado)
                            elif rol_empleado =='ROL_LIC_LABORATORIO':
                                jvplc_n=12345678
                                LicLaboratorioClinico.objects.create(jvplc=jvplc_n, empleado=nuevo_empleado)
                            elif rol_empleado == 'ROL_SECRETARIA':
                                Secretaria.objects.create(empleado=nuevo_empleado)
                            data['type']="success"
                            data['data']="Empleado Registrado"
                        except:
                            data['data']="Ya se a registrado el correo"
                else:
                    data['data']="Contraseña debe tener por lo menos 6 caracteres"
                    data['pass']="0"
            else:
                data['data']="Ingrese todos los campos"
    else:
        data['data']="Aceso denegado"
    return JsonResponse(data, safe=False)

@csrf_exempt
def editar_empleado(request):
    data={
                'type':'warning',
                'title':'',
                'data':'',
                'pass':''
            }
    if request.user.roles.codigo_rol=='ROL_ADMIN':
        if request.method == 'POST':
            nombre = request.POST['nombre_empleado']
            apellido = request.POST['apellido_empleado']
            direccion_empleado = request.POST['direccion_empleado']
            fecha_nacimiento = request.POST['fecha_nacimiento']
            sexo_empleado = request.POST['sexo_empleado']
            rol_empleado = request.user.roles.codigo_rol
            is_active = request.POST['es_activo']
            cod_empleado=request.POST['cod_empleado']
            #En esta vista no se editaran los datos de inicio de sesión del empleado
            if nombre != "" and apellido != "" and fecha_nacimiento != "" and direccion_empleado != "" and sexo_empleado != "" and rol_empleado != "":
                if is_active=="0" or is_active=="1":
                    edit_empleado=Empleado.objects.get(codigo_empleado=cod_empleado)

                    #Recuperando Rol anterior
                    rol_antiguo=str(edit_empleado.roles.id_rol)

                    #Actualizando Informacion
                    edit_empleado.nombres=nombre
                    edit_empleado.apellidos=apellido
                    edit_empleado.direccion=direccion_empleado
                    edit_empleado.fechaNacimiento=fecha_nacimiento
                    edit_empleado.sexo=sexo_empleado
                    edit_empleado.roles=Rol.objects.get(id_rol=int(rol_empleado))
                    edit_empleado.es_activo=int(is_active)
                    edit_empleado.save()

                    if rol_empleado == 'ROL_DOCTOR':
                        #De momento todos los medicos van a tener la especialidad General y 
                        #JVPM 12345678
                        #La gestión de las especialidades constituye a mi criterio una Historia adicional
                        #--- Es necesario agregar la TABLA ---ESPECIALIDAD---
                        especialidad="Medicina General"
                        jvmp_d=12345678
                        if rol_antiguo!=rol_empleado:
                            try:
                                Doctor.objects.create(especialidad_doctor=especialidad, jvmp=jvmp_d, empleado=edit_empleado)
                            except:
                                data['data']="Información actualizada"
                    elif rol_empleado == 'ROL_ENFERMERA':
                        if rol_antiguo!=rol_empleado:
                            try:
                                Enfermera.objects.create(empleado = edit_empleado)
                            except:
                                data['data']="Información actualizada"
                    elif rol_empleado =='ROL_LIC_LABORATORIO':
                        jvplc_n=12345678
                        if rol_antiguo!=rol_empleado:
                            try:
                                LicLaboratorioClinico.objects.create(jvplc=jvplc_n, empleado=edit_empleado)
                            except:
                                data['data']="Información actualizada"
                    elif rol_empleado == 'ROL_SECRETARIA':
                        if rol_antiguo!=rol_empleado:
                            try:
                                Secretaria.objects.create(empleado=edit_empleado)
                            except:
                                data['data']="Información actualizada"
                    data['type']="success"
                    data['data']="Datos actualizados"
                else:
                    data['data']="Error de datos, debe recargar la pagina."
            else:
                data['data']="Debe actualizar la información completa."
        else: 
            data['data']="Los datos no se han enviado de forma segura."
    else:
        data['data']="Aceso Denegados"
    return JsonResponse(data, safe=False)

@login_required(login_url='/login/')        
def vista_adminitracion_empleados(request):
    if request.user.roles.codigo_rol=='ROL_ADMIN':
        roles = Rol.objects.all()
        return render(request,"Control/gestionEmpleados.html", {"Rol":roles})
    else:
        return render(request,"Control/error403.html")

@login_required()  
def lista_empleados(request):
    if request.user.roles.codigo_rol == 'ROL_ADMIN':
        empleados = Empleado.objects.all().order_by('-roles').reverse()
        print(empleados[0].roles)
        serializer = EmpleadoSerializer(empleados, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        data = "Acceso denegado"
        return JsonResponse({'data': data}, safe=False)  

def get_empleado(request, cod_empleado):
    if request.user.roles.codigo_rol == 'ROL_ADMIN':
        empleado=Empleado.objects.filter(codigo_empleado=cod_empleado)
        serializer=SimpleEmpleadoSerializer(empleado, many=True)
        return JsonResponse(serializer.data, safe=False)  
    else:
        data = "Acceso denegado"
        return JsonResponse({'data': data}, safe=False)  

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


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from GestionUsuarios.models import Usuario
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
                correo=Usuario.objects.filter(codigoUsuario=email).first().email
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


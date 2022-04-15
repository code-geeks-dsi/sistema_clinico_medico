from django.shortcuts import render
from django.http import JsonResponse

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
def logearse(request):
    mensaje=""
    data={'mensaje':mensaje}
    return JsonResponse(data)
# Create your views here.

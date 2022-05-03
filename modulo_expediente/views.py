from django.shortcuts import render

# Create your views here.

def vista_sala_espera(request):
    return render(request,"salaEspera.html")

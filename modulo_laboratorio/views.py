from django.shortcuts import render

# Create your views here.

def sala_laboratorio(request):
    return render(request,"laboratorio/salaLaboratorio.html")

from django.http import JsonResponse
from django.shortcuts import render
from modulo_laboratorio.models import Categoria, CategoriaExamen
from modulo_laboratorio.serializers import CategoriaExamenSerializer

# Create your views here.

# Templete Sala de Espera laboratorio
def sala_laboratorio(request):
    categorias= Categoria.objects.all()
    rutina=CategoriaExamen.objects.filter(categoria=1)
    return render(request,"laboratorio/salaLaboratorio.html", {"Categoria":categorias, "Examen":rutina})

#View Recuperar Examenes por categoria
def get_categoria_examen(request, id_categoria):
    response={
            'data':'El Paciente ya existe en la cola',
            'accion':2
        }
    id_cat=id_categoria
    categoriaExamen=CategoriaExamen.objects.filter(categoria=id_cat)
    serializer = CategoriaExamenSerializer(categoriaExamen, many= True)
    response['data']=serializer.data
    return JsonResponse(response, safe=False)
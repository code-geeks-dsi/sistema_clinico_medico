from django.http import JsonResponse
from modulo_laboratorio.models import CategoriaExamen
from modulo_laboratorio.serializers import CategoriaExamenSerializer

def get_categoria_examen(request, id_categoria):
    response={
            'data':'El Examen ya existe en la cola',
            'accion':2
        }
    id_cat=id_categoria
    categoriaExamen=CategoriaExamen.objects.filter(categoria=id_cat)
    serializer = CategoriaExamenSerializer(categoriaExamen, many= True)
    response['data']=serializer.data
    return JsonResponse(response, safe=False)  
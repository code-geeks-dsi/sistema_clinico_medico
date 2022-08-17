from django.shortcuts import  render
from modulo_expediente.serializers import DosisListSerializer, MedicamentoSerializer
from modulo_expediente.filters import MedicamentoFilter
from modulo_expediente.models import ( Dosis, Medicamento )
from modulo_expediente.forms import (DosisFormulario,IngresoMedicamentos)
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
@csrf_exempt
@login_required
def dosis_medicamento(request):
    if request.user.roles.codigo_rol =='ROL_DOCTOR':
        if request.method=='POST':
            medicamento=DosisFormulario(request.POST)
            if medicamento.is_valid():
                medicamento.save()
                dosis=Dosis.objects.filter(receta_medica=request.POST['receta_medica'])
                serializer=DosisListSerializer(dosis, many=True)
                response={
                'type':'success',
                'title':'Guardado!',
                'data':'Dosis Guardada!',
                'dosis':serializer.data
            }
            else:
                response={
                'type':'warning',
                'title':'Error!',
                'data':medicamento.errors,
                'test':""
            }
    else:
        response={
                'type':'warning',
                'title':'Error!',
                'data':'Acceso denegado',
                'test':""
            }
    
    return JsonResponse(response)

#Método que elimina una dosis de la receta medica
@login_required
def eliminar_dosis(request, id_dosis):
    if request.user.roles.codigo_rol =='ROL_DOCTOR':
        try:
            dosis=Dosis.objects.get(id_dosis=id_dosis)
            dosis.delete()
            dosis=Dosis.objects.filter(receta_medica=request.GET['id_receta'])
            serializer=DosisListSerializer(dosis, many=True)
            response={
                'type':'success',
                'title':'Eliminado',
                'data':'Se ha eliminado la dosis de la receta medica',
                'dosis':serializer.data
            }
        except:
            response={
                'type':'warning',
                'title':'Error',
                'data':'La dosis no esta ingresada en la receta medica'
            }
    else:
        response={
                'type':'warning',
                'title':'Error',
                'data':'Acceso denegado'
            }
    return JsonResponse(response, safe=False)

def agregar_medicamento(request):
    idmedicamento=request.GET.get('id', None)
    if request.method == 'GET':
        if idmedicamento==None:
            formulario= IngresoMedicamentos()
        else:     
            medicamento=Medicamento.objects.get(id_medicamento=idmedicamento)
            formulario = IngresoMedicamentos(instance=medicamento)

    else:
        if idmedicamento==None:
            formulario= IngresoMedicamentos(request.POST)
            if  formulario.is_valid():
                new_medicamento=formulario.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Medicamento registrado con exito")
                # base_url = reverse('agregar_medicamento')
                # query_string =  urlencode({'id': new_medicamento.id_medicamento})
                # url = '{}?{}'.format(base_url, query_string)
                # return redirect(url)
        else:
            medicamento=Medicamento.objects.get(id_medicamento=idmedicamento)
            formulario = IngresoMedicamentos(request.POST, instance=medicamento)
            formulario.save()
            messages.add_message(request=request, level=messages.SUCCESS, message="El Medicamento se ha modificado con exito")
        
    return render(request,"medicamentos.html",{'formulario':formulario})

def busqueda_medicamento(request):
    queryset=Medicamento.objects.all()
    result= MedicamentoFilter(request.GET, queryset=queryset)
    medicamento =MedicamentoSerializer(result.qs, many=True)
    if(len(result.qs) ==0):
        response={
            'type':'warning',
            'title':'Error!',
            'data':'El medicamento aún no ha sido registrado'
        }
        return JsonResponse(response)
    return JsonResponse({'data':medicamento.data})
     #la clave tiene que ser data para que funcione con el metodo.

def autocompletado_medicamento(request):
    
    medicamentos=Medicamento.objects.values('nombre_generico',).all()
    medicamentosList=[]
    for medicamento in medicamentos:
        medicamentosList.append(medicamento['nombre_generico'])
    return JsonResponse({"data":medicamentosList})
    #la clave tiene que ser data para que funcione con el metodo



from modulo_expediente.forms import SignosVitalesForm
from modulo_expediente.models import ( Consulta, ContieneConsulta,  SignosVitales)
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import HttpResponseForbidden

from modulo_expediente.serializers import SignosVitalesSerializer
@csrf_exempt
@login_required
def modificar_signosVitales(request, id_consulta):
    datos={
        "empleado":request.user,
        "id_consulta":int(id_consulta),
        "unidad_temperatura":request.POST['unidad_temperatura'],
        "unidad_peso":request.POST['unidad_peso'],
        "valor_temperatura":request.POST['valor_temperatura'],
        "valor_peso":request.POST['valor_peso'],
        "valor_arterial_diasolica":request.POST['valor_presion_arterial_diastolica'],
        "valor_arterial_sistolica":request.POST['valor_presion_arterial_sistolica'],
        "valor_frecuencia_cardiaca":request.POST['valor_frecuencia_cardiaca'],
        "valor_saturacion_oxigeno":request.POST['valor_saturacion_oxigeno'],
    }
    response=SignosVitales.objects.modificar_signos_vitales(datos)
    contieneConsulta=ContieneConsulta.objects.filter(consulta__id_consulta=id_consulta).latest('fecha_de_cola')
    contieneConsulta.fase_cola_medica="3"
    contieneConsulta.save()

    return JsonResponse(response, safe=False)
def crear_signos_vitales(request,id_consulta):
    if request.method=='POST':
        consulta=Consulta.objects.get(id_consulta=id_consulta)
        form_signos_vitales=SignosVitalesForm(request.POST)
        if form_signos_vitales.is_valid():
            signos_vitales=form_signos_vitales.save(commit=False)
            signos_vitales.consulta=consulta
            signos_vitales.enfermera=request.user
            signos_vitales.save()
            response={
                'type':'success',
                'data':'Guardado!'
            }
        else:
            response={
                'type':'warning',
                'data':'No se pudo guardar. Intente de nuevo.'
            }
        return JsonResponse(response)
    return HttpResponseForbidden()
def get_signos_vitales(request,id_consulta):
    if request.method=='GET':
        try:
            signos_vitales=SignosVitales.objects.filter(consulta__id_consulta=id_consulta)
            
            response={
                'signos_vitales':SignosVitalesSerializer(signos_vitales,many=True).data
            }
        except:
            response={
                'signos_vitales':[]
            }
        return JsonResponse(response)
# def get_signos_vitales(request,id_consulta):
#     if request.method=='GET':
#         try:
#             signos_vitales=SignosVitales.objects.filter(consulta__id_consulta=id_consulta).values()
            
#             response={
#                 'signos_vitales':list(signos_vitales)
#             }
#         except:
#             response={
#                 'signos_vitales':[]
#             }
#         return JsonResponse(response)
        
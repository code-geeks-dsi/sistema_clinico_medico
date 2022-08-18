from modulo_expediente.models import ( ContieneConsulta,  SignosVitales)
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

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
    contieneConsulta=ContieneConsulta.objects.get(consulta__id_consulta=id_consulta)
    contieneConsulta.fase_cola_medica="3"
    contieneConsulta.save()

    return JsonResponse(response, safe=False)
def crear_signos_vitales(request,id_contiene_consulta):
    contiene_consulta=ContieneConsulta.object.get(id=id_contiene_consulta).select_related('consulta')
    consulta=contiene_consulta.consulta
    print(consulta)
    # contiene_consulta.fase_cola_medica="3"
    # contiene_consulta.save()
    # signos_vitales=SignosVitales(consulta=consulta,
    # enfermera=request.user,
    # unidad_temperatura=request.POST["unidad_temperatura"],
    # unidad_peso=request.POST["unidad_peso"],
    # valor_temperatura=request.POST["valor_temperatura"],
    # valor_peso=request.POST["valor_peso"],
    # valor_presion_arterial_diastolica=request.POST["valor_arterial_diasolica"],
    # valor_presion_arterial_sistolica=request.POST["valor_arterial_sistolica"],
    # valor_frecuencia_cardiaca=int(request.POST["valor_frecuencia_cardiaca"]),
    # valor_saturacion_oxigeno=request.POST["valor_saturacion_oxigeno"])
    
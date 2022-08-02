from django.db import models

class SignosVitalesManager(models.Manager):
    def modificar_signos_vitales(self, datos):
        response={
            'type':'warning',
            'title':'',
            'data':''
        }
        if datos["empleado"].roles.codigo_rol =='ROL_ENFERMERA':
            try:
                self.filter(consulta=datos["id_consulta"]).update(
                    unidad_temperatura=datos["unidad_temperatura"],
                    unidad_peso=datos["unidad_peso"],
                    valor_temperatura=datos["valor_temperatura"],
                    valor_peso=datos["valor_peso"],
                    valor_presion_arterial_diastolica=datos["valor_arterial_diasolica"],
                    valor_presion_arterial_sistolica=datos["valor_arterial_sistolica"],
                    valor_frecuencia_cardiaca=int(datos["valor_frecuencia_cardiaca"]),
                    valor_saturacion_oxigeno=datos["valor_saturacion_oxigeno"],
                    enfermera= datos["empleado"]
                )
                response['type']='success'
                response['data']='Se han registrado los signos vitales'
            except ValueError:
                response['data']="Ingrese todos los datos."
        else:
            response['data']="Error de datos, posiblemente no tienen el nivel de acceso necesario."
        return response



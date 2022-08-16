from django.contrib import admin
from modulo_control.models import Empleado,Rol

from modulo_expediente.models import (
    Consulta, Paciente, Expediente, ContieneConsulta, SignosVitales,Dosis,Medicamento, RecetaMedica, 
    Archivo, DocumentoExpediente
    )

# Register your models here.
admin.site.register(Paciente)
admin.site.register(Expediente)
admin.site.register(ContieneConsulta)
admin.site.register(Consulta)
admin.site.register(SignosVitales)
admin.site.register(Rol)
admin.site.register(Archivo)
admin.site.register(DocumentoExpediente)
admin.site.register(Dosis)

admin.site.register(Medicamento)
admin.site.register(RecetaMedica)


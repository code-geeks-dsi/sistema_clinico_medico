from django.contrib import admin
from modulo_control.models import Rol

from modulo_expediente.models import *

# Register your models here.
admin.site.register(Paciente)
admin.site.register(Expediente)
admin.site.register(ContieneConsulta)
admin.site.register(TipoConsulta)
admin.site.register(Consulta)
admin.site.register(SignosVitales)
admin.site.register(Rol)
admin.site.register(Archivo)
admin.site.register(DocumentoExpediente)
admin.site.register(Dosis)
admin.site.register(HorarioConsulta)
admin.site.register(Medicamento)
admin.site.register(RecetaMedica)
admin.site.register(CitaConsulta)
admin.site.register(RecetaOrdenExamenLaboratorio)
admin.site.register(RecetaOrdenExamenLaboratorioItem)


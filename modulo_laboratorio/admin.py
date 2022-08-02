from django.contrib import admin
from modulo_laboratorio.models import Categoria, CategoriaExamen, ExamenLaboratorio, Parametro, EsperaExamen, ContieneValor, RangoDeReferencia, Resultado

# Register your models here.
admin.site.register(Categoria)
admin.site.register(CategoriaExamen)
admin.site.register(ExamenLaboratorio)
admin.site.register(Parametro)
admin.site.register(EsperaExamen)
admin.site.register(ContieneValor)
admin.site.register(Resultado)
admin.site.register(RangoDeReferencia)

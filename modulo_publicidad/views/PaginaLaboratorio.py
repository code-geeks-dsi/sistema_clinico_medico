#Python

#Django
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView

class PaginaLaboratorio(TemplateView):
    template_name= "publicidad/paginaDeLaboratorio/paginaDeLaboratorio.html"
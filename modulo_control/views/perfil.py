#Django
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

class Perfil(LoginRequiredMixin, TemplateView):
    login_url='login'
    template_name = "Control/perfil.html"

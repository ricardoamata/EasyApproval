from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Curso

class AgregarCurso(ListView):
    template_name = 'main/cursoAgregar.html'
    model = Curso
    context_object_name = 'cursos'

"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[''] = 'algo'
        return context
"""
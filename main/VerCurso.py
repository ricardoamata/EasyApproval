from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from   django.views.generic.list import ListView
from main.models import Curso


def detail(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    return render(request, 'main/VerInfoCurso.html', {'curso': curso})

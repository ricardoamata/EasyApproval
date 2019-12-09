from django.shortcuts import render, redirect
from  django.views.generic.list import ListView
from .forms import CursoForm
from django.views.generic import TemplateView
from .models import Curso
from django.views.generic import CreateView, UpdateView


def home(request):
    return render(request, 'main/home.html')

class CursoAdd(TemplateView):
    template_name = 'main/cursoAgregar.html'

    def get(self, request, **kwargs):
        form = CursoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CursoForm(request.POST)
        if form.is_valid():
            obj = Curso.objects.all().first()
            obj.instructor = form.cleaned_data['instructor']
            obj.nombre = form.cleaned_data['nombre']
            obj.duracion = form.cleaned_data['duracion']
            obj.fecha_inicial = form.cleaned_data['fecha_inicial']
            obj.fecha_final = form.cleaned_data['fecha_final']
            obj.financiamiento = form.cleaned_data['financiamiento']
            obj.descripcion = form.cleaned_data['descripcion']
            obj.costo = form.cleaned_data['costo']
            obj.aula = form.cleaned_data['aula']
            obj.cupo = form.cleaned_data['cupo']
            obj.save()
            return redirect('/')
        else:
            form = CursoForm()
        return render(request,'main/cursoAgregar.html', {'form': form})

class CreacionCurso(CreateView):
    model= Curso
    template_name= 'main/cursoAgregar.html'
    form_class = CursoForm

class EditarCurso(UpdateView):
    model=Curso
    template_name = 'main/cursoAgregar.html'
    form_class = CursoForm

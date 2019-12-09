from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Curso
from .forms import CursoForm

class DraftAjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'hash_id': self.object.hash_id,
            }
            return JsonResponse(data)
        else:
            return response

class ListaCursos(ListView):
    template_name = 'curso/lista.html'
    model = Curso
    context_object_name = 'cursos'

class CursoView(DetailView):
    model = Curso
    template_name="curso/detail.html"
    context_object_name = 'curso'

class CreacionCurso(LoginRequiredMixin,
                    UserPassesTestMixin,
                    DraftAjaxableResponseMixin,
                    CreateView,):

    login_url = '/usuario/login'
    model = Curso
    template_name= 'curso/create.html'
    form_class = CursoForm
    success_url = '/'

    def test_func(self):
        return (self.request.user.profile.tipo == 1 or self.request.user.is_superuser)

class EliminacionCurso(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Curso
    template_name = 'curso/delete.html'
    success_url = reverse_lazy('curso:lista')

    def get_object(self):
        return Curso.objects.get(hash_id=self.kwargs['id'])

    def test_func(self):
        obj = self.get_object()
        if self.request.user != obj.owner and not self.request.user.is_superuser:
            raise PermissionDenied("No tienes permiso para eliminar este post")
        return True

class DraftView(LoginRequiredMixin,
                UserPassesTestMixin,
                DraftAjaxableResponseMixin,
                UpdateView):

    login_url = '/usuario/login'
    model = Curso
    template_name = 'curso/create.html'
    form_class = CursoForm
    success_url = "/"

    def get_object(self):
        return Curso.objects.get(hash_id=self.kwargs['id'])

    def test_func(self):
        obj = self.get_object()
        if obj.estado > 1:
            raise Http404
        if self.request.method == 'POST' and obj.estado == 1:
            raise PermissionDenied("El borrador ya no puede ser modificado.")
        if not self.request.user.is_superuser and self.request.user != obj.owner and self.request.user.profile != obj.instructor:
            raise PermissionDenied("No tienes permiso de acceso a este borrador de curso.")
        return True
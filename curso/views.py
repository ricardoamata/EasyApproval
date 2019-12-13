from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib import messages
import io
from django.core.files import File
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import date

from .models import Curso, Inscripcion
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            curso = self.get_object()
            inscrito = Inscripcion.objects.filter(curso=curso, alumno=self.request.user).exists()
            context['inscrito'] = inscrito
            if inscrito:
                inscripcion = Inscripcion.objects.get(curso=curso, alumno=self.request.user)
                if inscripcion.calificacionCurso or inscripcion.calificacionInstructor:
                    context['evaluado_por_alumno'] = True
            if curso.cupo_max:
                context['cupos_disponibles'] =  curso.cupo_max - curso.inscripcion_set.count()
        return context

class CreacionCurso(LoginRequiredMixin,
                    UserPassesTestMixin,
                    DraftAjaxableResponseMixin,
                    CreateView,):

    login_url = '/usuario/login'
    model = Curso
    template_name= 'curso/create.html'
    form_class = CursoForm
    success_url = '/'

    def handle_no_permission(self):
        raise PermissionDenied("Los alumnos no pueden crear cursos")

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

def inscribir(request, slug):
    curso = Curso.objects.get(slug=slug)
    if request.method == 'POST':
        if curso.inscripcion_set.filter(alumno=request.user).exists():
            return render(request, 'main/error_handler.html', context={'exception': 'Ya estas inscrito inscrito a este curso'})
        inscripcion = Inscripcion(curso=curso, alumno=request.user)
        inscripcion.save()
        return redirect('/curso/ver_curso/'+slug)

    return render(request, 'curso/inscripcion.html', context={'curso': curso})

def solicitar_aprobacion(request, id):
    curso = Curso.objects.get(hash_id=id)
    if curso.estado > 0:
        raise PermissionDenied("Este curso ya ha sido aprovado o ya se ha solicitado una aprobación")
    if request.user != curso.owner and request.user.profile != curso.instructor and not request.user.is_superuser:
        raise PermissionDenied("No tienes derechos para solicitar una aprobación para este curso")

    if request.method == 'POST':
        curso.estado = 1
        curso.save()
        return redirect('/curso/ver_borrador/'+str(id))
    return render(request, 'curso/solicitar_aprobacion.html', context={'curso': curso})

def desinscribir(request, slug):
    curso = Curso.objects.get(slug=slug)
    if request.method == 'POST':
        if not curso.inscripcion_set.filter(alumno=request.user).exists():
            return render(request, 'main/error_handler.html', context={'exception': 'No estas inscrito a este curso'})
        inscripcion = curso.inscripcion_set.get(alumno=request.user)
        inscripcion.delete()
        return redirect('/curso/ver_curso/'+slug)

    return render(request, 'curso/desinscribir.html', context={'curso': curso})

def generar(request, slug):
    curso = Curso.objects.get(slug=slug)
    inscripcion = Inscripcion.objects.get()

    nombre =  "constancia " + curso.slug
    #for inscripcion in Inscripcion.filter(curso=curso):
     #   alumnos = inscripcion.alumno
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    string = nombre + " para " + str(inscripcion.alumno) + ".pdf"
    p.drawString(50,50,string)
    #p.drawString(50,60,instructor)
    #p.drawString(60,70,fecha)
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    inscripcion.pdf.save(nombre, File(buffer))
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=nombre)


def ver_constancia(request):

    pass

def evaluar(request, slug):
    curso = Curso.objects.get(slug=slug)
    inscripcion = Inscripcion.objects.get(curso=curso, alumno=request.user)
    #if date.today() < inscripcion.curso.fecha_final:
    #    raise PermissionDenied("Aun no puedes evaluar este curso")
    if inscripcion.calificacionCurso or inscripcion.calificacionInstructor:
        raise PermissionDenied("Ya has evaluado este curso, no puedes evaluarlo nuevamente")
    if request.method == "POST":
        inscripcion.calificacionCurso = request.POST["evalCurso"]
        inscripcion.calificacionInstructor = request.POST["evalInstructor"]
        inscripcion.sugerenciaCurso = request.POST["sugerenciaCurso"]
        inscripcion.sugerenciaInstructor = request.POST["sugerenciaInstructor"]
        inscripcion.save()
        messages.success(request, 'Información guardada correctamente.')
        return redirect('/curso/ver_curso/' + slug)

    return render(request, 'curso/evaluar.html', context={'curso': curso})
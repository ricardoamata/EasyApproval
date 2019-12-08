from django.urls import path
from . import VerCurso
from .home_view import HomeView
#from .agregarCurso_view import AgregarCurso
from .views import CreacionCurso
from .views import EditarCurso


app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('crear_curso', CreacionCurso.as_view(),name='crear_curso'),
    path('Curso/<slug:curso_slug>/', VerCurso.detail, name='detail'),
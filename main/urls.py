from django.urls import path
from .home_view import HomeView
#from .agregarCurso_view import AgregarCurso
from .views import CreacionCurso
from .views import EditarCurso


app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('crear_curso', CreacionCurso.as_view(),name='crear_curso'),
    path('editar_curso/<slug:slug>', EditarCurso.as_view(),name='editar_curso')

]

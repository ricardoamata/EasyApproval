from django.urls import path
from .home_view import HomeView
#from .agregarCurso_view import AgregarCurso
from .views import CreacionCurso
from .views import EditarCurso


app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('agregarCurso', CreacionCurso.as_view(),name='crear_curso'),
    path('editarCurso/<int:pk>', EditarCurso.as_view(),name='editar_curso')

]

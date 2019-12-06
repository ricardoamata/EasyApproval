from django.urls import path
from .home_view import HomeView
from .agregarCurso_view import AgregarCurso
from .views import CreacionCurso
app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('agregarCurso', CreacionCurso.as_view(),name='crear_curso')
]
from django.urls import path
from . import VerCurso
from .home_view import HomeView

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('Curso/<int:curso_id>/', VerCurso.detail, name='detail'),
]
from django.urls import path

from curso.views import ListaCursos

app_name = 'main'

urlpatterns = [
    path('', ListaCursos.as_view(), name='home'),
]
from django.urls import path

from . import views

app_name = 'curso'

urlpatterns = [
    path('', views.ListaCursos.as_view(), name='lista'),
    path('ver_curso/<slug:slug>', views.CursoView.as_view(), name='detalle'),
    path('crear_borrador', views.CreacionCurso.as_view(), name='crear'),
    path('ver_borrador/<uuid:id>', views.DraftView.as_view(), name='editar'),
    path('eliminar_borrador/<uuid:id>', views.EliminacionCurso.as_view(), name='eliminar'),
]
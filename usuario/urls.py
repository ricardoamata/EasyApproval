from django.urls import path

from . import views

app_name = 'usuario'

urlpatterns = [
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.logout_view, name="logout"),
    path('api/add_draft', views.add_draft, name='add_draft'),
    path('api/remove_draft', views.remove_draft, name='remove_draft'),
]
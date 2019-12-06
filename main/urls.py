from django.urls import path
from .home_view import HomeView

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
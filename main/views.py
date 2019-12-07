from django.shortcuts import render
from django.views.generic import DetailView
from .models import Curso

def home(request):
    return render(request, 'main/home.html')
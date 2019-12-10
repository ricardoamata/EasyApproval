from django.shortcuts import render, redirect
from django.template import RequestContext

def home(request):
    return render(request, 'main/home.html')

def handler403(request, exception=None, *args, **argv):
    response = render(request, 'main/error_handler.html', context={'exception': exception})
    response.status_code = 403
    return response
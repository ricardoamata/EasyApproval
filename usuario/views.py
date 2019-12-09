from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate

class LoginView(TemplateView):
    next_page = '/'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        if 'next' in request.GET:
            self.next_page = request.GET['next']
        return render(request, 'usuario/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(self.next_page)
        return render(request, 'usuario/login.html', {"error":"The username or the password is wrong."})

    
def logout_view(request):
    logout(request)
    return redirect('/')

def add_draft(request):
    if request.method == 'POST' and request.user.is_authenticated:
        request.user.profile.numero_borradores += 1
        request.user.save()
        return JsonResponse({})
    return JsonResponse({}, status=403)


def remove_draft(request):
    if request.method == 'POST' and request.user.is_authenticated:
        if request.user.profile.numero_borradores:
            return JsonResponse({'msg': 'no hay borradores'}, status=400)
        request.user.profile.numero_borradores -= 1
        request.user.save()
        return JsonResponse({})
    return JsonResponse({}, status=403)
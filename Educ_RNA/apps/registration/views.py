from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.views import auth_login
from django.contrib.auth.models import User
from apps.registration.forms import UsuarioForm
from django.views.generic import CreateView
import requests
from django.contrib.auth import authenticate
# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        data = {'username': username, 'password': password}
        r = requests.post('http://127.0.0.1:8000/api/login/', data=data)
        if r.status_code == 404:
            messages.error(request, 'usuario o contraseña incorrecto')
            return redirect('/')
        else:
            if r.status_code == 200:
                user = authenticate(username=username, password=password)
                auth_login(request, user)
                return redirect('usuarios/index/')
            else:
                return HttpResponse()
    else:
        return render(request, 'registration/login.html')


class RegistroUsuario(CreateView):
    model = User
    template_name = "registration/registrar.html"
    form_class = UsuarioForm
    success_url = '/'

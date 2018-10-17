from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.views import auth_login
from django.contrib.auth.models import User
from apps.usuarios.forms import UsuarioForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
import requests
from django.contrib.auth import authenticate
from apps.usuarios.forms import BucketForm
# Create your views here.


def home(request):
    if request.method == "POST":
        data = {'name': request.POST.get('name', False)}
        r = requests.post('http://127.0.0.1:8000/api/bucketlists/', data=data)
        if r.status_code == 201:
            data = r.json()
            print(data)
            return HttpResponse()
        else:
            return render(request, 'registration/login.html')
    else:
        return render(request, 'usuarios/index.html')


def index(request):
    return render(request, 'usuarios/index.html')


def prueba(request):
    form = BucketForm()
    return render(request, 'usuarios/prueba.html', {'form': form})


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
    template_name = "usuarios/registrar.html"
    form_class = UsuarioForm
    success_url = '/'

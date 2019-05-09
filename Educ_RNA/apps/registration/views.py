from django.shortcuts import render
from django.conf import settings
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

# Vistas de la app registration, en este caso se trata de la logica y las llamadas a las funciones necesarias para todas
# las funcionalidades relacionadas con los registros de usuarios, asi como el login(ingreso) y el logout(salida)


class LogicaRegistration:

    # Funcion que envia al API las creedenciales para su autentificacion
    def login(request):
        # Si recibe un metodo POST realiza la autenticacion con el API
        if request.method == 'POST':
            # Obtiene los creedenciales ingresados por el usuario en el formulario de ingreso
            usuario = User(username=request.POST.get('username', False), password=request.POST.get('password', False))
            data = {'username': usuario.username, 'password': usuario.password}
            # Llamada al metodo del API que realizara la autenticacion, con los respectivos creedenciales
            r = requests.post(settings.API_PATH + 'login/', data=data)
            # En caso de recibir el codigo 404 se dispondra un mensaje de error
            if r.status_code == 404:
                messages.error(request, 'usuario o contraseña incorrecto')
                return redirect('/')
            else:
                # En caso de recibir el codigo 200 se autenticara el usuario y se le permitira el ingreso a la aplicacion
                if r.status_code == 200:
                    user = authenticate(username=usuario.username, password=usuario.password)
                    auth_login(request, user)
                    return redirect('usuarios/index/')
        # Si no recibe un metodo POST solo se renderizara la ventana
        else:
            return render(request, 'registration/login.html')

    # Funcion que carga el formulario de registro de usuario en pantalla
    class RegistroUsuario(CreateView):
        model = User
        template_name = "registration/registrar.html"
        form_class = UsuarioForm
        success_url = '/'

    # Funcion que realiza la llamada al API para que se registre el usuario.
    def registro_usuario(request):
        # En caso de recibir un metodo POST se realiza la llamada al API
        if request.method == 'POST':
            # Obtiene todos los valores introducidos por el usuario en el formulario de registro
            usuario = User(username=request.POST.get('username', False), password=request.POST.get('password1', False),
                           first_name=request.POST.get('first_name', False),
                           last_name=request.POST.get('last_name', False), email=request.POST.get('email', False))
            confirm_password = request.POST.get('password2', False)
            data = {'username': usuario.username, 'password': usuario.password, 'confirm_password': confirm_password,
                    'first_name': usuario.first_name, 'last_name': usuario.last_name, 'email': usuario.email}
            # Llamada al API con los datos para que se registre el usuario en la base de datos
            r = requests.post(settings.API_PATH + 'registrar-usuario/', data=data)
            # Se revisa la respuesta del API para determinar si ocurrieron errores con la contraseña
            # errorpass = r.text.partition("error[")[2].partition("]")[0]
            # Se revisa la respuesta del API para determinar si ocurrieron otros errores
            error = r.text.partition("[")[2].partition("]")[0]
            # Si existe un error, se muestra en pantalla
            if error:
                messages.error(request, error)
                return redirect('/registration/registrar')
            # En caso de no tener errores se redirige al login, siendo exitoso el registro
            return redirect('/')
        else:
            return HttpResponse()



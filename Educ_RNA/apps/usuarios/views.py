from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from apps.usuarios.forms import ModificarUsuarioForm
from django.shortcuts import get_object_or_404
import requests
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate
# Create your views here.

# Vistas de la app usuarios, en este caso se trata de la logica y las llamadas a las funciones necesarias para todas las
# funcionalidades relacionadas con el modulo de usuarios, como el perfil y la pagina de inicio


class LogicaUsuarios:

    # Funcion que renderiza la pagina de inicio
    def index(self):
        return render(self, 'usuarios/index.html')

    # Funcion que renderiza la pagina del perfil del usuario
    def perfil(self):
        return render(self, 'usuarios/perfil.html')

    # Funcion que renderiza la pagina de informacion nuestra
    def nosotros(self):
        return render(self, 'usuarios/nosotros.html')

    # Funcion que renderiza la pagina del progreso del usuario
    def progreso(self):
        return render(self, 'usuarios/progreso.html')

    # Funcion que carga el formulario de modificacion de usuario en pantalla
    class AbrirModificarUsuario(UpdateView):
        model = User
        template_name = "usuarios/modificar.html"
        form_class = ModificarUsuarioForm

    # Obtiene el usuario para desplegar la informacion en los campos
        def get_object(self):
            id_ = self.kwargs.get("id")
            return get_object_or_404(User, id=id_)

    # Funcion que modifica la informacion del usuario
    def modificacion_usuario(self):
        # En caso de recibir un metodo POST se realiza la llamada al API
        id_ = str(self.user.id)
        usuario = User()
        if self.method == 'POST':
            # Obtiene todos los valores introducidos por el usuario en el formulario de modificacion
            usuario.username = self.POST.get('username', False)
            usuario.first_name = self.POST.get('first_name', False)
            usuario.last_name = self.POST.get('last_name', False)
            data = {'username': usuario.username, 'first_name': usuario.first_name, 'last_name': usuario.last_name}
            # Llamada al API con los datos para que se modifique el usuario en la base de datos
            r = requests.put(settings.API_PATH + 'actualizar-usuario/'+id_, data=data)
            # Se revisa la respuesta del API para determinar si ocurrieron errores
            error = r.text.partition("[")[2].partition("]")[0]
            # Si el codigo es 400, se muestra el error en pantalla
            if r.status_code == 400:
                messages.error(self, error)
                return redirect('/usuarios/abrir-modificar/%3Fid='+id_)
            # En caso de no recibir codigo 400  se redirige al perfil, siendo exitosa la modificacion
            messages.success(self, "Usuario modificado exitosamente")
            return redirect('/usuarios/perfil')

    # Funcion que realiza el cambio de contraseña del usuario
    def cambio_constrasena(self):
        usuario = User()
        if self.method == 'POST':
            # Obtiene todos los valores introducidos por el usuario en el formulario de cambio de contraseña
            usuario.username = self.user.username
            old_password = self.POST.get('oldpass', False)
            new_password = self.POST.get('newpass', False)
            new_password2 = self.POST.get('newpass2', False)
            data = {'username': usuario.username, 'old_password': old_password, 'new_password': new_password, 'new_password2': new_password2}
            # Llamada al API con los datos para que se cambie la contraseña en la base de datos
            r = requests.put(settings.API_PATH + 'cambio-contrasena/', data=data)
            # Se revisa la respuesta del API para determinar si ocurrieron errores
            error = r.text.partition("[")[2].partition("]")[0]
            # Si el codigo es 400, se muestra el error en pantalla
            if error:
                messages.error(self, error)
                return redirect('/usuarios/cambiar-contrasena')
            # En caso de no recibir codigo 400  se redirige al perfil, siendo exitoso el cambio
            user = authenticate(username=usuario.username, password=new_password)
            update_session_auth_hash(self, user)
            messages.success(self, "Contraseña cambiada exitosamente")
            return redirect('/usuarios/perfil')
        else:
            return render(self, 'usuarios/cambiarcontraseña.html')

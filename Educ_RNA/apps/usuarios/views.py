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
from rest_framework.response import Response
from .models import Progreso, Calificacion
from django.http import HttpResponse
from apps.evaluaciones.models import Prueba
from apps.lecciones.models import Tema, Leccion
# Create your views here.

# Vistas de la app usuarios, en este caso se trata de la logica y las llamadas a las funciones necesarias para todas las
# funcionalidades relacionadas con el modulo de usuarios, como el perfil y la pagina de inicio


class LogicaUsuarios:
    user = User()
    method = HttpResponse()
    POST = method

    # Funcion que renderiza la pagina de inicio
    def index(self):
        return render(self, 'usuarios/index.html')

    # Funcion que renderiza la pagina del perfil del usuario
    def perfil(self):
        return render(self, 'usuarios/perfil.html')

    # Funcion que renderiza la pagina de informacion nuestra
    def nosotros(self):
        return render(self, 'usuarios/nosotros.html')

    def calificacion(self):
        try:
            calificacion = LogicaUsuarios.consultar_calificacion(self.user.pk)
            cdict = {'calificacion': calificacion.data}
            return render(self, 'usuarios/calificaciones.html', cdict)
        except ConnectionError as e:
            messages.error(self, 'Error de conexion')
            return redirect('/')

    # Funcion que renderiza la pagina del progreso del usuario
    def progreso(self):
        try:
            progreso = LogicaUsuarios.consultar_progreso(self.user.pk)
            cdict = {'progreso': progreso.data}
            return render(self, 'usuarios/progreso.html', cdict)
        except ConnectionError as e:
            messages.error(self, 'Error de conexion')
            return redirect('/usuarios/perfil')

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
        try:
            # En caso de recibir un metodo POST se realiza la llamada al API
            id_ = str(self.user.pk)
            if self.method == 'POST':
                # Obtiene todos los valores introducidos por el usuario en el formulario de modificacion
                usuario = User(username=self.POST.get('username', False), first_name=self.POST.get('first_name', False),
                               last_name=self.POST.get('last_name', False))
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
        except ConnectionError as e:
            messages.error(self, 'Error de conexion')
            return redirect('/usuarios/perfil')

    # Funcion que realiza el cambio de contraseña del usuario
    def cambio_constrasena(self):
        try:
            if self.method == 'POST':
                # Obtiene todos los valores introducidos por el usuario en el formulario de cambio de contraseña
                usuario = User(username=self.user.username, password=self.POST.get('oldpass', False))
                new_password = self.POST.get('newpass', False)
                new_password2 = self.POST.get('newpass2', False)
                data = {'username': usuario.username, 'old_password': usuario.password, 'new_password': new_password,
                        'new_password2': new_password2}
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
        except ConnectionError as e:
            messages.error(self, 'Error de conexion')
            return redirect('/usuarios/perfil')

    # Funcion que consulta las calificacioes de un determinado usuario
    @staticmethod
    def consultar_calificacion(usuario_id):
        try:
            lista = []
            # Llamada al metodo del api que consulta la calificacion de un usuario determinado por su id
            r = requests.get(settings.API_PATH + 'ver-calificacion/' + str(usuario_id))
            # Se convierte la respuesta en json para poder extraer sus datos
            rjson = r.json()
            # Se recorre la lista de calificaciones extrayendo los datos necesarios
            for item in rjson:
                id_ = item["id"]
                prueba_id = item["prueba_id"]
                nota_actual = item["nota"]
                mejor_nota = item["mejor_nota"]
                intentos = item["intentos"]
                # Llamada al metodo que obtiene una prueba por su id
                prueba = LogicaUsuarios.consultar_prueba_id(prueba_id)
                # Se utiliza el id de la leccion de la prueba obtenida para obtener la leccion correspondiente
                leccion = LogicaUsuarios.consultar_leccion_id(prueba.data.leccion_id)
                # Se extrae el nombre de la leccion
                nombre_leccion = leccion.data.nombre
                # Se intancia un objeto tipo Calificacion con todos los datos
                calificacion = Calificacion(pk=id_, nota=nota_actual, mejor_nota=mejor_nota, intentos=intentos,
                                            prueba_id=prueba_id)
                # Se agregan a la lista el objeto calificacion y el nombre de la leccion a la cual pertenece
                lista.append((calificacion, nombre_leccion))
            # Si la lista no esta vacia se devuelve un Response, con la lista y el codigo 200
            if len(lista) != 0:
                return Response(lista, 200)
            # Si la lista esta vacia se devuelve el mensaje de error correspondiente y un objeto vacio, con codigo 404
            else:
                nombre_leccion = "No ha hecho examenes"
                calificacion = Calificacion()
                lista.append((calificacion, nombre_leccion))
                return Response(lista, 404)
        except ConnectionError as e:
            raise e
        except KeyError as e:
            detail = rjson["detail"]
            return Response(detail, 404)

    # Funcion que consulta el progreso de un determinado usuario
    @staticmethod
    def consultar_progreso(usuario_id):
        try:
            # Llamada al metodo del api que consulta el progreso de un usuario determinado por su id
            r = requests.get(settings.API_PATH + 'ver-progreso/' + str(usuario_id))
            # Se convierte la respuesta en json para poder extraer sus datos
            rjson = r.json()
            # Se extra el id del tema del progreso y con el se instancia un objeto tipo Progreso
            if r.status_code == 200:
                progreso = Progreso(tema_id=rjson["tema_id"])
                tema_id = progreso.tema
                tema = LogicaUsuarios.consultar_tema_id(tema_id)
                nombre_tema = tema.data.nombre
                leccion = LogicaUsuarios.consultar_leccion_id(tema.data.leccion_id)
                nombre_leccion = leccion.data.nombre
                resp = (nombre_leccion, nombre_tema)
            else:
                resp = ('No ha empezado', 'No ha empezado')
            # Se devuelve un Response, con el objeto y el codigo 200
            return Response(resp, 200)
        except ConnectionError as e:
            raise e
        except KeyError as e:
            detail = rjson["detail"]
            return Response(detail, 404)

    # Funcion que consulta una leccion por el id
    @staticmethod
    def consultar_calificacion_prueba(usuario_id, prueba_id):
        try:
            # Llamada al metodo del api que consulta en la base de datos una leccion de un determinado id
            r = requests.get(settings.API_PATH + 'ver-calificacionprueba/' + str(usuario_id) + '/' + str(prueba_id))
            # Se convierte la respuesta en json para poder extraer sus datos
            rjson = r.json()
            # Se instancia un objeto tipo Leccion con los datos obtenidos de la llamada al api
            if r.status_code == 200:
                calificacion = Calificacion(pk=rjson["id"], mejor_nota=rjson["mejor_nota"])
                # Se devuelve un Response con el objeto y el codigo 200
                return Response(calificacion, 200)
            else:
                calificacion = Calificacion()
                # Se devuelve un Response con el objeto y el codigo 200
                return Response(calificacion, 404)
        except ConnectionError as e:
            # En caso de excepcion se devuelve el codigo de error 400
            raise e

    # Funcion que registra en la base de datos el progreso de un usuario
    @staticmethod
    def registrar_progreso(usuario_id, tema_id):
        try:
            # Se arma un dictionary con los datos a enviar al api
            data = {'usuario_id': usuario_id, 'tema_id': tema_id}
            # Llamada al metodo del api que registra el progreso, pasandole los datos para sus insercion
            r = requests.post(settings.API_PATH + 'registrar-progreso/', data=data)
        except ConnectionError as e:
            raise e

    # Funcion que actualiza en la base de datos el progreso de un usuario
    @staticmethod
    def actualizar_progreso(usuario_id, tema_id):
        try:
            # Se arma un dictionary con los datos a enviar al api
            data = {'usuario_id': usuario_id, 'tema_id': tema_id}
            # Llamada al metodo del api que actualiza el progreso, pasandole los datos para sus insercion
            r = requests.put(settings.API_PATH + 'actualizar-progreso/', data=data)
        except ConnectionError as e:
            raise e

    # Funcion que consulta un tema por el id
    @staticmethod
    def consultar_tema_id(tema_id):
        try:
            # Llamada al metodo del api que consulta en la base de datos un tema de un determinado id
            r = requests.get(settings.API_PATH + 'ver-tema/' + str(tema_id))
            # Se convierte la respuesta en json para poder extraer sus datos
            rjson = r.json()
            # Se instancia un objeto tipo Tema con los datos obtenidos de la llamada al api
            tema = Tema(pk=rjson["id"], nombre=rjson["nombre"], leccion_id=rjson["leccion_id"])
            # Se devuelve un Response con el objeto y el codigo 200
            return Response(tema, 200)
        except ConnectionError as e:
            # En caso de excepcion se devuelve el codigo de error 400
            raise e

    # Funcion que consulta una leccion por el id
    @staticmethod
    def consultar_leccion_id(leccion_id):
        try:
            # Llamada al metodo del api que consulta en la base de datos una leccion de un determinado id
            r = requests.get(settings.API_PATH + 'ver-leccion/' + str(leccion_id))
            # Se convierte la respuesta en json para poder extraer sus datos
            rjson = r.json()
            # Se instancia un objeto tipo Leccion con los datos obtenidos de la llamada al api
            leccion = Leccion(pk=rjson["id"], nombre=rjson["nombre"])
            # Se devuelve un Response con el objeto y el codigo 200
            return Response(leccion, 200)
        except ConnectionError as e:
            # En caso de excepcion se devuelve el codigo de error 400
            raise e

    # Funcion que consulta una prueba por el id de la leccion a la que pertenezca
    @staticmethod
    def consultar_prueba(leccion_id):
        try:
            # Llamada al metodo del api que consulta en la base de datos una prueba de una determinada leccion
            r = requests.get(settings.API_PATH + 'ver-prueba/' + str(leccion_id))
            # Se convierte la respuesta en json para poder extraer sus datos
            rjson = r.json()
            # Si la consulta es exitosa se instancia un objeto tipo Prueba con los datos obtenidos de la llamada al api
            if r.status_code == 200:
                prueba = Prueba(pk=rjson["id"])
                # Se devuelve un Response con el objeto prueba y el codigo 200
                return Response(prueba, 200)
            # Si la consulta no es exitosa se devuelve un objeto Prueba con id=1 y el codigo 200
            else:
                prueba = Prueba(pk=1)
                return Response(prueba, 200)
        except ConnectionError as e:
            # En caso de excepcion se devuelve el codigo de error 400
            raise e

    # Funcion que consulta un prueba por su propio id
    @staticmethod
    def consultar_prueba_id(prueba_id):
        try:
            # Llamada al api con el id de la prueba que se quiere consultar
            r = requests.get(settings.API_PATH + 'ver-pruebaid/' + str(prueba_id))
            # Se convierte la respuesta en json para poder extraer sus datos
            rjson = r.json()
            # Se intancia un objeto tipo Prueba con los datos del json
            prueba = Prueba(pk=rjson["id"], leccion_id=rjson["leccion_id"])
            # Se devuelve el objeto prueba con codigo 200
            return Response(prueba, 200)
        except ConnectionError as e:
            raise e
        except KeyError as e:
            detail = rjson["detail"]
            return Response(detail, 404)

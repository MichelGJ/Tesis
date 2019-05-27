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
from apps.lecciones.models import Tema, Leccion, Curso
from django.db import IntegrityError
from django.http import request
# Create your views here.

# Vistas de la app usuarios, en este caso se trata de la logica y las llamadas a las funciones necesarias para todas las
# funcionalidades relacionadas con el modulo de usuarios, como el perfil y la pagina de inicio


class LogicaUsuarios:
    user = User()
    method = HttpResponse()
    POST = method
    """
    Funciones de renderizacion
    """

    # Funcion que renderiza la pagina de inicio
    def index(self):
        return render(self, 'usuarios/index.html')

    # Funcion que renderiza la pagina del perfil del usuario
    def perfil(self):
        return render(self, 'usuarios/perfil.html')

    # Funcion que renderiza la pagina de informacion nuestra
    def nosotros(self):
        return render(self, 'usuarios/nosotros.html')

    # Funcion que renderiza la pagina de las calificaciones del usuario
    def calificacion(self):
        try:
            # Se consultan las calificaciones del usuario
            calificacion = LogicaUsuarios.consultar_calificacion(self.user.pk)
            # Se arma un dictionary para pasar los datos a la interfaz
            cdict = {'calificacion': calificacion.data}
            # Se renderiza la plantilla con los datos generados
            return render(self, 'usuarios/calificaciones.html', cdict)
        except ConnectionError as e:
            messages.error(self, 'Error de conexion')
            return redirect('/')

    # Funcion que renderiza la pagina del progreso del usuario
    def progreso(self):
        try:
            # Se consulta el progreso del usuario
            progreso = LogicaUsuarios.consultar_progreso(self.user.pk)
            # Se arma un dictionary para pasar los datos a la interfaz
            cdict = {'progreso': progreso.data}
            # Se renderiza la plantilla con los datos generados
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

    """
    Funciones Complementarias
    """

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
                if int(mejor_nota) >= 10:
                    aprobado = True
                else:
                    aprobado = False
                # Se agregan a la lista el objeto calificacion y el nombre de la leccion a la cual pertenece
                lista.append((calificacion, nombre_leccion, aprobado))
            # Si la lista no esta vacia se devuelve un Response, con la lista y el codigo 200
            if len(lista) != 0:
                return Response(lista, 200)
            # Si la lista esta vacia se devuelve el mensaje de error correspondiente y un objeto vacio, con codigo 404
            else:
                nombre_leccion = "No ha hecho examenes"
                calificacion = Calificacion(intentos=0)
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
        lista=[]
        try:
            # Llamada al metodo del api que consulta el progreso de un usuario determinado por su id
            r = requests.get(settings.API_PATH + 'ver-progreso/' + str(usuario_id))
            # Se convierte la respuesta en json para poder extraer sus datos
            rjson = r.json()
            for item in rjson:
                # Con el id del tema de la consulta se busca el tema
                tema = LogicaUsuarios.consultar_tema_id(item["tema_id"])
                # De la consulta del tema se obtiene su nombre
                nombre_tema = tema.data.nombre
                # Se busca la leccion con el id de leccion del tema consultado
                leccion = LogicaUsuarios.consultar_leccion_id(tema.data.leccion_id)
                # De la consulta de la leccion se obtiene su nombre
                nombre_leccion = leccion.data.nombre
                # Con el id del curso de la consulta se busca el curso
                curso = LogicaUsuarios.consultar_curso_id(item["curso_id"])
                # Se extrae el nombre del curso de la consulta
                nombre_curso = curso.data.nombre
                # Se arma un tuple con ambos nombres
                lista.append((nombre_curso, nombre_leccion, nombre_tema))
            # Se devuelve un Response, con el objeto y el codigo 200
            if len(lista) != 0:
                return Response(lista, 200)
            else:
                nombre_curso = "No ha empezado"
                nombre_leccion = "No ha empezado"
                nombre_tema = "No ha empezado"
                lista.append((nombre_curso, nombre_leccion, nombre_tema))
                return Response(lista, 404)
        except ConnectionError as e:
            raise e
        except KeyError as e:
            detail = rjson["detail"]
            return Response(detail, 400)

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
                calificacion = Calificacion(pk=rjson["id"], mejor_nota=rjson["mejor_nota"], nota=rjson["nota"],
                                            intentos=rjson["intentos"])
                # Se devuelve un Response con el objeto y el codigo 200
                return Response(calificacion, 200)
            else:
                calificacion = Calificacion(mejor_nota=0)
                # Se devuelve un Response con el objeto y el codigo 200
                return Response(calificacion, 404)
        except ConnectionError as e:
            # En caso de excepcion se devuelve el codigo de error 400
            raise e

    # Funcion que registra en la base de datos el progreso de un usuario
    @staticmethod
    def registrar_progreso(usuario_id, tema_id, curso_id):
        try:
            # Se arma un dictionary con los datos a enviar al api
            data = {'usuario_id': usuario_id, 'tema_id': tema_id, 'curso_id': curso_id}
            # Llamada al metodo del api que registra el progreso, pasandole los datos para sus insercion
            r = requests.post(settings.API_PATH + 'registrar-progreso/', data=data)
        except ConnectionError as e:
            raise e

    # Funcion que actualiza en la base de datos el progreso de un usuario
    @staticmethod
    def actualizar_progreso(usuario_id, tema_id, curso_id):
        try:
            # Se arma un dictionary con los datos a enviar al api
            data = {'usuario_id': usuario_id, 'tema_id': tema_id, 'curso_id': curso_id}
            # Llamada al metodo del api que actualiza el progreso, pasandole los datos para sus insercion
            r = requests.put(settings.API_PATH + 'actualizar-progreso/', data=data)
            return r
        except ConnectionError as e:
            raise e
        except IntegrityError as e:
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
            if r.status_code == 200:
                # Se convierte la respuesta en json para poder extraer sus datos
                rjson = r.json()
                # Se instancia un objeto tipo Leccion con los datos obtenidos de la llamada al api
                leccion = Leccion(pk=rjson["id"], nombre=rjson["nombre"], curso_id=rjson["curso_id"])
                # Se devuelve un Response con el objeto y el codigo 200
                return Response(leccion, 200)
        except ConnectionError as e:
            # En caso de excepcion se devuelve el codigo de error 400
            raise e

    # Funcion que consulta un curso por el id
    @staticmethod
    def consultar_curso_id(curso_id):
        try:
            # Llamada al metodo del api que consulta en la base de datos una leccion de un determinado id
            r = requests.get(settings.API_PATH + 'ver-curso/' + str(curso_id))
            if r.status_code == 200:
                # Se convierte la respuesta en json para poder extraer sus datos
                rjson = r.json()
                # Se instancia un objeto tipo Leccion con los datos obtenidos de la llamada al api
                curso = Curso(pk=rjson["id"], nombre=rjson["nombre"])
                # Se devuelve un Response con el objeto y el codigo 200
                return Response(curso, 200)
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

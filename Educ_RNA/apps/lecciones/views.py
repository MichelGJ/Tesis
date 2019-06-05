from django.shortcuts import render
import requests
from .models import Leccion, Tema, InfoTema, Link, Curso
from apps.usuarios.models import Progreso
import os
from django.conf import settings
from django.http import HttpResponse
from apps.usuarios.views import LogicaUsuarios
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.response import Response
from Educ_RNA.strings import Strings
# Create your views here.

# Vistas de la app lecciones, en este caso se trata de la logica y las llamadas a las funciones necesarias para todas
# las funcionalidades relacionadas con el modulo de las lecciones.


class LogicaLecciones:
    user = User()

    def error(self):
        return render(self, 'lecciones/error.html')

    # Funcion que renderiza la pagina de cursos
    def ver_cursos(self):
        try:
            lista = LogicaLecciones.consultar_cursos()
            # Se crea un dictionary con la lista , para poder pasarla a la vista
            cdict = {'lista': lista}
            # Se renderiza la vista con las lecciones
            return render(self, 'lecciones/cursos.html', cdict)
        # Manejo de excepciones
        except ConnectionError:
            messages.error(self, 'Error de conexion')
            return redirect('/lecciones/error')

    # Funcion que renderiza la pagina de lecciones
    def ver_lecciones(self, curso_id):
        try:
            notificacion = (False, '')
            # Consulta del curso actual, para obtener sus datos
            curso = LogicaUsuarios.consultar_curso_id(curso_id)
            # Llamada al metodo que consulta el progreso del usuario para verificar si ya existe un registro
            progreso = LogicaLecciones.consultar_progreso_curso(self.user.pk, curso_id)
            # Consulta de las lecciones del curso
            lista = LogicaLecciones.consultar_lecciones(self, curso_id)
            # Se obtiene el id de la primera leccion de la lista
            primera_leccion = lista[0][0].pk
            # Consulta de los temas de la primera leccion
            lista_temas = LogicaLecciones.consultar_temas(str(primera_leccion))
            # Se obtiene el id del primer tema de la lista
            primer_tema = lista_temas[0][0].pk
            # Si no existe un registro de progreso de este usuario se procede a llamar al metodo que lo crea
            if progreso.status_code == 404:
                LogicaUsuarios.registrar_progreso(self.user.pk, primer_tema, curso_id)
                notificacion = (True, Strings.MensajeLeccion.mensaje)
            # Se crea un dictionary con la lista, para poder pasarla a la vista
            cdict = {'lista': lista, 'primera': primera_leccion, 'curso': curso.data, 'notificacion': notificacion}
            # Se renderiza la vista con las lecciones
            return render(self, 'lecciones/lecciones.html', cdict)
        # Manejo de excepciones
        except ConnectionError:
            messages.error(self, 'Error de conexion')
            return redirect('/lecciones/error')

    # Funcion que llama a una funcion del API, la cual le envia la lista completa de temas dado una leccion.
    def ver_temas(self, leccion_id, curso_id):
        try:
            examen = False
            notificacion = Strings.MensajeLeccion.mensajetema
            # Consulta de la leccion actual, para obtener sus datos
            leccion = LogicaUsuarios.consultar_leccion_id(leccion_id)
            # Consulta del curso actual, para obtener sus datos
            curso = LogicaUsuarios.consultar_curso_id(curso_id)
            # Llamada a la funcion que consulta el progreso del usuario con fines de saber cuales temas habilitar
            progreso = LogicaLecciones.consultar_progreso_curso(self.user.pk, curso_id)
            tema_progreso = progreso.data.tema_id
            # Llamada a la funcion que consulta los temas y devuelve su lista
            lista = LogicaLecciones.consultar_temas(leccion_id)
            # Variable auxiliar con el fin de determinar si se habilita el examen de la leccion
            aux = lista[-1][0].pk
            if tema_progreso >= aux:
                examen = True
            # Se crea un dictionary con la lista, el id del tema del progreso y la variable auxiliar
            # para poder pasarlos a la vista
            cdict = {'lista': lista, 'examen': examen, 'leccion': leccion.data,
                     'curso': curso.data, 'notificacion': notificacion}
            # Se renderiza la vista con los temas correspondientes a la leccion seleccionada
            return render(self, 'lecciones/temas.html', cdict)
        # Manejo de excepciones
        except ConnectionError:
            messages.error(self, 'Error de conexion')
            return redirect('/lecciones/error')
        except IndexError:
            messages.error(self, 'No se encontraron los temas')
            return redirect('/lecciones/error')
        except KeyError:
            messages.error(self, 'No se encontro la informacion de los temas')
            return redirect('/lecciones/error')

    # Funcion que llama a una funcion del API, la cual le envia el link para la visualizacion y la ruta para la descarga
    # de la presentacion
    def presentacion(self, tema_id):
        try:
            # Consulta del tema actual para obtener sus datos
            tema = LogicaUsuarios.consultar_tema_id(tema_id)
            # Consulta de la leccion actual, para obtener sus datos
            leccion = LogicaUsuarios.consultar_leccion_id(tema.data.leccion_id)
            # Consulta del curso actual, para obtener sus datos
            curso = LogicaUsuarios.consultar_curso_id(leccion.data.curso_id)
            # Llamada al API para obtener los links de las presentaciones dado un tema
            page = requests.get(settings.API_PATH + 'ver-linkspresent/' + tema_id)
            # Se convierte en json la respuesta del API, para su lectura
            pagejson = page.json()
            # Se obtiene del json el link para visualizar la presentacion
            link = Link(presentacion=pagejson["presentacion"])
            # Se crea un dictionary con los datos que se enviaran a la vista
            cdict = {'link': link, 'tema': tema.data, 'leccion': leccion.data, 'curso': curso.data}
            # Se renderiza la pagina con la respectiva presentacion
            return render(self, 'lecciones/presentaciones.html', cdict)
        except KeyError:
            messages.error(self, 'No se encontro la presentacion')
            return redirect('/lecciones/error')

    # Funcion que recibe la ruta de una presentacion del API y se encarga de realizar la descarga
    def descargapresentacion(self, tema_id):
        try:
            # Llamada al API para obtener los links de las presentaciones dado un tema
            page = requests.get(settings.API_PATH + 'ver-linkspresent/' + tema_id)
            # Se convierte en json la respuesta del API, para su lectura
            pagejson = page.json()
            # Se obtiene del json la ruta del archivo a descargar
            path = Link(presentaciond=pagejson['presentaciond'])
            # Se obtiene el nombre del archvio de la propia ruta
            nombre = path.presentaciond[16:len(path.presentaciond)]
            # Se construye la ruta del archivo a descargar, con la ruta base static concatenada con la obtenida del API
            file_path = os.path.join(settings.STATICFILES_URL + path.presentaciond)
            # Si la ruta existe se procede a la descarga
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/force-download")
                    response['Content-Disposition'] = 'inline; filename=' + nombre
                    return response
            # Si el directorio no existe se devuelve error 404
            else:
                messages.error(self, 'El archivo no existe o la ruta es incorrecta')
                return redirect('/lecciones/error')
        except ConnectionError:
            messages.error(self, 'Error de conexion')
            return redirect('/lecciones/error')
        except KeyError:
            messages.error(self, 'No se encontro la presentacion')
            return redirect('/lecciones/error')

    # Funcion que obtiene el link de los podcast a traves del API
    def podcast(self, tema_id):
        try:
            # Consulta del tema actual para obtener sus datos
            tema = LogicaUsuarios.consultar_tema_id(tema_id)
            # Consulta de la leccion actual, para obtener sus datos
            leccion = LogicaUsuarios.consultar_leccion_id(tema.data.leccion_id)
            # Consulta del curso actual, para obtener sus datos
            curso = LogicaUsuarios.consultar_curso_id(leccion.data.curso_id)
            # Llamada al API para obtener la ruta del podcast dado un tema
            page = requests.get(settings.API_PATH + 'ver-linkpod/' + tema_id)
            # Se convierte en json la respuesta del API, para su lectura
            pagejson = page.json()
            # Se obtiene del json la ruta del podcast
            path = Link(podcast=pagejson['podcast'])
        # Se construye la ruta del archivo a descargar, con la ruta base de static concatenada con la obtenida del API
            file_path = os.path.join(settings.STATICFILES_URL + '/' + path.podcast)
            # Si la ruta existe se procede a mostrarl el pocast
            if os.path.exists(file_path):
                # Se arma un dictionary con los datos que se enviaran a la vista
                cdict = {'podcast': path.podcast, 'tema': tema.data, 'leccion': leccion.data, 'curso': curso.data}
                # Se renderiza la pagina con el respectivo podcast
                return render(self, 'lecciones/podcasts.html', cdict)
            else:
                messages.error(self, 'El archivo no existe o la ruta es incorrecta')
                return redirect('/lecciones/error')
        except KeyError:
            messages.error(self, 'No se encontro el podcast')
            return redirect('/lecciones/error')

    # Funcion que recibe la ruta de un podcast del API y se encarga de realizar su descarga
    def descargapodcast(self, tema_id):
        try:
            # Llamada al API para obtener la ruta del podcast dado un tema
            page = requests.get(settings.API_PATH + 'ver-linkpod/' + tema_id)
            # Se convierte en json la respuesta del API, para su lectura
            pagejson = page.json()
            # Se obtiene del json la ruta del podcast
            path = Link(podcast=pagejson['podcast'])
            # Se obtiene el nombre del podcast de la propia ruta
            nombre = path.podcast[9:len(path.podcast)]
        # Se construye la ruta del archivo a descargar, con la ruta base de static concatenada con la obtenida del API
            file_path = os.path.join(settings.STATICFILES_URL + '/' + path.podcast)
            # Si la ruta existe se procede a la descarga
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/force-download")
                    response['Content-Disposition'] = 'inline; filename=' + nombre
                    return response
            # Si la ruta no existe se devuelve error 404
            else:
                messages.error(self, 'El archivo no existe o la ruta es incorrecta')
                return redirect('/lecciones/error')
        except ConnectionError:
            messages.error(self, 'Error de conexion')
            return redirect('/lecciones/error')
        except KeyError:
            messages.error(self, 'No se encontro el podcast')
            return redirect('/lecciones/error')

    # Funcion que llama a una funcion del API, la cual le envia el link para la visualizacion y la ruta para la descarga
    # de la presentacion
    def codigo(self, tema_id):
        try:
            # Consulta del tema actual para obtener sus datos
            tema = LogicaUsuarios.consultar_tema_id(tema_id)
            # Consulta de la leccion actual, para obtener sus datos
            leccion = LogicaUsuarios.consultar_leccion_id(tema.data.leccion_id)
            # Consulta del curso actual, para obtener sus datos
            curso = LogicaUsuarios.consultar_curso_id(leccion.data.curso_id)
            # Llamada al API para obtener los links de los codigos dado un tema
            page = requests.get(settings.API_PATH + 'ver-linkcod/' + tema_id)
            # Se convierte en json la respuesta del API, para su lectura
            pagejson = page.json()
            # Se obtiene del json el link para visualizar el codigo
            link = Link(codigo=pagejson["codigo"], repocodigo=["repocodigo"])
            # Se crea un dictionary con los datos que se enviaran a la vista
            cdict = {'link': link, 'tema': tema.data, 'leccion': leccion.data, 'curso': curso.data}
            # Se renderiza la pagina con la respectiva presentacion
            return render(self, 'lecciones/codigo.html', cdict)
        except KeyError:
            messages.error(self, 'No se encontro el codigo')
            return redirect('/lecciones/error')
    """
    Funciones Complementarias
    """

    # Funcion que llama a una funcion del API, la cual le envia la lista completa de infotemas dado un tema.
    @staticmethod
    def verinfotemas(tema_id, otema):
        try:
            # Llamada al API para obtener la informacion de un tema seleccionada pasando el id
            page = requests.get(settings.API_PATH + 'ver-infotemas/' + str(tema_id))
            # Se convierte en json la respuesta del API, para su lectura
            pagejson = page.json()
            infotema = InfoTema(pk=pagejson["id"], presentacion=pagejson["presentacion"], podcast=pagejson["podcast"],
                                codigo=pagejson["codigo"], tema=otema)
            # Se devuelve el json de la respuesta del API
            return infotema
        except ConnectionError as e:
            raise e
        except KeyError as e:
            raise e

    # Funcion que devuelve la leccion en la que se encuentre el usuario
    def leccion_actual(self):
        try:
            # Se consulta las calificaciones del usuario
            calificaciones = LogicaUsuarios.consultar_calificacion(self.user.pk)
            # Si la consulta es exitosa se toma la ultima calificacion y con ella se consulta el id de la leccion
            #  a la que corresponda
            if calificaciones.status_code == 200:
                prueba = LogicaUsuarios.consultar_prueba_id(calificaciones.data[-1][0].prueba_id)
                leccion_actual = LogicaUsuarios.consultar_leccion_id(prueba.data.leccion_id)
                leccion_actual_id = leccion_actual.data.pk
            # Si no hay calificaciones se asigna id 0
            else:
                leccion_actual_id = 0
            # Se devuelve el id de la leccion
            return leccion_actual_id
        except ConnectionError as e:
            raise e

    # Funcion que devuelve la lista de las lecciones y si se deben habilitar o no
    def consultar_lecciones(self, curso_id):
        try:
            lista = []
            # Llamada al API
            page = requests.get(settings.API_PATH + 'ver-lecciones/' + str(curso_id))
            # Convierte la respuesta en un json
            pagejson = page.json()
            leccion_actual_id = LogicaLecciones.leccion_actual(self)
            # Se recorre la respuesta del api, obteniendo el id y nombre de las lecciones
            for item in pagejson:
                leccion = Leccion(nombre=item["nombre"], pk=item["id"])
                # Por cada leccion se consulta la prueba de la leccion anterior
                prueba = LogicaUsuarios.consultar_prueba(leccion.pk - 1)
                # Por cada leccion se consulta la calificacion de la prueba anterior
                calificacion = LogicaUsuarios.consultar_calificacion_prueba(self.user.pk, prueba.data.pk)
                # Se obtiene la mejor nota de la prueba anterior
                mejor_nota = int(calificacion.data.mejor_nota)
                # Si el la leccion del progreso es mayor a la leccion anterior y la mejor nota es mayor a 10
                # se desbloquea la leccion
                if leccion_actual_id >= int(item["id"] - 1) and mejor_nota >= 10:
                    desbloquear = True
                # Si no se cumplen las condiciones la leccion se queda bloqueada
                else:
                    desbloquear = False
                # Se arma una lista con los datos a pasar a la interfaz
                lista.append((leccion, desbloquear))
            return lista
        except ConnectionError as e:
            raise e

    @staticmethod
    def consultar_temas(leccion_id):
        try:
            lista = []
            # Llamada al API para obtener los temas de una leccion seleccionada pasando el id
            page = requests.get(settings.API_PATH + 'ver-temas/' + leccion_id)
            # Convierte la respuesta en un json
            pagejson = page.json()
            # Se recorre la respuesta del api, instanciando objetos tipo Tema con los datos obtenidos
            for item in pagejson:
                otema = Tema(nombre=item["nombre"], pk=item["id"])
                # Llamada al metodo que consulta el infotema de un tema determinado
                infotema = LogicaLecciones.verinfotemas(item["id"], otema)
                # Se construye una lista de Temas e Infotemas
                lista.append((otema, infotema))
            return lista
        except ConnectionError as e:
            raise e
        except IndexError as e:
            raise e
        except KeyError as e:
            raise e

    @staticmethod
    def consultar_cursos():
        try:
            lista = []
            # Llamada al API para obtener los temas de una leccion seleccionada pasando el id
            page = requests.get(settings.API_PATH + 'ver-cursos/')
            # Convierte la respuesta en un json
            pagejson = page.json()
            # Se recorre la respuesta del api, instanciando objetos tipo Tema con los datos obtenidos
            for item in pagejson:
                curso = Curso(nombre=item["nombre"], pk=item["id"])
                lista.append(curso)
            return lista
        except ConnectionError as e:
            raise e
        except IndexError as e:
            raise e
        except KeyError as e:
            raise e

    # Funcion que consulta un tema por el id
    @staticmethod
    def consultar_progreso_curso(usuario_id, curso_id):
        try:
            # Llamada al metodo del api que consulta en la base de datos un tema de un determinado id
            r = requests.get(settings.API_PATH + 'ver-progreso2/' + str(usuario_id) + '/' + str(curso_id))
            if r.status_code == 200:
                # Se convierte la respuesta en json para poder extraer sus datos
                rjson = r.json()
                # Se instancia un objeto tipo Tema con los datos obtenidos de la llamada al api
                progreso = Progreso(pk=rjson["id"], tema_id=rjson["tema_id"])
                status = 200
            else:
                progreso = Progreso()
                status = 404
            # Se devuelve un Response con el objeto y el codigo 200
            return Response(progreso, status=status)
        except ConnectionError as e:
            # En caso de excepcion se devuelve el codigo de error 400
            raise e

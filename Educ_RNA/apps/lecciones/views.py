from django.shortcuts import render
import requests
from .models import Leccion, Tema, InfoTema, Link
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from apps.usuarios.views import LogicaUsuarios
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.

# Vistas de la app lecciones, en este caso se trata de la logica y las llamadas a las funciones necesarias para todas
# las funcionalidades relacionadas con el modulo de las lecciones.


class LogicaLecciones:
    user = User()

    def error(self):
        return render(self, 'lecciones/error.html')

    # Funcion que llama a una funcion del API, la cual le envia la lista completa de lecciones.
    def ver_lecciones(self):
        try:
            # Llamada al metodo que consulta el progreso del usuario para verificar si ya existe un registro
            progreso = LogicaUsuarios.consultar_progreso(self.user.pk)
            # Si no existe un registro de progreso de este usuario se procede a llamar al metodo que lo crea
            if progreso.status_code == 404:
                LogicaUsuarios.registrar_progreso(self.user.pk, 1)
            leccion_actual_id = LogicaLecciones.leccion_actual(self)
            lista = LogicaLecciones.consultar_lecciones(self)
            # Se crea un dictionary con la lista , para poder pasarla a la vista
            cdict = {'lista': lista, 'leccion_actual': leccion_actual_id}
            # Se renderiza la vista con las lecciones
            return render(self, 'lecciones/lecciones.html', cdict)
        # Manejo de excepciones
        except ConnectionError as e:
            messages.error(self, 'Error de conexion')
            return redirect('/lecciones/error')

    # Funcion que llama a una funcion del API, la cual le envia la lista completa de temas dado una leccion.
    def ver_temas(self, leccion_id):
        try:
            # Llamada al metodo que consulta el progreso del usuario con fines de saber cuales temas habilitar
            progreso = LogicaUsuarios.consultar_progreso(self.user.pk)
            if progreso.status_code == 200:
                tema_progreso = progreso.data.tema_id
            else:
                tema_progreso = 0
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
            # Variable auxiliar con el fin de determinar si se habilita el examen de la leccion
            aux = lista[-1][0].pk + 1
            # Se crea un dictionary con la lista, el id del tema del progreso y la variable auxiliar
            # para poder pasarlos a la vista
            cdict = {'lista': lista, 'progreso': tema_progreso, 'examen': aux}
            # Se renderiza la vista con los temas correspondientes a la leccion seleccionada
            return render(self, 'lecciones/temas.html', cdict)
        # Manejo de excepciones
        except ConnectionError as e:
            messages.error(self, 'Error de conexion')
            return redirect('/lecciones/error')
        except IndexError as e:
            messages.error(self, 'No se encontraron los temas')
            return redirect('/lecciones/error')
        except KeyError as e:
            messages.error(self, 'No se encontro la informacion de los temas')
            return redirect('/lecciones/error')

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

    # Funcion que llama a una funcion del API, la cual le envia el link para la visualizacion y la ruta para la descarga
    # de la presentacion
    def presentacion(self, tema_id):
        try:
            # Llamada al API para obtener los links de las presentaciones dado un tema
            page = requests.get(settings.API_PATH + 'ver-linkspresent/' + tema_id)
            # Se convierte en json la respuesta del API, para su lectura
            pagejson = page.json()
            # Se obtiene del json el link para visualizar la presentacion
            link = Link(presentacion=pagejson["presentacion"])
            # Se crea un dictionary con los datos que se enviaran a la vista
            cdict = {'link': link, 'id_': tema_id}
            # Se renderiza la pagina con la respectiva presentacion
            return render(self, 'lecciones/presentaciones.html', cdict)
        except KeyError as e:
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
        except ConnectionError as e:
            messages.error(self, 'Error de conexion')
            return redirect('/lecciones/error')
        except KeyError as e:
            messages.error(self, 'No se encontro la presentacion')
            return redirect('/lecciones/error')

    # Funcion que obtiene el link de los podcast a traves del API
    def podcast(self, tema_id):
        try:
            # Llamada al API para obtener la ruta del podcast dado un tema
            page = requests.get(settings.API_PATH + 'ver-linkpod/' + tema_id)
            # Se convierte en json la respuesta del API, para su lectura
            pagejson = page.json()
            # Se obtiene del json la ruta del podcast
            path = Link(podcast=pagejson['podcast'])
            # Se obtiene el nombre del podcast de la propia ruta
            nombre = path.podcast[9:len(path.podcast) - 4]
        # Se construye la ruta del archivo a descargar, con la ruta base de static concatenada con la obtenida del API
            file_path = os.path.join(settings.STATICFILES_URL + '/' + path.podcast)
            # Si la ruta existe se procede a mostrarl el pocast
            if os.path.exists(file_path):
                # Se arma un dictionary con los datos que se enviaran a la vista
                cdict = {'podcast': path.podcast, 'id_': tema_id, 'nombre': nombre}
                # Se renderiza la pagina con el respectivo podcast
                return render(self, 'lecciones/podcasts.html', cdict)
            else:
                messages.error(self, 'El archivo no existe o la ruta es incorrecta')
                return redirect('/lecciones/error')
        except KeyError as e:
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
        except ConnectionError as e:
            messages.error(self, 'Error de conexion')
            return redirect('/lecciones/error')
        except KeyError as e:
            messages.error(self, 'No se encontro el podcast')
            return redirect('/lecciones/error')

    def leccion_actual(self):
        try:
            calificaciones = LogicaUsuarios.consultar_calificacion(self.user.pk)
            if calificaciones.status_code == 200:
                prueba = LogicaUsuarios.consultar_prueba_id(calificaciones.data[-1][0].prueba_id)
                leccion_actual = LogicaUsuarios.consultar_leccion_id(prueba.data.leccion_id)
                leccion_actual_id = leccion_actual.data.pk
            else:
                leccion_actual_id = 0
            return leccion_actual_id
        except ConnectionError as e:
            raise e

    def consultar_lecciones(self):
        try:
            lista = []
            # Llamada al API
            page = requests.get(settings.API_PATH + 'ver-lecciones/')
            # Convierte la respuesta en un json
            pagejson = page.json()
            # Se recorre la respuesta del api, obteniendo el id y nombre de las lecciones
            for item in pagejson:
                leccion = Leccion(nombre=item["nombre"], pk=item["id"])
                prueba = LogicaUsuarios.consultar_prueba(leccion.pk - 1)
                calificacion = LogicaUsuarios.consultar_calificacion_prueba(self.user.pk, prueba.data.pk)
                if calificacion.status_code == 200:
                    mejor_nota = int(calificacion.data.mejor_nota)
                else:
                    mejor_nota = 0
                lista.append((leccion, int(item["id"] - 1), mejor_nota))
            return lista
        except ConnectionError as e:
            raise e

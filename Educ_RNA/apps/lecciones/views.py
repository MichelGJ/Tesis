from django.shortcuts import render
import requests
from .models import Leccion, Tema, InfoTema, Link
import os
from django.conf import settings
from django.http import HttpResponse, Http404
# Create your views here.

# Vistas de la app lecciones, en este caso se trata de la logica y las llamadas a las funciones necesarias para todas
# las funcionalidades relacionadas con el modulo de las lecciones.


class LogicaLecciones:

    # Funcion que llama a una funcion del API, la cual le envia la lista completa de lecciones.
    def ver_lecciones(self):
        try:
            lista = []
            # Llamada al API
            page = requests.get(settings.API_PATH + 'ver-lecciones/')
            # Convierte la respuesta en un json
            pagejson = page.json()
            # Se recorre la respuesta del api, obteniendo el id y nombre de las lecciones
            for item in pagejson:
                leccion = Leccion(nombre=item["nombre"], pk=item["id"])
                lista.append(leccion)
            # Se crea un dictionary con la lista , para poder pasarla a la vista
            cdict = {'lista': lista}
            print(lista)
            # Se renderiza la vista con las lecciones
            return render(self, 'lecciones/lecciones.html', cdict)
        # Manejo de excepciones
        except requests.ConnectionError as e:
            error = "Error de conexion"
            cdict = {'error': error}
            return render(self, 'lecciones/error.html', cdict)

    # Funcion que llama a una funcion del API, la cual le envia la lista completa de temas dado una leccion.
    def ver_temas(self, leccion_id):
        try:
            lista = []
            # Llamada al API para obtener los temas de una leccion seleccionada pasando el id
            page = requests.get(settings.API_PATH + 'ver-temas/' + leccion_id)
            # Convierte la respuesta en un json
            pagejson = page.json()
            # Se recorre la respuesta del api, obteniendo el id y nombre de los temas, asi como su informacion
            for item in pagejson:
                otema = Tema(nombre=item["nombre"], pk=item["id"])
                infotema = LogicaLecciones.verinfotemas(item["id"])
                itema = InfoTema(presentacion=infotema.get("presentacion"), podcast=infotema.get("podcast"),
                                 codigo=infotema.get("codigo"), tema=otema)
                lista.append((otema, itema))
            # Se crea un dictionary con la lista, para poder pasarla a la vista
            cdict = {'lista': lista}
            # Se renderiza la vista con los temas correspondientes a la leccion seleccionada
            return render(self, 'lecciones/temas.html', cdict)
        # Manejo de excepciones
        except requests.ConnectionError as e:
            error = "Error de conexion"
            cdict = {'error': error}
            return render(self, 'lecciones/error.html', cdict)

    # Funcion que llama a una funcion del API, la cual le envia la lista completa de infotemas dado un tema.
    @staticmethod
    def verinfotemas(tema_id):
        # Llamada al API para obtener la informacion de un tema seleccionada pasando el id
        page = requests.get(settings.API_PATH + 'ver-infotemas/' + str(tema_id))
        # Se convierte en json la respuesta del API, para su lectura
        pagejson = page.json()
        # Se devuelve el json de la respuesta del API
        return pagejson

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
            error = "No se enconcontro la presentacion"
            cdict = {'error': error}
            return render(self, 'lecciones/error.html', cdict)

    # Funcion que recibe la ruta de una presentacion del API y se encarga de realizar la descarga
    def descargapresentacion(self, tema_id):
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
        error = "El archivo no existe o la ruta es incorrecta"
        cdict = {'error': error}
        return render(self, 'lecciones/error.html', cdict)

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
            # Se arma un dictionary con los datos que se enviaran a la vista
            cdict = {'podcast': path.podcast, 'id_': tema_id, 'nombre': nombre}
            # Se renderiza la pagina con el respectivo podcast
            return render(self, 'lecciones/podcasts.html', cdict)
        except KeyError as e:
            error = "No se encontro el podcast"
            cdict = {'error': error}
            return render(self, 'lecciones/error.html', cdict)

    # Funcion que recibe la ruta de un podcast del API y se encarga de realizar su descarga
    def descargapodcast(self, tema_id):
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
        error = "El archivo no existe o la ruta es incorrecta"
        cdict = {'error': error}
        return render(self, 'lecciones/error.html', cdict)

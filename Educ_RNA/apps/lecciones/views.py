from django.shortcuts import render, redirect
import requests
from .models import Leccion
from django.http import HttpResponse
from django.utils.encoding import smart_str
import os
from django.conf import settings
from django.http import HttpResponse, Http404
# Create your views here.

# Vistas de la app lecciones, en este caso se trata de la logica y las llamadas a las funciones necesarias para todas
# las funcionalidades relacionadas con el modulo de las lecciones.


# Funcion que llama a una funcion del API, la cual le envia la lista completa de lecciones.
def ver_lecciones(request):
    try:
        lista = []
        # Llamada al API
        page = requests.get(settings.API_PATH + 'ver-lecciones/')
        # Convierte la respuesta en un json
        pagejson = page.json()
        # Se recorre la respuesta del api, obteniendo el id y nombre de las lecciones
        for item in pagejson:
            lista.append((item["id"], item["nombre"]))
        # Se crea un dictionary con la lista , para poder pasarla a la vista
        cdict = {'lista': lista}
        # Se renderiza la vista con las lecciones
        return render(request, 'lecciones/lecciones.html', cdict)
    # Manejo de excepciones
    except requests.ConnectionError as e:
            error = e.response
            print(error)


# Funcion que llama a una funcion del API, la cual le envia la lista completa de temas dado una leccion.
def ver_temas(request, leccion_id):
    try:
        lista = []
        # Llamada al API para obtener los temas de una leccion seleccionada pasando el id
        page = requests.get(settings.API_PATH + 'ver-temas/' + leccion_id)
        # Convierte la respuesta en un json
        pagejson = page.json()
        # Se recorre la respuesta del api, obteniendo el id y nombre de los temas, asi como su informacion
        for item in pagejson:
            infotema = verinfotemas(item["id"])
            lista.append((item["id"], item["nombre"], infotema.get("presentacion"), infotema.get("podcast"),
                          infotema.get("codigo")))
        # Se crea un dictionary con la lista, para poder pasarla a la vista
        cdict = {'lista': lista}
        # Se renderiza la vista con los temas correspondientes a la leccion seleccionada
        return render(request, 'lecciones/temas.html', cdict)
    # Manejo de excepciones
    except requests.ConnectionError as e:
            error = e.response
            print(error)


# Funcion que llama a una funcion del API, la cual le envia la lista completa de infotemas dado un tema.
def verinfotemas(tema_id):
    # Llamada al API para obtener la informacion de un tema seleccionada pasando el id
    page = requests.get(settings.API_PATH + 'ver-infotemas/' + str(tema_id))
    # Se convierte en json la respuesta del API, para su lectura
    pagejson = page.json()
    # Se devuelve el json de la respuesta del API
    return pagejson


# Funcion que llama a una funcion del API, la cual le envia el link para la visualizacion y la ruta para la descarga
# de la presentacion
def presentacion(request, tema_id):
    try:
        # Llamada al API para obtener los links de las presentaciones dado un tema
        page = requests.get(settings.API_PATH + 'ver-linkspresent/' + tema_id)
        # Se convierte en json la respuesta del API, para su lectura
        pagejson = page.json()
        # Se obtiene del json el link para visualizar la presentacion
        link = pagejson["presentacion"]
        # Se crea un dictionary con los datos que se enviaran a la vista
        cdict = {'presentacion': link, 'id_': tema_id}
        # Se renderiza la pagina con la respectiva presentacion
        return render(request, 'lecciones/presentaciones.html', cdict)
    except KeyError as e:
        error = "No se enconcontro la presentacion"
        cdict = {'error': error}
        return render(request, 'lecciones/error.html', cdict)


# Funcion que recibe la ruta de una presentacion del API y se encarga de realizar la descarga
def descargapresentacion(request, tema_id):
    # Llamada al API para obtener los links de las presentaciones dado un tema
    page = requests.get(settings.API_PATH + 'ver-linkspresent/' + tema_id)
    # Se convierte en json la respuesta del API, para su lectura
    pagejson = page.json()
    # Se obtiene del json la ruta del archivo a descargar
    path = pagejson['presentaciond']
    # Se obtiene el nombre del archvio de la propia ruta
    nombre = path[16:len(path)]
    # Se construye la ruta del archivo a descargar, con la ruta base static concatenada con la obtenida del API
    file_path = os.path.join(settings.STATICFILES_URL + path)
    # Si la ruta existe se procede a la descarga
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + nombre
            return response
    # Si el directorio no existe se devuelve error 404
    error = "El archivo no existe o la ruta es incorrecta"
    cdict = {'error': error}
    return render(request, 'lecciones/error.html', cdict)


# Funcion que obtiene el link de los podcast a traves del API
def podcast(request, tema_id):
    try:
        # Llamada al API para obtener la ruta del podcast dado un tema
        page = requests.get(settings.API_PATH + 'ver-linkpod/' + tema_id)
        # Se convierte en json la respuesta del API, para su lectura
        pagejson = page.json()
        # Se obtiene del json la ruta del podcast
        path = pagejson['podcast']
        # Se obtiene el nombre del podcast de la propia ruta
        nombre = path[9:len(path) - 4]
        # Se arma un dictionary con los datos que se enviaran a la vista
        cdict = {'podcast': path, 'id_': tema_id, 'nombre': nombre}
        # Se renderiza la pagina con el respectivo podcast
        return render(request, 'lecciones/podcasts.html', cdict)
    except KeyError as e:
        error = "No se encontro el podcast"
        cdict = {'error': error}
        return render(request, 'lecciones/error.html', cdict)


# Funcion que recibe la ruta de un podcast del API y se encarga de realizar su descarga
def descargapodcast(request, tema_id):
    # Llamada al API para obtener la ruta del podcast dado un tema
    page = requests.get(settings.API_PATH + 'ver-linkpod/' + tema_id)
    # Se convierte en json la respuesta del API, para su lectura
    pagejson = page.json()
    # Se obtiene del json la ruta del podcast
    path = pagejson['podcast']
    # Se obtiene el nombre del podcast de la propia ruta
    nombre = path[9:len(path)]
    # Se construye la ruta del archivo a descargar, con la ruta base de static concatenada con la obtenida del API
    file_path = os.path.join(settings.STATICFILES_URL + '/' + path)
    # Si la ruta existe se procede a la descarga
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + nombre
            return response
    # Si la ruta no existe se devuelve error 404
    error = "El archivo no existe o la ruta es incorrecta"
    cdict = {'error': error}
    return render(request, 'lecciones/error.html', cdict)

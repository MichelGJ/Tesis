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
    pagejson = page.json()
    return pagejson


# Funcion que llama a una funcion del API, la cual le envia el link para la visualizacion de la presentacion
# y el nombre del archivo para su dercarga
def presentacion(request, tema_id):
    # Llamada al API para obtener los links de las presentaciones dado un tema
    page = requests.get(settings.API_PATH + 'ver-linkspresent/' + tema_id)
    pagejson = page.json()
    cdict = {'presentacion': pagejson["presentacion"], 'id_': tema_id}
    return render(request, 'lecciones/presentaciones.html', cdict)


def descargapresentacion(request, tema_id):
    page = requests.get(settings.API_PATH + 'ver-linkspresent/' + tema_id)
    pagejson = page.json()
    path = pagejson['presentaciond']
    nombre = path[16:len(path)]
    file_path = os.path.join(settings.STATICFILES_URL + path)
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + nombre
            return response
    raise Http404


def podcast(request, tema_id):
    page = requests.get(settings.API_PATH + 'ver-linkpod/' + tema_id)
    pagejson = page.json()
    path = pagejson['podcast']
    nombre = path[9:len(path) - 4]
    cdict = {'podcast': pagejson["podcast"], 'id_': tema_id, 'nombre': nombre}
    return render(request, 'lecciones/podcasts.html', cdict)


def descargapodcast(request, tema_id):
    page = requests.get(settings.API_PATH + 'ver-linkpod/' + tema_id)
    pagejson = page.json()
    path = pagejson['podcast']
    nombre = path[9:len(path)]
    file_path = os.path.join(settings.STATICFILES_URL + '/' + path)
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + nombre
            return response
    raise Http404
from django.shortcuts import render
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
            infotema = requests.get(settings.API_PATH + 'ver-infotemas/' + str(item["id"]))
            pagejson2 = infotema.json()
            lista.append((item["id"], item["nombre"], pagejson2.get("presentacion"), pagejson2.get("podcast"),
                          pagejson2.get("codigo")))
        # Se crea un dictionary con la lista, para poder pasarla a la vista
        cdict = {'lista': lista}
        # Se renderiza la vista con los temas correspondientes a la leccion seleccionada
        return render(request, 'lecciones/temas.html', cdict)
    # Manejo de excepciones
    except requests.ConnectionError as e:
            error = e.response
            print(error)


def presentacion(request, tema_id):
    # Llamada al API para obtener la informacion de un tema seleccionada pasando el id
    lista = []
    page = requests.get(settings.API_PATH + 'ver-linkspresent/' + tema_id)
    pagejson = page.json()
    return render(request, 'lecciones/presentaciones.html', {'presentacion': pagejson["presentacion"],
                                                             'presentaciond': pagejson["presentaciond"]})


def descarga(request, nombre):
    path = '/presentaciones/' + nombre
    file_path = os.path.join(settings.MEDIA_ROOT + path)
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + nombre
            return response
    raise Http404

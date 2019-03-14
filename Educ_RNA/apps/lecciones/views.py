from django.shortcuts import render
import requests
from django.http import HttpResponse
# Create your views here.

# Vistas de la app lecciones, en este caso se trata de la logica y las llamadas a las funciones necesarias para todas
# las funcionalidades relacionadas con el modulo de las lecciones.


# Funcion que llama a una funcion del API, la cual le envia la lista completa de lecciones.
def ver_lecciones(request):
    try:
        lecciones = []
        ids = []
        # Llamada al API
        page = requests.get('http://127.0.0.1:8000/api/ver-lecciones/')
        # Convierte la respuesta en un json
        pagejson = page.json()
        for item in pagejson:
            # Agrega a una lista el nombre de las lecciones del json
            lecciones.append(item.get("nombre"))
            ids.append(item.get("id"))
        zipped_list = zip(ids, lecciones)
        cdict = {'zipped_list': zipped_list}
        return render(request, 'lecciones/lecciones.html', cdict)
    # Manejo de excepciones
    except requests.ConnectionError as e:
            error = e.response
            print(error)


def ver_temas(request, leccion_id):
    try:
        temas = []
        ids = []
        # Llamada al API
        page = requests.get('http://127.0.0.1:8000/api/ver-temas/' + leccion_id)
        # Convierte la respuesta en un json
        pagejson = page.json()
        for item in pagejson:
            # Agrega a una lista el nombre de las lecciones del json
            temas.append(item.get("nombre"))
            ids.append(item.get("id"))
        zipped_list = zip(ids, temas)
        cdict = {'zipped_list': zipped_list}
        return render(request, 'lecciones/temas.html', cdict)
    # Manejo de excepciones
    except requests.ConnectionError as e:
            error = e.response
            print(error)

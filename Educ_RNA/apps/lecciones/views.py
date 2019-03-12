from django.shortcuts import render
import requests
from django.http import HttpResponse
# Create your views here.

# Vistas de la app lecciones, en este caso se trata de la logica y las llamadas a las funciones necesarias para todas
# las funcionalidades relacionadas con el modulo de las lecciones.


# Funcion que llama a una funcion del API, la cual le envia la lista completa de lecciones.
def ver_lecciones(request):
    try:
        nombre = []
        # Llamada al API
        page = requests.get('http://127.0.0.1:8000/api/ver_lecciones/')
        # Convierte la respuesta en un json
        pagejson = page.json()
        for item in pagejson:
            # Agrega a una lista el nombre de las lecciones del json
            nombre.append(item.get("nombre"))
            nombre.append(" ")
        return HttpResponse(nombre)
    # Manejo de excepciones
    except requests.ConnectionError as e:
            error = e.response
            print(error)


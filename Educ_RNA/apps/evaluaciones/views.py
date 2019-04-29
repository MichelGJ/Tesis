from django.shortcuts import render
from django.shortcuts import render, redirect
import requests
from .models import Leccion
from django.http import HttpResponse
from django.utils.encoding import smart_str
import os
import random
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, Http404


# Create your views here.
def quiz(request, tema_id):
    try:
        listapreg = []
        listaresp = []
        quiz_id = verquiz(tema_id)
        preguntas = verpreguntasquiz(quiz_id)
        for item in preguntas:
            listapreg.append((item["id"], item["contenido"]))
        # Se crea un dictionary con la lista , para poder pasarla a la vista
        pregunta = random.choice(listapreg)
        respuestas = verrespuestas(str(pregunta[0]))
        for i in respuestas:
            listaresp.append((i["id"], i["contenido"], i["correcta"]))
        # En el caso de que alguna de las listas no tenga elementos se abre una pagina de error
        if len(listapreg) == 0 or len(listaresp) == 0:
            error = 'No se encontro el quiz'
            cdict = {'error': error}
            return render(request, 'lecciones/error.html', cdict)
        cdict = {'pregunta': pregunta, 'listaresp': listaresp, 'tema_id': tema_id}
        # Se renderiza la vista con las lecciones
        return render(request, 'evaluaciones/quiz.html', cdict)
        # Manejo de excepciones
    except requests.ConnectionError as e:
        error = e.response
        print(error)


def verquiz(tema_id):
    page = requests.get(settings.API_PATH + 'ver-quiz/' + tema_id)
    pagejson = page.json()
    quiz_id = str(pagejson["id"])
    return quiz_id


def verpreguntasquiz(quiz_id):
    page = requests.get(settings.API_PATH + 'ver-pregquiz/' + quiz_id)
    pagejson = page.json()
    return pagejson


def verpreguntaid(pregunta_id):
    page = requests.get(settings.API_PATH + 'ver-pregunta/' + pregunta_id)
    pagejson = page.json()
    return pagejson


def verrespuestas(pregunta_id):
    page = requests.get(settings.API_PATH + 'ver-resp/' + pregunta_id)
    pagejson = page.json()
    return pagejson


def verrespuestacorrecta(respuesta_id):
    page = requests.get(settings.API_PATH + 'ver-respid/' + respuesta_id)
    pagejson = page.json()
    return pagejson["correcta"]


def corregirquiz(request, respuesta_id, pregunta_id, tema_id):
    try:
        listaresp = []
        correcta = verrespuestacorrecta(respuesta_id)
        pregunta = verpreguntaid(pregunta_id)
        respuestas = verrespuestas(pregunta_id)
        incorrecto = 'RESPUESTA INCORRECTA'
        correcto = 'RESPUESTA CORRECTA'
        for i in respuestas:
            listaresp.append((i["contenido"], i["correcta"]))
        if correcta:
            cdict = {'pregunta': pregunta["contenido"], 'listaresp': listaresp, 'tema_id': tema_id, 'mensaje': 'true'}
            messages.success(request, correcto)
            return render(request, 'evaluaciones/quiz2.html', cdict)
        else:
            if not correcta:
                cdict = {'pregunta': pregunta["contenido"], 'listaresp': listaresp, 'tema_id': tema_id, 'mensaje': 'false'}
                messages.error(request, incorrecto)
                return render(request, 'evaluaciones/quiz2.html', cdict)
    except requests.ConnectionError as e:
        error = e.response
        print(error)

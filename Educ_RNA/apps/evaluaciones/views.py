from django.shortcuts import render
import requests
import random
from django.conf import settings
from django.contrib import messages
from .models import Prueba, Pregunta, Quiz, Respuesta


class LogicaEvaluaciones:

    # Create your views here.
    def quiz(self, tema_id):
        try:
            # Se obtienen todos los datos necesarios para desplegar una pregunta
            quiz = LogicaEvaluaciones.verquiz(tema_id)
            preguntas = LogicaEvaluaciones.verpreguntasquiz(quiz.pk)
            pregunta = random.choice(preguntas)
            respuestas = LogicaEvaluaciones.verrespuestas(pregunta.pk)
            # En el caso de que alguna de las listas no tenga elementos se abre una pagina de error
            if len(preguntas) == 0 or len(respuestas) == 0:
                error = 'No se encontro el quiz'
                cdict = {'error': error}
                return render(self, 'lecciones/error.html', cdict)
            # Se crea un dictionary con los datos , para poder pasarla a la vista
            cdict = {'pregunta': pregunta, 'listaresp': respuestas, 'tema_id': tema_id}
            # Se renderiza la vista con las lecciones
            return render(self, 'evaluaciones/quiz.html', cdict)
            # Manejo de excepciones
        except requests.ConnectionError as e:
            error = "Error de conexion"
            cdict = {'error': error}
            return render(self, 'lecciones/error.html', cdict)
        except KeyError as e:
            error = "No se enconcontro el quiz"
            cdict = {'error': error}
            return render(self, 'lecciones/error.html', cdict)
        except IndexError as e:
            error = "No se enconcontraron las preguntas o respuestas"
            cdict = {'error': error}
            return render(self, 'lecciones/error.html', cdict)

    @staticmethod
    def verquiz(tema_id):
        page = requests.get(settings.API_PATH + 'ver-quiz/' + tema_id)
        pagejson = page.json()
        quiz = Quiz(pk=pagejson["id"])
        return quiz

    @staticmethod
    def verpreguntasquiz(quiz_id):
        listapreg = []
        page = requests.get(settings.API_PATH + 'ver-pregquiz/' + str(quiz_id))
        pagejson = page.json()
        for item in pagejson:
            opregunta = Pregunta(pk=item["id"], contenido=item["contenido"])
            listapreg.append(opregunta)
        return listapreg

    @staticmethod
    def verpreguntaid(pregunta_id):
        page = requests.get(settings.API_PATH + 'ver-pregunta/' + pregunta_id)
        pagejson = page.json()
        return pagejson

    @staticmethod
    def verrespuestas(pregunta_id):
        listaresp = []
        page = requests.get(settings.API_PATH + 'ver-resp/' + str(pregunta_id))
        pagejson = page.json()
        for item in pagejson:
            orespuesta = Respuesta(pk=item["id"], contenido=item["contenido"], correcta=item["correcta"])
            listaresp.append(orespuesta)
        return listaresp

    @staticmethod
    def verrespuestacorrecta(respuesta_id):
        page = requests.get(settings.API_PATH + 'ver-respid/' + respuesta_id)
        pagejson = page.json()
        return pagejson["correcta"]

    def corregirquiz(self, respuesta_id, pregunta_id, tema_id):
        try:
            correcta = LogicaEvaluaciones.verrespuestacorrecta(respuesta_id)
            pregunta = LogicaEvaluaciones.verpreguntaid(pregunta_id)
            respuestas = LogicaEvaluaciones.verrespuestas(pregunta_id)
            incorrecto = 'RESPUESTA INCORRECTA'
            correcto = 'RESPUESTA CORRECTA'
            if correcta:
                cdict = {'pregunta': pregunta["contenido"], 'listaresp': respuestas, 'tema_id': tema_id, 'mensaje': 'true'}
                messages.success(self, correcto)
                return render(self, 'evaluaciones/quiz2.html', cdict)
            else:
                if not correcta:
                    cdict = {'pregunta': pregunta["contenido"], 'listaresp': respuestas, 'tema_id': tema_id, 'mensaje': 'false'}
                    messages.error(self, incorrecto)
                    return render(self, 'evaluaciones/quiz2.html', cdict)
        except requests.ConnectionError as e:
            error = "Error de conexion"
            cdict = {'error': error}
            return render(self, 'lecciones/error.html', cdict)

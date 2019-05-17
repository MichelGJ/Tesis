from django.shortcuts import render
from django.shortcuts import redirect
import requests
import random
from django.conf import settings
from django.contrib import messages
from .models import Pregunta, Quiz, Respuesta, Prueba
from apps.usuarios.views import LogicaUsuarios


class LogicaEvaluaciones:

    # Funcion que renderiza las preguntas del quiz del tema seleccionado
    def quiz(self, tema_id):
        try:
            # Se obtienen todos los datos necesarios para desplegar una pregunta
            quiz = LogicaEvaluaciones.verquiz(tema_id)
            preguntas = LogicaEvaluaciones.verpreguntasquiz(quiz.pk)
            pregunta = random.choice(preguntas)
            respuestas = LogicaEvaluaciones.verrespuestas(pregunta.pk)
            # En el caso de que alguna de las listas no tenga elementos se abre una pagina de error
            if len(preguntas) == 0 or len(respuestas) == 0:
                messages.error(self, 'No se enconcontraron las preguntas o respuestas')
                return redirect('/lecciones/error')
            # Se crea un dictionary con los datos , para poder pasarla a la vista
            cdict = {'pregunta': pregunta, 'listaresp': respuestas, 'tema_id': tema_id}
            # Se consulta el progreso del usuario en la base de datos
            progreso = LogicaUsuarios.consultar_progreso(self.user.pk)
            # Si existe el registro se actualiza el progreso si es un tema mayor
            if progreso.status_code == 200:
                tema_actualizar = str(int(tema_id) + 1)
                LogicaUsuarios.actualizar_progreso(self.user.pk, tema_actualizar)
            # Se renderiza la vista con las lecciones
            return render(self, 'evaluaciones/quiz.html', cdict)
            # Manejo de excepciones
        except ConnectionError as e:
            messages.error(self, 'Error de conexion')
            return redirect('/lecciones/error')
        except KeyError as e:
            messages.error(self, 'No se encontro el quiz')
            return redirect('/lecciones/error')
        except IndexError as e:
            messages.error(self, 'No se encontraron las preguntas y/o respuestas')
            return redirect('/lecciones/error')

    # Funcion que consulta el id de un quiz de un determinado tema
    @staticmethod
    def verquiz(tema_id):
        try:
            # Llamada al metodo del api que consulta el quiz de un tema determinado
            page = requests.get(settings.API_PATH + 'ver-quiz/' + tema_id)
            # Se convierte la respuesta en json para poder extraer sus datos
            pagejson = page.json()
            # Se extrae el id y se instancia un objeto tipo quiz con ese id
            quiz = Quiz(pk=pagejson["id"])
            # Se devuelve el objeto tipo Quiz
            return quiz
        except ConnectionError as e:
            raise e
        except KeyError as e:
            raise e

    # Funcion que consulta las preguntas de un determinado quiz
    @staticmethod
    def verpreguntasquiz(quiz_id):
        try:
            listapreg = []
            # Llamada al metodo del api que consulta las preguntas de un determinado quiz
            page = requests.get(settings.API_PATH + 'ver-pregquiz/' + str(quiz_id))
            # Se convierte la respuesta en json para poder extraer sus datos
            pagejson = page.json()
            # Se recorre la lista de preguntas y se forma una lista de preguntas con objetos tipo Pregunta
            for item in pagejson:
                opregunta = Pregunta(pk=item["id"], contenido=item["contenido"])
                listapreg.append(opregunta)
                # Se devuelve la lista de preguntas
            return listapreg
        except ConnectionError as e:
            raise e
        except KeyError as e:
            raise e

    # Funcion que consulta una pregunta dado su id
    @staticmethod
    def verpreguntaid(pregunta_id):
        try:
            # Llamada al api que busca una pregunta de un determinado id
            page = requests.get(settings.API_PATH + 'ver-pregunta/' + pregunta_id)
            # Se convierte la respuesta en json para poder extraer sus datos
            pagejson = page.json()
            # Se instancia un objeto tipo Pregunta con el contenido devuelto por el api
            pregunta = Pregunta(contenido=pagejson["contenido"])
            # Se devuelve un objeto tipo Pregunta
            return pregunta
        except ConnectionError as e:
            raise e
        except KeyError as e:
            raise e

    # Funcion que consulta las respuestas de una determinada pregunta
    @staticmethod
    def verrespuestas(pregunta_id):
        try:
            listaresp = []
            # Llamada al api que consulta las respuestas de una pregunta determinada
            page = requests.get(settings.API_PATH + 'ver-resp/' + str(pregunta_id))
            # Se convierte la respuesta en json para poder extraer sus datos
            pagejson = page.json()
            # Se recorre la lista de respuestas y se forma una lista de respuestas con objetos tipo Respuesta
            for item in pagejson:
                orespuesta = Respuesta(pk=item["id"], contenido=item["contenido"], correcta=item["correcta"])
                listaresp.append(orespuesta)
            # Se devuelve la lista de respuestas
            return listaresp
        except ConnectionError as e:
            raise e
        except KeyError as e:
            raise e

    # Funcion que consulta si una respuesta es correcta o incorecta
    @staticmethod
    def verrespuestacorrecta(respuesta_id):
        try:
            # Llamada al metodo del api que consulta una respuesta dado su id
            page = requests.get(settings.API_PATH + 'ver-respid/' + respuesta_id)
            # Se convierte la respuesta en json para poder extraer sus datos
            pagejson = page.json()
            # Se instancia un obejeto tipo Respuesta con el dato necesitado que devolvio el apo
            respuesta = Respuesta(correcta=pagejson["correcta"])
            # Se devuelve un objeto tipo Respuesta
            return respuesta
        except ConnectionError as e:
            raise e
        except KeyError as e:
            raise e

    # Funcion que renderiza la pagina de correcion de una pregunta del quiz
    def corregirquiz(self, respuesta_id, pregunta_id, tema_id):
        try:
            # Se llaman a los metodos necesarios para obtener los datos que se requieren
            respuesta = LogicaEvaluaciones.verrespuestacorrecta(respuesta_id)
            pregunta = LogicaEvaluaciones.verpreguntaid(pregunta_id)
            respuestas = LogicaEvaluaciones.verrespuestas(pregunta_id)
            incorrecto = 'RESPUESTA INCORRECTA'
            correcto = 'RESPUESTA CORRECTA'
            # Si la respuesta es correcta se arma el dictionary y se indica que la respuesta es correcta mandando true
            # como mensaje
            if respuesta.correcta:
                cdict = {'pregunta': pregunta.contenido, 'listaresp': respuestas, 'tema_id': tema_id, 'mensaje': 'true'}
                messages.success(self, correcto)
                # Se renderiza la pagina de correccion de pregunta con todos los datos necesarios
                return render(self, 'evaluaciones/quiz2.html', cdict)
            else:
                # Si la respuesta no es correcta se arma el dictionary y se indica que la respuesta es incorrecta
                # mandando false como mensaje
                if not respuesta.correcta:
                    cdict = {'pregunta': pregunta.contenido, 'listaresp': respuestas, 'tema_id': tema_id, 'mensaje': 'false'}
                    messages.error(self, incorrecto)
                    # Se renderiza la pagina de correccion de preguntas con todos los datos necesarios
                    return render(self, 'evaluaciones/quiz2.html', cdict)
        except ConnectionError as e:
            messages.error(self, 'Error de conexion')
            return redirect('/lecciones/error')

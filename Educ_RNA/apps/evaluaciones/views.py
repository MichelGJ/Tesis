from django.shortcuts import render
from django.shortcuts import redirect
import requests
import random
from django.conf import settings
from django.contrib import messages
from .models import Pregunta, Quiz, Respuesta, Prueba
from apps.usuarios.views import LogicaUsuarios
import apps.lecciones.views as lecciones
from django.db import IntegrityError

listaquiz = []
aux_quiz = 0
listaexamen = []
aux_examen = 0
nota = 0
listaresp = []
id_curso = 0

class LogicaEvaluaciones:

    def instrucciones(self, tema_id, leccion_id, curso_id):
        global listaquiz
        global aux_quiz
        global aux_examen
        global listaexamen
        global nota
        global id_curso
        id_curso = curso_id
        aux_quiz = 0
        aux_examen = 0
        listaexamen = []
        listaquiz = []
        nota = 0
        if leccion_id == '0':
            aux = False
            instrucciones = ('Quiz ' + tema_id, '- El siguiente quiz tiene 5 preguntas, no hay tiempo límite ni nota.',
                             '- Solo es para afianzar tu conocimiento.',
                             '- Así que no te preocupes y escoge la opción que más te parezca.',
                             '- Nosotros te indicaremos si fue correcta o no.')
            cdict = {'tema_id': tema_id, 'instrucciones': instrucciones, 'aux': aux}
            return render(self, 'evaluaciones/instrucciones.html', cdict)
        elif tema_id == '0':
            aux = True
            instrucciones = ('Examen ' + leccion_id, '- El siguiente examen tiene 20 preguntas.',
                             '- Cada pregunta tiene un tiempo limite de 45 segundos.',
                             '- Selecciona la opción que crea correcta para avanzar.',
                             '- Para aprobar necesita obtener 10 preguntas correctas.')
            cdict = {'leccion_id': leccion_id, 'instrucciones': instrucciones, 'aux': aux}
            return render(self, 'evaluaciones/instrucciones.html', cdict)
        else:
            messages.error(self, 'Error')
            return redirect('/lecciones/error')

    # Funcion que renderiza las preguntas del quiz del tema seleccionado
    def quiz(self, tema_id):
        try:
            global listaquiz
            global aux_quiz
            global listaresp
            listaresp = []
            # Se obtienen todos los datos necesarios para desplegar una pregunta
            quiz = LogicaEvaluaciones.verquiz(tema_id)
            if aux_quiz == 0:
                listaquiz = LogicaEvaluaciones.verpreguntasquiz(quiz.pk)
                pregunta = random.choice(listaquiz)
                respuestas = LogicaEvaluaciones.verrespuestas(pregunta.pk)
            elif 1 <= aux_quiz < 5:
                pregunta = random.choice(listaquiz)
                respuestas = LogicaEvaluaciones.verrespuestas(pregunta.pk)
            # En el caso de que alguna de las listas no tenga elementos se abre una pagina de error
            if len(listaquiz) == 0 or len(respuestas) == 0:
                listaquiz = []
                aux_quiz = 0
                messages.error(self, 'No se enconcontraron las preguntas o respuestas')
                return redirect('/lecciones/error')
            # Se crea un dictionary con los datos , para poder pasarla a la vista
            cdict = {'pregunta': pregunta, 'listaresp': respuestas, 'tema_id': tema_id}
            # Se renderiza la vista con las lecciones
            return render(self, 'evaluaciones/quiz.html', cdict)
            # Manejo de excepciones
        except ConnectionError as e:
            listaquiz = []
            aux_quiz = 0
            messages.error(self, 'Error de conexion')
            return redirect('/lecciones/error')
        except KeyError as e:
            listaquiz = []
            aux_quiz = 0
            messages.error(self, 'No se encontro el quiz')
            return redirect('/lecciones/error')
        except IndexError as e:
            listaquiz = []
            aux_quiz = 0
            messages.error(self, 'No se encontraron las preguntas y/o respuestas')
            return redirect('/lecciones/error')

    def examen(self, leccion_id):
        try:
            global listaexamen
            global aux_examen
            global listaresp
            global nota
            listaresp = []
            # Se obtienen todos los datos necesarios para desplegar una pregunta
            prueba = LogicaEvaluaciones.verprueba(leccion_id)
            listaexamen = LogicaEvaluaciones.verpreguntasexamen(prueba.pk)
            pregunta = random.choice(listaexamen)
            respuestas = LogicaEvaluaciones.verrespuestas(pregunta.pk)
            listaexamen.remove(pregunta)
            aux_examen = aux_examen + 1
            # En el caso de que alguna de las listas no tenga elementos se abre una pagina de error
            if len(listaexamen) == 0 or len(respuestas) == 0:
                listaexamen = []
                aux_examen = 0
                messages.error(self, 'No se enconcontraron las preguntas o respuestas')
                return redirect('/lecciones/error')
            # Se crea un dictionary con los datos , para poder pasarla a la vista
            cdict = {'pregunta': pregunta, 'listaresp': respuestas, 'leccion_id': leccion_id}
            # Se renderiza la vista con las lecciones
            return render(self, 'evaluaciones/examen.html', cdict)
            # Manejo de excepciones
        except ConnectionError as e:
            listaquiz = []
            aux_quiz = 0
            messages.error(self, 'Error de conexion')
            return redirect('/lecciones/error')
        except KeyError as e:
            listaquiz = []
            aux_quiz = 0
            messages.error(self, 'No se encontro el quiz')
            return redirect('/lecciones/error')
        except IndexError as e:
            listaquiz = []
            aux_quiz = 0
            messages.error(self, 'No se encontraron las preguntas y/o respuestas')
            return redirect('/lecciones/error')

    def examen2(self, respuesta_id, leccion_id):
        try:
            global listaexamen
            global aux_examen
            global listaresp
            global nota
            listaresp = []
            lista = []
            # Se obtienen todos los datos necesarios para desplegar una pregunta
            prueba = LogicaEvaluaciones.verprueba(leccion_id)
            if 1 <= aux_examen <= 20:
                respuestaanterior = LogicaEvaluaciones.verrespuestacorrecta(respuesta_id)
                if respuestaanterior.correcta:
                    nota = nota + 1
                pregunta = random.choice(listaexamen)
                respuestas = LogicaEvaluaciones.verrespuestas(pregunta.pk)
                listaexamen.remove(pregunta)
                aux_examen = aux_examen + 1
            elif aux_examen == 21:
                calificacion = LogicaUsuarios.consultar_calificacion_prueba(self.user.pk, prueba.pk)
                if calificacion.status_code == 404:
                    LogicaEvaluaciones.registrar_calificacion(self.user.pk, prueba.pk, nota)
                elif calificacion.status_code == 200:
                    LogicaEvaluaciones.actualizar_calificacion(self.user.pk, prueba.pk, nota)
                calificacion_actualizada = LogicaUsuarios.consultar_calificacion_prueba(self.user.pk, prueba.pk)
                leccion = LogicaUsuarios.consultar_leccion_id(leccion_id)
                # Se extrae el nombre de la leccion
                nombre_leccion = leccion.data.nombre
                print(calificacion_actualizada.data.nota)
                if int(calificacion_actualizada.data.nota) >= 10:
                    aprobado = True
                    mensaje = "¡Felicidades, ha aprobado el examen! :D"
                else:
                    aprobado = False
                    mensaje = "Lo sentimos, reprobó el examen... intente nuevamente :( "
                # Se agregan a la lista el objeto calificacion y el nombre de la leccion a la cual pertenece
                tup = (calificacion_actualizada.data, nombre_leccion, aprobado, mensaje)
                cdict = {'calificacion': tup, 'curso_id': lecciones.id_curso}
                return render(self, 'evaluaciones/resultados.html', cdict)
            # En el caso de que alguna de las listas no tenga elementos se abre una pagina de error
            if len(listaexamen) == 0 or len(respuestas) == 0:
                listaexamen = []
                aux_examen = 0
                messages.error(self, 'No se enconcontraron las preguntas o respuestas')
                return redirect('/lecciones/error')
            # Se crea un dictionary con los datos , para poder pasarla a la vista
            cdict = {'pregunta': pregunta, 'listaresp': respuestas, 'leccion_id': leccion_id}
            # Se renderiza la vista con las lecciones
            return render(self, 'evaluaciones/examen.html', cdict)
            # Manejo de excepciones
        except ConnectionError as e:
            listaquiz = []
            aux_quiz = 0
            messages.error(self, 'Error de conexion')
            return redirect('/lecciones/error')
        except KeyError as e:
            listaquiz = []
            aux_quiz = 0
            messages.error(self, 'No se encontro el quiz')
            return redirect('/lecciones/error')
        except IndexError as e:
            listaquiz = []
            aux_quiz = 0
            messages.error(self, 'No se encontraron las preguntas y/o respuestas')
            return redirect('/lecciones/error')

    @staticmethod
    def registrar_calificacion(usuario_id, prueba_id, notas):
        try:
            # Se arma un dictionary con los datos a enviar al api
            data = {'usuario_id': usuario_id, 'prueba_id': prueba_id, 'nota': str(notas), 'mejor_nota': '0', 'intentos':0}
            # Llamada al metodo del api que registra el progreso, pasandole los datos para sus insercion
            r = requests.post(settings.API_PATH + 'registrar-calificacion/', data=data)
        except ConnectionError as e:
            raise e

    @staticmethod
    def actualizar_calificacion(usuario_id, prueba_id, notas):
        try:
            # Se arma un dictionary con los datos a enviar al api
            data = {'usuario_id': usuario_id, 'prueba_id': prueba_id, 'nota': str(notas), 'mejor_nota': '0',
                    'intentos': 0}
            # Llamada al metodo del api que registra el progreso, pasandole los datos para sus insercion
            r = requests.put(settings.API_PATH + 'actualizar-calificacion/', data=data)
        except ConnectionError as e:
            raise e

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

    # Funcion que consulta el id de un examen de una determinada leccion
    @staticmethod
    def verprueba(leccion_id):
        try:
            # Llamada al metodo del api que consulta el examen de una leccion determinada
            page = requests.get(settings.API_PATH + 'ver-prueba/' + leccion_id)
            # Se convierte la respuesta en json para poder extraer sus datos
            pagejson = page.json()
            # Se extrae el id y se instancia un objeto tipo quiz con ese id
            prueba = Prueba(id=pagejson["id"])
            # Se devuelve el objeto tipo Quiz
            return prueba
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

    # Funcion que consulta las preguntas de un determinado examen
    @staticmethod
    def verpreguntasexamen(prueba_id):
        try:
            listapreg = []
            # Llamada al metodo del api que consulta las preguntas de un determinado examen
            page = requests.get(settings.API_PATH + 'ver-pregprueba/' + str(prueba_id))
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
            pregunta = Pregunta(id=pagejson["id"], contenido=pagejson["contenido"])
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
            global listaresp
            # Llamada al api que consulta las respuestas de una pregunta determinada
            page = requests.get(settings.API_PATH + 'ver-resp/' + str(pregunta_id))
            # Se convierte la respuesta en json para poder extraer sus datos
            pagejson = page.json()
            # Se recorre la lista de respuestas y se forma una lista de respuestas con objetos tipo Respuesta
            for item in pagejson:
                orespuesta = Respuesta(pk=item["id"], contenido=item["contenido"], correcta=item["correcta"])
                listaresp.append(orespuesta)
            # Se devuelve la lista de respuestas
            random.shuffle(listaresp)
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
            global aux_quiz
            global listaquiz
            global listaresp
            global id_curso
            # Se llaman a los metodos necesarios para obtener los datos que se requieren
            respuesta = LogicaEvaluaciones.verrespuestacorrecta(respuesta_id)
            pregunta = LogicaEvaluaciones.verpreguntaid(pregunta_id)
            respuestas = listaresp
            incorrecto = 'RESPUESTA INCORRECTA'
            correcto = 'RESPUESTA CORRECTA'
            tema = LogicaUsuarios.consultar_tema_id(tema_id)
            leccion = LogicaUsuarios.consultar_leccion_id(tema.data.leccion_id)
            aux_quiz = aux_quiz + 1
            if respuesta.correcta:
                cdict = {'pregunta': pregunta.contenido, 'listaresp': respuestas, 'tema_id': tema_id,
                         'mensaje': 'true', 'leccion': leccion.data.id, 'curso_id': id_curso}
                messages.success(self, correcto)
                if aux_quiz == 5:
                    aux_quiz = 0
                    listaquiz = []
                    # Se consulta el progreso del usuario en la base de datos
                    progreso = LogicaUsuarios.consultar_progreso(self.user.pk)
                    # Si existe el registro se actualiza el progreso si es un tema mayor
                    if progreso.status_code == 200:
                        tema_actualizar = str(int(tema_id) + 1)
                        LogicaUsuarios.actualizar_progreso(self.user.pk, tema_actualizar, id_curso)
                    # Se renderiza la pagina de correccion de pregunta con todos los datos necesarios
                    return render(self, 'evaluaciones/quiz3.html', cdict)
                else:
                    listaquiz.remove(pregunta)
                    # Se renderiza la pagina de correccion de pregunta con todos los datos necesarios
                    return render(self, 'evaluaciones/quiz2.html', cdict)
                    # Si la respuesta no es correcta se arma el dictionary y se indica que la respuesta es incorrecta
                    # mandando false como mensaje
            elif not respuesta.correcta:
                cdict = {'pregunta': pregunta.contenido, 'listaresp': respuestas, 'tema_id': tema_id,
                         'mensaje': 'false', 'leccion': leccion.data.id, 'curso_id': id_curso}
                messages.error(self, incorrecto)
                if aux_quiz == 5:
                    aux_quiz = 0
                    listaquiz = []
                    # Se consulta el progreso del usuario en la base de datos
                    progreso = LogicaUsuarios.consultar_progreso(self.user.pk)
                    # Si existe el registro se actualiza el progreso si es un tema mayor
                    if progreso.status_code == 200:
                        tema_actualizar = str(int(tema_id) + 1)
                        LogicaUsuarios.actualizar_progreso(self.user.pk, tema_actualizar, id_curso)
                    # Se renderiza la pagina de correccion de preguntas con todos los datos necesarios
                    return render(self, 'evaluaciones/quiz3.html', cdict)
                else:
                    listaquiz.remove(pregunta)
                    # Se renderiza la pagina de correccion de preguntas con todos los datos necesarios
                    return render(self, 'evaluaciones/quiz2.html', cdict)
        except ConnectionError as e:
            messages.error(self, 'Error de conexion')
            return redirect('/lecciones/error')

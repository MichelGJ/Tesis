from django.shortcuts import render
from django.shortcuts import redirect
import requests
import random
from django.conf import settings
from django.contrib import messages
from .models import Pregunta, Quiz, Respuesta, Prueba
from apps.usuarios.views import LogicaUsuarios
from apps.lecciones.views import LogicaLecciones
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from Educ_RNA.strings import Strings


class LogicaEvaluaciones:
    timeout = False
    id_curso = 0
    user = User()
    aux_quiz = 0
    aux_examen = 0
    nota = 0
    listaquiz = []
    listaexamen = []
    listaresp = []

    def instrucciones(self, tema_id, leccion_id, curso_id):
        # Se reinician todas las variables del modulo para evitar errores
        LogicaEvaluaciones.id_curso = curso_id
        LogicaEvaluaciones.aux_quiz = 0
        LogicaEvaluaciones.aux_examen = 0
        LogicaEvaluaciones.listaexamen = []
        LogicaEvaluaciones.listaquiz = []
        LogicaEvaluaciones.nota = 0
        # Si el id de la leccion recibido es 0, se renderizan las instrucciones del quiz
        if leccion_id == '0':
            # Se consulta el tema para obtener sus datos
            tema = LogicaUsuarios.consultar_tema_id(tema_id)
            # La variable aux se fija en False, para que el boton de continuar redirija al quiz
            aux = False
            # Se arman las instrucciones
            instrucciones = ('Quiz: ' + tema.data.nombre, Strings.InstruccionesQuiz.quiz1,
                             Strings.InstruccionesQuiz.quiz2, Strings.InstruccionesQuiz.quiz3,
                             Strings.InstruccionesQuiz.quiz4)
            # Se construye un dictionary con los valores a pasar al template
            cdict = {'tema_id': tema_id, 'instrucciones': instrucciones, 'aux': aux}
            # Se renderiza la pagina de instrucciones
            return render(self, 'evaluaciones/instrucciones.html', cdict)
        # Si el id del tema recibido es 0, se renderizan las instrucciones del examen
        elif tema_id == '0':
            # Se consulta la leccion para obtener sus datos
            leccion = LogicaUsuarios.consultar_leccion_id(leccion_id)
            # La variable aux se fija en True, para que el boton de continuar redirija al examen
            aux = True
            # Se arman las instrucciones
            instrucciones = ('Examen: ' + leccion.data.nombre, Strings.InstruccionesExamen.examen1,
                             Strings.InstruccionesExamen.examen2, Strings.InstruccionesExamen.examen3,
                             Strings.InstruccionesExamen.examen4)
            # Se construye un dictionary con los valores a pasar al template
            cdict = {'leccion_id': leccion_id, 'instrucciones': instrucciones, 'aux': aux}
            # Se renderiza la pagina de instrucciones
            return render(self, 'evaluaciones/instrucciones.html', cdict)
        else:
            messages.error(self, 'Error')
            return redirect('/lecciones/error')

    # Funcion que renderiza las preguntas del quiz del tema seleccionado
    def quiz(self, tema_id):
        try:
            LogicaEvaluaciones.listaresp = []
            tema = LogicaUsuarios.consultar_tema_id(tema_id)
            # Se obtienen todos los datos necesarios para desplegar una pregunta
            quiz = LogicaEvaluaciones.verquiz(tema_id)
            if LogicaEvaluaciones.aux_quiz == 0:
                LogicaEvaluaciones.listaquiz = LogicaEvaluaciones.verpreguntasquiz(quiz.pk)
                pregunta = random.choice(LogicaEvaluaciones.listaquiz)
                respuestas = LogicaEvaluaciones.verrespuestas(pregunta.pk)
            elif 1 <= LogicaEvaluaciones.aux_quiz < 5:
                pregunta = random.choice(LogicaEvaluaciones.listaquiz)
                respuestas = LogicaEvaluaciones.verrespuestas(pregunta.pk)
            # En el caso de que alguna de las listas no tenga elementos se abre una pagina de error
            if len(LogicaEvaluaciones.listaquiz) == 0 or len(respuestas) == 0:
                listaquiz = []
                aux_quiz = 0
                messages.error(self, 'No se enconcontraron las preguntas o respuestas')
                return redirect('/lecciones/error')
            # Se crea un dictionary con los datos , para poder pasarla a la vista
            cdict = {'pregunta': pregunta, 'listaresp': respuestas, 'tema_id': tema_id, 'nombre_tema': tema.data.nombre}
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

    # Funcion que renderiza la pagina de correcion de una pregunta del quiz
    def corregirquiz(self, respuesta_id, pregunta_id, tema_id):
        try:
            # Se llaman a los metodos necesarios para obtener los datos que se requieren
            respuesta = LogicaEvaluaciones.verrespuestacorrecta(respuesta_id)
            pregunta = LogicaEvaluaciones.verpreguntaid(pregunta_id)
            respuestas = LogicaEvaluaciones.listaresp
            incorrecto = 'RESPUESTA INCORRECTA'
            correcto = 'RESPUESTA CORRECTA'
            tema = LogicaUsuarios.consultar_tema_id(tema_id)
            leccion = LogicaUsuarios.consultar_leccion_id(tema.data.leccion_id)
            LogicaEvaluaciones.aux_quiz = LogicaEvaluaciones.aux_quiz + 1
            if respuesta.correcta:
                cdict = {'pregunta': pregunta.contenido, 'listaresp': respuestas, 'tema_id': tema_id,
                         'mensaje': 'true', 'leccion': leccion.data.id, 'curso_id': LogicaEvaluaciones.id_curso,
                         'nombre_tema': tema.data.nombre}
                messages.success(self, correcto)
                if LogicaEvaluaciones.aux_quiz == 5:
                    LogicaEvaluaciones.terminar_quiz(self, tema_id, LogicaEvaluaciones.id_curso)
                    return render(self, 'evaluaciones/quiz3.html', cdict)
                else:
                    LogicaEvaluaciones.listaquiz.remove(pregunta)
                    # Se renderiza la pagina de correccion de pregunta con todos los datos necesarios
                    return render(self, 'evaluaciones/quiz2.html', cdict)
                    # Si la respuesta no es correcta se arma el dictionary y se indica que la respuesta es incorrecta
                    # mandando false como mensaje
            elif not respuesta.correcta:
                cdict = {'pregunta': pregunta.contenido, 'listaresp': respuestas, 'tema_id': tema_id,
                         'mensaje': 'false', 'leccion': leccion.data.id, 'curso_id': LogicaEvaluaciones.id_curso}
                messages.error(self, incorrecto)
                if LogicaEvaluaciones.aux_quiz == 5:
                    LogicaEvaluaciones.terminar_quiz(self, tema_id, LogicaEvaluaciones.id_curso)
                    return render(self, 'evaluaciones/quiz3.html', cdict)
                else:
                    LogicaEvaluaciones.listaquiz.remove(pregunta)
                    # Se renderiza la pagina de correccion de preguntas con todos los datos necesarios
                    return render(self, 'evaluaciones/quiz2.html', cdict)
        except ConnectionError as e:
            messages.error(self, 'Error de conexion')
            return redirect('/lecciones/error')

    def examen(self, leccion_id):
        try:
            LogicaEvaluaciones.listaresp = []
            leccion = LogicaUsuarios.consultar_leccion_id(leccion_id)
            # Se obtienen todos los datos necesarios para desplegar una pregunta
            prueba = LogicaEvaluaciones.verprueba(leccion_id)
            LogicaEvaluaciones.listaexamen = LogicaEvaluaciones.verpreguntasexamen(prueba.pk)
            pregunta = random.choice(LogicaEvaluaciones.listaexamen)
            respuestas = LogicaEvaluaciones.verrespuestas(pregunta.pk)
            LogicaEvaluaciones.listaexamen.remove(pregunta)
            LogicaEvaluaciones.aux_examen = LogicaEvaluaciones.aux_examen + 1
            # En el caso de que alguna de las listas no tenga elementos se abre una pagina de error
            if len(LogicaEvaluaciones.listaexamen) == 0 or len(respuestas) == 0:
                LogicaEvaluaciones.listaexamen = []
                LogicaEvaluaciones.aux_examen = 0
                messages.error(self, 'No se enconcontraron las preguntas o respuestas')
                return redirect('/lecciones/error')
            # Se crea un dictionary con los datos , para poder pasarla a la vista
            cdict = {'pregunta': pregunta, 'listaresp': respuestas, 'leccion_id': leccion_id,
                     'nombre_leccion': leccion.data.nombre}
            # Se renderiza la vista con las lecciones
            return render(self, 'evaluaciones/examen.html', cdict)
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

    @csrf_exempt
    def examen2(self, respuesta_id, leccion_id):
        try:
            LogicaEvaluaciones.listaresp = []
            lista = []
            prueba = LogicaEvaluaciones.verprueba(leccion_id)
            pregunta = random.choice(LogicaEvaluaciones.listaexamen)
            respuestas = LogicaEvaluaciones.verrespuestas(pregunta.pk)
            if respuesta_id == "0":
                LogicaEvaluaciones.timeout = True
                return render(self, 'evaluaciones/examen.html')
            if LogicaEvaluaciones.timeout:
                LogicaEvaluaciones.listaexamen.remove(pregunta)
                LogicaEvaluaciones.timeout = False
                LogicaEvaluaciones.aux_examen = LogicaEvaluaciones.aux_examen + 1
            else:
                if 1 <= LogicaEvaluaciones.aux_examen < 20:
                    respuestaanterior = LogicaEvaluaciones.verrespuestacorrecta(respuesta_id)
                    if respuestaanterior.correcta:
                        LogicaEvaluaciones.nota = LogicaEvaluaciones.nota + 1
                    LogicaEvaluaciones.listaexamen.remove(pregunta)
                    LogicaEvaluaciones.aux_examen = LogicaEvaluaciones.aux_examen + 1
                elif LogicaEvaluaciones.aux_examen == 20:
                    calificacion = LogicaUsuarios.consultar_calificacion_prueba(self.user.pk, prueba.pk)
                    if calificacion.status_code == 404:
                        LogicaEvaluaciones.registrar_calificacion(self.user.pk, prueba.pk, LogicaEvaluaciones.nota)
                    elif calificacion.status_code == 200:
                        LogicaEvaluaciones.actualizar_calificacion(self.user.pk, prueba.pk, LogicaEvaluaciones.nota)
                    calificacion_actualizada = LogicaUsuarios.consultar_calificacion_prueba(self.user.pk, prueba.pk)
                    leccion = LogicaUsuarios.consultar_leccion_id(leccion_id)
                    # Se extrae el nombre de la leccion
                    nombre_leccion = leccion.data.nombre
                    if int(calificacion_actualizada.data.nota) >= 10:
                        aprobado = True
                        mensaje = Strings.MensajesExamen.paso
                    else:
                        aprobado = False
                        mensaje = Strings.MensajesExamen.raspo
                    # Se agregan a la lista el objeto calificacion y el nombre de la leccion a la cual pertenece
                    tup = (calificacion_actualizada.data, nombre_leccion, aprobado, mensaje)
                    cdict = {'calificacion': tup, 'curso_id': LogicaEvaluaciones.id_curso}
                    return render(self, 'evaluaciones/resultados.html', cdict)
                # En el caso de que alguna de las listas no tenga elementos se abre una pagina de error
                if len(LogicaEvaluaciones.listaexamen) == 0 or len(respuestas) == 0:
                    listaexamen = []
                    aux_examen = 0
                    messages.error(self, 'No se enconcontraron las preguntas o respuestas')
                    return redirect('/lecciones/error')
            # Se crea un dictionary con los datos , para poder pasarla a la vista
            cdict = {'pregunta': pregunta, 'listaresp': respuestas, 'leccion_id': leccion_id}
            # Se renderiza la vista con las lecciones
            print(LogicaEvaluaciones.nota)
            return render(self, 'evaluaciones/examen.html', cdict)
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
            # Llamada al api que consulta las respuestas de una pregunta determinada
            page = requests.get(settings.API_PATH + 'ver-resp/' + str(pregunta_id))
            # Se convierte la respuesta en json para poder extraer sus datos
            pagejson = page.json()
            # Se recorre la lista de respuestas y se forma una lista de respuestas con objetos tipo Respuesta
            for item in pagejson:
                orespuesta = Respuesta(pk=item["id"], contenido=item["contenido"], correcta=item["correcta"])
                LogicaEvaluaciones.listaresp.append(orespuesta)
            # Se devuelve la lista de respuestas
            random.shuffle(LogicaEvaluaciones.listaresp)
            return LogicaEvaluaciones.listaresp
        except ConnectionError as e:
            raise e
        except KeyError as e:
            raise e

    # Funcion que consulta si una respuesta es correcta o incorecta
    @staticmethod
    def verrespuestacorrecta(respuesta_id):
        try:
            if respuesta_id == "0":
                respuesta = Respuesta(correcta=False)
                return respuesta
            else:
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

    def terminar_quiz(self, tema_id, curso_id):
        global aux_quiz
        global listaquiz
        try:
            aux_quiz = 0
            listaquiz = []
            # Se consulta el progreso del usuario en la base de datos
            progreso = LogicaLecciones.consultar_progreso_curso(self.user.pk, curso_id)
            # Si existe el registro se actualiza el progreso si es un tema mayor
            if progreso.status_code == 200:
                LogicaUsuarios.actualizar_progreso(self.user.pk, tema_id, curso_id)
            # Se renderiza la pagina de correccion de preguntas con todos los datos necesarios
        except ConnectionError as e:
            messages.error(self, 'Error de conexion')
            return redirect('/lecciones/error')

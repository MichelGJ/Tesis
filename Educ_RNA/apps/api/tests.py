from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import Leccion, Tema, InfoTema, Link, Quiz, Pregunta, Prueba, Respuesta, Progreso, Calificacion, Curso
# Create your tests here.


class RegistrationTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.password = '20977974m'
        self.confirm_password = '20977974m'
        self.user = User(username='MICHELJRAICHE', first_name='Michel', last_name='Jraiche',
                         email='micheljraiche@gmail.com')

    def test_api_registrar(self):
        data = {'username': self.user.username, 'password': self.password, 'confirm_password': self.confirm_password,
                'first_name': self.user.first_name, 'last_name': self.user.last_name, 'email': self.user.email}
        response = self.client.post(reverse('registrarusuario'), data=data)
        username = response.json()["username"]
        self.assertEquals(username, self.user.username)
        self.assertEquals(response.status_code, 201)

    def test_api_usuario_duplicado(self):
        data = {'username': self.user.username, 'password': self.password, 'confirm_password': self.confirm_password,
                'first_name': self.user.first_name, 'last_name': self.user.last_name, 'email': self.user.email}
        usuario = User.objects.create(username=self.user.username, first_name=self.user.first_name,
                                      last_name=self.user.last_name, email=self.user.email)
        usuario.set_password(self.password)
        usuario.save()
        response = self.client.post(reverse('registrarusuario'), data=data)
        responsejson = str(response.json()['username'])
        respuesta = responsejson.partition("[")[2].partition("]")[0]
        error = "'Ya existe un usuario con este nombre.'"
        self.assertEquals(respuesta, error)
        self.assertEquals(response.status_code, 400)

    def test_api_correo_invalido(self):
        data = {'username': self.user.username, 'password': self.password, 'confirm_password': self.confirm_password,
                'first_name': self.user.first_name, 'last_name': self.user.last_name, 'email': 'micheljraiche@hotmail'}
        response = self.client.post(reverse('registrarusuario'), data=data)
        responsejson = str(response.json()['email'])
        respuesta = responsejson.partition("[")[2].partition("]")[0]
        error = "'Introduzca una dirección de correo electrónico válida.'"
        self.assertEquals(respuesta, error)
        self.assertEquals(response.status_code, 400)

    def test_api_contrasena_invalida(self):
        data = {'username': self.user.username, 'password': '20977974', 'confirm_password': '20977974',
                'first_name': self.user.first_name, 'last_name': self.user.last_name, 'email': self.user.email}
        response = self.client.post(reverse('registrarusuario'), data=data)
        responsejson = response.json()['username']
        respuesta = responsejson.partition("[")[2].partition("]")[0]
        error = "'Esta contraseña es completamente numérica.'"
        self.assertEquals(respuesta, error)
        self.assertEquals(response.status_code, 201)

    def test_api_contrasena_invalida2(self):
        data = {'username': self.user.username, 'password': '19467m', 'confirm_password': '19467m',
                'first_name': self.user.first_name, 'last_name': self.user.last_name, 'email': self.user.email}
        response = self.client.post(reverse('registrarusuario'), data=data)
        responsejson = response.json()['username']
        respuesta = responsejson.partition("[")[2].partition("]")[0]
        error = "'Esta contraseña es demasiado corta. Debe contener al menos 8 caracteres.'"
        self.assertEquals(respuesta, error)
        self.assertEquals(response.status_code, 201)

    def test_api_contrasena_no_coinciden(self):
        data = {'username': self.user.username, 'password': '20977974p', 'confirm_password': '20977974i',
                'first_name': self.user.first_name, 'last_name': self.user.last_name, 'email': self.user.email}
        response = self.client.post(reverse('registrarusuario'), data=data)
        responsejson = response.json()['username']
        respuesta = responsejson.partition("[")[2].partition("]")[0]
        error = "'Claves no coinciden'"
        self.assertEquals(respuesta, error)
        self.assertEquals(response.status_code, 201)

    def test_api_login(self):
        user = User.objects.create(username=self.user.username)
        user.set_password(self.password)
        user.save()
        data = {'username': self.user.username, 'password': self.password}
        response = self.client.post(reverse('login'), data=data)
        self.assertEquals(response.status_code, 200)

    def test_api_fail_login(self):
        data = {'username': self.user.username, 'password': '201457k'}
        response = self.client.post(reverse('login'), data=data)
        self.assertEquals(response.status_code, 404)


class UsuariosTests(TestCase):

    def setUp(self):
        self.password = '20977974m'
        self.client = APIClient()
        self.user = User.objects.create(id=1, username='MICHELJRAICHE', first_name='Michel', last_name='Jraiche',
                                        email='micheljraiche@gmail.com')
        self.user2 = User.objects.create(id=2, username='MICHEL', first_name='Michel', last_name='Jraiche',
                                         email='michel@gmail.com')
        self.user.set_password(self.password)
        self.user.save()
        self.curso = Curso.objects.create(id=1, nombre='Curso')
        self.leccion = Leccion.objects.create(id=1, nombre='Leccion')
        self.leccion2 = Leccion.objects.create(id=2, nombre='Leccion2')
        self.tema = Tema.objects.create(id=1, nombre='Tema', leccion=self.leccion)
        self.tema2 = Tema.objects.create(id=2, nombre='Tema2', leccion=self.leccion)
        self.prueba = Prueba.objects.create(id=1, leccion=self.leccion2)
        self.progreso = Progreso.objects.create(usuario_id=self.user.id, tema_id=self.tema.id, curso_id=self.curso.id)
        self.calificacion = Calificacion.objects.create(usuario_id=self.user.id, prueba_id=self.prueba.id, nota='14',
                                                        mejor_nota='14', intentos=1)

    def test_api_actualizar_usuario(self):
        data = {'username': 'MichelGJ', 'first_name': 'Mich', 'last_name': 'Jraich'}
        response = self.client.put(reverse('actualizarusuario', args=str(self.user.id)), data=data)
        user = User.objects.get(id=self.user.id)
        username = user.username
        self.assertEquals(username, 'MichelGJ')
        self.assertEquals(response.status_code, 200)

    def test_api_fail_actualizar_usuario(self):
        data = {'username': self.user2.username, 'first_name': 'Mich', 'last_name': 'Jraich'}
        response = self.client.put(reverse('actualizarusuario', args=str(self.user.id)), data=data)
        responsejson = str(response.json()['username'])
        respuesta = responsejson.partition("[")[2].partition("]")[0]
        error = "'Ya existe un usuario con este nombre.'"
        self.assertEquals(respuesta, error)
        self.assertEquals(response.status_code, 400)

    def test_api_cambio_contrasena(self):
        data = {'username': self.user.username, 'old_password': self.password, 'new_password': '20977974p',
                'new_password2': '20977974p'}
        response = self.client.put(reverse('cambiocontrasena'), data=data)
        responsejson = response.json()
        mensaje = "Success."
        self.assertEquals(responsejson, mensaje)
        self.assertEquals(response.status_code, 200)

    def test_api_contrasena_nueva_invalida(self):
        data = {'username': self.user.username, 'old_password': self.password, 'new_password': '19467m',
                'new_password2': '19467m'}
        response = self.client.put(reverse('cambiocontrasena'), data=data)
        responsejson = str(response.json()['new_password'])
        respuesta = responsejson.partition("[")[2].partition("]")[0]
        error = "'Esta contraseña es demasiado corta. Debe contener al menos 8 caracteres.'"
        self.assertEquals(respuesta, error)
        self.assertEquals(response.status_code, 400)

    def test_api_contrasena_actual_incorrecta(self):
        data = {'username': self.user.username, 'old_password': '20977974y', 'new_password': '20977974p',
                'new_password2': '20977974p'}
        response = self.client.put(reverse('cambiocontrasena'), data=data)
        responsejson = str(response.json()['old_password'])
        respuesta = responsejson.partition("[")[2].partition("]")[0]
        error = "'Clave actual incorrecta'"
        self.assertEquals(respuesta, error)
        self.assertEquals(response.status_code, 400)

    def test_api_registrar_progreso(self):
        data = {'usuario_id': self.user2.id, 'tema_id': self.tema.id, 'curso_id': self.curso.id}
        response = self.client.post(reverse('registrarprogreso'), data=data)
        progreso = Progreso.objects.get(usuario_id=self.user2.id)
        tema_id = progreso.tema_id
        self.assertEquals(tema_id, self.tema.id)
        self.assertEquals(response.status_code, 201)

    def test_api_fail_registrar_progreso(self):
        try:
            data = {'usuario_id': self.user.id, 'tema_id': self.tema2.id,  'curso_id': self.curso.id}
            response = self.client.post(reverse('registrarprogreso'), data=data)
        except IntegrityError:
            pass

    def test_api_actualizar_progreso(self):
        data = {'usuario_id': self.user.id, 'tema_id': self.tema2.id, 'curso_id': self.curso.id}
        response = self.client.put(reverse('actualizarprogreso'), data=data)
        progreso = Progreso.objects.get(usuario_id=self.user.id)
        tema_id = progreso.tema_id
        self.assertEquals(tema_id, self.tema2.id)
        self.assertEquals(response.status_code, 200)

    def test_api_fail_actualizar_progreso(self):
        data = {'usuario_id': self.user.id, 'tema_id': self.tema.id, 'curso_id': self.curso.id}
        response = self.client.put(reverse('actualizarprogreso'), data=data)
        self.assertEquals(response.status_code, 400)

    def test_api_consultar_progreso(self):
        response = self.client.get(reverse('verprogreso', args=str(self.user.id)))
        responsejson = response.json()
        tema_id = responsejson[0]["tema_id"]
        self.assertEquals(tema_id, self.progreso.tema_id)

    def test_api_registrar_calificacion(self):
        data = {'usuario_id': self.user2.id, 'prueba_id': self.prueba.id, 'nota': '12', 'mejor_nota': '0',
                'intentos': '0'}
        response = self.client.post(reverse('registrarcalificacion'), data=data)
        calificacion = Calificacion.objects.get(usuario_id=self.user2.id, prueba_id=self.prueba.id)
        nota = calificacion.nota
        mejor_nota = calificacion.mejor_nota
        self.assertEquals(nota, '12')
        self.assertEquals(mejor_nota, '12')
        self.assertEquals(response.status_code, 200)

    def test_api_fail_registrar_calificacion(self):
        try:
            data = {'usuario_id': self.user.id, 'prueba_id': self.prueba.id, 'nota': '12', 'mejor_nota': '0',
                    'intentos': '0'}
            response = self.client.post(reverse('registrarcalificacion'), data=data)
        except IntegrityError:
            pass

    def test_api_actualizar_calificacion(self):
        data = {'usuario_id': self.user.id, 'prueba_id': self.prueba.id, 'nota': '12', 'mejor_nota': '0',
                'intentos': '0'}
        response = self.client.put(reverse('actualizarcalificacion'), data=data)
        calificacion = Calificacion.objects.get(usuario_id=self.user.id, prueba_id=self.prueba.id)
        nota = calificacion.nota
        mejor_nota = calificacion.mejor_nota
        self.assertEquals(nota, '12')
        self.assertEquals(mejor_nota, '14')
        self.assertEquals(response.status_code, 200)


class LeccionesTests(TestCase):

    def setUp(self):
        self.curso = Curso.objects.create(id=1, nombre='Curso')
        self.leccion = Leccion.objects.create(id=1, nombre='Leccion', curso_id=self.curso.id)
        self.leccion2 = Leccion.objects.create(id=2, nombre='Leccion2', curso_id=self.curso.id)
        self.tema = Tema.objects.create(id=1, nombre='Tema', leccion=self.leccion)
        self.tema2 = Tema.objects.create(id=2, nombre='Tema2', leccion=self.leccion)
        self.infotema = InfoTema.objects.create(presentacion=True, podcast=True, codigo=False, tema=self.tema)
        self.link = Link.objects.create(presentacion='LinkPresentacion', podcast='LinkPodcast', codigo='LinkCodigo',
                                        tema=self.tema)

    def test_api_ver_lecciones(self):
        response = self.client.get(reverse('verlec', args=str(self.curso.id)))
        responsejson = response.json()
        leccion = responsejson[0]['nombre']
        leccion2 = responsejson[1]['nombre']
        self.assertEquals(leccion, self.leccion.nombre)
        self.assertEquals(leccion2, self.leccion2.nombre)
        self.assertEquals(response.status_code, 200)

    def test_api_ver_leccion_id(self):
        response = self.client.get(reverse('verleccionid', args=str(self.leccion2.id)))
        responsejson = response.json()
        leccion = responsejson['nombre']
        self.assertEquals(leccion, self.leccion2.nombre)
        self.assertEquals(response.status_code, 200)

    def test_api_fail_ver_leccion_id(self):
        response = self.client.get(reverse('verleccionid', args='3'))
        self.assertEquals(response.status_code, 404)

    def test_api_ver_temas(self):
        response = self.client.get(reverse('vertemas', args=str(self.leccion.id)))
        responsejson = response.json()
        tema = responsejson[0]['nombre']
        tema2 = responsejson[1]['nombre']
        self.assertEquals(tema, self.tema.nombre)
        self.assertEquals(tema2, self.tema2.nombre)
        self.assertEquals(response.status_code, 200)

    def test_api_ver_tema_id(self):
        response = self.client.get(reverse('vertemaid', args=str(self.tema2.id)))
        responsejson = response.json()
        tema = responsejson['nombre']
        self.assertEquals(tema, self.tema2.nombre)
        self.assertEquals(response.status_code, 200)

    def test_api_fail_ver_tema_id(self):
        response = self.client.get(reverse('vertemaid', args='3'))
        self.assertEquals(response.status_code, 404)

    def test_api_ver_infotema(self):
        response = self.client.get(reverse('verinfotema', args='1'))
        responsejson = response.json()
        presentacion = responsejson['presentacion']
        podcast = responsejson['podcast']
        codigo = responsejson['codigo']
        self.assertEquals(presentacion, self.infotema.presentacion)
        self.assertEquals(podcast, self.infotema.podcast)
        self.assertEquals(codigo, self.infotema.codigo)
        self.assertEquals(response.status_code, 200)

    def test_api_ver_link_presentacion(self):
        response = self.client.get(reverse('verpresentaciones', args='1'))
        responsejson = response.json()
        presentacion = responsejson['presentacion']
        self.assertEquals(presentacion, self.link.presentacion)
        self.assertEquals(response.status_code, 200)

    def test_api_ver_link_podcast(self):
        response = self.client.get(reverse('verpodcast', args='1'))
        responsejson = response.json()
        podcast = responsejson['podcast']
        self.assertEquals(podcast, self.link.podcast)
        self.assertEquals(response.status_code, 200)


class EvaluacionesTests(TestCase):

    def setUp(self):
        self.curso = Curso.objects.create(id=1, nombre='Curso')
        self.leccion = Leccion.objects.create(id=1, nombre='Leccion')
        self.leccion2 = Leccion.objects.create(id=2, nombre='Leccion2')
        self.tema = Tema.objects.create(id=1, nombre='Tema', leccion=self.leccion)
        self.quiz = Quiz.objects.create(id=1, tema=self.tema)
        self.prueba = Prueba.objects.create(id=2, leccion=self.leccion2)
        self.pregunta1 = Pregunta.objects.create(id=1, contenido='PruebaPregunta1', quiz=self.quiz)
        self.pregunta2 = Pregunta.objects.create(id=2, contenido='PruebaPregunta2', prueba=self.prueba, quiz=self.quiz)
        self.respuesta1 = Respuesta.objects.create(id=1, contenido='PruebaRespuesta1', pregunta=self.pregunta1, correcta=True)
        self.respuesta2 = Respuesta.objects.create(id=2, contenido='PruebaRespuesta2', pregunta=self.pregunta1, correcta=False)

    def test_api_get_quiz(self):
        response = self.client.get(reverse('verquiz', args=str(self.tema.id)))
        responsejson = response.json()
        quiz_id = responsejson["id"]
        self.assertEquals(quiz_id, self.quiz.id)
        self.assertEquals(response.status_code, 200)

    def test_api_fail_get_quiz(self):
        response = self.client.get(reverse('verquiz', args='2'))
        self.assertEquals(response.status_code, 404)

    def test_api_get_prueba(self):
        response = self.client.get(reverse('verprueba', args=str(self.leccion2.id)))
        responsejson = response.json()
        prueba_id = responsejson["id"]
        self.assertEquals(prueba_id, self.prueba.id)
        self.assertEquals(response.status_code, 200)

    def test_api_fail_get_prueba(self):
        response = self.client.get(reverse('verprueba', args='1'))
        self.assertEquals(response.status_code, 404)

    def test_api_get_prueba_id(self):
        response = self.client.get(reverse('verpruebaid', args=str(self.prueba.id)))
        responsejson = response.json()
        prueba_id = responsejson["id"]
        self.assertEquals(prueba_id, self.prueba.id)
        self.assertEquals(response.status_code, 200)

    def test_api_fail_get_prueba_id(self):
        response = self.client.get(reverse('verpruebaid', args='1'))
        self.assertEquals(response.status_code, 404)

    def test_api_get_pregunta_quiz(self):
        response = self.client.get(reverse('verpregquiz', args=str(self.quiz.id)))
        responsejson = response.json()
        pregunta = responsejson[0]['contenido']
        pregunta2 = responsejson[1]['contenido']
        self.assertEquals(pregunta, self.pregunta1.contenido)
        self.assertEquals(pregunta2, self.pregunta2.contenido)
        self.assertEquals(response.status_code, 200)

    def test_api_get_pregunta_prueba(self):
        response = self.client.get(reverse('verpregprueba', args=str(self.prueba.id)))
        responsejson = response.json()
        pregunta = responsejson[0]['contenido']
        self.assertEquals(pregunta, self.pregunta2.contenido)
        self.assertEquals(response.status_code, 200)

    def test_get_pregunta_id(self):
        response = self.client.get(reverse('verpregunta', args=str(self.pregunta2.id)))
        responsejson = response.json()
        pregunta = responsejson['contenido']
        self.assertEquals(pregunta, self.pregunta2.contenido)
        self.assertEquals(response.status_code, 200)

    def test_get_respuesta(self):
        response = self.client.get(reverse('verresp', args=str(self.pregunta1.id)))
        responsejson = response.json()
        respuesta = responsejson[0]['contenido']
        respuesta2 = responsejson[1]['contenido']
        self.assertEquals(respuesta, self.respuesta1.contenido)
        self.assertEquals(respuesta2, self.respuesta2.contenido)
        self.assertEquals(response.status_code, 200)

    def test_get_respuesta_id(self):
        response = self.client.get(reverse('verrespid', args=str(self.respuesta2.id)))
        responsejson = response.json()
        respuesta = responsejson['contenido']
        self.assertEquals(respuesta, self.respuesta2.contenido)
        self.assertEquals(response.status_code, 200)



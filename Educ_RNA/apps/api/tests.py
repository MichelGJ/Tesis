from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Leccion, Tema, InfoTema, Link, Quiz, Pregunta, Prueba, Respuesta
# Create your tests here.


class RegistrationTests(TestCase):

    def setUp(self):
        self.username = 'MICHELJRAICHE'
        self.password = '20977974m'
        self.confirm_password = '20977974m'
        self.first_name = 'Michel'
        self.last_name = 'Jraiche'
        self.email = 'micheljraiche@gmail.com'
        self.client = APIClient()

    def test_api_registrar(self):
        data = {'username': self.username, 'password': self.password, 'confirm_password': self.confirm_password,
                'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email}
        response = self.client.post(reverse('registrarusuario'), data=data)
        self.assertEquals(response.status_code, 201)

    def test_api_usuario_duplicado(self):
        data = {'username': self.username, 'password': self.password, 'confirm_password': self.confirm_password,
                'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email}
        response = self.client.post(reverse('registrarusuario'), data=data)
        response2 = self.client.post(reverse('registrarusuario'), data=data)
        responsejson = str(response2.json()['username'])
        respuesta = responsejson.partition("[")[2].partition("]")[0]
        error = "'Ya existe un usuario con este nombre.'"
        self.assertEquals(respuesta, error)
        self.assertEquals(response2.status_code, 400)

    def test_api_correo_invalido(self):
        data = {'username': self.username, 'password': self.password, 'confirm_password': self.confirm_password,
                'first_name': self.first_name, 'last_name': self.last_name, 'email': 'micheljraiche@hotmail'}
        response = self.client.post(reverse('registrarusuario'), data=data)
        responsejson = str(response.json()['email'])
        respuesta = responsejson.partition("[")[2].partition("]")[0]
        error = "'Introduzca una dirección de correo electrónico válida.'"
        self.assertEquals(respuesta, error)
        self.assertEquals(response.status_code, 400)

    def test_api_contrasena_invalida(self):
        data = {'username': self.username, 'password': '20977974', 'confirm_password': '20977974',
                'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email}
        response = self.client.post(reverse('registrarusuario'), data=data)
        responsejson = response.json()['username']
        respuesta = responsejson.partition("[")[2].partition("]")[0]
        error = "'Esta contraseña es completamente numérica.'"
        self.assertEquals(respuesta, error)
        self.assertEquals(response.status_code, 201)

    def test_api_contrasena_invalida2(self):
        data = {'username': self.username, 'password': '19467m', 'confirm_password': '19467m',
                'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email}
        response = self.client.post(reverse('registrarusuario'), data=data)
        responsejson = response.json()['username']
        respuesta = responsejson.partition("[")[2].partition("]")[0]
        error = "'Esta contraseña es demasiado corta. Debe contener al menos 8 caracteres.'"
        self.assertEquals(respuesta, error)
        self.assertEquals(response.status_code, 201)

    def test_api_contrasena_no_coinciden(self):
        data = {'username': self.username, 'password': '20977974p', 'confirm_password': '20977974i',
                'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email}
        response = self.client.post(reverse('registrarusuario'), data=data)
        responsejson = response.json()['username']
        respuesta = responsejson.partition("[")[2].partition("]")[0]
        error = "'Claves no coinciden'"
        self.assertEquals(respuesta, error)
        self.assertEquals(response.status_code, 201)

    def test_api_login(self):
        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()
        data = {'username': self.username, 'password': self.password}
        response = self.client.post(reverse('login'), data=data)
        self.assertEquals(response.status_code, 200)

    def test_api_fail_login(self):
        data = {'username': self.username, 'password': '201457k'}
        response = self.client.post(reverse('login'), data=data)
        self.assertEquals(response.status_code, 404)


class UsuariosTests(TestCase):

    def setUp(self):
        self.username = 'MICHELJRAICHE'
        self.password = '20977974m'
        self.confirm_password = '20977974m'
        self.first_name = 'Michel'
        self.last_name = 'Jraiche'
        self.email = 'micheljraiche@gmail.com'
        self.client = APIClient()
        self.user = User.objects.create(username=self.username, first_name=self.first_name, last_name=self.last_name)
        self.user.set_password(self.password)
        self.user.save()

    def test_api_actualizar_usuario(self):
        data = {'username': 'MichelGJ', 'first_name': 'Mich', 'last_name': 'Jraich'}
        response = self.client.put(reverse('actualizarusuario', args=str(self.user.id)), data=data)
        self.assertEquals(response.status_code, 200)

    def test_api_fail_actualizar_usuario(self):
        user = User.objects.create(username='Horashio', first_name='Horacio', last_name='Orrillo')
        user.set_password(self.password)
        user.save()
        data = {'username': self.username, 'first_name': 'Mich', 'last_name': 'Jraich'}
        response = self.client.put(reverse('actualizarusuario', args=str(user.id)), data=data)
        responsejson = str(response.json()['username'])
        respuesta = responsejson.partition("[")[2].partition("]")[0]
        error = "'Ya existe un usuario con este nombre.'"
        self.assertEquals(respuesta, error)
        self.assertEquals(response.status_code, 400)

    def test_api_cambio_contrasena(self):
        data = {'username': self.username, 'old_password': self.password, 'new_password': '20977974p',
                'new_password2': '20977974p'}
        response = self.client.put(reverse('cambiocontrasena'), data=data)
        responsejson = response.json()
        error = "Success."
        self.assertEquals(responsejson, error)
        self.assertEquals(response.status_code, 200)

    def test_api_contrasena_nueva_invalida(self):
        data = {'username': self.username, 'old_password': self.password, 'new_password': '19467m',
                'new_password2': '19467m'}
        response = self.client.put(reverse('cambiocontrasena'), data=data)
        responsejson = str(response.json()['new_password'])
        respuesta = responsejson.partition("[")[2].partition("]")[0]
        error = "'Esta contraseña es demasiado corta. Debe contener al menos 8 caracteres.'"
        self.assertEquals(respuesta, error)
        self.assertEquals(response.status_code, 400)

    def test_api_contrasena_actual_incorrecta(self):
        data = {'username': self.username, 'old_password': '20977974y', 'new_password': '20977974p',
                'new_password2': '20977974p'}
        response = self.client.put(reverse('cambiocontrasena'), data=data)
        responsejson = str(response.json()['old_password'])
        respuesta = responsejson.partition("[")[2].partition("]")[0]
        error = "'Clave actual incorrecta'"
        self.assertEquals(respuesta, error)
        self.assertEquals(response.status_code, 400)


class LeccionesTests(TestCase):

    def setUp(self):
        self.leccion = 'Leccion'
        self.leccion2 = 'Leccion2'
        self.tema = 'Tema'
        self.tema2 = 'Tema2'
        self.presentacion = True
        self.podcast = True
        self.codigo = False
        self.linkpres = 'LinkPresentacion'
        self.linkpod = 'LinkPodcast'
        self.linkcod = 'LinkCodigo'
        leccion = Leccion.objects.create(id=1, nombre=self.leccion)
        leccion2 = Leccion.objects.create(id=2, nombre=self.leccion2)
        tema = Tema.objects.create(id=1, nombre=self.tema, leccion=leccion)
        tema2 = Tema.objects.create(id=2, nombre=self.tema2, leccion=leccion)
        InfoTema.objects.create(presentacion=self.presentacion, podcast=self.podcast, codigo=self.codigo, tema=tema)
        Link.objects.create(presentacion=self.linkpres, podcast=self.linkpod, codigo=self.linkcod, tema=tema)

    def test_api_ver_lecciones(self):
        response = self.client.get(reverse('verlec'))
        responsejson = response.json()[0]['nombre']
        responsejson2 = response.json()[1]['nombre']
        self.assertEquals(responsejson, self.leccion)
        self.assertEquals(responsejson2, self.leccion2)
        self.assertEquals(response.status_code, 200)

    def test_api_ver_temas(self):
        response = self.client.get(reverse('vertemas', args='1'))
        responsejson = response.json()[0]['nombre']
        responsejson2 = response.json()[1]['nombre']
        self.assertEquals(responsejson, self.tema)
        self.assertEquals(responsejson2, self.tema2)
        self.assertEquals(response.status_code, 200)

    def test_api_ver_infotema(self):
        response = self.client.get(reverse('verinfotema', args='1'))
        responsejson = response.json()['presentacion']
        responsejson2 = response.json()['podcast']
        responsejson3 = response.json()['codigo']
        self.assertEquals(responsejson, self.presentacion)
        self.assertEquals(responsejson2, self.podcast)
        self.assertEquals(responsejson3, self.codigo)
        self.assertEquals(response.status_code, 200)

    def test_api_ver_link_presentacion(self):
        response = self.client.get(reverse('verpresentaciones', args='1'))
        responsejson = response.json()['presentacion']
        self.assertEquals(responsejson, self.linkpres)
        self.assertEquals(response.status_code, 200)

    def test_api_ver_link_podcast(self):
        response = self.client.get(reverse('verpodcast', args='1'))
        responsejson = response.json()['podcast']
        self.assertEquals(responsejson, self.linkpod)
        self.assertEquals(response.status_code, 200)


class EvaluacionesTests(TestCase):

    def setUp(self):
        self.leccion = 'Leccion'
        self.leccion2 = 'Leccion2'
        self.tema = 'Tema'
        self.tema2 = 'Tema2'
        self.pregunta1 = 'PruebaPregunta1'
        self.pregunta2 = 'PruebaPregunta2'
        self.respuesta1 = 'PruebaRespuesta1'
        self.respuesta2 = 'PruebaRespuesta2'
        leccion = Leccion.objects.create(id=1, nombre=self.leccion)
        leccion2 = Leccion.objects.create(id=2, nombre=self.leccion2)
        tema = Tema.objects.create(id=1, nombre=self.tema, leccion=leccion)
        quiz = Quiz.objects.create(id=1, tema=tema)
        prueba = Prueba.objects.create(id=2, leccion=leccion2)
        pregunta1 = Pregunta.objects.create(id=1, contenido=self.pregunta1, quiz=quiz)
        pregunta2 = Pregunta.objects.create(id=2, contenido=self.pregunta2, prueba=prueba, quiz=quiz)
        Respuesta.objects.create(id=1, contenido=self.respuesta1, pregunta=pregunta1, correcta=True)
        Respuesta.objects.create(id=2, contenido=self.respuesta2, pregunta=pregunta1, correcta=False)

    def test_api_get_quiz(self):
        response = self.client.get(reverse('verquiz', args='1'))
        responsejson = response.json()['id']
        self.assertEquals(responsejson, 1)
        self.assertEquals(response.status_code, 200)

    def test_api_fail_get_quiz(self):
        response = self.client.get(reverse('verquiz', args='2'))
        self.assertEquals(response.status_code, 404)

    def test_api_get_prueba(self):
        response = self.client.get(reverse('verprueba', args='2'))
        responsejson = response.json()['id']
        self.assertEquals(responsejson, 2)
        self.assertEquals(response.status_code, 200)

    def test_api_fail_get_prueba(self):
        response = self.client.get(reverse('verprueba', args='1'))
        self.assertEquals(response.status_code, 404)

    def test_api_get_pregunta_quiz(self):
        response = self.client.get(reverse('verpregquiz', args='1'))
        responsejson = response.json()[0]['contenido']
        responsejson2 = response.json()[1]['contenido']
        pregunta1 = self.pregunta1
        pregunta2 = self.pregunta2
        self.assertEquals(responsejson, pregunta1)
        self.assertEquals(responsejson2, pregunta2)
        self.assertEquals(response.status_code, 200)

    def test_api_get_pregunta_prueba(self):
        response = self.client.get(reverse('verpregprueba', args='2'))
        responsejson = response.json()[0]['contenido']
        pregunta = self.pregunta2
        self.assertEquals(responsejson, pregunta)
        self.assertEquals(response.status_code, 200)

    def test_get_pregunta_id(self):
        response = self.client.get(reverse('verpregunta', args='2'))
        responsejson = response.json()['contenido']
        pregunta = self.pregunta2
        self.assertEquals(responsejson, pregunta)
        self.assertEquals(response.status_code, 200)

    def test_get_respuesta(self):
        response = self.client.get(reverse('verresp', args='1'))
        responsejson = response.json()[0]['contenido']
        responsejson2 = response.json()[1]['contenido']
        respuesta1 = self.respuesta1
        respuesta2 = self.respuesta2
        self.assertEquals(responsejson, respuesta1)
        self.assertEquals(responsejson2, respuesta2)
        self.assertEquals(response.status_code, 200)

    def test_get_respuesta_id(self):
        response = self.client.get(reverse('verrespid', args='2'))
        responsejson = response.json()['contenido']
        respuesta = self.respuesta2
        self.assertEquals(responsejson, respuesta)
        self.assertEquals(response.status_code, 200)



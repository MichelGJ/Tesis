from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

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

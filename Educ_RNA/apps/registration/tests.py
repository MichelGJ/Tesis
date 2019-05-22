from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
# Create your tests here.


class LoginTestCase(TestCase):

    def setUp(self):
        self.password = '20977974m'
        self.confirm_password = '20977974m'
        self.user = User(username='MICHELJRAICHE', first_name='Michel', last_name='Jraiche',
                         email='micheljraiche@gmail.com')

    def test_login(self):
        user = User.objects.create(username=self.user.username)
        user.set_password(self.password)
        user.save()
        data = {'username': self.user.username, 'password': self.password}
        response = self.client.post(reverse('plogin'), data=data)
        self.assertEquals(response.status_code, 302)

    def test_fail_login(self):
        data = {'username': self.user.username, 'password': '20977974uy'}
        response = self.client.post(reverse('plogin'), data=data)
        self.assertEquals(response.status_code, 302)

    def test_registrar(self):
        data = {'username': self.user.username, 'password1': self.password, 'password2': self.confirm_password,
                'first_name': self.user.first_name, 'last_name': self.user.last_name, 'email': self.user.email}
        response = self.client.post(reverse('registro'), data=data)
        self.assertRedirects(response, 'login.html')
        self.assertEquals(response.status_code, 302)


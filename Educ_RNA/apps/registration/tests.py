from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
# Create your tests here.


class LoginTestCase(TestCase):

    def setUp(self):
        self.password = '20977974m'
        self.confirm_password = '20977974m'
        self.user = User.objects.create(username='MICHELJRAICHE', first_name='Michel', last_name='Jraiche',
                                        email='micheljraiche@gmail.com')

    def test_registrar(self):
        data = {'username': "MJJJ", 'password1': self.password, 'password2': self.confirm_password,
                'first_name': self.user.first_name, 'last_name': self.user.last_name, 'email': 'michjraich23@gmail.com'}
        response = self.client.post(reverse('registro'), data=data, follow=True)
        self.assertRedirects(response, expected_url=reverse('registrar'), status_code=302,
                             target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_login(self):
        data = {'username': "MJJJ", 'password': self.password}
        response = self.client.post(reverse('plogin'), data=data, follow=True)
        self.assertRedirects(response, expected_url='usuarios/index/', status_code=302,
                             target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        self.assertEquals(response.status_code, 302)

    def test_fail_login(self):
        data = {'username': self.user.username, 'password': '20977974uy'}
        response = self.client.post(reverse('plogin'), data=data)
        self.assertEquals(response.status_code, 302)



from django.test import TestCase, Client

from django.urls import reverse, resolve

from users.views import register

class TestForms(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_post(self):
        """ Test if right data provided """

        url = reverse('users-register')

        right_register = self.client.post(url, {
            'first_name': 'mohsen',
            'last_name': 'ali',
            'email': 'joker@gmail.com',
            'gender': 1,
            'username': 'joker',
            'password1': 'testing1234',
            'password2': 'testing1234',            
        })

        #to check did they make redirect to home page or not
        self.assertEqual(right_register.status_code, 302)

        
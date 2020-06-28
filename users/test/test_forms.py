from users.forms import UserRegisterForm

from django.test import TestCase, Client

from django.urls import reverse, resolve

from users.views import register

class TestForms(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_right_data(self):
        """ Test if right data provided """

        url = reverse('register')

        right_register = self.client.post(url, {
            'first_name': 'mohsen',
            'last_name': 'ali',
            'username': 'joker',
            'password1': 'testing1234'
            'password2': 'testing1234'
        })

        form = UserRegisterForm(right_register.POST)

        self.assertEqual(right_register.status_code, 200)
        self.assertTemplateUsed(right_register, 'blog/home.html')
        self.assertTrue(form.is_valid())

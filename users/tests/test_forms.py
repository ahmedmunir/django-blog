from users.forms import UserRegisterForm

from django.test import TestCase, Client

from django.urls import reverse, resolve

from users.views import register

class TestForms(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_right_data(self):
        """ Test if right data provided """

        form = UserRegisterForm(data= {
            'first_name': 'mohsen',
            'last_name': 'ali',
            'username': 'joker',
            'email': 'joker@gmail.com',
            'password1': 'testing1234',
            'password2': 'testing1234'            
        })

        self.assertTrue(form.is_valid())

    @classmethod
    def tearDownClass(cls):
        print("users test_forms completed")
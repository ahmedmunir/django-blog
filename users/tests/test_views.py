from django.test import TestCase, Client

from django.urls import reverse, resolve

from users.views import register

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_register(self):
        """ Testing get register function """
        response = self.client.get(reverse('users-register'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'users/register.html')

    @classmethod
    def tearDownClass(cls):
        print("users test_views completed")
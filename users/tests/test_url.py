from django.test import TestCase

from django.urls import reverse, resolve

from users.views import register


class TestUrl(TestCase):

    def test_get_register(self):
        """ Testing get register function """
        url = reverse('users-register')

        self.assertEqual(resolve(url).func, register)


from django.test import TestCase

from django.urls import reverse, resolve

from blogapp.views import home, about


class TestUrls(TestCase):

    """ Testing Home URL """
    def test_home(self):
        url = reverse('blog-home')

        self.assertEqual(resolve(url).func, home)

    """ Testing About URL """
    def test_about(self):
        url = reverse('blog-about')

        self.assertEqual(resolve(url).func, about)

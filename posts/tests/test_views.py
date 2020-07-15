from django.urls import reverse

from users.models import UserCustom

from posts.models import Post

from django.test import TestCase, Client

class TestViews(TestCase):

    def setUp(self):
        """ Initialize some inputs for virutal Database"""
        self.user = UserCustom.objects.create(username='Ahmed', email='ahmed@gmail.com', password='ahmed1234', gender=1)

        self.post = Post.objects.create(title='post', content='This is post created', author=self.user)

        self.client = Client()

    def test_get_home(self):
        """ Testing get home page"""

        response = self.client.get(reverse('blog-home'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'blogapp/home.html')

    def test_get_about(self):
        """ Testing get about page """
        response = self.client.get(reverse('blog-about'))

        self.assertEqual(response.status_code, 302)



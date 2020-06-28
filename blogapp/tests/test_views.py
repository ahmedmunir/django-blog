from django.urls import reverse

from django.contrib.auth.models import User

from blogapp.models import Post

from django.test import TestCase, Client

class TestViews(TestCase):

    def setUp(self):
        """ Initialize some inputs for virutal Database"""
        self.user = User.objects.create(username='Ahmed', email='ahmed@gmail.com', password='ahmed1234')

        self.post = Post.objects.create(title='post', content='This is post created', author=self.user)

        self.client = Client()

    def test_get_home(self):
        """ Testing get home page"""

        response = self.client.get(reverse('blog-home'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'blog/home.html')

    def test_get_about(self):
        """ Testing get about page """
        response = self.client.get(reverse('blog-about'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'blog/about.html')

    @classmethod
    def tearDownClass(cls):
        print("blogapp test_urls completed")
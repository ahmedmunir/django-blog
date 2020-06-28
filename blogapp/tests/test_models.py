from django.test import TestCase

from django.contrib.auth.models import User

from blogapp.models import Post

class TestModels(TestCase):

    def setUp(self):
        """ Initialize some inputs for virutal Database"""
        self.user = User.objects.create(username='Ahmed', email='ahmed@gmail.com', password='ahmed1234')

        self.post = Post.objects.create(title='post', content='This is post created', author=self.user)

    def test_posts_count(self):
        """ Test how many posts associated with user"""
        self.assertEqual(self.user.posts.count(), 1)

    
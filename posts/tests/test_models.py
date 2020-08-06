from django.test import TestCase

from users.models import NewUser

from posts.models import Post

class TestModels(TestCase):

    def setUp(self):
        """ Initialize some inputs for virutal Database"""
        self.user = NewUser.objects.create(username='Ahmed', email='ahmed@gmail.com', password='ahmed1234', gender=1)

        self.post = Post.objects.create(title='post', content='This is post created', author=self.user)

    def test_posts_count(self):
        """ Test how many posts associated with user"""
        self.assertEqual(self.user.posts.count(), 1)


    
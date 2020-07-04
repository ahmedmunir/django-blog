from django.db import models

from django.shortcuts import reverse

from django.contrib.auth.models import User
# Create your models here.

from django.utils import timezone

from blogapp.models import Post

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')

    text = models.TextField()

    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'comment:{self.text}, \n posted by:{self.owner.username}, \n on post: {self.post.title}'
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.id})
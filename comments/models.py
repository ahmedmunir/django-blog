from django.db import models

from django.shortcuts import reverse

from django.contrib.auth.models import User

from django.utils import timezone

from posts.models import Post

from users.models import NewUser

# Create your models here.
class Comment(models.Model):
    owner = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')

    text = models.TextField()

    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'comment:{self.text}, \n posted by:{self.owner.username}, \n on post: {self.post.title}'
    
    # CBV will use this function to know where to go after successfully 
    # create update comment
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.id})
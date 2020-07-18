from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import NewUser
from ckeditor.fields import RichTextField

# Create your models here.

class Category(models.Model):
    title       =       models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Post(models.Model):
    
    title           =       models.CharField(max_length=100)
    overview        =       models.TextField()
    content         =       RichTextField(null=True)
    date_posted     =       models.DateTimeField(default=timezone.now)
    view_count      =       models.IntegerField(default=0)
    author          =       models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='posts')
    thumbnail       =       models.ImageField(upload_to='posts_pics')
    categories      =       models.ManyToManyField(Category)
    featured        =       models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

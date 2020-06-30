from django.db import models

from django.contrib.auth.models import User

from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # profile_pics is a directory that will be created at same level with project to save images
    # inside of it.
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # execute normal save() function that we inherit from models.Model
        super().save(*args, **kwargs)

        # now we can do what ever we want with this instance.
        # open image path
        img = Image.open(self.image.path)

        # check if it is large image
        if img.width > 300 or img.height > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
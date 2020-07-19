from django.db import models

from django.contrib.auth.models import User

# Import PIL to manipulate image files
from PIL import Image

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):

    def create_user(self, email, username, gender, password=None):
        """
        Creates and saves a User with the given email, username, gender
        and password.
        """
        if not email:
            raise ValueError("Users must have Email")
        if not username:
            raise ValueError("Users must have username")

        user = self.model(

            # lowercase the domain portion of the email address
            email = self.normalize_email(email),
            username = username,
            gender = gender
        )

        #This function will hash given password from NewUser
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, gender, password):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            gender = gender
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class NewUser(AbstractBaseUser, PermissionsMixin):
    """
        New User model after modification
    """

    #Gender choices, values that will be displayed to user.
    GENDER_CHOICES = (
        (1, 'male'),
        (2, 'female'),
    )    

    # Any Field that you want to add or modify to your user Email
    email           = models.EmailField(max_length=60, unique=True)
    username        = models.CharField(max_length=60)
    gender          = models.IntegerField(choices=GENDER_CHOICES)   

    # Those Fields are Required with AbstractBaseUser to work as expected.
    date_joined     = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser

    # we define what manager we will follow, we have custom manager now not default BaseUserManager
    objects = UserManager()

    # This is Required by Django to know which field to Login to User (For Authentication)
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'gender']

    def __str__(self):
        return f"{self.email}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
    

class Profile(models.Model):

    """
        Profile model that associated with User
    """
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE)

    # save new uploaded image to directory /profile_pics/
    image = models.ImageField(upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):

        # execute normal save() function that we inherit from models.Model
        super().save(*args, **kwargs)

        # choose male or female avatar depending on gender
        if self.user.gender == 1:
            self.image = 'male.jpg'
        elif self.user.gender == 2:
            self.image = 'female.jpg'

        # resize image to be 300 * 300
        img = Image.open(self.image.path)

        # check if it is large image
        if img.width > 300 or img.height > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


from django.db import models

from django.contrib.auth.models import User

from PIL import Image


#we need to import those to make every other extensions of Django execute as expected.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# if your user model defines different fields, 
# you’ll need to define a custom manager that extends BaseUserManager 
# providing two additional methods create_user & create_superuser

class UserManager(BaseUserManager):

    # we build create_user with new required field which was by default:
    # username & password & confirm password to create new User.
    # now we will get Rrequired Fields from UserCustom class.
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

        #This function will hash given password from UserCustom
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

#our new User Class, we inherit from AbstractBaseUser
class UserCustom(AbstractBaseUser, PermissionsMixin):

    # Here we put trick of Choices where each choice is a tuple
    # first Value of tuple will be the value that will be stored at DB
    # second value will be presented to any from that will be associated
    # with DB.

    GENDER_CHOICES = (
        (1, 'male'),
        (2, 'female'),
        (3, 'not specified'),
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
    
    # List of Required fields at registeration of create SuperUser
    # and it must have all fields that will not be added automatically
    # or have default value.
    REQUIRED_FIELDS = ['username', 'gender']

    def __str__(self):
        return f"{self.email}"

    #If you want your custom User model to also work with the admin, 
    #your User model must define some additional attributes and methods
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
    

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(UserCustom, on_delete=models.CASCADE)

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


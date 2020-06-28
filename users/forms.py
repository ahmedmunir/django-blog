from django import forms

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

#we inherit all properties from UserCreationForm
class UserRegisterForm(UserCreationForm):

    #create email field
    email = forms.EmailField()

    #create first name field (we need to separate it with _)
    first_name = forms.CharField(max_length=64)

    last_name = forms.CharField(max_length=64)

    class Meta:
        model = User

        #how fields will be display.
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
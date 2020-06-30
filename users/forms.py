from django import forms

from django.contrib.auth.models import User
from users.models import Profile

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
        #those are columns name inside DB Model (User)
        # Any column consists of more than one word will be separated by _
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


# we will create Form and its type is ModelForm, it will communicate with DB to easily
# update instance or add new instance to DB.
# Actually we did this with UserRegisterForm, we inherit from UserCreationForm which is a model Form
# and connects to User model.
class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User

        # fields that will display at this Form, we got them from Model we inherit from
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = ['image']
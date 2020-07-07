from django import forms

from django.contrib.auth.models import User
from users.models import Profile, UserCustom

from django.contrib.auth.forms import UserCreationForm

#we inherit all properties from UserCreationForm
class UserRegisterForm(UserCreationForm):
    """
        Registeration Form after modification to accept new Fields
    """

    #create email field
    email = forms.EmailField()

    class Meta:
        model = UserCustom

        fields = ['username', 'email', 'gender', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    """
        Update User data Form
    """

    class Meta:
        model = UserCustom

        fields = ['username', 'email', 'gender']

class ProfileUpdateForm(forms.ModelForm):

    """
        Update Profile (image) form.
    """

    class Meta:
        model = Profile

        fields = ['image']
from django.shortcuts import render, redirect

from users.forms import UserRegisterForm

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from users.forms import UserUpdateForm, ProfileUpdateForm

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

from users.models import Profile

# Create your views here.

# Register Route
def register(request):

    #check for request
    if request.method == "POST":

        #assign the values sent by POST request to form
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            #add data to database
            form.save()
            
            messages.success(request, f'Your account created successfully, you can Log in now!')

            #redirect to name of function
            return redirect('login')

    else:
        if request.user.is_authenticated:
            return redirect('blog-home')
        else:
            form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# Provilde Route
@login_required
def profile(request):

    #at POST Request
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES, 
                                   instance=request.user.profile)
        
        # check validation
        if u_form.is_valid() and p_form.is_valid():

            # delete previous image before adding new one.
            # but the deletion will not occur if the user current image profile
            # is the default image
            # because we need this default image for new users.
            if 'profile_pics' in Profile.objects.filter(user=request.user).first().image.url:
                Profile.objects.filter(user=request.user).first().image.delete(False)
            u_form.save()
            p_form.save()

            messages.success(request, 'Your data updated Successfully!')
            return redirect('profile')
    
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }


    return render(request, 'users/profile.html', context)

# About Page
@login_required
def about(request):
    return render(request, 'users/about.html')

"""
Custom Login page because The Generic CBV LoginView will redirect user to login.html
Even that user is already logged in.
"""
class CustomLogin(LoginView):

    # we need to define template here or at URL for redirect when user failed to login
    template_name = "users/login.html"

    def get(self, request):

        context = {
            "form": AuthenticationForm
        }

        if request.user.is_authenticated:
            return redirect('blog-home')
        return render(request, 'users/login.html', context)




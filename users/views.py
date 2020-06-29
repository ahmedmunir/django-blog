from django.shortcuts import render, redirect

# this forms associated with User model, there is another forms that can be used to create HTML 
# Form field
#from django.contrib.auth.forms import UserCreationForm

from users.forms import UserRegisterForm

#import flash messages
from django.contrib import messages
#All messages available:
    # messages.debug
    # messages.success
    # messages.info
    # messages.warning
    # messages.error

# we import login_authnetication decorator to make sure that user is already logged in before redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):

    #check for request
    if request.method == "POST":

        #assign the values sent by POST request to form
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            #add data to database
            form.save()
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account created successfully, you can Log in now!')

            #redirect to name of function
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')
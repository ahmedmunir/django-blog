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
            messages.success(request, f'Account created for {username}')

            #redirect to name of function
            return redirect('blog-home')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
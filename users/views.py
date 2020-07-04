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

from users.forms import UserUpdateForm, ProfileUpdateForm

# Create your views here.
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

@login_required
def profile(request):

    #at POST Request
    if request.method == 'POST':
        # Create a form instance from request.user data, it will extract data from request.user
        # and fill Form with this data.
        # we use instance here to fill form and to use save() function.
        # save() method. This method creates and saves a database object from the data bound to the form
        # keyword argument instance; if this is supplied, save() will update that instance. 
        # If it’s not supplied, save() will create a new instance of the specified model.
        # so in this case we need to update so we provide instance keyword argument.
        # in case of UserRegisterForm() we need to create new instance so we didn't add instace keyword arguemnt.
        # in case of upload files we need to add request.FILES
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES, 
                                   instance=request.user.profile)

        # that's why at UserRegisterForm we didn't use instance
        # to let save() create new data model.
        
        # check validation
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, 'Your data updated Successfully!')
            return redirect('profile')
    
    else:
        # we need to populate current forms to have the current data
        # and those are Model Forms, they will not work and populate data unless we passed
        # data to them from the same type by keyword argument instance=request.user
        # which will be User instance.
        # but we use instace= because we not pass normal data (json data like request.POST)
        # we pass instance, so we need to define that this is instance not json data.
        # so as a conclusion:
        # form can populate data at client side using data= or instance= and we pass to both
        # correct data
        # if data is not provided, it will get current instance data.
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }


    return render(request, 'users/profile.html', context)
"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

#here we put the name of function that we want to display at specific route
from users import views as users_register

#using class based views which already built in for login & logout
# CBV handle HTTP requests & has built in FORMS that will inject inside Template
# has built in functionality to handle Errors inside Template.
# dealing with database for authentication also provided
from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

from users.views import CustomLogin

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('posts.urls')),

    path('post/<int:post_id>/comment/', include('comments.urls')),

    path('register/', users_register.register, name='users-register'),

    path('profile/', users_register.profile, name='profile'),

    path('login/', CustomLogin.as_view(), name='login'),

    path('logout/', login_required(auth_views.LogoutView.as_view(template_name='users/logout.html')), name='logout'),

    path('password-reset/', 
    auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), 
    name='password_reset'),

    path('password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
    name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'
    ),
    name='password_reset_confirm'
    ),

    path('password-reset-complete/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
        ),
    name='password_reset_complete'
    ),

    path('password_change/',
    login_required(auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html'
    )),
    name='password_change'
    ),

    path('password_change_done/',
    login_required(auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'
    )),
    name='password_change_done'
    ),    

]


#configure URLS for static media files uploaded by user
from django.conf import settings
from django.conf.urls.static import static

# we just configure that we will add this URL only in DEBUG (development Mode)
if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
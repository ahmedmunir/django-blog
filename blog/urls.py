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

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('blogapp.urls')),

    path('register/', users_register.register, name='users-register'),

    path('profile/', users_register.profile, name='profile'),

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout')
]


#configure URLS for static media files uploaded by user
from django.conf import settings
from django.conf.urls.static import static

# we just configure that we will add this URL only in DEBUG (development Mode)
if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
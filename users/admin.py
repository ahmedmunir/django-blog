from django.contrib import admin

from users.models import UserCustom, Profile

# Register your models here.
admin.site.register(Profile)

from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UpdateUserForm(forms.ModelForm):
    """
    Update User Form. Doesn't allow changing password in the Admin.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserCustom
        fields = ('email', 'password', 'username', 'gender', 'is_active', 'is_admin', 'is_staff', 'is_superuser')

        def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
            return self.initial["password"]

class NewUserAdmin(UserAdmin):
    form        = UpdateUserForm

    #what details about each user will be displayed at Table of CustomUsers
    list_display = ('email', 'username', 'is_admin', 'is_staff', 'date_joined')

    # add a search bar above table of CustomUsers to search for specific user.
    search_fields = ('email', 'username')

    # define data that can't be modified by anyone even Admin
    readonly_fields = ('date_joined', 'last_login')

    # define which data will be displayed at Edit User page
    # fieldsets is tuple of tuples where each tupe consists of 2 data:
    # 1 name of Headline (could be None) like 'Personal Info'.
    # 2 dictionary has key (fields) and tuple of fields that will display under this headline
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser')}),
        ('time', {'fields': ('date_joined', 'last_login')})
    )


    # define which fields that will display when we want to add new User from Admin page
    # so we need to provide all fields that are required.
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2', 'username', 'gender'),
        }),
    )

admin.site.register(UserCustom, NewUserAdmin)

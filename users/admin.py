from django.contrib import admin

from users.models import NewUser, Profile

from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UpdateUserForm(forms.ModelForm):
    """
    Update User Form. Doesn't allow changing password in the Admin.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = NewUser
        fields = ('email', 'password', 'username', 'gender', 'is_active', 'is_admin', 'is_staff', 'is_superuser')

        def clean_password(self):
            return self.initial["password"]

class NewUserAdmin(UserAdmin):
    """
        New Admin dashboard to display new Fields.
    """
    
    form = UpdateUserForm

    list_display = ('email', 'username', 'is_admin', 'is_staff', 'date_joined')

    search_fields = ('email', 'username')

    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser')}),
        ('time', {'fields': ('date_joined', 'last_login')})
    )

    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2', 'username', 'gender'),
        }),
    )

# Register your models here.
admin.site.register(Profile)
admin.site.register(NewUser, NewUserAdmin)

from django.contrib import admin
from django.contrib.auth import get_user_model  # can also do from.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    search_fields = ['email', 'username', 'full_name']
    list_display = ['username', 'email', 'is_active', 'is_staff', 'is_admin', 'last_login', 'timestamp']
    list_filter = ['is_active', 'is_staff',  'is_admin']
    ordering = ['email']
    filter_horizontal = []

    form = UserAdminChangeForm  # for updating user in admin
    add_form = UserAdminCreationForm    # for creating user in admin

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('full_name', 'email')}), # if you have any personal info fields e.g. names, include them as strings in the empty tuple.
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_mto')})
    )
    '''
    add_fieldsets is not a standard ModelAdmin attribute. UserAdmin overides get_fieldsets
    to use this attribute when creating a user. '''
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )


admin.site.register(User, UserAdmin)


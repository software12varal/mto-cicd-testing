# from django.models import SuperAdmin
# from django import forms
from django import forms

from .models import SuperAdmin


class SuperAdminUpdateProfileForm(forms.ModelForm):
    class Meta:
        model = SuperAdmin
        fields = ['full_name', 'contact_number', 'email', 'designation']

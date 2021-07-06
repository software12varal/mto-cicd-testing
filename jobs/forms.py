from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import MTOAdminUser, Jobs, Jobstatus, MicroTask
from django import forms


class MTOAdminSignUpForm(UserCreationForm):
    class Meta:
        model = MTOAdminUser
        fields = ['full_name', 'username', 'email', 'varal_role_id']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False
        user.is_admin = True
        user.set_password(self.cleaned_data['password1'])
        # user.save()
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(MTOAdminSignUpForm, self).__init__(*args, **kwargs)

        self.fields['full_name'].widget.attrs['class'] = 'form-control'
        self.fields['full_name'].widget.attrs['placeholder'] = 'first middle last'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['varal_role_id'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'


class AdminUpdateProfileForm(forms.ModelForm):
    class Meta:
        model = MTOAdminUser
        fields = ['full_name', 'varal_role_id']


class JobsForm(forms.ModelForm):
    class Meta:
        model = MicroTask
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(JobsForm, self).__init__(*args, **kwargs)

        self.fields['microtask_name'].widget.attrs['class'] = 'form-control'
        self.fields['microtask_category'].widget.attrs['class'] = 'form-control'
        self.fields['job_cost'].widget.attrs['class'] = 'form-control'
        self.fields['time_required'].widget.attrs['class'] = 'form-control'
        self.fields['skills'].widget.attrs['class'] = 'form-control'
        self.fields['people_required_for_valid_tc'].widget.attrs['class'] = 'form-control'
        self.fields['job_sample'].widget.attrs['class'] = 'form-control'
        self.fields['job_instructions'].widget.attrs['class'] = 'form-control'
        self.fields['tc_type'].widget.attrs['class'] = 'form-control'
        # self.fields['tc_type'].widget.attrs['type'] = 'select'


class JobForm(ModelForm):  # change_from = MALRequirementForm
    class Meta:
        model = Jobs
        fields = '__all__'



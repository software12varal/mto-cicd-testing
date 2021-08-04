from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.core.validators import RegexValidator
from .models import MTOAdminUser, Jobs, MicroTask
from django import forms

job_categories = MicroTask.objects.all()


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


# updated
class AdminUpdateProfileForm(forms.ModelForm):
    class Meta:
        model = MTOAdminUser
        fields = ['full_name', 'varal_role_id', 'contact_number', 'email', 'designation', 'department']


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
        self.fields['sample'].widget.attrs['class'] = 'form-control'
        self.fields['instructions'].widget.attrs['class'] = 'form-control'
        self.fields['tc_type'].widget.attrs['class'] = 'form-control'
        # self.fields['tc_type'].widget.attrs['type'] = 'select'


class JobForm(ModelForm):
    class Meta:
        model = Jobs
        fields = ['identification_number', 'assembly_line_id', 'assembly_line_name',
                  'person_name', 'output', 'job_name', 'cat_id', 'target_date', 'total_budget',
                  'job_description', 'job_quantity', 'input_folder', 'sample', 'instructions']

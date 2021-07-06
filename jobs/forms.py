from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.core.validators import RegexValidator
from .models import MTOAdminUser, Jobs, Jobstatus, MicroTask
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
        self.fields['sample'].widget.attrs['class'] = 'form-control'
        self.fields['instructions'].widget.attrs['class'] = 'form-control'
        self.fields['tc_type'].widget.attrs['class'] = 'form-control'
        # self.fields['tc_type'].widget.attrs['type'] = 'select'


# class JobForm(ModelForm):  # change_from = MALRequirementForm
#     class Meta:
#         model = Jobs
#         fields = '__all__'

class JobForm(forms.Form):
    Jobstatus = [('cr', 'Created'),
                 ('co', 'Completed'),
                 ('ur', 'Under review'),
                 ('as', 'Assigned')
                 ]
    alphanumeric = RegexValidator(
        r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    sample = forms.FileField()
    instructions = forms.FileField()
    identification_number = forms.CharField(
        max_length=50, validators=[alphanumeric])
    assembly_line_id = forms.CharField(
        max_length=50, validators=[alphanumeric])
    assembly_line_name = forms.CharField()
    person_name = forms.CharField(help_text="Name of the person in charge")
    target_date = forms.DateTimeField(help_text='e.g 2021-10-25 14:30:59')
    # as per predecesor 2 there is no need of person_email
    # person_email = models.EmailField(null=True)
    output = forms.FilePathField(
        path='media/documents/job_documents/output', help_text="Link of the output folder")
    # models.ForeignKey(MicroTask, on_delete=models.CASCADE)
    job_name = forms.CharField(
        max_length=300, help_text='e.g develop website')
    cat_id = forms.ModelChoiceField(job_categories)
    total_budget = forms.IntegerField(help_text="e.g currency AED")
    job_description = forms.CharField(
        max_length=1000, help_text='e.g car website')
    job_quantity = forms.IntegerField(help_text="e.g Quantity of Job")
    input_folder = forms.FilePathField(path='media/documents/job_documents/input',
                                       help_text="Link of the Input folder")
    # job_status = forms.ChoiceField(choices=Jobstatus, required=False)

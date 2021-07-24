from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django_countries.widgets import CountrySelectWidget

from .models import MTO
from jobs.models import Jobs, MicroTask

User = get_user_model()

job_categories = [

    ('cw', 'Content Writing'),
    ('da', 'Document Analysis'),
    ('de', 'Data Entry'),
    ('cr', 'Combining Rules from Semi-Legal documents'),
    ('df', 'Data Entry(Fields)'),
    ('cd', 'Collecting copies of documents'),
    ('cp', 'Content Copy & Paste'),
    ('cf', 'Combining Data Entry Fields'),
    ('fn', 'Find Non-Copyrighted Images and Uploading'),
    ('ac', 'Apply Compliance to Fields'),
    ('ng', 'Naming'),
    ('ce', 'Compliance Extraction'),
    ('id', 'Identifying One Line Decision'),
    ('ab', 'A+B TC For Document Extraction'),
    ('tc', 'TC For One Line Decision'),
]


class SignUpForm(UserCreationForm):

    job_category = forms.MultipleChoiceField(
                                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}),choices=job_categories)

    class Meta(UserCreationForm.Meta):
        model = MTO
        fields = ['username', 'full_name', 'email', 'paypal_id', 'password1',
                  'password2', 'contact_number', 'location', 'job_category']
        widgets = {
            'contact_number': forms.NumberInput(attrs={'placeholder': 'Enter contact number', 'class': 'form-control'}),
            'location': CountrySelectWidget(attrs={'class': 'form-control'}, layout='{widget}'),
        }

    # def save(self, commit=True):
    #     job_categories = self.cleaned_data['job_category']
    #     job_categories_ids = json.dumps([job.id for job in job_categories])
    #
    #     user = super().save(commit=False)
    #     if User.objects.using('varal_job_posting_db').filter(username=user.username).exists():
    #         messages.info(self.request, f"{user.username} exists in varal job posting db")
    #     elif User.objects.using('vendor_os_db').filter(username=user.username).exists():
    #         messages.info(self.request, f"{user.username} exists in vendor os db")
    #     else:
    #         user.is_mto = True
    #         user.is_active = False
    #         user.job_category = job_categories_ids
    #         user.save()
    #         return user
    #hai.save()

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['full_name'].widget.attrs['class'] = 'form-control'
        self.fields['full_name'].widget.attrs['placeholder'] = 'first middle last'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['paypal_id'].widget.attrs['class'] = 'form-control'
        self.fields['paypal_id'].widget.attrs['placeholder'] = 'Enter paypal ID'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
        self.fields['contact_number'].widget.attrs['class'] = 'form-control'
        self.fields['contact_number'].widget.attrs['placeholder'] = 'Contact number'
        self.fields['location'].widget.attrs['class'] = 'form-control'
        self.fields['location'].widget.attrs['placeholder'] = 'Location'
        self.fields['job_category'].widget.attrs['class'] = 'form-control'
        self.fields['job_category'].widget.attrs['placeholder'] = 'Job category'


class MTOUpdateProfileForm(forms.ModelForm):
    job_category = forms.MultipleChoiceField(
                                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}),choices=job_categories)

    class Meta:
        model = MTO
        fields = ['contact_number', 'location', 'paypal_id']
        widgets = {
            'contact_number': forms.NumberInput(attrs={'placeholder': 'Enter contact number', 'class': 'form-control'}),
            'location': CountrySelectWidget(attrs={'class': 'form-control'}, layout='{widget}'
                                            ),
            'paypal_id': forms.TextInput(attrs={'placeholder': 'Enter PayPal ID', 'class': 'form-control'}),
        }


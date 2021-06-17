from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    '''A form for creating new users. Includes all required fields plus
    repeated password'''
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self): # checking that the two passwords match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True): # save he proovided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    ''' A form for updating users, includes all the fields on the user, but
    replaces the password fields with admin's password hash display field. '''

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        ''' Regardless of what the user provides retrun the initial value.
        This is done here rather than on the field, because the field does
        not have access to the initial value. '''
        return self.initial['password']


# class SignUpForm(forms.Form):
#     full_name = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'first middle last'}))
#     email = forms.EmailField(widget=EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
#     paypal_id = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter paypal ID'}))
#     password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
#     password2 = forms.CharField(
#         widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))
#
#     def clean(self):
#         cleaned_data = super().clean()
#         email = cleaned_data['email']
#         password = cleaned_data['password']
#         password2 = cleaned_data['password2']
#         if password != password2:
#             raise forms.ValidationError('Passwords did not match', code='invalid password')
#         if User.objects.using('vendor_os_db').filter(username=email).exists():
#             raise forms.ValidationError('A user with that username already exists', code='invalid username')
#         return
#
#     def save(self):
#         cleaned_data = super().clean()
#         full_name = cleaned_data['full_name']
#         email = cleaned_data['email']
#         paypal_id = cleaned_data['paypal_id']
#         password = cleaned_data['password']
#
#         user = User(email=email, username=email) # let us use email as username meanwhile
#         user.set_password(password)
#         user.save(using='vendor_os_db')
#         MTO.objects.create(full_name=full_name, paypal_id=paypal_id, user=user)
#         return
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Additional_Info
from django_countries.widgets import CountrySelectWidget

class UserSearchForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'first_name', 'last_name', 'email'}

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = {'date_of_birth', 'photo', 'bio', 'country', 'state', 'phone_number', 'city', 'zipcode'}
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'country': CountrySelectWidget(),
        }
        
class AdditionEditForm(forms.ModelForm):
    class Meta:
        model = Additional_Info
        fields = {'age', 'gender', 'medical_history', 'additional_information'}
        
        
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                               widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
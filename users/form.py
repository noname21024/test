from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EmailAddressForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['email']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields= ['image']    
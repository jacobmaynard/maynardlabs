from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from maynardlabs.models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'birth_day','phone_number', 'address')

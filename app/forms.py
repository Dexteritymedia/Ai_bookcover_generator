from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import CustomerPayment, CoverGenerator, Profile

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    #email = forms.EmailField(label="Email",widget=forms.EmailInput(attrs={"class":"form-control"}))
    #password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"class":"form-control"}))
    #password2 = forms.CharField(label="Password confirmation",widget=forms.PasswordInput(attrs={"class":"form-control"}))
    #username = forms.CharField(label="Username",widget=forms.TextInput(attrs={"class":"form-control"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerPaymentForm(forms.ModelForm):
    class Meta:
        model = CustomerPayment
        fields = []

class CoverGeneratorForm(forms.ModelForm):
    prompt = forms.CharField(label="Write a prompt",widget=forms.Textarea(attrs={"class":"form-control", "rows":"5"}))
    class Meta:
        model = CoverGenerator
        fields = ['prompt']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
    


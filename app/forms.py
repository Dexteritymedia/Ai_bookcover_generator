from django import forms
from django.forms.models import modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import CustomerPayment, CoverGenerator, Profile, ImageEditing

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


class ImageManipulationForm(forms.Form):
    FONT_CHOICES = (
        ('Roboto', 'Roboto'),
        ('ZCOOL', 'ZCOOL'),
    )
    font_type = forms.ChoiceField(choices = FONT_CHOICES)
    font_size = forms.IntegerField(label=" Font Size",widget=forms.NumberInput(attrs={"class":"form-control"}))
    color = forms.CharField(label=" Color",widget=forms.TextInput(attrs={"type": "color", "class":"form-control"}))
    text = forms.CharField(label="Text",widget=forms.TextInput(attrs={"class":"form-control"}))
    x_axis = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'step': '5', 'min': '-100', 'max': '100', 'id':'x_axis'}), required=False)
    y_axis = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'step': '5', 'min': '-100', 'max': '100', 'id':'y_axis'}), required=False)

    class Meta:
        fields = ['font_type', 'font_size', 'color', 'text', 'x_axis', 'y_axis']



class ImageEditingForm(forms.ModelForm):
    color = forms.CharField(label="Pick a color",widget=forms.TextInput(attrs={"type":"colr"}))
    class Meta:
        model = ImageEditing
        fields = ['font', 'x', 'y', 'size', 'color', 'name']


ImageEditingFormSet = modelformset_factory(ImageEditing, form=ImageEditingForm, extra=3)
    


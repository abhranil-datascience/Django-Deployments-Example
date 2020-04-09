from django import forms
from django.core import validators
from CustomUserApp.models import CustomUser

class UserRegistrationForm(forms.Form):

    FirstName=forms.CharField(max_length=50,required=True,label="FirstName",validators=[validators.RegexValidator('^[a-zA-Z]+$',message="Invalid First Name")])
    Lastname=forms.CharField(max_length=50,required=True,label="LastName",validators=[validators.RegexValidator('^[a-zA-Z]+$',message="Invalid Last Name")])
    Email=forms.EmailField(max_length=50,required=True,label="EmailID")
    Password=forms.CharField(max_length=50,required=True,widget=forms.PasswordInput,label="Password")
    SEX_CHOICES =(("M", "Male"),("F", "Female"),("O", "Other"),)
    Sex=forms.ChoiceField(choices = SEX_CHOICES,label="Sex",required=True)
    Portfolio=forms.URLField(max_length=50,required=False,label="Portfolio URL")
    ProfilePicture=forms.ImageField(required=False,label="Profile Picture",validators=[validators.FileExtensionValidator(message="Invalid File")])

class UserLoginForm(forms.Form):

    Email=forms.EmailField(max_length=50,required=True,label="EmailID")
    Password=forms.CharField(label='Password',widget=forms.PasswordInput)

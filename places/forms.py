from django import forms
from . import models
from django.forms import ModelForm

class Account(forms.Form):
    name = forms.CharField(label='Your name',max_length=100)
    email = forms.EmailField(label='Your Email', max_length=100)

class Comment(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'style':'resize:none;'}))
        
from django import forms

class Account(forms.Form):
    name = forms.CharField(label='Your name',max_length=100)
    email = forms.EmailField(label='Your Email', max_length=100)


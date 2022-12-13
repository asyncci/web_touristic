from django import forms

class LoginAccountForm(forms.Form):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(max_length=100,widget=forms.PasswordInput())

class RegisterAccountForm(forms.Form):
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    repeat_email = forms.EmailField(max_length=50)
    password = forms.CharField(max_length=100,widget=forms.PasswordInput())
    repeat_password = forms.CharField(max_length=100,widget=forms.PasswordInput())
    
class VerifyToken(forms.Form):
    token = forms.CharField(max_length=4)
    email = forms.EmailField(widget=forms.TextInput(attrs={'type':'text'}))

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'type':'text','style':'resize:none;'}))

class RateForm(forms.Form):
    rate = forms.IntegerField(max_value=5,min_value=1)
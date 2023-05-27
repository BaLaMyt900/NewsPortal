from django.contrib.auth.forms import forms
from allauth.account.forms import SignupForm


class UserRegistraionForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistraionForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={'class': 'form-control mb-3'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-3'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-3'})
        print(self.fields)


class UserLoginForm(forms.Form):  # форма авторизации пользователя
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))

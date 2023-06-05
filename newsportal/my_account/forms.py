from django.contrib.auth.forms import forms
from allauth.account.forms import SignupForm


class UserRegistraionForm(SignupForm):
    """ Форма регистрации Своего класса пользователя PortalUser """
    def __init__(self, *args, **kwargs):
        super(UserRegistraionForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control mb-3'})
        self.fields['username'].label = 'Логин'
        self.fields['email'].widget = forms.TextInput(attrs={'class': 'form-control mb-3'})
        self.fields['email'].label = 'Адрес электронной почты'
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-3'})
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-3'})
        self.fields['password2'].label = 'Потверждение пароля'

class UserLoginForm(forms.Form):
    """ форма авторизации пользователя """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))

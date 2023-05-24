from django.contrib.auth.forms import forms
from portal.models import PortalUser


class UserRegistrationForm(forms.ModelForm):  # Форма регистрации пользователя
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))

    class Meta:
        model = PortalUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'email': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': "Вводить необязательно"}),
            'first_name': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': "Вводить необязательно"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': "Вводить необязательно"})
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']


class UserLoginForm(forms.Form):  # форма авторизации пользователя
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))

from django.contrib.auth.forms import forms
from django.forms import ModelForm
from portal.models import PortalUser, Category, Post


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))

    class Meta:
        model = PortalUser
        fields = ('username', 'email', 'password', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'email': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': "Вводить Email необязательно"})
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))


class PostForm(ModelForm):
    title = forms.CharField()
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    __types = [('A', 'Статья'), ('N', 'Новость')]
    type = forms.ChoiceField(choices=__types)
    text = forms.CharField()

    class Meta:
        model = Post
        fields = ('title', 'categories', 'type', 'text')

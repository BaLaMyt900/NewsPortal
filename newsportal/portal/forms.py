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


types = [
        ('A', 'Статья'),
        ('N', 'Новость')
    ]


class PostForm(ModelForm):
    title = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    categories = forms.ModelMultipleChoiceField(label='Категория', queryset=Category.objects.all(),
                                                widget=forms.SelectMultiple(attrs={'class': 'form-switch',
                                                                                   'role': 'switch', 'type': 'checkbox'}))
    types = [('A', 'Статья'), ('N', 'Новость')]
    type = forms.ChoiceField(label='Тип поста', choices=types, widget=forms.Select(attrs={'class': 'form-control'}))
    text = forms.CharField(label='Текст поста', widget=forms.Textarea(attrs={'class': 'form-control mb-3'}))

    class Meta:
        model = Post
        fields = ('title', 'categories', 'type', 'text')



# class PostForm(forms.Form):
#     title = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
#     category = [(_.pk, _.name) for _ in Category.objects.all()]
#     categories = forms.ModelMultipleChoiceField(label='Категория', queryset=Category.objects.all(),
#                                                 widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
#     types = [
#         ('A', 'Статья'),
#         ('N', 'Новость')
#     ]
#     type = forms.ChoiceField(label='Тип поста', choices=types, widget=forms.Select(attrs={'class': 'form-control'}))
#     text = forms.CharField(label='Текст поста', widget=forms.Textarea(attrs={'class': 'form-control mb-3'}))
#     class Meta:
#         model = Post
#         fields = ('title', 'categories', 'type', 'text')

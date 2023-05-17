from django.contrib.auth.forms import forms


class PostForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    category = [(_.name, _.name) for _ in Category.objects.all()]
    categories = forms.MultipleChoiceField(choices=category)
    types = [
        ('A', 'Статья'),
        ('N', 'Новость')
    ]
    type = forms.ChoiceField(choices=types)

    class Meta:
        model = Post
        fields = ('title', 'text', 'categories', 'type')
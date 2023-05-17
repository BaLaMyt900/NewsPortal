from django.shortcuts import render, redirect
from portal.models import Author, Post, Comment, PortalUser
from django.views import View
from django.views.generic import ListView


"""    Авторы   """


class AuthorsView(ListView):  # Страница вывода всех авторов
    model = Author
    template_name = 'authors.html'
    paginate_by = 10

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '-rating')
        return ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'authors'
        return context


"""  Стартовая страница  """


class IndexView(ListView):  # Начальная страница. Ограничение 8 постов
    model = Post
    paginate_by = 8
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'home'
        return context




def comment_submit(request):  # функция создания комментария
    Comment.objects.create(post=Post.objects.get(id=request.POST.get('id')), user=request.user,
                           text=request.POST.get('text'))
    return redirect(request.META.get('HTTP_REFERER', '/'))

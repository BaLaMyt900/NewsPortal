from django.shortcuts import render, redirect
from portal.models import Author, Post, Comment, PortalUser
from django.views import View
from django.views.generic import ListView, DetailView

"""    Авторы   """


class AuthorsView(View):  # класс отображения списка авторов
    def get(self, request):
        authors = Author.objects.all().order_by('user')
        ordering_type = 'user'
        posts_count = [(author, len(Post.objects.filter(author=author))) for author in authors]
        return render(request, 'authors.html', {'page': 'authors', 'authors': authors,
                                                    'ordering_type': ordering_type, 'posts_count': posts_count})

    def post(self, request):
        order_type = request.POST.get('order_by')
        authors = Author.objects.all().order_by(order_type)
        posts_count = [(author, len(Post.objects.filter(author=author))) for author in authors]
        return render(request, 'authors.html', {'page': 'authors', 'authors': authors,
                                                    'ordering_type': order_type, 'posts_count': posts_count})



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

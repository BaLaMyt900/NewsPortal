from django.shortcuts import render, redirect
from portal.models import Author, Post, Comment
from django.views import View
from django.views.generic import ListView



class AuthorsView(View):
    """ класс отображения списка авторов """
    def get(self, request):
        authors = Author.objects.all().order_by('user')
        ordering_type = 'user'
        return render(request, 'authors.html', {'page': 'authors', 'authors': authors, 'ordering_type': ordering_type})

    def post(self, request):
        order_type = request.POST.get('order_by')
        authors = Author.objects.all().order_by(order_type)
        return render(request, 'authors.html', {'page': 'authors', 'authors': authors, 'ordering_type': order_type})


class IndexView(ListView):
    """ Начальная страница. Ограничение 8 постов """
    model = Post
    paginate_by = 8
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'home'
        return context


def handler404(request, *args, **argv):
    return render(request, '404.html')

def comment_submit(request):
    """ функция создания комментария """
    Comment.objects.create(post=Post.objects.get(id=request.POST.get('id')), user=request.user,
                           text=request.POST.get('text'))
    return redirect(request.META.get('HTTP_REFERER', '/'))

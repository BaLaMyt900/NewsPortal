from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from portal.models import Author, Post, PostCategory, Comment, PortalUser, PostActivity, CommentActivity, Category
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from portal.forms import UserRegistrationForm, LoginForm, PostForm
from django.contrib.auth import authenticate, login, get_user
from .filters import PostFilter


class PostView(View):  # класс отображения одиночного поста
    def get(self, request):
        try:
            post = Post.objects.get(id=request.GET.get('id'))
        except Post.DoesNotExist:
            return render(request, '404.html')
        except ValueError:
            return render(request, '404.html')
        else:
            comments = Comment.objects.filter(post=post.id)
            try:
                post_activity = PostActivity.objects.get(user=request.user, activity=post)
            except PostActivity.DoesNotExist:
                post_activity = None
            except TypeError:
                post_activity = None
            try:
                comment_activity = [item.activity.id for item in CommentActivity.objects.filter(user=request.user)]
            except CommentActivity.DoesNotExist:
                comment_activity = None
            except TypeError:
                comment_activity = None
            try:
                post.category = PostCategory.objects.filter(post_id=post.id).values('category_id__name')
            except PostCategory.DoesNotExist:
                post.category = None
            return render(request, 'posts/post.html', {'post': post, 'comments': comments,
                                                       'comment_activity': comment_activity,
                                                       'post_activity': post_activity})

    def post(self, request):
        if request.POST.get('post'):
            if request.POST.get('post') == '+':
                post = Post.objects.get(id=int(request.POST.get('id')))
                post.like(request.user)
                PortalUser.objects.get(id=post.author.user.id).update_rating()
            elif request.POST.get('post') == '-':
                post = Post.objects.get(id=int(request.POST.get('id')))
                post.dislike(request.user)
                PortalUser.objects.get(id=post.author.user.id).update_rating()
        elif request.POST.get('comment'):
            if request.POST.get('comment') == '+':
                Comment.objects.get(id=request.POST.get('id')).like(request.user)
                Post.objects.get(id=request.POST.get('post_id')).author.user.update_rating()
            elif request.POST.get('comment') == '-':
                Comment.objects.get(id=request.POST.get('id')).dislike(request.user)
                Post.objects.get(id=request.POST.get('post_id')).author.user.update_rating()
        return redirect(request.META.get('HTTP_REFERER', '/'))


class LK(View):  # класс отображения личного кабинета
    def get(self, request, error=None):
        try:
            user = PortalUser.objects.get(id=request.GET.get('id'))
        except PortalUser.DoesNotExist:
            return render(request, '404.html')
        except ValueError:
            return render(request, '404.html')
        else:
            owner = True if request.user == user.username else False
            raw_comments = Comment.objects.filter(user=user)
            if raw_comments:
                comments = []
                for comment in raw_comments:
                    comments.append({
                        'post': comment.post.title,
                        'text': comment.text[:50] + '...' if len(comment.text) > 47 else comment.text,
                        'rating': comment.rating,
                        'date': comment.date,
                        'post_id': comment.post.id
                    })
            else:
                comments = False
            if Author.objects.filter(user=user).exists():
                author = Author.objects.get(user=user)
                posts = Post.objects.filter(author=author).order_by('-rating')
                if posts:
                    for post in posts:
                        if len(post.title) > 40:
                            post.title = post.title[:37] + '...'
                        if len(post.text) > 60:
                            post.text = post.text[:57   ] + '...'
                return render(request, 'account/account.html', {'user': user, 'owner': owner,
                                                                'comments': comments, 'posts': posts, 'author': author})
            if error:
                return render(request, 'account/account.html', {'user': user, 'owner': owner, 'comments': comments, 'error': 'password'})
            return render(request, 'account/account.html', {'user': user, 'owner': owner, 'comments': comments})

    def post(self, request):
        if request.POST.get('author'):
            Author.objects.create(user=PortalUser.objects.get(username=request.user))
        elif request.POST.get('delete_post'):
            Post.objects.get(pk=request.POST.get('delete_post')).delete()
        elif request.POST.get('change_acc'):
            user = get_user(request)
            if user.check_password(request.POST.get('password')):
                user.username = request.POST.get('username')
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.email = request.POST.get('email')
                user.save()
                return self.get(request)
            else:
                return self.get(request, 'error')
        elif request.POST.get('delete_acc'):
            PortalUser.objects.get(username=request.user).delete()
            return redirect('/exit/')
        return redirect(request.META.get('HTTP_REFERER', '/'))


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


class PostsView(ListView):
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    ordering = ['-post_time']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'posts'
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/new_post.html'
    fields = ['title', 'text', 'type', 'categories']
    success_url = reverse_lazy('post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Author.objects.get(user=self.request.user)
        post.save()
        form.save_m2m()
        return redirect(f'/post/?id={post.id}')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.values_list('id', 'name')
        return context


class PostSearch(ListView):
        model = Post
        template_name = 'posts/post_search.html'
        context_object_name = 'posts'
        ordering = ['-post_time']

        def __toint(self, value):
            try:
                value = int(value)
            except TypeError:
                return None
            else:
                return value

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
            context['page'] = 'search'
            context['authors'] = Author.objects.values('user__username', 'id')
            context['categories'] = Category.objects.values('name', 'id')
            context['curr_author'] = self.__toint(self.request.GET.get('author'))
            context['curr_type'] = self.request.GET.get('type')
            context['curr_categories'] = list(map(int, self.request.GET.getlist('categories')))
            return context



def post_edit(request):  # функция редактирования поста
    if request.method == 'POST' and request.user.is_authenticated:
        post_form = PostForm(request.POST)
        post_id = request.POST.get('post_id')
        forms_category = [_.category_id for _ in PostCategory.objects.filter(post_id=post_id)]
        if post_form.is_valid():
            post_new = post_form.save(commit=False)
            post = Post.objects.get(id=post_id)
            post.edit(post_new)
            for cat in PostCategory.objects.filter(post_id=post_id):
                cat.delete()
            for cat in request.POST.getlist('categories'):
                PostCategory.objects.create(post_id=post_id, category_id=int(cat))
            return redirect(f'/post/?id={post.id}')
    else:
        post_form = PostForm()
    category = [(_.id, _.name) for _ in Category.objects.all()]
    return render(request, 'posts/post_edit.html', {'form': post_form, 'categories': category,
                                                   'edit': True if request.POST.get('edit_post') else False,
                                                   'post_cat': forms_category if forms_category else None})


def indexview(request):  # функция отображения стартовой старницы
    posts = Post.objects.all()[:8]
    if posts:
        for post in posts:
            post.text = post.preview()
    data = {
        'page': 'home',
        'posts': posts
    }
    return render(request, 'index.html', {'data': data})


def register(request):  # функция регистрации клиента
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            if new_user is not None:
                if new_user.is_active:
                    login(request, new_user)
                    return redirect('/')
                else:
                    return render(request, 'account/account_blocked.html')
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'register_form': user_form})


def user_login(request):  # функция логирования клиента
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    return render(request, 'account/account_blocked.html')
            else:
                return render(request, 'account/login.html', {'form': form, 'error': 1})
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def comment_submit(request):  # функция создания комментария
    Comment.objects.create(post=Post.objects.get(id=request.POST.get('id')), user=request.user,
                           text=request.POST.get('text'))
    return redirect(request.META.get('HTTP_REFERER', '/'))

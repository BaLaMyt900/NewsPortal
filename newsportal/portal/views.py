from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from portal.models import Author, Post, PostCategory, Comment, PortalUser, PostActivity, CommentActivity, Category
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from portal.forms import UserRegistrationForm, UserLoginForm, PostForm
from django.contrib.auth import authenticate, login
from .filters import PostFilter


"""      ПОСТЫ      """


class PostView(DetailView):
    model = Post
    template_name = 'posts/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object.pk).values('user__username', 'text', 'date', 'rating')
        try:
            context['comment_activity'] = \
                [_['activity_id'] for _ in
                 CommentActivity.objects.filter(user_id=self.request.user.id).values('activity_id')]
        except CommentActivity.DoesNotExist:
            pass
        try:
            context['post_activity'] = PostActivity.objects.get(user_id=self.request.user, activity_id=self.object.id)
        except PostActivity.DoesNotExist:
            pass
        try:
            self.object.category = PostCategory.objects.filter(post_id=self.object.id).values('category_id__name')
        except PostCategory.DoesNotExist:
            pass
        return context

    def post(self, request, pk):
        if request.POST.get('post'):
            if request.POST.get('post') == '+':
                post = Post.objects.get(id=pk)
                post.like(request.user)
                PortalUser.objects.get(id=post.author.user.id).update_rating()
            elif request.POST.get('post') == '-':
                post = Post.objects.get(id=pk)
                post.dislike(request.user)
                PortalUser.objects.get(id=post.author.user.id).update_rating()
        elif request.POST.get('comment'):
            if request.POST.get('comment') == '+':
                Comment.objects.get(id=pk.like(request.user))
                Post.objects.get(id=pk).author.user.update_rating()
            elif request.POST.get('comment') == '-':
                Comment.objects.get(id=pk).dislike(request.user)
                Post.objects.get(id=pk).author.user.update_rating()
        return redirect(request.META.get('HTTP_REFERER', '/'))


class PostsView(ListView):  # Страница показа всех постов с пагинацией
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    ordering = ['-post_time']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'posts'
        return context


class PostCreate(LoginRequiredMixin, CreateView):  # Страница создания поста
    model = Post
    template_name = 'posts/new_post.html'
    fields = ['title', 'text', 'type', 'categories']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Author.objects.get(user=self.request.user)
        post.save()
        form.save_m2m()
        return redirect(f'/post/{post.id}')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.values_list('id', 'name')
        return context


class PostEdit(UpdateView):  # Страница редактирования поста
    model = Post
    template_name = 'posts/post_edit.html'
    fields = ['title', 'type', 'categories', 'text']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.values_list('id', 'name')
        context['curr_categories'] = \
            [_["category_id"] for _ in PostCategory.objects.filter(post_id=self.object.id).values('category_id')]
        return context

    def form_valid(self, form):
        post = form.save()
        return redirect(f'/post/{post.id}')


class PostSearch(ListView):  #  Страница поиска поста
    model = Post
    template_name = 'posts/post_search.html'
    ordering = ['-post_time']
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['page'] = 'search'
        context['authors'] = Author.objects.values('user__username', 'id')
        context['categories'] = Category.objects.values('name', 'id')
        context['curr_author'] = self.request.GET.get('author__user__username')
        context['curr_type'] = self.request.GET.get('type')
        context['curr_categories'] = list(map(int, self.request.GET.getlist('categories')))
        context['curr_date'] = self.request.GET.get('post_time__date__lte')
        return context


"""  Личный кабинет   """


class AccountView(DetailView):  # Страница отображения личного кабинета
    model = PortalUser
    template_name = 'account/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['comments'] = Comment.objects.filter(user=self.object)
        except Comment.DoesNotExist:
            pass
        else:
            for comment in context['comments']:
                comment.text = comment.text[:47] + '...' if len(comment.text) > 50 else comment.text
        if Author.objects.filter(user=self.object).exists():
            context['author'] = True
            posts = Post.objects.filter(author__user=self.object).order_by('-rating')
            for post in posts:
                post.text = post.text[:47] + '...' if len(post.text) > 50 else post.text
            context['posts'] = posts
        return context

    def post(self, request, pk):
        self.object = PortalUser.objects.get(pk=pk)
        if request.POST.get('author'):
            Author.objects.create(user=self.object)
        elif request.POST.get('delete_post'):
            post = Post.objects.get(pk=request.POST.get('delete_post'))
            post.delete()
            self.object.update_rating()
        elif request.POST.get('change_acc'):
            if self.object.check_password(request.POST.get('password')):
                self.object.username = request.POST.get('username')
                self.object.first_name = request.POST.get('first_name')
                self.object.last_name = request.POST.get('last_name')
                self.object.email = request.POST.get('email')
                self.object.save()
                return self.get(request)
        elif request.POST.get('delete_acc'):
            self.object.delete()
            return redirect('/exit/')
        return redirect(request.META.get('HTTP_REFERER', '/'))


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


"""   Регистрация и логин   """


class UserRegisterView(FormView):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        if new_user is not None:
            if new_user.is_active:
                login(self.request, new_user)
                return redirect('/')
            else:
                return render(self.request, 'account/account_blocked.html')


class UserLoginView(FormView):  #Страница логирования клиента. Перейдет если в модальном окне произошла ошибка
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password'])
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect(self.request.META.get('HTTP_REFERER', '/'))
            else:
                return render(self.request, 'account/account_blocked.html')
        else:
            return render(self.request, 'account/login.html', {'form': form, 'error': 1})



def comment_submit(request):  # функция создания комментария
    Comment.objects.create(post=Post.objects.get(id=request.POST.get('id')), user=request.user,
                           text=request.POST.get('text'))
    return redirect(request.META.get('HTTP_REFERER', '/'))

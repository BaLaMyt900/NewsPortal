import asyncio
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from portal.models import Author, Post, Comment, Category, CommentActivity, PostActivity, PostCategory, \
    Subscribers
from posts.filters import PostFilter


"""      ПОСТЫ      """


class PostView(DetailView):
    model = Post
    template_name = 'posts/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object.pk).values('id', 'user__id', 'user__username',
                                                                                 'text', 'date', 'rating')
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
        except TypeError:
            pass
        try:
            self.object.category = PostCategory.objects.filter(post_id=self.object.id).values('category_id__name',
                                                                                              'category_id')
        except PostCategory.DoesNotExist:
            pass
        try:
            user_subs = Subscribers.objects.filter(user=self.request.user).values('category__id')
            self.object.user_subs = [_['category__id'] for _ in user_subs]
        except Subscribers.DoesNotExist:
            pass
        except TypeError:
            pass
        return context


class PostsView(ListView):  # Страница показа всех постов с пагинацией
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'posts'
        return context


@sync_to_async
def mass_mail_send(post):
    """  Рассылка!  """
    list_subs = []  # сборка Емаил адресов подписчиков, если он указан в ЛК
    categories = [_['category__id'] for _ in PostCategory.objects.filter(post=post).values('category__id')]
    categories = Category.objects.filter(id__in=categories)
    for subs in Subscribers.objects.filter(category__in=categories):
        if subs.user.username == post.author.user.username:
            continue  # Пропуск, если пользователь = автор статьи
        if subs.user.email:  # создается отправление если у пользователя введен емаил
            list_subs.append((subs.user.email, subs.user.username, subs.category.name))
    for email, username, cat in list_subs:
        context = {
            'user': username,
            'post': post,
            'cat': cat
        }
        message = EmailMessage(
            f'Вышла новая {"Статья" if post.type == "A" else "Новость"} в Вашей выбранной категории!',
            render_to_string('posts/email/new_post_email.html', context=context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]
        )
        message.content_subtype = 'html'
        message.send()


class PostCreate(PermissionRequiredMixin, CreateView):  # Страница создания поста
    permission_required = ('portal.add_post',)
    model = Post
    template_name = 'posts/new_post.html'
    fields = ['title', 'text', 'type', 'categories']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Author.objects.get(user=self.request.user)
        post.save()
        form.save_m2m()
        post.author.new_post()
        asyncio.run(mass_mail_send(post))
        return redirect(f'/post/{post.id}')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.values_list('id', 'name')
        context['is_valid'] = Author.objects.get(user=self.request.user).numbers_of_posts != 0
        return context


class PostEdit(PermissionRequiredMixin, UpdateView):  # Страница редактирования поста
    permission_required = ('portal.change_post',)
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


class PostSearch(ListView):  # Страница поиска поста
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

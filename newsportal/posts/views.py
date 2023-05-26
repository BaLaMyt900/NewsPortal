from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mass_mail
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from portal.models import Author, Post, Comment, PortalUser, Category, CommentActivity, PostActivity, PostCategory, \
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
                Comment.objects.get(id=request.POST.get('id')).like(request.user)
                Post.objects.get(id=pk).author.user.update_rating()
            elif request.POST.get('comment') == '-':
                Comment.objects.get(id=request.POST.get('id')).dislike(request.user)
                Post.objects.get(id=pk).author.user.update_rating()
        # elif request.POST.get('subs_category'):
        #     Subscribers.objects.create(user=request.user,
        #                                category=Category.objects.get(id=request.POST.get('subs_category')))
        # elif request.POST.get('unsubs_category'):
        #     Subscribers.objects.get(user=request.user,
        #                             category=Category.objects.get(id=request.POST.get('unsubs_category'))).delete()
        return redirect(request.META.get('HTTP_REFERER', '/'))

def subscribe(request):
    print(request)


class PostsView(ListView):  # Страница показа всех постов с пагинацией
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'posts'
        return context


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
        """  Рассылка!  """
        list_subs = []  # сборка Емаил адресов подписчиков, если он указан в ЛК
        categories = [_['category__id'] for _ in PostCategory.objects.filter(post=post).values('category__id')]
        categories = Category.objects.filter(id__in=categories)
        for subs in Subscribers.objects.filter(category__in=categories):
            if subs.user.username == post.author.user.username:
                continue  # Пропуск, если пользователь = автор статьи
            if subs.user.email:
                send = ((  # создается отправление если у пользователя введен емаил
                    f'Здравствуй, {subs.user.username}. Новая статья в твоём любимом разделе!',
                    post.mail_preview(),
                    None,   # Чтобы отправщик взял Default значение из settings
                    [subs.user.email],
                ))
                if send not in list_subs:  # Проверка, чтобы не было повторений
                    list_subs.append(send)
        send_mass_mail(list_subs, fail_silently=True)
        return redirect(f'/post/{post.id}')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.values_list('id', 'name')
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

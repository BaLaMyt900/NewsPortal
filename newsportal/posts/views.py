from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from portal.models import Author, Post, Comment, PortalUser, Category, CommentActivity, PostActivity, PostCategory
from posts.filters import PostFilter


"""      ПОСТЫ      """


class PostView(DetailView):
    model = Post
    template_name = 'posts/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object.pk).values('id', 'user__id', 'user__username', 'text', 'date', 'rating')
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
                Comment.objects.get(id=request.POST.get('id')).like(request.user)
                Post.objects.get(id=pk).author.user.update_rating()
            elif request.POST.get('comment') == '-':
                Comment.objects.get(id=request.POST.get('id')).dislike(request.user)
                Post.objects.get(id=pk).author.user.update_rating()
        return redirect(request.META.get('HTTP_REFERER', '/'))


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
    permission_required = ('portal.add_post', )
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


class PostEdit(PermissionRequiredMixin, UpdateView):  # Страница редактирования поста
    permission_required = ('portal.change_post', )
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

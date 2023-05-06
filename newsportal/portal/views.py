import django.utils.timezone
from django.shortcuts import render, redirect
from portal.models import Author, Post, PostCategory, Comment, PortalUser, PostActivity, CommentActivity, Category
from django.views import View
from portal.forms import UserRegistrationForm, LoginForm, PostForm
from django.contrib.auth import authenticate, login


class PostView(View):
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
                post.category = [__.name for __ in Category.objects.filter(id__in=
                                                [_.category_id for _ in PostCategory.objects.filter(post_id=post.id)])]
                post.category = ', '.join(post.category)
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
                Author.objects.get(user=post.author.user).update_rating()
            elif request.POST.get('post') == '-':
                post = Post.objects.get(id=int(request.POST.get('id')))
                post.dislike(request.user)
                Author.objects.get(user=post.author.user).update_rating()
        elif request.POST.get('comment'):
            if request.POST.get('comment') == '+':
                Comment.objects.get(id=request.POST.get('id')).like(request.user)
                Post.objects.get(id=request.POST.get('post_id')).author.update_rating()
            elif request.POST.get('comment') == '-':
                Comment.objects.get(id=request.POST.get('id')).dislike(request.user)
                Post.objects.get(id=request.POST.get('post_id')).author.update_rating()
        return redirect(request.META.get('HTTP_REFERER', '/'))


class LK(View):
    def get(self, request):
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
                        'text': comment.text[:50],
                        'rating': comment.rating,
                        'date': comment.date,
                        'post_id': comment.post.id
                    })
            else:
                comments = False
            if Author.objects.filter(user=user).exists():
                posts = Post.objects.filter(author=Author.objects.get(user=user))
                return render(request, 'account/account.html', {'user': user, 'owner': owner,
                                                                'comments': comments, 'posts': posts, 'author': True})
            return render(request, 'account/account.html', {'user': user, 'owner': owner, 'comments': comments})

    def post(self, request):
        if request.POST.get('author') == '+':
            Author.objects.create(user=PortalUser.objects.get(username=request.user))
        elif request.POST.get('delete_post'):
            Post.objects.get(pk=request.POST.get('delete_post')).delete()
        return redirect(request.META.get('HTTP_REFERER', '/'))


class AuthorsView(View):
    def get(self, request):
        authors = Author.objects.all().order_by('user')
        ordering_type = 'user'
        return render(request, 'authors.html', {'page': 'authors', 'authors': authors,
                                                    'ordering_type': ordering_type})

    def post(self, request):
        order_type = request.POST.get('order_by')
        authors = Author.objects.all().order_by(order_type)
        return render(request, 'authors.html', {'page': 'authors', 'authors': authors,
                                                    'ordering_type': order_type})


# class AuthorView(View):
#     def get(self, request):
#         data = {
#             'page': 'authors'
#         }
#         return render(request, 'authors.html', {'data': data})


class PostsView(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-post_time')
        ordering_type = '-post_time'
        return render(request, 'posts/posts.html', {'page': 'posts', 'posts': posts,
                                                    'ordering_type': ordering_type})

    def post(self, request):
        order_type = request.POST.get('order_by')
        posts = Post.objects.all().order_by(order_type)
        return render(request, 'posts/posts.html', {'page': 'posts', 'posts': posts,
                                                    'ordering_type': order_type})


def post_create(request):
    if request.method == 'POST' and request.user.is_authenticated:
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = Author.objects.get(user=request.user)
            post.save()
            post_form.save_m2m()
            return redirect(f'/post/?id={post.id}')
    else:
        post_form = PostForm()
    return render(request, 'posts/new_post.html', {'form': post_form})


def indexview(request):
    posts = Post.objects.all()[:8]
    data = {
        'page': 'home',
        'posts': posts
    }
    return render(request, 'index.html', {'data': data})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'register_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return render(request, 'account/account_blocked.html')
            else:
                return render(request, 'account/login.html', {'form': form, 'error': 1})

    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def comment_submit(request):
    Comment.objects.create(post=Post.objects.get(id=request.POST.get('id')), user=request.user,
                           text=request.POST.get('text'))
    return redirect(request.META.get('HTTP_REFERER', '/'))

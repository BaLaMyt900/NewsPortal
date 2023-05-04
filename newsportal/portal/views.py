from django.shortcuts import render, redirect
from portal.models import Author, Post, PostCategory, Comment
from django.views import View
from django.contrib.auth.models import User
from newsportal.forms import UserRegistrationForm, LoginForm
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
            user = request.user
            return render(request, 'post.html', {'post': post, 'comments': comments, 'user': user})

    def post(self, request):
        if request.POST.get('post'):
            if request.POST.get('post') == '+':
                post = Post.objects.get(id=int(request.POST.get('id')))
                post.like()
                Author.objects.get(id=post.author.id).update_rating()
            elif request.POST.get('post') == '-':
                post = Post.objects.get(id=int(request.POST.get('id')))
                post.dislike()
                Author.objects.get(id=post.author.id).update_rating()
        elif request.POST.get('comment'):
            if request.POST.get('comment') == '+':
                Comment.objects.get(id=request.POST.get('id')).like()
                Post.objects.get(id=request.POST.get('post_id')).author.update_rating()
            elif request.POST.get('comment') == '-':
                Comment.objects.get(id=request.POST.get('id')).dislike()
                Post.objects.get(id=request.POST.get('post_id')).author.update_rating()
        return redirect(request.META.get('HTTP_REFERER', '/'))


class AuthorView(View):
    def get(self, request):
        data = {
            'page': 'authors'
        }
        return render(request, 'authors.html', {'data': data})


class PostsView(View):
    def get(self, request):
        data = {
            'page': 'posts'
        }
        return render(request, 'posts.html', {'data': data})


def indexview(request):
    raw_posts = Post.objects.all()[:8]
    if raw_posts:
        posts = []
        for post in raw_posts:
            posts.append({
                'author': post.author,
                'text': post.preview(),
                'rating': post.rating,
                'category': PostCategory.objects.get(post=post.id).category,
                'title': post.title,
                'id': post.id
            })
        data = {
            'page': 'home',
            'posts': posts
        }
    else:
        data = {
            'page': 'home'
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
                    return redirect('index.html')
                else:
                    return render(request, 'account/account_blocked.html')

    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def comment_submit(request):
    Comment.objects.create(post=Post.objects.get(id=request.POST.get('id')), user=request.user,
                           text=request.POST.get('text'))
    return redirect(request.META.get('HTTP_REFERER', '/'))

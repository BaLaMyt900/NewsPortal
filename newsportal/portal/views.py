from django.shortcuts import render, redirect
from portal.models import Author, Post, PostCategory, Comment
from django.views import View
from django.contrib.auth.models import User


class IndexView(View):
    def get(self, request):
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
            return render(request, 'post.html', {'post': post, 'comments': comments})

    def post(self, request):
        if request.POST.get('Like'):
            post = Post.objects.get(id=int(request.POST.get('id')))
            post.like()
            Author.objects.get(id=post.author.id).update_rating()
        elif request.POST.get('Dislike'):
            post = Post.objects.get(id=int(request.POST.get('id')))
            post.dislike()
            Author.objects.get(id=post.author.id).update_rating()
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


def comment_submit(request):
    Comment.objects.create(post=Post.objects.get(id=request.POST.get('id')), user=User.objects.get(username='Аноним'),
                           text=request.POST.get('text'))
    return redirect(request.META.get('HTTP_REFERER', '/'))
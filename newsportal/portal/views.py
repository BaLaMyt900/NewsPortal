from django.shortcuts import render
from portal.models import Author, Post, PostCategory, Comment
from django.views import View


def index(request):
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
    print(data)
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
            return render(request, 'post.html', {'post': post})

def authors(request):
    data = {
        'page': 'authors'
    }
    return render(request, 'authors.html', {'data': data})

def posts(request):
    data = {
        'page': 'posts'
    }
    return render(request, 'posts.html', {'data': data})
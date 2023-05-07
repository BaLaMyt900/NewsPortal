from django.contrib import admin
from django.urls import path
from portal.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', indexview),
    path('authors/', AuthorsView.as_view()),
    path('posts/', PostsView.as_view()),
    path('post/', PostView.as_view()),
    path('post/new_post', post_create),
    path('ihjoudhgpreuahodfnbjofg/', comment_submit, name='comment_submit'),
    path('account/register/', register),
    path('account/login/', user_login),
    path('account/', LK.as_view()),
    path('exit/', LogoutView.as_view(next_page='/'), name='exit')
]

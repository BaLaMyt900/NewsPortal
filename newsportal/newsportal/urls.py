import os
from django.contrib import admin
from django.urls import path
from portal.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('authors/', AuthorView.as_view()),
    path('posts/', PostsView.as_view()),
    path('post/', PostView.as_view()),
    path('ihjoudhgpreuahodfnbjofg/', comment_submit, name='comment_submit')
]

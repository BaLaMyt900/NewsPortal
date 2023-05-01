import os
from django.contrib import admin
from django.urls import path
from portal.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('authors/', authors),
    path('posts/', posts),
    path('post/', PostView.as_view())
]

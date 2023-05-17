from django.contrib import admin
from django.urls import path
from portal.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('authors/', AuthorsView.as_view()),
    path('posts/', PostsView.as_view()),
    path('post/<int:pk>', PostView.as_view(), name='post'),
    path('post/new_post', PostCreate.as_view()),
    path('ihjoudhgpreuahodfnbjofg/', comment_submit, name='comment_submit'),
    path('account/register/', UserRegisterView.as_view()),
    path('account/login/', UserLoginView.as_view()),
    path('account/<int:pk>', AccountView.as_view()),
    path('exit/', LogoutView.as_view(next_page='/'), name='exit'),
    path('post/post_edit/<int:pk>', PostEdit.as_view()),
    path('post/search', PostSearch.as_view())
]

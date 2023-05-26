from django.urls import path
from posts.views import *

urlpatterns = [
    path('<int:pk>', PostView.as_view()),
    path('list', PostsView.as_view()),
    path('new_post', PostCreate.as_view()),
    path('post_edit/<int:pk>', PostEdit.as_view()),
    path('search', PostSearch.as_view()),
    path('subs/subscribe/<int:pk>', subscribe)
]

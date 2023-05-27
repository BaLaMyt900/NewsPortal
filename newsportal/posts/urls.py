from django.urls import path
from posts.views import PostView, PostsView, PostCreate, PostEdit, PostSearch
from posts.ajax import subscribe, unsubscribe, postlike, postdislike, commlike, commdislike

urlpatterns = [
    path('<int:pk>', PostView.as_view()),
    path('list', PostsView.as_view()),
    path('new_post', PostCreate.as_view()),
    path('post_edit/<int:pk>', PostEdit.as_view()),
    path('search', PostSearch.as_view()),
    path('subs/subscribe/<int:pk>', subscribe),
    path('subs/unsubscribe/<int:pk>', unsubscribe),
    path('like/<int:pk>', postlike),
    path('dislike/<int:pk>', postdislike),
    path('comm/like/<int:pk>', commlike),
    path('comm/dislike/<int:pk>', commdislike)
]

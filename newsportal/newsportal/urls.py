from django.contrib import admin
from django.urls import path, include
from portal.views import IndexView, AuthorsView, comment_submit
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('account/', include("account.urls")),
    path('post/', include("posts.urls")),
    path('authors/', AuthorsView.as_view()),
    path('ihjoudhgpreuahodfnbjofg/', comment_submit, name='comment_submit'),
    path('exit/', LogoutView.as_view(next_page='/'), name='exit'),

]

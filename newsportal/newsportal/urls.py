from django.contrib import admin
from django.urls import path, include
from portal.views import IndexView, AuthorsView, comment_submit

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),  # КЭШ НЕ ДОБАВЛЕН! Так как перестает корректно работать авторизация
    path('account/', include('my_account.urls')),
    path('accounts/', include("allauth.urls")),
    path('post/', include("posts.urls")),
    path('authors/', AuthorsView.as_view()),
    path('ihjoudhgpreuahodfnbjofg/', comment_submit, name='comment_submit')
]

handler404 = 'portal.views.handler404'

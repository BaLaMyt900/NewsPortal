from django.contrib import admin
from django.urls import path, include
from portal.views import IndexView, AuthorsView, comment_submit
from rest_framework import routers
from portal.rest_api.views import AuthorViewSet, NewsViewSet, ArticlesViewSet, CommentViewSet, PortalUserViewSet

router = routers.DefaultRouter()
router.register(r'author', AuthorViewSet)
router.register(r'news', NewsViewSet)
router.register(r'articles', ArticlesViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'user', PortalUserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
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

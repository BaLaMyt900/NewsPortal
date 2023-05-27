from django.http import JsonResponse
from django.shortcuts import redirect

from portal.models import Subscribers, Category, Post, PortalUser, PostActivity, Comment, CommentActivity

""" AJAX обработка подписок  """


def subscribe(request, pk):  # Подписка пользователем на категорию с проверками
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                Subscribers.objects.get(user=request.user,
                                        category=Category.objects.get(id=pk))
            except Subscribers.DoesNotExist:
                Subscribers.objects.create(user=request.user,
                                           category=Category.objects.get(id=pk))
                return JsonResponse(status=200, data={'status': 201})
            else:
                return JsonResponse(status=200, data={'status': 400, 'error': 'Подписка уже существует.'})
        else:
            return JsonResponse(status=200, data={'status': 400, 'error': 'Пользователь не авторизирован.'})
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))


def unsubscribe(request, pk):  # Отписка пользователя от категории с проверками
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                subs = Subscribers.objects.get(user=request.user,
                                               category=Category.objects.get(id=pk))
            except Subscribers.DoesNotExist:
                return JsonResponse(status=200, data={'status': 400, 'error': 'подписки не существует.'})
            else:
                subs.delete()
                return JsonResponse(status=200, data={'status': 201})
        else:
            return JsonResponse(status=200, data={'status': 400, 'error': 'Пользователь не авторизирован.'})
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))


"""  AJAX обработка оценки постов  """


def postlike(request, pk):
    if request.method == 'POST':
        if request.user.is_authenticated:
            post = Post.objects.get(id=pk)
            try:
                PostActivity.objects.get(user=request.user, activity=post)
            except PostActivity.DoesNotExist:
                post.like(request.user)
                PortalUser.objects.get(id=post.author.user.id).update_rating()
                return JsonResponse(status=200, data={'status': 201})
            else:
                return JsonResponse(status=200, data={'status': 400, 'error': 'Пользователь уже оценил статью.'})
        else:
            return JsonResponse(status=200, data={'status': 400, 'error': 'Пользователь не авторизован.'})
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))


def postdislike(request, pk):
    if request.method == 'POST':
        if request.user.is_authenticated:
            post = Post.objects.get(id=pk)
            try:
                PostActivity.objects.get(user=request.user, activity=post)
            except PostActivity.DoesNotExist:
                post.dislike(request.user)
                PortalUser.objects.get(id=post.author.user.id).update_rating()
                return JsonResponse(status=200, data={'status': 201})
            else:
                return JsonResponse(status=200, data={'status': 400, 'error': 'Пользователь уже оценил статью.'})
        else:
            return JsonResponse(status=200, data={'status': 400, 'error': 'Пользователь не авторизован.'})
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))


"""  AJAX обработка оценки комментариев  """


def commlike(request, pk):
    if request.method == 'POST':
        if request.user.is_authenticated:
            comm = Comment.objects.get(pk=pk)
            try:
                CommentActivity.objects.get(user=request.user, activity=comm)
            except CommentActivity.DoesNotExist:
                comm.like(request.user)
                comm.post.author.user.update_rating()
                return JsonResponse(status=200, data={'status': 201})
            else:
                return JsonResponse(status=200, data={'status': 400, 'error': 'Пользователь уже оценил статью.'})
        else:
            return JsonResponse(status=200, data={'status': 400, 'error': 'Пользователь не авторизован.'})
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))


def commdislike(request, pk):
    if request.method == 'POST':
        if request.user.is_authenticated:
            comm = Comment.objects.get(pk=pk)
            try:
                CommentActivity.objects.get(user=request.user, activity=comm)
            except CommentActivity.DoesNotExist:
                comm.dislike(request.user)
                comm.post.author.user.update_rating()
                return JsonResponse(status=200, data={'status': 201})
            else:
                return JsonResponse(status=200, data={'status': 400, 'error': 'Пользователь уже оценил статью.'})
        else:
            return JsonResponse(status=200, data={'status': 400, 'error': 'Пользователь не авторизован.'})
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))


from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView
from my_account.forms import UserRegistraionForm
from portal.models import Author, Post, Comment, PortalUser
from django.contrib.auth import logout as auth_logout
from allauth.account.views import SignupView
"""  Личный кабинет   """


class AccountView(DetailView):  # Страница отображения карточки пользователя
    model = PortalUser
    template_name = 'account/account.html'

    def get(self, request, *args, **kwargs):  # Если авторизованный пользователь заходит на свой профиль
        if request.user.is_authenticated and request.user.pk == kwargs['pk']:
            return redirect('/account/profile/')  # Перевести на страницу без гет запроса
        else:
            return super().get(request, *args, **kwargs)  # Вернуть свой же гет

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['comments'] = Comment.objects.filter(user=self.object)
        except Comment.DoesNotExist:
            pass
        else:
            for comment in context['comments']:
                comment.text = comment.text[:47] + '...' if len(comment.text) > 50 else comment.text
        if Author.objects.filter(user=self.object).exists():
            context['author'] = True
            posts = Post.objects.filter(author__user=self.object).order_by('-rating')
            for post in posts:
                post.text = post.text[:47] + '...' if len(post.text) > 50 else post.text
            context['posts'] = posts
        return context


class MyAccountView(DetailView, PermissionRequiredMixin, LoginRequiredMixin):  # Страница ЛК пользователя
    permission_required = ('portal.change_portaluser',)
    template_name = 'account/my_account.html'
    model = PortalUser

    def get_object(self, queryset=None):  # Достать ключ без гет запроса
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['comments'] = Comment.objects.filter(user=self.object)
        except Comment.DoesNotExist:
            pass
        else:
            for comment in context['comments']:
                comment.text = comment.text[:47] + '...' if len(comment.text) > 50 else comment.text
        if Author.objects.filter(user=self.object).exists():
            context['author'] = True
            posts = Post.objects.filter(author__user=self.object).order_by('-rating')
            for post in posts:
                post.text = post.text[:47] + '...' if len(post.text) > 50 else post.text
            context['posts'] = posts
        return context

    def post(self, request):
        user = self.get_object()
        if request.POST.get('author'):
            Author.objects.create(user=user)
            Group.objects.get(name='authors').user_set.add(user)
        elif request.POST.get('delete_post'):
            post = Post.objects.get(pk=request.POST.get('delete_post'))
            post.delete()
            user.update_rating()
        elif request.POST.get('change_acc'):
            if user.check_password(request.POST.get('password')):
                user.username = request.POST.get('username')
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.email = request.POST.get('email')
                user.save()
        elif request.POST.get('delete_acc'):
            user.delete()
            return redirect('/')
        return redirect('/account/profile/')


"""   Регистрация и логин   """


class UserRegisterView(SignupView):
    template_name = 'account/register.html'
    form_class = UserRegistraionForm


class UserLoginAjax(View):  # Логин в модальном через AJAX
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            if '@' in username:
                user = authenticate(email=username, password=password)
            else:
                user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return JsonResponse(
                    data={'status': 201},
                    status=200
                )
            else:
                return JsonResponse(data={
                    'status': 400,
                    'error': 'Пользователь не найден.'
                }, status=200)
        else:
            return JsonResponse(data={
                'status': 400,
                'error': 'Логин или пароль пустые.'
            }, status=200)


class UserLogout(View):  # Выход из аккаунта с возвратом на ту же страницу
    def post(self, request):
        auth_logout(request)
        return redirect(self.request.META.get('HTTP_REFERER', '/'))



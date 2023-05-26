from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, FormView
from portal.models import Author, Post, Comment, PortalUser
from my_account.forms import UserRegistrationForm, UserLoginForm
from django.core.mail import send_mail
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv(filename='email_config.env'))


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
            return redirect('/exit/')
        # elif request.POST.get('test_mail'):
            # send_mail(
            #     subject='SEND_DJANGO',
            #     message='Тестирую оправку почты джанго ЯНДЕКС ЭТО НЕ СПАМ!!!!',
            #     from_email=f'{os.environ.get("LOGIN")}@yandex.ru',
            #     recipient_list=['balamyt900@gmail.com']
            # )
        return redirect('/account/profile/')


"""   Регистрация и логин   """


class UserRegisterView(FormView):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        Group.objects.get(name='common').user_set.add(new_user)
        if new_user is not None:
            if new_user.is_active:
                login(self.request, new_user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('/')
            else:
                return render(self.request, 'account/account_blocked.html')


class UserLoginView(FormView):  # Страница логирования клиента. Перейдет если в модальном окне произошла ошибка
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password'])
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect(self.request.META.get('HTTP_REFERER', '/'))
            else:
                return render(self.request, 'account/account_blocked.html')
        else:
            return render(self.request, self.template_name, {'form': self.get_form(), 'error': True})


class UserLoginAjax(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            if '@' in username:
                user = authenticate(email=username, password=password)
            else:
                user = authenticate(login=username, password=password)
            if user:
                username(request, user)
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

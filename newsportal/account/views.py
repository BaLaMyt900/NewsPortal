from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import DetailView, FormView
from portal.models import Author, Post, Comment, PortalUser
from account.forms import UserRegistrationForm, UserLoginForm

"""  Личный кабинет   """


class AccountView(DetailView):  # Страница отображения личного кабинета
    model = PortalUser
    template_name = 'account/account.html'

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

    def post(self, request, pk):
        self.object = PortalUser.objects.get(pk=pk)
        if request.POST.get('author'):
            Author.objects.create(user=self.object)
        elif request.POST.get('delete_post'):
            post = Post.objects.get(pk=request.POST.get('delete_post'))
            post.delete()
            self.object.update_rating()
        elif request.POST.get('change_acc'):
            if self.object.check_password(request.POST.get('password')):
                self.object.username = request.POST.get('username')
                self.object.first_name = request.POST.get('first_name')
                self.object.last_name = request.POST.get('last_name')
                self.object.email = request.POST.get('email')
                self.object.save()
                return self.get(request)
        elif request.POST.get('delete_acc'):
            self.object.delete()
            return redirect('/exit/')
        return redirect(request.META.get('HTTP_REFERER', '/'))


"""   Регистрация и логин   """


class UserRegisterView(FormView):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        if new_user is not None:
            if new_user.is_active:
                login(self.request, new_user)
                return redirect('/')
            else:
                return render(self.request, 'account/account_blocked.html')


class UserLoginView(FormView):  #Страница логирования клиента. Перейдет если в модальном окне произошла ошибка
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



from django.urls import path
from my_account.views import AccountView, MyAccountView, UserLoginAjax, UserRegisterView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name='signup'),
    path('profile/<int:pk>', AccountView.as_view()),
    path('profile/', MyAccountView.as_view(), name='profile'),
    path('login/', UserLoginAjax.as_view(), name='login_ajax'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout')
]

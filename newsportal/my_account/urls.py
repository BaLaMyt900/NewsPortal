from django.shortcuts import redirect
from django.urls import path
from my_account.views import AccountView, MyAccountView, UserLoginAjax, UserLogout, UserRegisterView

urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name='signup'),
    path('profile/<int:pk>', AccountView.as_view()),
    path('profile/', MyAccountView.as_view(), name='profile'),
    path('login/', UserLoginAjax.as_view(), name='login_ajax'),
    path('logout/', UserLogout.as_view(), name='logout_ajax'),
]

from django.urls import path
from my_account.views import UserRegisterView, UserLoginView,\
    AccountView, MyAccountView, UserLoginAjax, UserLogoutAjax

urlpatterns = [
    path('register/', UserRegisterView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('profile/<int:pk>', AccountView.as_view()),
    path('profile/', MyAccountView.as_view()),
    path('login_ajax', UserLoginAjax.as_view(), name='login_ajax'),
    path('logout_ajax', UserLogoutAjax.as_view(), name='logout_ajax')
]

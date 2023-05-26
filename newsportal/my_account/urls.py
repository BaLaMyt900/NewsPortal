from django.urls import path
from my_account.views import UserRegisterView,\
    AccountView, MyAccountView, UserLoginAjax, UserLogout

urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name='signup'),
    path('profile/<int:pk>', AccountView.as_view()),
    path('profile/', MyAccountView.as_view()),
    path('login/', UserLoginAjax.as_view(), name='login_ajax'),
    path('logout/', UserLogout.as_view(), name='logout_ajax')
]

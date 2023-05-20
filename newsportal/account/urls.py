from django.urls import path
from account.views import UserRegisterView, UserLoginView, AccountView

urlpatterns = [
    path('register/', UserRegisterView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('<int:pk>', AccountView.as_view()),
]
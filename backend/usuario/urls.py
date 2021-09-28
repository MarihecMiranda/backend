from django.views.generic import TemplateView
from django.urls import path, include, re_path
from .views import LogoutView, SignupView, GetCSRFToken, LoginView, LogoutView, DeleteAccountView, GetUserView, UpdateUserView

urlpatterns = [
    path('register', SignupView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('delete', DeleteAccountView.as_view()),
    path('csrf_cookie', GetCSRFToken.as_view()),
    path('users', GetUserView.as_view()),
    path('update', UpdateUserView.as_view())

]
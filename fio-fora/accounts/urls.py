from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.AccountLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('conta/', views.account_page, name='account'),
    path('cadastro/', views.signup, name='signup'),
    path('cadastro/<str:role>/', views.register, name='register'),
    path('recuperar-senha/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('recuperar-senha/enviado/', views.PasswordResetSentView.as_view(), name='password_reset_done'),
    path('recuperar-senha/concluido/', views.PasswordResetFinishedView.as_view(), name='password_reset_complete'),
    path('recuperar-senha/<uidb64>/<token>/', views.PasswordResetNewPasswordView.as_view(), name='password_reset_confirm'),
    path('usuarios/', views.user_list, name='user_list'),
]

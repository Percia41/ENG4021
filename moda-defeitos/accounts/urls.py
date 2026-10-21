from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path('', views.AccountLoginView.as_view(), name='login_page'),
    path('login/', views.AccountLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login_page'), name='logout'),
    path('conta/', views.account_page, name='account_page'),
    path('recuperar-senha/', views.password_reset_page, name='password_reset_page'),
    path('cadastro/', views.account_type_page, name='account_type_page'),
    path('cadastro/comprador/', views.register, {'role': 'buyer'}, name='buyer_register_page'),
    path('cadastro/vendedor/', views.register, {'role': 'seller'}, name='seller_register_page'),
    path('cadastro/marca/', views.register, {'role': 'brand'}, name='brand_register_page'),
]

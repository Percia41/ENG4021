from django.urls import path

from . import views


urlpatterns = [
    path('', views.AccountLoginView.as_view(), name='login_page'),
    path('login/', views.AccountLoginView.as_view(), name='login'),
    path('recuperar-senha/', views.password_reset_page, name='password_reset_page'),
    path('cadastro/', views.account_type_page, name='account_type_page'),
    path('cadastro/comprador/', views.register, {'role': 'buyer'}, name='buyer_register_page'),
    path('cadastro/vendedor/', views.register, {'role': 'seller'}, name='seller_register_page'),
    path('cadastro/marca/', views.register, {'role': 'brand'}, name='brand_register_page'),
]

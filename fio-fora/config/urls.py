"""Rotas do projeto: o admin e as rotas de cada app."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('products.urls')),
    path('', include('cart.urls')),
    path('', include('orders.urls')),
    path('', include('favorites.urls')),
]

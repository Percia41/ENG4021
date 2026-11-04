from django.urls import path

from . import views

urlpatterns = [
    path('favoritos/', views.favorites_list, name='favorites'),
    path('favoritos/adicionar/<int:product_id>/', views.favorite_add, name='favorite_add'),
    path('favoritos/remover/<int:product_id>/', views.favorite_remove, name='favorite_remove'),
]

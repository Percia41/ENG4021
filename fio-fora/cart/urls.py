from django.urls import path

from . import views

urlpatterns = [
    path('carrinho/', views.cart_page, name='cart'),
    path('carrinho/adicionar/<int:product_id>/', views.cart_add, name='cart_add'),
    path('carrinho/itens/<int:item_id>/quantidade/', views.cart_update_item, name='cart_update_item'),
    path('carrinho/itens/<int:item_id>/remover/', views.cart_remove_item, name='cart_remove_item'),
]

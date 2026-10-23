from django.urls import path

from . import views, seller_views


urlpatterns = [
    path('pecas/cadastrar/', seller_views.product_create, name='seller_product_create'),
    path('minhas-pecas/', seller_views.my_products, name='my_products'),
    path('simulador/', seller_views.discount_simulator, name='discount_simulator'),
    path('usuarios/', views.user_list, name='user_list'),
    path('vitrine/', views.home, name='home'),
    path('produtos/novo/', views.product_create, name='product_create'),
    path('produtos/<int:product_id>/editar/', views.product_update, name='product_update'),
    path('produtos/<int:product_id>/remover/', views.product_delete, name='product_delete'),
]

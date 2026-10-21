from django.urls import path

from . import views


urlpatterns = [
    path('usuarios/', views.user_list, name='user_list'),
    path('vitrine/', views.home, name='home'),
    path('produtos/novo/', views.product_create, name='product_create'),
    path('produtos/<int:product_id>/editar/', views.product_update, name='product_update'),
    path('produtos/<int:product_id>/remover/', views.product_delete, name='product_delete'),
]

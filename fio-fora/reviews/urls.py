from django.urls import path

from . import views

urlpatterns = [
    path('pedidos/itens/<int:item_id>/avaliar/', views.review_save, name='review_save'),
]

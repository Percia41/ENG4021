from django.conf import settings
from django.db import models
from django.db.models import Exists, OuterRef

from products.models import Product


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "favorito"
        verbose_name_plural = "favoritos"
        constraints = [models.UniqueConstraint(fields=["user", "product"], name="unique_user_favorite")]


def mark_favorites(products, user):
    """Anota cada peça com is_favorite (True/False) para o usuário informado."""
    return products.annotate(is_favorite=Exists(
        Favorite.objects.filter(user_id=user.pk, product=OuterRef('pk'))
    ))
